def convert_eps_str_to_float(eps_5yr_total_str):
	if (eps_5yr_total_str.startswith('(') and eps_5yr_total_str.endswith(')')):
		return -1.0 * float(eps_5yr_total_str.replace('(', '').replace(')', ''))
	else:
		return float(eps_5yr_total_str)	

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
	if value.startswith('$'):
		value = value[1:]
	if value.endswith('B'):
		return float(value[:len(value)-1]) * 1000
	elif value.endswith('T'):
		return float(value[:len(value)-1]) * 1000000
	elif value.endswith('M'):
		return float(value[:len(value)-1])

class BalanceSheet:
	def __init__(self, total_assets, total_liabilities, total_shareholder_equity, longterm_debt):
		self.total_assets = total_assets
		self.total_liabilities = total_liabilities
		self.total_shareholder_equity = total_shareholder_equity
		self.longterm_debt = longterm_debt
		self.book_value = self.total_assets - self.total_liabilities
		self.total_capitalization = self.total_shareholder_equity + self.longterm_debt
		self.ratio = self.book_value / self.total_capitalization

	def is_conservatively_financed(self):
		return self.ratio >= .50

	def get_financing_ratio(self):
		return self.ratio

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






