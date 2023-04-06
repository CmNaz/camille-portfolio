from client import Client
from json import loads
from datetime import datetime

import requests

import websocket, json, pprint
import config, c, math
from binance.client import Client
from binance.enums import *
import numba as nb
import numpy as np
import mienzo as m

TRADE_SYMBOL='BTCUSDT'
closesHR=[]
closesTHR=[]

instanceShort=0
instanceLong=0
newShort=False
newLong=False

upTrend=False

client=Client(config.API_KEY, config.API_SECRET, tld='com')


class BiHR(Client):
    def __init__(self, url, exchange, lock):
        super().__init__(url, exchange)

        # local data management
        self.lock = lock
        
    def on_open(self):
        global closesHR, closesTHR
        for kline in client.get_historical_klines_generator(TRADE_SYMBOL, Client.KLINE_INTERVAL_1HOUR, "3 years ago"):
            closesHR.append(float(kline[4]))
        closesHR.pop()
        closesTHR=closesHR

        print('opened hour connection')

    def on_close(self):
        print('closed hour connection')

    def on_message(self, message):
        print('received hourly message')
        global closesHR, closesTHR, upTrend, instanceShort, instanceLong, newLong, newShort

        json_message=json.loads(message)
        pprint.pprint(json_message)

        candle=json_message['k']
        candle_closed=candle['x']
        closeHR=candle['c']

        if candle_closed:
            #image recognition from image to text/numbers
            print("1-hour candle was closed at {}".format(closeHR))
            closesTHR.append(float(closeHR))
            print("All 1-hour closes:")
            print(closesTHR[-5:])
            print("Past Trades: ")
            print(c.pasTrades)
            print("Track Test: ")
            print(c.trackTest)

            #if len(closes) > 24:
            np_closes=np.array(closesTHR)
            # rsi6=talib.RSI(np_closes, 6)
            # rsi12=talib.RSI(np_closes, 12)
            # rsi24=talib.RSI(np_closes, 24)
            rsi6 = c.get_rsi(np_closes, 6 )
            rsi12 = c.get_rsi(np_closes, 12 )
            rsi24 = c.get_rsi(np_closes, 24 )
            print("All 1-hour RSIs Calculated Thus Far:")
            print(rsi6)
            print(rsi12)
            print(rsi24)
            last_rsi_6=rsi6[-1]
            last_rsi_12=rsi12[-1]
            last_rsi_24=rsi24[-1]
            print("Current 1-hour RSI 6 is: {}".format(last_rsi_6))
            print("Current 1-hour RSI 12 is: {}".format(last_rsi_12))
            print("Current 1-hour RSI 24 is: {}".format(last_rsi_24))

            upmidDistance=last_rsi_6 - last_rsi_12
            middownDistance=last_rsi_12 - last_rsi_24

            if upmidDistance>2 and middownDistance>2:
                upTrend=True
                m.upTrend=upTrend
                instanceShort=0
                m.instanceShort=instanceShort
                instanceLong+=1
                m.instanceLong=instanceLong
                if instanceLong==1:
                    newLong=True
                    m.newLong=newLong

                
            if upmidDistance<-2 and middownDistance<-2:
                upTrend=False
                m.upTrend=upTrend
                instanceLong=0
                m.instanceLong=instanceLong
                instanceShort+=1
                m.instanceShort=instanceShort
                if instanceShort==1:
                    newShort=True
                    m.newShort=newShort
