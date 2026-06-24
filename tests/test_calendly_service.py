import unittest
from unittest.mock import patch, MagicMock
import calendly_service
import os

class TestCalendlyService(unittest.TestCase):

    def setUp(self):
        os.environ["CALENDLY_API_KEY"] = "test_key"

    @patch('requests.get')
    def test_get_user_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"resource": {"uri": "user_uri"}}
        mock_get.return_value = mock_response

        result = calendly_service.get_user_info()
        self.assertEqual(result["resource"]["uri"], "user_uri")
        mock_get.assert_called_once_with("https://api.calendly.com/users/me", headers=unittest.mock.ANY, timeout=10)

    @patch('requests.get')
    def test_get_user_info_no_key(self, mock_get):
        with patch.dict(os.environ, {}, clear=True):
            result = calendly_service.get_user_info()
            self.assertEqual(result["error"], "Calendly API key not configured")

    @patch('requests.get')
    def test_list_event_types_success(self, mock_get):
        # Mocking user_info first because list_event_types calls it if user_uri is not provided
        mock_response_user = MagicMock()
        mock_response_user.status_code = 200
        mock_response_user.json.return_value = {"resource": {"uri": "user_uri"}}

        mock_response_events = MagicMock()
        mock_response_events.status_code = 200
        mock_response_events.json.return_value = {"collection": []}

        mock_get.side_effect = [mock_response_user, mock_response_events]

        result = calendly_service.list_event_types()
        self.assertEqual(result["collection"], [])
        self.assertEqual(mock_get.call_count, 2)

if __name__ == '__main__':
    unittest.main()
