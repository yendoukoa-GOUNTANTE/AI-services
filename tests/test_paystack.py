import unittest
from unittest.mock import patch, MagicMock
import os
import secrets
import hmac
import hashlib
import json

# Mock environment variables before importing app
os.environ['PAYSTACK_SECRET_KEY'] = 'test_sk'

from app import app, db, User, Payment, ActivityLog

class PaystackTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        suffix = secrets.token_hex(4)
        self.api_key = f"key_{suffix}"
        self.test_user = User(username=f'user_{suffix}@example.com', api_key=self.api_key, credits=100)
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        db.drop_all()
        db.session.remove()
        self.app_context.pop()

    @patch('paystack_service.initialize_transaction')
    def test_initialize_payment(self, mock_init):
        ref = "ref_" + secrets.token_hex(4)
        mock_init.return_value = {
            'status': True,
            'message': 'Authorization URL created',
            'data': {
                'authorization_url': 'https://checkout.paystack.com/test',
                'access_code': 'test_access_code',
                'reference': ref
            }
        }

        response = self.client.post('/api/v1/payment/paystack/initialize',
                                    json={'amount': '100', 'currency': 'NGN'},
                                    headers={'X-API-Key': self.api_key})

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['status'])
        self.assertEqual(data['data']['reference'], ref)

        payment = Payment.query.filter_by(paystack_reference=ref).first()
        self.assertIsNotNone(payment)
        self.assertEqual(payment.amount, 10000)

    @patch('paystack_service.verify_transaction')
    def test_verify_payment_and_fulfillment(self, mock_verify):
        ref = "ref_" + secrets.token_hex(4)
        payment = Payment(user_id=self.test_user.id, amount=10000, currency='NGN', status='pending', paystack_reference=ref)
        db.session.add(payment)
        db.session.commit()

        mock_verify.return_value = {
            'status': True,
            'message': 'Verification successful',
            'data': {
                'status': 'success',
                'reference': ref,
                'amount': 10000
            }
        }

        response = self.client.get(f'/api/v1/payment/paystack/verify/{ref}',
                                   headers={'X-API-Key': self.api_key})

        self.assertEqual(response.status_code, 200)

        payment = Payment.query.filter_by(paystack_reference=ref).first()
        self.assertEqual(payment.status, 'succeeded')

        user = User.query.get(self.test_user.id)
        # 10000 kobo = 100 major units = 1000 credits.
        # Initial 100 + 1000 = 1100
        self.assertEqual(user.credits, 1100)

    def test_webhook_signature_verification(self):
        ref = "ref_" + secrets.token_hex(4)
        payment = Payment(user_id=self.test_user.id, amount=5000, currency='NGN', status='pending', paystack_reference=ref)
        db.session.add(payment)
        db.session.commit()

        payload = {
            'event': 'charge.success',
            'data': {
                'reference': ref,
                'status': 'success',
                'amount': 5000
            }
        }

        data = json.dumps(payload)
        secret = 'test_sk'
        signature = hmac.new(secret.encode('utf-8'), data.encode('utf-8'), hashlib.sha512).hexdigest()

        # Test with correct signature
        response = self.client.post('/api/v1/payment/paystack/webhook',
                                    data=data,
                                    content_type='application/json',
                                    headers={'x-paystack-signature': signature})
        self.assertEqual(response.status_code, 200)

        # Verify fulfillment
        user = User.query.get(self.test_user.id)
        self.assertEqual(user.credits, 600) # 100 + 500

        # Test with incorrect signature
        response = self.client.post('/api/v1/payment/paystack/webhook',
                                    data=data,
                                    content_type='application/json',
                                    headers={'x-paystack-signature': 'wrong_sig'})
        self.assertEqual(response.status_code, 400)

    def test_double_fulfillment_prevention(self):
        ref = "ref_" + secrets.token_hex(4)
        payment = Payment(user_id=self.test_user.id, amount=5000, currency='NGN', status='pending', paystack_reference=ref)
        db.session.add(payment)
        db.session.commit()

        # Simulate webhook call
        payload = {'event': 'charge.success', 'data': {'reference': ref, 'status': 'success', 'amount': 5000}}
        data = json.dumps(payload)
        signature = hmac.new(b'test_sk', data.encode('utf-8'), hashlib.sha512).hexdigest()

        self.client.post('/api/v1/payment/paystack/webhook', data=data, content_type='application/json', headers={'x-paystack-signature': signature})

        user = User.query.get(self.test_user.id)
        self.assertEqual(user.credits, 600)

        # Simulate verify call (e.g. user redirects to success page)
        with patch('paystack_service.verify_transaction') as mock_verify:
            mock_verify.return_value = {'status': True, 'data': {'status': 'success', 'reference': ref, 'amount': 5000}}
            self.client.get(f'/api/v1/payment/paystack/verify/{ref}', headers={'X-API-Key': self.api_key})

        user = User.query.get(self.test_user.id)
        self.assertEqual(user.credits, 600) # Should still be 600, not 1100

if __name__ == '__main__':
    unittest.main()
