from bs4 import BeautifulSoup
import requests
import sys
import webbrowser

def get_djia_tickers_and_links():
	url = "https://www.marketwatch.com/investing/index/DJIA"
	djia_soup = BeautifulSoup(requests.get(url).text, 'html.parser')
	table = djia_soup.find("div", {"class":"element element--table ByIndexGainers"})
	company_links = [company_element.get('href') for company_element in table.find_all("a")]
	index_of_ticker_in_link = len("https://www.marketwatch.com/investing/stock/")
	company_tickers = [link[index_of_ticker_in_link:].upper() for link in company_links]
	return (company_tickers,company_links)

#djia_tickers,djia_company_links = get_djia_tickers_and_links()

#for link in djia_company_links:
	#company_soup = BeautifulSoup(requests.get(link).text, 'html.parser')
	#TODO: extract market cap and print whether or not it's > 30B

"""
print("--- Stocks in the DJIA ---")
print("Courtesy of MarketWatch")

i = 1
for ticker in djia_tickers:
	print(str(i) + " " + ticker)
	i+=1
"""

def has_large_market_cap(market_cap):
	if market_cap.startswith('$'):
		market_cap = market_cap[1:]
	if market_cap.endswith('T'):
		return True
	if market_cap.endswith('B'):
		return float(market_cap[:len(market_cap)-1]) >= 30
	else: 
		return False

"""
print(has_large_market_cap("31B")) #true
print(has_large_market_cap("300M")) #false
print(has_large_market_cap("29B")) #false
print(has_large_market_cap("30B")) #true
print(has_large_market_cap("2T")) #true
"""

def in_millions(value):
	if value.startswith('$'):
		value = value[1:]
	if value.endswith('B'):
		return float(value[:len(value)-1]) * 1000
	elif value.endswith('T'):
		return float(value[:len(value)-1]) * 1000000
	elif value.endswith('M'):
		return float(value[:len(value)-1])

def is_conservatively_financed(total_assets, total_liabilities, market_cap):
	book_value = total_assets - total_liabilities
	return book_value >= .50 * market_cap

