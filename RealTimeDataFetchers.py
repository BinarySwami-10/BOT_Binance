
def binance_recent_trades():                                        
	import pandas as pd
	mktData=get_page('https://dapi.binance.com/dapi/v1/trades?symbol=ETHUSD_PERP').json()
	dataframe=pd.DataFrame(mktData)[::-1]
	for x in dataframe.iterrows():
		print(x)

	print(page.text)
	print(dataframe.to_string())
	print(dataframe.to_string())
	for i in reversed(mktData):
		print(f"{i['qty']:6}{i['price']}")
		print(f"{i.items()}")