import unittest
from unittest.mock import Mock, patch
from common.portfolio import MockPortfolio
from common.util import format_sse

class TestMockPortfolio(unittest.TestCase):

    def setUp(self):
        self.alpha_mock = Mock()
        self.announcer_mock = Mock()
        self.portfolio = MockPortfolio(id=1, name="Test Portfolio", balance=1000.0, alpha=self.alpha_mock, announcer=self.announcer_mock)

    def test_initialization(self):
        self.assertEqual(self.portfolio.id, 1)
        self.assertEqual(self.portfolio.name, "Test Portfolio")
        self.assertEqual(self.portfolio.starting, 1000.0)
        self.assertEqual(self.portfolio.buying_power, 1000.0)
        self.assertDictEqual(self.portfolio.portfolio, {})

    @patch('common.util.format_sse') 
    def test_buy_stock(self, mock_format_sse):
        self.alpha_mock.price.return_value = 100.0
        response, status_code = self.portfolio.ex_buy("AAPL", 5)
        self.assertEqual(status_code, 200)
        self.assertIn("AAPL", self.portfolio.portfolio)
        self.assertEqual(self.portfolio.buying_power, 500.0)
        self.announcer_mock.announce.assert_called_once()

    @patch('common.util.format_sse')
    def test_sell_stock(self, mock_format_sse):
        self.alpha_mock.price.return_value = 100.0
        self.portfolio.portfolio = {"AAPL": {"price": 100.0, "amount": 5}}
        self.portfolio.buying_power = 500.0
        response, status_code = self.portfolio.ex_sell_all("AAPL")
        self.assertEqual(status_code, 200)
        self.assertNotIn("AAPL", self.portfolio.portfolio)
        self.assertEqual(self.portfolio.buying_power, 1000.0)
        self.announcer_mock.announce.assert_called_once()