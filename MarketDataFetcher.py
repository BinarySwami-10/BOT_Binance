from mxproxy import mx
import time
import math
def get_lastprice(INDEX):
	if 'USDT' in INDEX:
		url=f'https://www.binance.com/fapi/v1/ticker/price?symbol={INDEX}'
	else:
		url=f'https://www.binance.com/dapi/v1/premiumIndex?symbol={INDEX}'

	response=mx.get_page(url).json()
	# print(response)
	return float(response['price'])




def roundoff(strfloat,precision=1):
	basedigits=len(strfloat.split('.'))
	if basedigits <=2:
		precision=3

	return round(float(strfloat),precision)

def calc_trend(INDEX):
	data=get_lastprice(INDEX)
	estimate=roundoff(data['estimatedSettlePrice'])
	indexPrice=roundoff(data['indexPrice'])
	markPrice=roundoff(data['markPrice'])
	deltaEI= estimate - indexPrice 
	deltaEM= estimate - markPrice
	directionI = '🔼' if deltaEI > 0 else '🔽'
	directionM = '🔼' if deltaEM > 0 else '🔽'
	print(f"{INDEX}: I:{directionI}\t|\tM:{directionM} INFO: E={estimate:<7} I={indexPrice:<7} M={markPrice:<7}")
	...

def last_n_trades(SYMBOL='ETHUSD_PERP',limit='1000'):
	p=mx.get_page(f'https://dapi.binance.com/dapi/v1/trades?symbol={SYMBOL}&limit={limit}').json()
	for i,v in enumerate(p):
		print(p)

	
if __name__ == '__main__':
	SYMBOL='RAYUSDT'
	# last_n_trades()
	while True:
		print (get_lastprice(SYMBOL))
# 'altzone', 'asctime', 'clock', 'ctime', 'daylight', 'get_clock_info', 'gmtime', 'localtime', 'mktime', 'monotonic', 'monotonic_ns', 'perf_counter', 'perf_counter_ns', 'process_time', 'process_time_ns', 'sleep', 'strftime', 'strptime', 'struct_time', 'thread_time', 'thread_time_ns', 'time', 'time_ns', 'timezone', 'tzname'

