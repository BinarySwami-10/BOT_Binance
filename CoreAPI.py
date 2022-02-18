import modulex as mx
import OrderMaker
import requests
from data import Defaults
true = True
false = False


# --------------------------
class USD_M:
	limiturl = 'https://www.binance.com/bapi/futures/v1/private/future/order/place-order'
	strategy_url = 'https://www.binance.com/bapi/futures/v1/private/future/strategy/place-order'

	OTOCO = mx.jload('data/TEMPLATE_USDM_OTOCO.json')


# --------------------------
class OrderExecutor:

	def bulk_execute(orderlist, debug=0):
		headers = mx.parse_raw_headers('data/headers.raw')
		for o in reversed(orderlist):
			print(o)
			url = USD_M.strategy_url
			order_template = mx.jload('./data/TEMPLATE_USDM_OTOCO.json')

			base_order, tp_order, sl_order = tuple(order_template['subOrderList'])
			base_order['quantity'] = o['size']
			tp_order['quantity'] = o['size']
			sl_order['quantity'] = o['size']

			[z.update({'symbol':o['symbol']}) for z in [base_order, tp_order, sl_order]]

			if o['direction'] == 'long':
				base_order['side'] = 'BUY'
				tp_order['side'] = 'SELL'
				sl_order['side'] = 'SELL'

				base_order['price'] = o['trigPrice']

				# tp_order['stopPrice'] = o['takeProfit']
				tp_order['price'] = o['takeProfit']

				# sl_order['stopPrice'] = o['stopLoss']
				sl_order['stopPrice'] = o['stopLoss']

			if o['direction'] == 'short':
				base_order['side'] = 'SELL'
				tp_order['side'] = 'BUY'
				sl_order['side'] = 'BUY'

				base_order['price'] = o['trigPrice']

				# tp_order['stopPrice'] = o['takeProfit']
				tp_order['price'] = o['takeProfit']

				# sl_order['stopPrice'] = o['stopLoss']
				sl_order['stopPrice'] = o['stopLoss']

			if not debug:
				r = requests.post(USD_M.strategy_url, json=order_template, headers=headers)
				print('RESPOSE: ', r.text)
			else:
				print(mx.jdumps(order_template)) if debug >= 2 else ...

	def gen_orders(SYMBOL, **kwargs,):
		data = {}
		if hasattr(Defaults, SYMBOL):
			data = eval(f'Defaults.{SYMBOL}')  
			data.update(kwargs)
		else: 
			print(f'Please add {SYMBOL} to defaults')
		SETTINGS = {**data, **kwargs}
		return (OrderMaker.gen_orders(**SETTINGS))


def main():
	SYMBOL = 'GALAUSDT'
	CUSTOMS = {
		'direction': 'long',
		'count': 8,
		'sltpRatio': 0.25,
	}

	ORDERLIST = OrderExecutor.gen_orders(SYMBOL, **CUSTOMS)
	# [print(x) for x in ORDERLIST]
	OrderExecutor.bulk_execute(ORDERLIST, debug=0)


if __name__ == '__main__':
	main()
