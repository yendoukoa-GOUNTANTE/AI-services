import pytest
from unittest.mock import patch, MagicMock

def test_flutterwave_initialize(client, auth_headers):
    with patch('flutterwave_service.initialize_transaction') as mock_init:
        mock_init.return_value = {"status": "success", "data": {"link": "https://flw.com/pay"}}

        response = client.post('/api/v1/payment/flutterwave/initialize', json={
            "amount": "1000",
            "currency": "NGN"
        }, headers=auth_headers)

        assert response.status_code == 200
        assert response.json['status'] == 'success'

def test_flutterwave_verify(client, auth_headers):
    with patch('flutterwave_service.verify_transaction') as mock_verify:
        mock_verify.return_value = {"status": "success", "data": {"status": "successful"}}

        response = client.get('/api/v1/payment/flutterwave/verify/123', headers=auth_headers)

        assert response.status_code == 200
        assert response.json['status'] == 'success'

def test_twilio_assistance_execution(client, auth_headers):
    with patch('google_ai.generate_twilio_message_data') as mock_data:
        with patch('twilio_service.send_sms') as mock_send:
            mock_data.return_value = {"to_number": "+1234567890", "message_body": "Hello"}
            mock_send.return_value = {"status": "success", "sid": "SM123"}

            response = client.post('/api/v1/mobile/twilio', json={
                "prompt": "Send hello to +1234567890",
                "execute": True
            }, headers=auth_headers)

            assert response.status_code == 200
            assert response.json['status'] == 'success'
            assert response.json['sid'] == 'SM123'
