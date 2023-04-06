from client import Client
from json import loads
from datetime import datetime

import requests

import websocket, json, pprint, talib
import config, c, math
from binance.client import Client
from binance.enums import *
import numba as nb
import numpy as np
import mienzo as m


#YOU NEED THREADING LOL

TRADE_SYMBOL='BTCUSDT'
TRADE_QUANTITY=0
closes15=[]
closesT15=[]


in_position=False
long_position=False
short_position=False

opened=0
closed=0
shortClosed=0
shortOpened=0


profitShort=1
profit=1

closedRev=0
openedRev=0

STABLE_SHORT=20
STABLE_LONG=11
SHORT_QUANTITY_START=0
SHORT_QUANTITY_END=0
LONG_QUANTITY=0



client=Client(config.API_KEY, config.API_SECRET, tld='com')



class Bi15(Client):
    def __init__(self, url, exchange, lock):
        super().__init__(url, exchange)

        # local data management
        self.lock = lock
        
    

    def on_open(self):
        global closes15, closesT15
        for kline in client.get_historical_klines_generator(TRADE_SYMBOL, Client.KLINE_INTERVAL_15MINUTE, "3 years ago"):
            closes15.append(float(kline[4]))
        closes15.pop()
        closesT15=closes15
        #code for historical klines looped through array that is received or added to numpy closes
        #global closes.append(float(kline));  for kline in client.gethistorical "4 years ago UTC"

        print('opened connection')


    def on_close(self):
        print('closed connection')


    def on_message(self, message):
        global closes15, in_position, close15, closesT15, closedRev, openedRev, closed, opened, TRADE_QUANTITY, long_position, short_position
        global shortClosed, shortOpened, SHORT_QUANTITY_START,SHORT_QUANTITY_END, LONG_QUANTITY, LONG_QUANTITY, profitShort, profit
        print('received message')
        json_message=json.loads(message)
        candle=json_message['k']
        candle_closed=candle['x']
        close15=candle['c']

        print("Open price: "+candle['o']+" Closing price: "+close15)

        
        
        
        #we want the sell quantity to get the successful position start and divide the closing price by it 

        if candle_closed:
            #image recognition from image to text/numbers
            print("15-min candle was closed at {}".format(close15))
            closesT15.append(float(close15))
            print("All 15-min closes:")
            print(closesT15[-5:])
            print("Past Trades: ")
            print(c.pasTrades)
            print("Track Test: ")
            print(c.trackTest)

            #if len(closes) > 24:
            np_closes=np.array(closesT15)
            # rsi6=talib.RSI(np_closes, 6)
            # rsi12=talib.RSI(np_closes, 12)
            # rsi24=talib.RSI(np_closes, 24)
            rsi6 = c.get_rsi(np_closes, 6 )
            rsi12 = c.get_rsi(np_closes, 12 )
            rsi24 = c.get_rsi(np_closes, 24 )
            print("All 15-min RSIs Calculated Thus Far:")
            print(rsi6)
            print(rsi12)
            print(rsi24)
            last_rsi_6=rsi6[-1]
            last_rsi_12=rsi12[-1]
            last_rsi_24=rsi24[-1]
            print("Current 15-min RSI 6 is: {}".format(last_rsi_6))
            print("Current 15-min RSI 12 is: {}".format(last_rsi_12))
            print("Current 15-min RSI 24 is: {}".format(last_rsi_24))
            print("Value of UpTrend: {}".format(m.upTrend))
            print("Value of Long Position: "+long_position+ "  Long Quantity: "+LONG_QUANTITY)
            print("Price at which position opened in Long: "+opened+"  Price Closed in Long: "+closed )
            print("Value of Short Position: "+short_position+ "  Short Quantity Start: "+SHORT_QUANTITY_START+" Short Quantity End: "+SHORT_QUANTITY_END)
            print("Price at which position opened in Short: "+shortOpened+"  Price Closed in Short: "+shortClosed )

            shortClosed=float(close15)
            profitShort=c.round_up(shortOpened/shortClosed)
            closed=float(close15)
            profit=c.round_up(closed/opened)
            SHORT_QUANTITY_END=STABLE_SHORT/close15

            if not m.upTrend and long_position or long_position and profit<0.972:
                #get quantity to sell btc amount for quick stop loss
                print("STOP LOSS IN LONG POSITION TRIGGERED! CHANGED TO DOWNTREND!")
                c.stop_loss(m.upTrend, SHORT_QUANTITY_START, SHORT_QUANTITY_END, LONG_QUANTITY, 'USDT')
                
                
            if m.upTrend and short_position or short_position and profitShort<0.972:
                #give up short position accept defeat buy back with loss and calculate if your money is 1/3 of the asset make sure to research on prices
                print("STOP LOSS IN SHORT POSITION TRIGGERED! CHANGED TO UPTREND")
                c.stop_loss(m.upTrend, SHORT_QUANTITY_START, SHORT_QUANTITY_END, LONG_QUANTITY, 'BTC')

            upmidDistance=last_rsi_6 - last_rsi_12
            middownDistance=last_rsi_12 - last_rsi_24

            if upmidDistance<-1.5 and middownDistance<-1.5 and last_rsi_24<45 or m.newLong:
                if m.upTrend:
                    if long_position:
                        print("It is oversold but you have it already so YEET")

                    else:
                        openedRev=float(close15)
                        profitRev=c.round_up(closedRev/openedRev)
                        if profitRev>1.03 or last_rsi_24<43 :
                            c.long_buy_hist(last_rsi_6, last_rsi_12, last_rsi_24)
                            
                            TRADE_QUANTITY=c.round_up(STABLE_LONG/close15)
                            order_successful= c.order_buy(TRADE_QUANTITY, TRADE_SYMBOL)
                        
                            if order_successful:
                                opened=float(close15)
                                long_position=True
                                c.long_buy_conf(last_rsi_6, last_rsi_12, last_rsi_24)
                                

                else: 
                    if short_position:
                        #if last_rsi_6>60
                        if profitShort > 1.022 or last_rsi_6<15:
                            hoh=c.close_short(SHORT_QUANTITY_START, SHORT_QUANTITY_END, 'BTC')
                            #market buy then repay
                            if hoh:
                                short_position=False
                                m.newShort=False
                                print("SHORT TRADE FINISHED!")
                    else:
                        print("Downtrend but still looking for optimal short position!") 


            if upmidDistance>2 and middownDistance>2: #61
                c.long_sell_hist(last_rsi_6, last_rsi_12, last_rsi_24)
                closedRev=float(close15)

                if m.upTrend and last_rsi_6>75 and last_rsi_24>60:
                    if long_position:
                        print("Overbought! Checking if profitable...")
                        
                        if profit > 1.03:
                            #sell logic binance
                            order_successful= c.order_sell(TRADE_QUANTITY,TRADE_SYMBOL)
                            
                            if order_successful:
                                long_position=False
                                m.newLong=False
                                c.long_sell_conf(last_rsi_6, last_rsi_12, last_rsi_24)
                        else:
                            print("LIESSS!!!")
                        
                    else: 
                        print("It is overbought, but you're not in a position, so YEET!")

                elif not m.upTrend and last_rsi_6>61 and last_rsi_24>48 or m.newShort:
                    if short_position:
                        print("Already in short position!")

                    else:
                        print("Currently in downtrend and getting potential OPEN SHORT POSITION")
                        SHORT_QUANTITY_START=STABLE_SHORT/close15
                        shortOpened=float(close15)
                        hoh=c.open_short(SHORT_QUANTITY_START, 'BTC')
                        if hoh:
                            print("YOU HAVE OPENED A SHORT TRADE")
                            short_position=True
                        else:
                            print("YOU HAVE NOT OPENED THE SHORT TRADE ERROR ERROR")