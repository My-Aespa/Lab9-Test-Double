import unittest
from unittest.mock import patch
from source.currency_exchanger import CurrencyExchanger  # Import from the main module

def get_mock_currency_api_response():
    """
    Method to create a sample response for currency exchange API
    """
    mock_api_response = {
        'base': 'THB',
        'result': {'KRW': 38.69}  # Mock exchange rate from THB to KRW
    }
    class MockResponse:
        def __init__(self, json_data):
            self.json_data = json_data
            self.status_code = 200

        def json(self):
            return self.json_data

    return MockResponse(mock_api_response)

class TestCurrencyExchanger(unittest.TestCase):
    def setUp(self):
        self.exchanger = CurrencyExchanger(base_currency="THB", target_currency="KRW")
        self.mock_api_response = get_mock_currency_api_response()

    @patch('requests.get')
    def test_currency_exchange(self, mock_get):
        # Assign mock's return value
        mock_get.return_value = self.mock_api_response

        # Act - execute class under test
        amount_in_krw = self.exchanger.currency_exchange(500)

        # Check whether the mocked method is called
        mock_get.assert_called_once_with("https://coc-kku-bank.com/foreign-exchange", params={'from': 'THB', 'to': 'KRW'})

        # Assert the conversion calculation
        expected_amount_in_krw = 500 * 38.69
        self.assertAlmostEqual(amount_in_krw, expected_amount_in_krw, places=2)

if __name__ == '__main__':
    unittest.main()
