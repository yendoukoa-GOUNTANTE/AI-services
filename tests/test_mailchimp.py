import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Mock mailchimp_marketing before importing app
for mod in ['mailchimp_marketing', 'mailchimp_marketing.api_client']:
    try:
        __import__(mod)
    except ImportError:
        sys.modules[mod] = MagicMock()

import app

class MailchimpIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.app.test_client()
        with app.app.app_context():
            app.db.create_all()
            # Create a test user
            self.test_user = app.User(username='testuser', api_key='testkey')
            app.db.session.add(self.test_user)
            app.db.session.commit()
            self.api_key = 'testkey'

    def tearDown(self):
        with app.app.app_context():
            app.db.session.remove()
            app.db.drop_all()

    @patch('mailchimp_service.subscribe_to_newsletter')
    def test_mailchimp_subscribe(self, mock_subscribe):
        mock_subscribe.return_value = {"status": "success", "id": "12345"}

        response = self.client.post('/api/v1/mailchimp/subscribe',
                                    json={'email': 'test@example.com'},
                                    headers={'X-API-Key': self.api_key})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'success')
        mock_subscribe.assert_called_once_with('test@example.com')

    @patch('google_ai.generate_email_campaign')
    @patch('mailchimp_service.create_campaign')
    @patch('mailchimp_service.set_campaign_content')
    def test_mailchimp_create_campaign(self, mock_set_content, mock_create_campaign, mock_generate_ai):
        mock_generate_ai.return_value = {
            'subject_line': 'Test Subject',
            'preview_text': 'Test Preview',
            'title': 'Test Title',
            'html_content': '<h1>Test</h1>'
        }
        mock_create_campaign.return_value = {"status": "success", "id": "camp123"}
        mock_set_content.return_value = {"status": "success"}

        response = self.client.post('/api/v1/mailchimp/campaigns',
                                    json={'prompt': 'test campaign'},
                                    headers={'X-API-Key': self.api_key})

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['campaign_id'], 'camp123')
        mock_generate_ai.assert_called_once_with('test campaign')

    @patch('google_ai.provide_email_marketing_assistance')
    def test_email_marketing_specialist(self, mock_assistance):
        mock_assistance.return_value = "AI response"

        response = self.client.post('/api/v1/marketing/email-specialist',
                                    json={'prompt': 'how to grow my list?'},
                                    headers={'X-API-Key': self.api_key})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'AI response')
        mock_assistance.assert_called_once_with('how to grow my list?')

if __name__ == '__main__':
    unittest.main()
