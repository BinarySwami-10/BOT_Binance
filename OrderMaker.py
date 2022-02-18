import pyautogui
import time
import DataFetcher
from data import Defaults
# import modulex as mx
# from mxproxy import mx


def gen_orders(
	symbol='SANDUSDT',
	size=1,
	sizeAccleration=1,
	delta='2%',
	sltpRatio=3,
	accleration=0,
	stepsize='1%',
	count=5,
	direction='long',
	roundoff=1
	):
	''' 
	generates list of orders which is then executed via gui bot
	lastPrice: 	current price of cryptocurrency instrument ,
	delta:	 	delta for buy and sell margin ,
	sltpRatio: ratio between take profit and stop loss,
	direction: 	valid(long,short) ,
	count: 		amount of orders to be generated ,
	stepPercent: sliding window step ,
	accleration : accleration in % for step stepsize.,
	sizeAccleration : sizeAccleration integer for order size,
	roundoff	: rounds off to nth place
	mardelRatio : margin to delta ratio
	trigPrice: 	is slghtly away from mark price in the long/short direction when price reached, 
				executs order with delta mergin.,
	'''
	lastPrice = round(DataFetcher.get_lastprice(symbol), roundoff)
	# print({'lastPrice':lastPrice,'roundoff':roundoff})

	if '%' in str(delta):
		delta = (lastPrice / 100) * float(delta[0:-1])
	if '%' in str(stepsize):
		stepsize = (lastPrice / 100) * float(stepsize[0:-1])

	delta = round(float(delta), roundoff)
	stepsize = round(float(stepsize), roundoff)
	sizeAccleration = float(sizeAccleration)
	count = int(count)

	adaptiveStep = round(stepsize * (accleration / 100), 3)
	orderlist = []
	for i in range(count):
		# print('TRACER',orderlist)
		if direction == 'short':
			sigma = round(stepsize * (i + 1), roundoff)
			marketSpread = f'{round((sigma/lastPrice)*100,1)}%'
			stepsize += adaptiveStep
			trigPrice = round(lastPrice + sigma, roundoff)
			orderlist.append({
								'symbol':symbol,
								'trigPrice': format(trigPrice,'.4f'),
								'takeProfit': round(trigPrice - delta, roundoff),
								'stopLoss': round(trigPrice + delta*sltpRatio, roundoff),
								'stepDeltaRatio': f'{round(stepsize,3):<4}|{delta}',
								'Spread': f'{marketSpread}|{sigma:4}',
								'direction': direction,
								'size': size + (sizeAccleration * i)
							})

		if direction == 'long':
			sigma = round(stepsize * (i + 1), roundoff)
			marketSpread = f'{round((-sigma/lastPrice)*100,1)}%'
			stepsize += adaptiveStep
			trigPrice = round(lastPrice - sigma, roundoff)
			orderlist.append({
								'symbol':symbol,
								'trigPrice': format(trigPrice,'.4f'),
								'takeProfit': round(trigPrice + delta, roundoff),
								'stopLoss': round(trigPrice - delta*sltpRatio, roundoff),
								'stepDeltaRatio': f'{round(stepsize,3):<4}|{delta}',
								'Spread': f'{marketSpread}|{sigma:4}',
								'direction': direction,
								'size': size + (sizeAccleration * i)
							})

	return orderlist


if __name__ == '__main__':
	# import BinanceFuturesOrderGUI as GUIAPP

	# pyautogui.moveTo(x=1064, y=468)
	# pyautogui.press('tab',presses=2,interval=0.25)
	# pyautogui.moveTo(x=1189, y=468)
	# position_prober()

	ords = gen_orders(**Defaults.SANDUSDT,direction='short')
	[print(o) for o in ords]

	RULES = '''
	#TRADING RULES 
	#---STEP SIZE 1.5X DELTA
	#---STEP SIZE ~1% of current price
	#---DELTA ~1% of current price
		>>> if market is 66%red in last 10 candles then buy and viceversa for sell
		>>> close all python generated orders before placing new python order
	'''
