from bs4 import BeautifulSoup
import requests

def convert_eps_str_to_float(eps_5yr_total_str):
	if (eps_5yr_total_str.startswith('(') and eps_5yr_total_str.endswith(')')):
		return -1.0 * float(eps_5yr_total_str.replace('(', '').replace(')', ''))
	else:
		return float(eps_5yr_total_str)	

def getsoup_marketcap(ticker):
	marketcap_url = "https://www.marketwatch.com/investing/stock/{}?mod=over_search".format(ticker)
	return BeautifulSoup(requests.get(marketcap_url).text, 'html.parser')

def getsoup_balancesheet(ticker):
	balancesheet_url = "https://www.marketwatch.com/investing/stock/{}/financials/balance-sheet".format(ticker)
	return BeautifulSoup(requests.get(balancesheet_url).text, 'html.parser')

def getsoup_incomestatement(ticker):
	incomestatement_url = "https://www.marketwatch.com/investing/stock/{}/financials".format(ticker)
	return BeautifulSoup(requests.get(incomestatement_url).text, 'html.parser')

def is_large_marketcap_in_millions(marketcap):
	return marketcap >= 30000

def has_large_market_cap(market_cap_str):
	if market_cap_str.startswith('$'):
		market_cap_str = market_cap_str[1:]
	if market_cap_str.endswith('T'):
		return True
	if market_cap_str.endswith('B'):
		return float(market_cap_str[:len(market_cap_str)-1]) >= 30
	else:
		return False

def in_millions(value):
	value = value.replace('$', '')
	if value.startswith('(') and value.endswith(')'):
		negative = True
		value = value.replace('(', '')
		value = value.replace(')', '')
	else:
		negative = False
	ret = None
	if value.endswith('B'):
		ret = float(value[:len(value)-1]) * 1000
	elif value.endswith('T'):
		ret = float(value[:len(value)-1]) * 1000000
	elif value.endswith('M'):
		ret = float(value[:len(value)-1])
	else:
		ret = float(value)
	if negative:
		return -1.0 * ret
	else:
		return ret

class BalanceSheet:
	def __init__(self, total_assets, total_liabilities, total_shareholder_equity, longterm_debt):
		self.total_assets = total_assets
		self.total_liabilities = total_liabilities
		self.total_shareholder_equity = total_shareholder_equity
		self.longterm_debt = longterm_debt
		self.book_value = self.total_assets - self.total_liabilities
		self.total_capitalization = self.total_shareholder_equity + self.longterm_debt

	def is_conservatively_financed(self):
		return self.book_value >= .50 * self.total_capitalization

	def print_report(self, ticker):
		print("--- 3. Conservatively Financed? ---")
		print("Analyzing [{}] balance sheet... (values are in millions of dollars)".format(ticker))
		print("Total Assets: " + str(self.total_assets))
		print("Total Liabilities: " + str(self.total_liabilities))
		print("Total Shareholders' Equity: " + str(self.total_shareholder_equity))
		print("Long-Term Debt: " + str(self.longterm_debt))
		print("Book Value = Total Assets - Total Liabilities = " + str(self.book_value))
		print("Total Capitalization = Total Shareholders' Equity + Long-Term Debt = " + str(self.total_capitalization))
		print("\nA stock is conservatively financed if its Book Value is at least 1/2 times its Total Capitalization.\nIn other words, we want the result of (Book Value / Total Capitalization) to be > .5")
		print("Ratio: " + str(self.book_value / self.total_capitalization))

	@staticmethod
	def from_marketwatch_soup(ticker):
		balancesheet_soup = getsoup_balancesheet(ticker)

		row_offset_of_recent_years_total_assets = 11
		total_assets_str = balancesheet_soup.find(string="Total Assets").parent.parent.parent.contents[row_offset_of_recent_years_total_assets].find('span').text
		total_liabilities_str = balancesheet_soup.find(string="Total Liabilities").parent.parent.parent.contents[row_offset_of_recent_years_total_assets].find('span').text
		total_shareholder_equity_str = balancesheet_soup.find(string="Total Shareholders' Equity").parent.parent.parent.contents[row_offset_of_recent_years_total_assets].find('span').text
		longterm_debt_str = balancesheet_soup.find(string="Long-Term Debt").parent.parent.parent.contents[row_offset_of_recent_years_total_assets].find('span').text

		total_assets = in_millions(total_assets_str)
		total_liabilities = in_millions(total_liabilities_str)
		total_shareholder_equity = in_millions(total_shareholder_equity_str)
		longterm_debt = in_millions(longterm_debt_str)

		return BalanceSheet(total_assets, total_liabilities, total_shareholder_equity, longterm_debt)

class IncomeStatement:
	def __init__(self, diluted_eps_history, last_yr_basic_eps):
		self.diluted_eps_history = diluted_eps_history
		self.last_yr_basic_eps = last_yr_basic_eps

	def get_max_purchase_price(self):
		years = len(self.diluted_eps_history)
		multiplier = 15 * self.last_yr_basic_eps
		if years >= 5:
			mean = sum(self.diluted_eps_history[-5:]) / 5
			return min(20 * mean, multiplier)
		else:
			return multiplier
		
class TickerData:
	def __init__(self, 
			ticker, 
			marketcap,
			prominent,
			balancesheet,
			consistent_dividends,
			incomestatement,
			current_market_price):
		self.ticker = ticker
		self.marketcap = marketcap
		self.prominent = prominent
		self.balancesheet = balancesheet
		self.consistent_dividends = consistent_dividends
		self.incomestatement = incomestatement
		self.current_market_price = current_market_price

	def is_sound(self):
		return is_large_marketcap_in_millions(self.marketcap) and self.prominent and self.balancesheet.is_conservatively_financed() and self.consistent_dividends

	def is_reasonably_priced(self):
		return self.current_market_price <= self.incomestatement.get_max_purchase_price()

	def should_buy(self):
		return self.is_sound() and self.is_reasonably_priced()






