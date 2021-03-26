def convert_eps_str_to_float(eps_5yr_total_str):
	if (eps_5yr_total_str.startswith('(') and eps_5yr_total_str.endswith(')')):
		return -1.0 * float(eps_5yr_total_str.replace('(', '').replace(')', ''))
	else:
		return float(eps_5yr_total_str)

def is_conservatively_financed(total_assets, total_liabilities, total_shareholder_equity, longterm_debt):
	book_value = total_assets - total_liabilities
	total_capitalization = total_shareholder_equity + longterm_debt

	return book_value >= .50 * total_capitalization