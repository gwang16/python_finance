import bs4 as bs # parses html
import pickle # save any python object
import requests # send GET requests to webpages

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

save_sp500_tickers()