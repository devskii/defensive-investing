from bs4 import BeautifulSoup
from helper_functions import *
import requests
import sys
import webbrowser

if len(sys.argv) == 2:
	ticker = sys.argv[1]
	
	# Pull financial data upfront
	marketcap_soup = getsoup_marketcap(ticker)
	incomestatement_soup = getsoup_incomestatement(ticker)

	balancesheet = BalanceSheet.from_marketwatch_soup(ticker)

	# Check large market cap
	marketcap = marketcap_soup.find(string="Market Cap").parent.find_next_sibling('span').text
	print("")
	print("--- 1. Large? --- ")
	print("Market cap of [{}] is [{}]".format(ticker, marketcap))
	if not has_large_market_cap(marketcap):
		print("[{}] is too small to be considered a sound investment for the defensive investor.".format(ticker))
		exit(0)
	else:
		print("[{}] is large enough for further analysis.".format(ticker))
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
	elif prominence == 'n':
		print("Since [{}] is not prominent it cannot be considered further.".format(ticker))
		exit(0)
	else:
		print("USER ERROR: Please answer 'y' or 'n' next time")
		exit(0)
	print("")

	balancesheet.print_report(ticker)
	if balancesheet.is_conservatively_financed():
		print("[{}] is conservatively financed.".format(ticker))
	else:
		print("[{}] is not conservatively financed, therefore it is not good for the defensive investor.".format(ticker))
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
	elif consistent_dividends == 'n':
		print("Since [{}] has an inconsistent dividend history it cannot be considered further.".format(ticker))
		exit(0)
	else:
		print("USER ERROR: Please answer 'y' or 'n' next time")
		exit(0)
	print("")

	# Check out the earnings to see what prices you would pay.
	indices_of_last_5yr_diluted_eps = [3, 5, 7, 9, 11]
	eps_5yr_total = 0
	for i in indices_of_last_5yr_diluted_eps:
		eps_5yr_total_str = incomestatement_soup.find(string="EPS (Diluted)").parent.parent.parent.contents[i].find('span').text
		eps_5yr_total += convert_eps_str_to_float(eps_5yr_total_str)
	eps_5yr_mean = eps_5yr_total / 5

	eps_last_year = convert_eps_str_to_float(incomestatement_soup.find(string="EPS (Basic)").parent.parent.parent.contents[11].find('span').text)
	
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
