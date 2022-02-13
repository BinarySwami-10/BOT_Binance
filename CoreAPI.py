import modulex as mx
import OrderMaker
import Defaults
true = True
false = False

# -	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-


class USD_M:
	limiturl = 'http://www.binance.com/bapi/futures/v1/private/future/order/place-order'
	otourl = 'http://www.binance.com/bapi/futures/v1/private/future/strategy/place-order'

	OTO_Order = {
            "strategyType": "OTO",
            "subOrderList":
            [
                {
                    "strategySubId": 1,
                    "firstDrivenId": 0,
                    "secondDrivenId": 0,
                    "side": "BUY",
                    "positionSide": "BOTH",
                    "symbol": "SANDUSDT",
                    "type": "LIMIT",
                    "timeInForce": "GTC",
                    "quantity": 1,
                    "price": 7.38,
                    "securityType": "USDT_FUTURES",
                    "reduceOnly": false
                    },
                {
                    "strategySubId": 2,
                    # "firstTrigger": "PLACE_ORDER",
                    "firstDrivenOn": "PARTIALLY_FILLED_OR_FILLED",
                    "firstDrivenId": 1,
                    "secondDrivenId": 1,
                    "side": "SELL",
                    "positionSide": "BOTH",
                    "symbol": "SANDUSDT",
                    "type": "LIMIT",
                    "timeInForce": "GTC",
                    "quantity": 1,
                    "price": 7.36,
                    "securityType": "USDT_FUTURES",
                    "reduceOnly": false
                    },
                ]
            }

	LIMIT_Order = {
            "symbol": "SANDUSDT",
            "type": "LIMIT",
            "side": "SELL",
            "positionSide": "BOTH",
            "quantity": 1,
            "reduceOnly": False,
            "timeInForce": "GTC",
            "price": "6.86",
            "placeType": "order-form"
            }

	responseTemplate = {
            "code": "000000",
            "message": None,
            "messageDetail": None,
            "data": {
                "strategyId": 73531738,
                "clientStrategyId": "s3j1r1ZtwQqns6DJhlRrUw",
                "strategyType": "OTO",
                "strategyStatus": "WORKING",
                "updateTime": 1637934005172
                },
            "success": True
            }

# -	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-


class OrderExecutor:
	def bulk_execute(orderlist, future='USD_M', mode='OTO', debug=0):
		headers = mx.parse_headers('headers.raw')

		for o in reversed(orderlist):
			print('RAW_ORDER', o)

			if future == 'USD_M':

				if mode == 'OTO':
					url = USD_M.otourl
					order_template = USD_M.OTO_Order
					first = order_template['subOrderList'][0]
					second = order_template['subOrderList'][1]
					first['quantity'] = o['size']
					second['quantity'] = o['size']

					if o['direction'] == 'long':
						first['side'] = 'BUY'
						first['price'] = o['trigPrice']

						second['side'] = 'SELL'
						second['price'] = o['takeProfit']

					if o['direction'] == 'short':
						first['side'] = 'SELL'
						first['price'] = o['trigPrice']

						second['side'] = 'BUY'
						second['price'] = o['takeProfit']

					print(mx.jdumps(order_template['subOrderList']))
					order_data = mx.jdumps(USD_M.OTO_Order)

				if mode == 'LIMIT':
					url = USD_M.limiturl
					order_data = mx.jdumps(USD_M.LIMIT_Order)

				if not debug:
					r = mx.post_page(url, order_data, headers)
					print(r.json())
				else:
					print('RAW_ORDER', o)

	def generate_orders(SYMBOL, **kwargs,):
		data = eval(f'Defaults.{SYMBOL}')
		data.update(kwargs)

		return(OrderMaker.gen_orders(**data))


# -	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-

class COIN_M:
	LIMIT_Order = {
            "placeType": "order-form",
            "positionSide": "LONG",
            "price": "3107",
            "quantity": 3,
            "side": "BUY",
            "symbol": "ETHUSD_PERP",
            "timeInForce": "GTC",
            "type": "LIMIT"
            }
	OTO_Order = {
            "strategyType": "OTO",
            "subOrderList": [{
                "firstDrivenId": 0,
                "positionSide": "LONG",
                "price": "3107",
                "quantity": 3,
                "secondDrivenId": 0,
                "securityType": "COIN_FUTURES",
                "side": "BUY",
                "strategySubId": 1,
                "symbol": "ETHUSD_PERP",
                "timeInForce": "GTC",
                "type": "LIMIT"
                }, {
                "firstDrivenId": 1,
                "firstDrivenOn": "PARTIALLY_FILLED_OR_FILLED",
                "firstTrigger": "PLACE_ORDER",
                "positionSide": "LONG",
                "priceProtect": True,
                "quantity": 3,
                "secondDrivenId": 0,
                "securityType": "COIN_FUTURES",
                "side": "SELL",
                "stopPrice": "3120",
                "strategySubId": 2,
                "symbol": "ETHUSD_PERP",
                "timeInForce": "GTE_GTC",
                "type": "TAKE_PROFIT_MARKET",
                "workingType": "CONTRACT_PRICE"
                }]
            }


def main():
	SYMBOL = 'CHRUSDT'
	CUSTOMS = {
            'direction': 'long',
          		'count': 6,
          		'stepsize': 0.01,
          		'delta': 0.04,
          		'sizeAccleration': 1,

            }

	ORDERLIST = OrderExecutor.generate_orders(SYMBOL, **CUSTOMS)
	[print(x) for x in ORDERLIST]
	# OrderExecutor.bulk_execute(ORDERLIST)
	# -------- EXAMPLE --------
	# {'trigPrice': '7.25', 'takeProfit': 7.28, 'stepDeltaRatio': '0.02|0.03', 'Spread': '-0.3%|0.02', 'direction': 'long', 'size': 1.0}
	# {'trigPrice': '7.23', 'takeProfit': 7.26, 'stepDeltaRatio': '0.02|0.03', 'Spread': '-0.6%|0.04', 'direction': 'long', 'size': 2.0}


if __name__ == '__main__':
	main()
