# Defensive Investing
This is a script that will analyze a stock to determine whether it is a good Buying Opportunity. 

> The criteria for stock evaluation are based on advice from the book, "The Intelligent Investor," by Benjamin Graham, revised 1973 edition with commentary from Jason Zweig.

## How to run the script
In your command line, in the directory where the script is located, run `python3 evaluate.py TICK` where TICK is the stock ticker symbol that you want to analyze. You will be prompted with a series of questions and calculations. Some of these will open stock analysis websites (SeekingAlpha and Charles Schwab) in your browser and ask you to make a decision based on data from those pages.

## What we're looking for in a company
1. Large cap
2. Conservatively financed
    - Book Value >= 1/2 * Total Capitalization
    - 1/2 <= (Total Assets - Total Liabilities) / (Total Shareholders' Equity + Long-Term Debt)
4. Prominent 
    - Stock is in the largest 25% of companies in its sector
5. Continual Dividend History
    - At least 10 years continual dividends

### What price would we pay for a good company?
The recommendation is to spend no more than 25 times the mean Earnings Per Share over the last 5-7 years, and no more than 20 times last year's EPS. 
    
- Buy Limit Price = min( `25 * five-year average EPS`, `20 * most recent year's EPS` )
