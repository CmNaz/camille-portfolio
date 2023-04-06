import threading, time, c, config, trn
import numpy as np
import pandas as pd
import websocket, json
from binance.client import Client
from binance.enums import *
import datetime

now=datetime.datetime.now()

client=Client(config.API_KEY, config.API_SECRET, tld='com')
class bi5MIN(threading.Thread):
    def __init__(self,u,u2):
        super(bi5MIN, self).__init__()
        self.lock=threading.Lock()
        self.u=u
        self.u2=u2
        self.u.long_position=c.long_position
        self.u.short_position=c.short_position

        self.u.opened=c.opened
        self.u.closed=c.closed
        self.u.shortClosed=c.shortClosed
        self.u.shortOpened=c.shortOpened

        self.u.profitShort=c.profitShort
        self.u.profit=c.profit

        self.u.closedRev=c.closedRev
        self.u.openedRev=c.openedRev

       
        self.u.SHORT_QUANTITY_START=c.SHORT_QUANTITY_START
        self.u.SHORT_QUANTITY_END=c.SHORT_QUANTITY_END
        self.u.LONG_QUANTITY=c.LONG_QUANTITY

        self.u.instanceShort=c.instanceShort
        self.u.instanceLong=c.instanceLong
        self.u.newShort=c.newShort
        self.u.newLong=c.newLong
        
        self.u.profitRev=c.profitRev
        self.u.shortCont=c.shortCont
        self.SOCKET="wss://stream.binance.com:9443/ws/"+self.u.TRADE_SYMBOL.lower()+"@kline_5m"
        self.death=False
 
    # function using _stop function
    def stop(self):
        self.death=True
        return

    def run(self):
        while True:
            def doUsual(self):
                print("All 5-min closes:\r")
                print(self.u.closesT15[-5:])
                print("Past Trades: \r")
                print(c.pasTrades[-10:])
                print("Track Test: \r")
                print(c.trackTest[-10:])
                self.u.do()
            def doNot(self):
                print("All 5-MIN closes:\r\r")
                print(self.u.closesT15[-5:])
                
                c.closesT15_3=self.u.closesT15[-5:]
                print(c.pasTrades[-10:])
                print("Track Test: \r\r")
                print(c.trackTest[-10:])

                array_high=np.array(c.highs15_5)
                array_high=pd.Series(array_high)
                array_low=np.array(c.lows15_5)
                array_low=pd.Series(array_low)
                array_close=self.u.closesT15
                c.KDJ(self, array_high, array_low, array_close)
                #if len(closes) > 24:
                np_closes=np.array(self.u.closesT15)
                # rsi6=talib.RSI(np_closes, 6)
                # rsi12=talib.RSI(np_closes, 12)
                # rsi24=talib.RSI(np_closes, 24)
                rsi6 = c.get_rsi(np_closes, 6 )
                rsi12 = c.get_rsi(np_closes, 12 )
                rsi24 = c.get_rsi(np_closes, 24 )
                print("All 5-MIN RSIs Calculated Thus Far:\r")
                print(rsi6[-5:])
                print(rsi12[-5:])
                print(rsi24[-5:])
                last_rsi_6=round(float(rsi6[-1:]), 2)
                last_rsi_12=round(float(rsi12[-1:]), 2)
                last_rsi_24=round(float(rsi24[-1:]), 2)
                c.rsi6_3=last_rsi_6
                c.rsi12_3=last_rsi_12
                c.rsi24_3=last_rsi_24
                print("Current 5-MIN RSI 6 is: {}".format(last_rsi_6))
                print("Current 5-MIN RSI 12 is: {}".format(last_rsi_12))
                print("Current 5-MIN RSI 24 is: {}".format(last_rsi_24))

                upmidDistance=last_rsi_6 - last_rsi_12
                middownDistance=last_rsi_12 - last_rsi_24

                trn.t(self, upmidDistance, middownDistance)
                
            def on_openHR(w):
                self.lock.acquire()
                for kline in client.get_historical_klines_generator(self.u.TRADE_SYMBOL, Client.KLINE_INTERVAL_5MINUTE, "2 days ago"):
                    self.u.closes15.append(float(kline[4]))
                    c.highs15_5.append(float(kline[2]))
                    c.lows15_5.append(float(kline[3]))
                self.u.closes15.pop()
                c.highs15_5.pop()
                c.lows15_5.pop()
                print(c.highs15_5)
                print(c.lows15_5)
                self.u.closesT15=self.u.closes15
                self.u2.closesTHR=self.u.closesT15

                #doUsual(self)
                self.lock.release()
                time.sleep(2)

                print('~~~~~~~OPENED 5-MIN CONNECTION~~~~~~~')
                c.status3=True
                
            def on_closeHR(w):
                print('~~~~~~~CLOSED 5-MIN CONNECTION~~~~~~~')
                c.status3=False

            def on_messageHR(w, msg):
                self.lock.acquire()
                print('['+self.u.TRADE_SYMBOL+'] received 5-MIN message')
                json_message=json.loads(msg)
                candle=json_message['k']
                candle_closed=candle['x']
                self.u.close15=candle['c']
                high15=candle['h']
                low15=candle['l']

                print("Open price: "+candle['o']+" Closing price: "+self.u.close15)

                self.u.close15=float(self.u.close15)
                
                if now.minute%15==0:
                    while not c.MIN15_end:
                        time.sleep(1)

                if candle_closed:
                    #image recognition from image to text/numbers
                    print("5-MIN candle was closed at {}".format(self.u.close15))
                    self.u.closesT15.append(float(self.u.close15))
                    self.u2.closesTHR=self.u.closesT15
                    c.highs15_5.append(float(high15))
                    c.lows15_5.append(float(low15))

                    if not c.usual and c.zctr<10 and c.zctr>6:
                        doUsual(self)
                        c.strl3=self.u.statement15
                    elif not c.usual and c.zctr>9:
                        doNot(self)
                    
                    c.MIN15_end=False
                    c.MIN5_end=True
                self.lock.release()
                time.sleep(0.5)
            
            if self.death:
                w.close()
                return
                    
            w=websocket.WebSocketApp(self.SOCKET, on_open=on_openHR, on_close=on_closeHR, on_message=on_messageHR)
            w.run_forever()
            #upTrend, instanceShort, instanceLong, newLong, newShort, close15, closesT15,
