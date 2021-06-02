from helper_functions import *
import unittest

class TestEvaluator(unittest.TestCase):

	def test_eps_conversion(self):
		self.assertEqual(8.28, convert_eps_str_to_float("8.28"))
		self.assertEqual(0.0, convert_eps_str_to_float("0"))
		self.assertEqual(-3.1, convert_eps_str_to_float("(3.1)"))

	def test_conservative_financing(self):
		total_assets = 52150.0
		total_liabilities = 28470.0
		total_shareholder_equity = 22230.0
		longterm_debt = 10890.0

		balancesheet = BalanceSheet(total_assets, total_liabilities, total_shareholder_equity, longterm_debt)

		self.assertTrue(balancesheet.is_conservatively_financed())

	def test_non_conservative_financing(self):
		total_assets = 323890.0
		total_liabilities = 258550.0
		total_shareholder_equity = 65340.0
		longterm_debt = 107050.0

		balancesheet = BalanceSheet(total_assets, total_liabilities, total_shareholder_equity, longterm_debt)

		self.assertFalse(balancesheet.is_conservatively_financed())

	def test_decide_to_buy_company(self):
		marketcap = 229720
		prominent = True
		total_assets = 153090
		total_liabilities = 72050
		total_shareholder_equity = 81040
		longterm_debt = 34250
		consistent_dividends = True
		diluted_eps_history = [3.65, 3.65, 3.65, 3.65, 3.65, 3.65, 3.65, 3.65, 3.65, 3.65]
		last_yr_basic_eps = 4.98
		current_market_price = 57.42

		ticker_data = TickerData(
			'ABCDE', 
			marketcap,
			prominent,
			BalanceSheet(total_assets, total_liabilities, total_shareholder_equity, longterm_debt),
			consistent_dividends,
			IncomeStatement(diluted_eps_history, last_yr_basic_eps),
			current_market_price)

		self.assertTrue(ticker_data.is_sound())
		self.assertTrue(ticker_data.is_reasonably_priced())
		self.assertTrue(ticker_data.should_buy())
