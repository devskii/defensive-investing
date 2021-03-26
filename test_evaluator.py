import helper_functions
import unittest

class TestEvaluator(unittest.TestCase):

	def test_eps_conversion(self):
		self.assertEqual(8.28, helper_functions.convert_eps_str_to_float("8.28"))
		self.assertEqual(0.0, helper_functions.convert_eps_str_to_float("0"))
		self.assertEqual(-3.1, helper_functions.convert_eps_str_to_float("(3.1)"))

	def test_conservative_financing(self):
		total_assets = 52150.0
		total_liabilities = 28470.0
		total_shareholder_equity = 22230.0
		longterm_debt = 10890.0

		self.assertTrue(helper_functions.is_conservatively_financed(total_assets, total_liabilities, total_shareholder_equity, longterm_debt))

	def test_non_conservative_financing(self):
		total_assets = 323890.0
		total_liabilities = 258550.0
		total_shareholder_equity = 65340.0
		longterm_debt = 107050.0

		self.assertFalse(helper_functions.is_conservatively_financed(total_assets, total_liabilities, total_shareholder_equity, longterm_debt))