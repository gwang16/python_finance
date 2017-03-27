import bs4 as bs # parses html
import pickle # save any python object
import requests # send GET requests to webpages

import datetime as dt
import os 
import pandas as pd
import pandas_datareader.data as web

def save_sp500_tickers():
	# get sourcecode from webpages
	resp = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
	
	# use bs to parse html, specifically find table object 
	soup = bs.BeautifulSoup(resp.text, "html.parser")
	table = soup.find('table', {'class':'wikitable sortable'})

	# for each row, save the ticker to a list
	tickers = []
	for row in table.findAll('tr')[1:]: #ignore first row (header)
		ticker = row.findAll('td')[0].text #ignore all but first column, the ticker
		tickers.append(ticker)

	# save tickers (a python list) to a pickle file
	with open('sp500tickers.pickle', 'wb') as f:
		pickle.dump(tickers, f)

	print(tickers)
	return tickers

#save_sp500_tickers()

def get_data_from_yahoo(reload_sp500 = False):
	# check if require to re-download tickers from wiki
	if reload_sp500:
		tickers = save_sp500_tickers()
	# otherwise just read from the saved pickle file
	else:
		with open('sp500tickers.pickle', 'rb') as f:
			tickers = pickle.load(f)
	# create directory to save data
	if not os.path.exists('stock_dfs'):
		os.makedirs('stock_dfs')

	# grab data from yahoo api and save 
	start = dt.datetime(2000, 1, 1)
	end = dt.datetime(2017, 3, 1)
	
	for ticker in tickers:
		mapping = str.maketrans(".","-")
		ticker = ticker.translate(mapping)
		print(ticker)
		if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
			df = web.DataReader(ticker, 'yahoo', start, end)
			df.to_csv('stock_dfs/{}.csv'.format(ticker))
		else:
			print('Already have {}'.format(ticker))

get_data_from_yahoo(True)