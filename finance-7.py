import bs4 as bs # parses html
import pickle # save any python object
import requests # send GET requests to webpages

import datetime as dt
import os 
import pandas as pd
import pandas_datareader.data as web

def main():
	get_data_from_yahoo(True)
	compile_data()


def save_sp500_tickers():
	# get sourcecode from webpages
	resp = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
	
	# use bs to parse html, specifically find table object 
	soup = bs.BeautifulSoup(resp.text, "html.parser")
	table = soup.find('table', {'class':'wikitable sortable'})

	# for each row, save the ticker to a list
	tickers = []
	for row in table.findAll('tr')[1:]: # ignore first row (header)
		ticker = row.findAll('td')[0].text # ignore all but first column, the ticker
		mapping = str.maketrans(".","-") # wiki turns - in company names to . so this reverses the process
		ticker = ticker.translate(mapping)
		tickers.append(ticker)

	# save tickers (a python list) to a pickle file
	with open('sp500tickers.pickle', 'wb') as f:
		pickle.dump(tickers, f)

	print(tickers)
	return tickers


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
		print(ticker)
		if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
			df = web.DataReader(ticker, 'yahoo', start, end)
			df.to_csv('stock_dfs/{}.csv'.format(ticker))
		else:
			print('Already have {}'.format(ticker))


def compile_data():
	
	# read ticker names from pickle object
	with open('sp500tickers.pickle', 'rb') as f:
		tickers = pickle.load(f)

	# create empty data frame object
	main_df = pd.DataFrame()

	# read price csv for each ticker, and combine closing price into one dataframe 
	for count,ticker in enumerate(tickers):
		df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
		df.set_index('Date', inplace = True)
		df.rename(columns = {'Adj Close': ticker}, inplace = True)
		df.drop(['Open','High','Low','Close','Volume'], 1, inplace = True)

		if main_df.empty:
			main_df = df
		else:
			main_df = main_df.join(df, how = 'outer')

		if count % 10 == 0:
			print(count)

	print(main_df.head())
	main_df.to_csv('sp500_joined_closes.csv')


if __name__ == '__main__':
	main()




