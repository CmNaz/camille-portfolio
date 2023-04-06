#there used to be talib here
import config, math
from binance.client import Client
from binance.enums import *
import numba as nb
import numpy as np
client=Client(config.API_KEY, config.API_SECRET, tld='com')

pasTrades=[]
trackTest=[]

@nb.jit(fastmath=True, nopython=True)   
def calc_rsi( array, deltas, avg_gain, avg_loss, n ):

    # Use Wilder smoothing method
    up   = lambda x:  x if x > 0 else 0
    down = lambda x: -x if x < 0 else 0
    i = n+1
    for d in deltas[n+1:]:
        avg_gain = ((avg_gain * (n-1)) + up(d)) / n
        avg_loss = ((avg_loss * (n-1)) + down(d)) / n
        if avg_loss != 0:
            rs = avg_gain / avg_loss
            array[i] = 100 - (100 / (1 + rs))
        else:
            array[i] = 100
        i += 1

    return array

def get_rsi( array, n = 14 ):   

    deltas = np.append([0],np.diff(array))

    avg_gain =  np.sum(deltas[1:n+1].clip(min=0)) / n
    avg_loss = -np.sum(deltas[1:n+1].clip(max=0)) / n

    array = np.empty(deltas.shape[0])
    array.fill(np.nan)

    array = calc_rsi( array, deltas, avg_gain, avg_loss, n )
    return array

#rsi = get_rsi( array or series, 14 )

def round_up(n, decimals=6):
    multiplier = 10 ** decimals
    return round(n * multiplier) / multiplier

def order_buy(quantity, symbol):
    try:
        print("sending order\r")
        order=client.order_market_buy(symbol=symbol, quantity=quantity)
        print(order)
        
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True 

def order_sell(quantity, symbol):
    try:
        print("sending order\r")
        order=client.order_market_sell(symbol=symbol, quantity=quantity)
        print(order)
        
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True 

def long_buy_hist(j6,j12,j24):
    print("Oversold! Buy! Buy! Buy!\r")
    entranceInfo6="Potential LONG buy at RSI 6: {}".format(j6)
    entranceInfo12="RSI 12: {}".format(j12)
    entranceInfo24="RSI 24: {}".format(j24)
    trackTest.append(entranceInfo6+" "+entranceInfo12+" "+entranceInfo24)

def long_buy_conf(a6,a12,a24):
    print("You have successfully engaged in a LONG position!\r")
    entranceInfo6="Bought at RSI 6: {}".format(a6)
    entranceInfo12="RSI 12: {}".format(a12)
    entranceInfo24="RSI 24: {}".format(a24)
    pasTrades.append(entranceInfo6+" "+entranceInfo12+" "+entranceInfo24)

def long_sell_hist(k6, k12, k24):
    entranceInfo6="Potential LONG sell at RSI 6: {}".format(k6)
    entranceInfo12="RSI 12: {}".format(k12)
    entranceInfo24="RSI 24: {}".format(k24)
    trackTest.append(entranceInfo6+" "+entranceInfo12+" "+entranceInfo24)

def long_sell_conf(b6, b12, b24):
    print("You have exited your previous LONG position! Searching for a new one...\r")
    entranceInfo6="Sold at RSI 6: {}".format(b6)
    entranceInfo12="RSI 12: {}".format(b12)
    entranceInfo24="RSI 24: {}".format(b24)
    pasTrades.append(entranceInfo6+" "+entranceInfo12+" "+entranceInfo24)
    
def open_short(quantity, asset, symbol):
    non=borrow_margin(quantity, asset, symbol)
    if non:
        print("BORROWED BITCOIN SUCCESSFULLY\r")
        print("CONFIRMING SELL...\r")
        nan=margin_sell(quantity, symbol)
        if nan:
            print("SOLD BITCOIN SUCCESS! WAITING FOR BUY BACK OPPORTUNITIES...\r")
            return True
        
        else:
            print("JOKE'S ON YOU SELL FAILED\r")
            return False
    
    else:
        print("LOL CAN'T EVEN START THE SHORT POSITION PATHETIC\r")
        return False

def close_short(startquantity, endquantity, asset, symbol):
    non=margin_buy(endquantity, symbol)
    if non:
        print("BUY BACK BITCOIN SUCCESS! WAITING FOR BITCOIN REPAYMENT...\r")
        nan=repay_margin(startquantity, asset, symbol)
        if nan:
            print("YOU FRIKKIN DID IT MATE! CHEERS!\r")
            return True
        else:
            print("YOU CAN'T ESCAPE! MUST REPAY MANUALLY LOL\r")
            return False
    else:
        print("FAILED TO BUY BACK BITCOIN HUHU\r")
        return False

def margin_sell(quantity,symbol):
    try:
        print("sending order\r")
        order = client.create_margin_order(symbol=symbol,side=SIDE_SELL,type=ORDER_TYPE_MARKET,quantity=quantity,isIsolated='TRUE')
        print(order)
        
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True 

def margin_buy(quantity,symbol):
    try:
        print("sending order\r")
        order = client.create_margin_order(symbol=symbol,side=SIDE_BUY,type=ORDER_TYPE_MARKET,quantity=quantity,isIsolated='TRUE')#,isIsolated='TRUE'
        print(order)
        
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True 
    

def borrow_margin(quantity,asset,symbol):
    try:
        print("borrowing bitcoin...\r")
        order=client.create_margin_loan(asset=asset, amount=quantity,isIsolated='TRUE',symbol=symbol)
        print(order)
        
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True 

def repay_margin(quantity,asset,symbol):
    try:
        print("sending order\r")
        order=client.repay_margin_loan(asset=asset, amount=quantity,isIsolated='TRUE',symbol=symbol)
        print(order)
        
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True 

def stop_loss(trendUp, startquant, endquant, longquant, asset, symbol):
    if trendUp:
        print("Trend has turned up while in SHORT position! Initiating stop loss BUY BACK AND REPAY! \r")
        heh=close_short(startquant, endquant, asset, symbol )
        if heh:
            return True

    else: 
        print("Trend has turned down while in LONG position! Initiating stop loss SELL!\r")
        print("\r")
        heh=order_sell(longquant, symbol )
        if heh:
            return True