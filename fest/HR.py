import threading, time, c, config, trn
import numpy as np
import pandas as pd
import websocket, json
from binance.client import Client
from binance.enums import *

client=Client(config.API_KEY, config.API_SECRET, tld='com')

class biHR(threading.Thread):
    def __init__(self,u):
        super(biHR, self).__init__()
        self.lock=threading.Lock()
        self.u=u
        self.SOCKET="wss://stream.binance.com:9443/ws/"+self.u.TRADE_SYMBOL.lower()+"@kline_1h"
        self.death=False
 
    # function using _stop function
    def stop(self):
        self.death=True
        return

    def run(self):
        while True:
            def do(self):
                print("All 1-hour closes:\r\r")
                print(self.u.closesTHR[-5:])
                c.closesTHR_1=self.u.closesTHR[-5:]
                print("Past Trades: \r\r")
                print(c.pasTrades[-10:])
                print("Track Test: \r\r")
                print(c.trackTest[-10:])

                #if len(closes) > 24:
                np_closes=np.array(self.u.closesTHR)
                series=pd.Series(np_closes) #take off if orig rsi formula
                c.stoch(self,np_closes)
                array_high=np.array(c.highsHR)
                array_high=pd.Series(array_high)
                array_low=np.array(c.lowsHR)
                array_low=pd.Series(array_low)
                array_close=self.u.closesTHR
                if c.usual:
                    c.KDJ(self, array_high, array_low, array_close)
                # rsi6=talib.RSI(np_closes, 6)
                # rsi12=talib.RSI(np_closes, 12)
                # rsi24=talib.RSI(np_closes, 24)
                rsi6 = c.computeRSI(series, 6 )
                rsi12 = c.computeRSI(series, 12 )
                rsi24 = c.computeRSI(series, 24 )
                print("All 1-hour RSIs Calculated Thus Far:\r")
                print(rsi6[-5:])
                print(rsi12[-5:])
                print(rsi24[-5:])
                last_rsi_6=round(float(rsi6[-1:]),2)
                last_rsi_12=round(float(rsi12[-1:]), 2)
                last_rsi_24=round(float(rsi24[-1:]), 2)
                print(type(last_rsi_6))
                c.rsi6_1=last_rsi_6
                c.rsi12_1=last_rsi_12
                c.rsi24_1=last_rsi_24
                print("Current 1-hour RSI 6 is: {}".format(last_rsi_6))
                print("Current 1-hour RSI 12 is: {}".format(last_rsi_12))
                print("Current 1-hour RSI 24 is: {}".format(last_rsi_24))

                upmid=last_rsi_6 - last_rsi_12
                middown=last_rsi_12 - last_rsi_24

                
                if c.usual:
                    #trn.t(self, upmidDistance, middownDistance)
                    try:
                        def up():
                            self.u.upTrend=True
                            self.u.instanceShort=0
                            self.u.instanceLong+=1
                            if self.u.instanceLong==1:
                                self.u.newLong=True
                                self.u.shortClosed=None  

                        def down():
                            self.u.upTrend=False
                            self.u.instanceLong=0
                            self.u.instanceShort+=1
                            if self.u.instanceShort==1:
                                self.u.newShort=True
                                self.u.closed=None

                        def t():
                            if upmid>2 and middown>2:
                                self.u.strupTrend=True #
                                self.u.strdownTrend=False#
                                up()
                                
                            elif upmid<-2 and middown<-2:
                                self.u.strdownTrend=True
                                self.u.strupTrend=False
                                down()

                            else:
                                self.u.strdownTrend=False
                                self.u.strupTrend=False

                            if self.u.upTrend:
                                if c.kdjstrdownTrend and not self.u.strupTrend:
                                    self.u.newLong=False#
                                    down()
                                        
                            elif not self.u.upTrend:
                                if c.kdjstrupTrend and not self.u.strdownTrend:
                                    self.u.newShort=False#
                                    up()
                                #check whether elif is useful wait until tomorrow       
                                elif c.kdjstrdownTrend and not self.u.strupTrend and self.u.instanceShort==0:
                                    self.u.newLong=False
                                    down()
                            
                            c.upTrend=self.u.upTrend
                            c.strdownTrend=self.u.strdownTrend
                            c.strupTrend=self.u.strupTrend
                            c.instanceShort=self.u.instanceShort
                            c.instanceLong=self.u.instanceLong
                            c.closed=self.u.closed
                            c.shortClosed=self.u.shortClosed
                            c.newLong=self.u.newLong
                            c.newShort=self.u.newShort
                        t()
                    except Exception as e:
                        print(e)
                        c.errmsg=e
                        
                else: 
                    print("1-HR is not activated, therefore no config change")
            #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            
            
        
            #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


            
            def on_openHR(w):
                self.lock.acquire()
                for kline in client.get_historical_klines_generator(self.u.TRADE_SYMBOL, Client.KLINE_INTERVAL_1HOUR, "3 months ago"):
                    self.u.closesHR.append(float(kline[4]))
                    c.highsHR.append(float(kline[2]))
                    c.lowsHR.append(float(kline[3]))
                self.u.closesHR.pop()
                c.highsHR.pop()
                c.lowsHR.pop()
                print(c.highsHR)
                print(c.lowsHR)
                self.u.closesTHR=self.u.closesHR
                c.start=True
                do(self)
                
                
                print('~~~~~~~OPENED HOUR CONNECTION~~~~~~~')
                c.status1=True
                self.lock.release()
                time.sleep(0.5)

            def on_closeHR(w):
                print('~~~~~~~CLOSED HOUR CONNECTION~~~~~~~')
                c.status1=False

            def on_messageHR(w, msg):
                self.lock.acquire()
                print('['+self.u.TRADE_SYMBOL+'] received hourly message')
                
                json_message=json.loads(msg)
                
                candle=json_message['k']
                candle_closed=candle['x']
                self.u.closeHR=candle['c']
                highHR=candle['h']
                lowHR=candle['l']
                

                print("Open price: "+candle['o']+" Closing price: "+self.u.closeHR)

                if candle_closed:
                    #image recognition from image to text/numbers
                    print("1-hour candle was closed at {}".format(self.u.closeHR))
                    self.u.closesTHR.append(float(self.u.closeHR))
                    c.highsHR.append(float(highHR))
                    c.lowsHR.append(float(lowHR))
                    do(self)
                    c.HR_end=True
                self.lock.release()
                time.sleep(2)
                    
            if self.death:
                w.close()
                return

            w=websocket.WebSocketApp(self.SOCKET, on_open=on_openHR, on_close=on_closeHR, on_message=on_messageHR)
            w.run_forever()
            #upTrend, instanceShort, instanceLong, newLong, newShort, close15, closesT15,