if len(sys.argv) == 2:
	ticker = sys.argv[1]
	
	# Check large market cap
	marketcap_url = "https://www.marketwatch.com/investing/stock/{}?mod=over_search".format(ticker)
	marketcap_soup = BeautifulSoup(requests.get(marketcap_url).text, 'html.parser')
	marketcap = marketcap_soup.find(string="Market Cap").parent.find_next_sibling('span').text
	print("")
	print("--- 1. Large? --- ")
	print("Market cap of [{}] is [{}]".format(ticker, marketcap))
	if not has_large_market_cap(marketcap):
		print("[{}] is too small to be considered a sound investment for the defensive investor.".format(ticker))
		print("NO")
		exit(0)
	else:
		print("[{}] is large enough for further analysis.".format(ticker))
		print("YES")
	print("")

	# Check prominent
	print("--- 2. Prominent? ---")
	print("Opening Schwab Research peers analysis in your web browser...")
	print("(Hint: Click \"View all industry peers\" under the chart, then sort by Market Cap).")
	prominence_url = "https://client.schwab.com/secure/cc/research/stocks/stocks.html?path=/research/Client/Stocks/Peers/Peers/&symbol={}".format(ticker)
	webbrowser.open(prominence_url)
	prominence = input("Is [{}] in the largest 25% of its sector? [y/n]".format(ticker))
	if prominence == 'y':
		print("Since [{}] is prominent it can be considered further.".format(ticker))
		print("YES")
	elif prominence == 'n':
		print("Since [{}] is not prominent it cannot be considered further.".format(ticker))
		print("NO")
		exit(0)
	else:
		print("USER ERROR: Please answer 'y' or 'n' next time")
		exit(0)
	print("")

	# Check conservatively financed
	balancesheet_url = "https://www.marketwatch.com/investing/stock/{}/financials/balance-sheet".format(ticker)
	balancesheet_soup = BeautifulSoup(requests.get(balancesheet_url).text, 'html.parser')
	row_offset_of_recent_years_total_assets = 11
	total_assets_str = balancesheet_soup.find(string="Total Assets").parent.parent.parent.contents[row_offset_of_recent_years_total_assets].find('span').text
	total_liabilities_str = balancesheet_soup.find(string="Total Liabilities").parent.parent.parent.contents[row_offset_of_recent_years_total_assets].find('span').text
	total_shareholder_equity_str = balancesheet_soup.find(string="Total Shareholders' Equity").parent.parent.parent.contents[row_offset_of_recent_years_total_assets].find('span').text
	longterm_debt_str = balancesheet_soup.find(string="Long-Term Debt").parent.parent.parent.contents[row_offset_of_recent_years_total_assets].find('span').text
	print("--- 3. Conservatively Financed? ---")
	print("Analyzing [{}] balance sheet...".format(ticker))
	print("Attempting to pull data from Marketwatch...")
	print("Total Assets: " + total_assets_str)
	print("Total Liabilities: " + total_liabilities_str)
	print("Total Shareholders' Equity: " + total_shareholder_equity_str)
	print("Long-Term Debt: " + longterm_debt_str)
	book_value_in_millions = in_millions(total_assets_str) - in_millions(total_liabilities_str)
	capitalization_in_millions = in_millions(total_shareholder_equity_str) + in_millions(longterm_debt_str)
	ratio = book_value_in_millions / capitalization_in_millions
	print("1. Common Stock (at Book Value) = {}M".format(book_value_in_millions))
	print("2. Capitalization, including Bank Debt = {}M".format(capitalization_in_millions))
	print("3. Ratio = {}".format(ratio))
	if ratio > .50:
		print("[{}] is conservatively financed.".format(ticker))
		print("YES")
	else:
		print("[{}] is not conservatively financed, therefore it is not good for the defensive investor.".format(ticker))
		print("NO")
		exit(0)
	print("")

	# Check continual historic dividend payouts for at least 10-20 years
	print("--- 4. Consistent Dividend History? ---")
	print("Opening Schwab Research dividend analysis in your web browser...")
	dividendhist_url = "https://client.schwab.com/secure/cc/research/stocks/stocks.html?path=/research/Client/Stocks/Dividends&symbol={}".format(ticker)
	webbrowser.open(dividendhist_url)
	print("Opening SeekingAlpha dividend history in your web browser...")
	seekingalpha_divhist_url = "https://seekingalpha.com/symbol/{}/dividends/history".format(ticker)
	webbrowser.open(seekingalpha_divhist_url)
	consistent_dividends = input("Has [{}] paid continual dividends for at least 10 years? [y/n]".format(ticker))
	if consistent_dividends == 'y':
		print("Since [{}] has paid consistent dividends for 10+ years it can be considered further".format(ticker))
		print("YES")
	elif consistent_dividends == 'n':
		print("Since [{}] has an inconsistent dividend history it cannot be considered further.".format(ticker))
		print("NO")
		exit(0)
	else:
		print("USER ERROR: Please answer 'y' or 'n' next time")
		exit(0)
	print("")

	# Check out the earnings to see what prices you would pay.
	incomestatement_url = "https://www.marketwatch.com/investing/stock/{}/financials".format(ticker)
	incomestatement_soup = BeautifulSoup(requests.get(incomestatement_url).text, 'html.parser')
	indices_of_last_5yr_diluted_eps = [3, 5, 7, 9, 11]
	eps_5yr_total = 0
	for i in indices_of_last_5yr_diluted_eps:
		eps_5yr_total += float(incomestatement_soup.find(string="EPS (Diluted)").parent.parent.parent.contents[i].find('span').text)
	eps_5yr_mean = eps_5yr_total / 5
	eps_last_year = float(incomestatement_soup.find(string="EPS (Basic)").parent.parent.parent.contents[11].find('span').text)
	max_purchase_price = min(25*eps_5yr_mean, 20*eps_last_year)
	current_price = float(incomestatement_soup.find('h3', {"class":"intraday__price"}).find('bg-quote').text.replace(',', ''))
	print("-- 5. Reasonably Priced? ---")
	print("Analyzing [{}] earnings to determine reasonable purchase price...".format(ticker))
	print("EPS (Diluted) 5yr mean: {}".format(eps_5yr_mean))
	print("EPS (Basic) last year: {}".format(eps_last_year))
	print("1. MAX PURCHASE PRICE = {}".format(max_purchase_price))
	print("2. CURRENT MARKET PRICE: {}".format(current_price))
	print("")
	print("--- DECISION ---")
	if (current_price <= max_purchase_price):
		print("BUY: [{}] could be a sound investment at a reasonable price.".format(ticker))
	else:
		print("HOLD: The price of [{}] is too high.".format(ticker))
	print("")