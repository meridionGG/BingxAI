from bingx.api import BingxAPI
from keys import APIKEY, SECRETKEY
from get_price import get_price

API_KEY = APIKEY
SECRET_KEY = SECRETKEY
bingx = BingxAPI(API_KEY, SECRET_KEY, timestamp="local")

def convert(param):

    symbol = (param["торговая пара"]).upper()

    positionSide = param["позиция"].lower()

    if positionSide == "шорт":
        positionSide = "SHORT"
        side = "SELL"
    elif positionSide == "лонг":
        positionSide = "LONG"
        side = "BUY"

    leverage = param["плечо"]
    type = param["точка входа"]

    stopLoss = param["стоп-лосс"]
    print(f"stoploss - {stopLoss}")

    if stopLoss == None:
        stopLoss = "0"

    takeProfit = param["тейк-профит"]

    if takeProfit == None:
        takeProfit = "0"

    deposit_percent = int(param["% от депозита"])

    quantity = get_price(symbol, deposit_percent)

    if type != float:
        return create_market_trade(symbol, side, leverage, type, quantity, stopLoss, takeProfit, positionSide)


    return create_limit_trade(symbol, side, leverage, type, quantity, stopLoss, takeProfit, positionSide)

def create_market_trade(symbol, side, leverage, type, quantity, stopLoss, takeProfit, positionSide):
    print(1)

    order_data = bingx.open_market_order(pair=f'{symbol}-USDT', position_side=positionSide, volume=quantity, tp=takeProfit, sl=stopLoss)
    print(order_data)

def create_limit_trade(symbol, side, positionSide, leverage, type, quantity, stopLoss, takeProfit):
    print(2)

    order_data = bingx.open_limit_order(pair=f'{symbol}-USDT', position_side=positionSide, price=85500, volume=quantity, tp=takeProfit, sl=stopLoss)
    print(order_data)