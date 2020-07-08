import datetime, iso8601, json, os, urllib.request

def ascending_rank_24h_change(coin_gains):
	'''sorts tuple by 2nd parameter'''

	return(sorted(coin_gains, reverse = True, key = lambda x: x[1]))   

def sort_daily_pct_gains(active_coins):
	'''sorts active coins by highest gains in 24 hour period'''
	
	coin_gains = []

	for coin in active_coins:
		valid_coin = coin.get('1d')
		if (valid_coin is not None):
			coin_gains.append((coin.get('name'), float(coin.get('1d').get('price_change_pct'))))

	sorted_coins = ascending_rank_24h_change(coin_gains)
	return(sorted_coins) 

if __name__ == "__main__":
	API_PASSWORD = os.environ.get('API_PASSWORD')
	url = "https://api.nomics.com/v1/currencies/ticker?key=" + API_PASSWORD + "&interval=1d"
	response = urllib.request.urlopen(url).read()
	currencies_json = json.loads(response.decode('utf-8'))

	print(f'Number of Total Currencies {len(currencies_json)}')

	refreshed_currency_count = 0
	outdated_currency_count = 0

	updated_currencies = []
	outdated_currencies = []

	for currency in currencies_json:
		interim_timestamp = currency.get('price_timestamp')
		interim_timestamp_datetime = iso8601.parse_date(interim_timestamp)
		now = datetime.datetime.utcnow()
		current = (now.isoformat("T") + "Z")
		current_datetime = iso8601.parse_date(current)
		time_delta = (current_datetime - interim_timestamp_datetime)
		seconds_since_refresh = time_delta.total_seconds()
		if (seconds_since_refresh < 3600):
			refreshed_currency_count += 1
			updated_currencies.append((currency))
		else:
			outdated_currency_count += 1

	sorted_gainers = sort_daily_pct_gains(updated_currencies)
	print(sorted_gainers)
