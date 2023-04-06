import threading, time, c, config
import numpy as np
import pandas as pd
import websocket, json
from binance.client import Client
from binance.enums import *
import datetime

now=datetime.datetime.now()

client=Client(config.API_KEY, config.API_SECRET, tld='com')
class bi1MIN(threading.Thread):
    def __init__(self,u):
        super(bi1MIN, self).__init__()
        self.lock=threading.Lock()
        self.u=u

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
        self.SOCKET="wss://stream.binance.com:9443/ws/"+self.u.TRADE_SYMBOL.lower()+"@kline_1m"
        self.death=False
 
    # function using _stop function
    def stop(self):
        self.death=True
        return
 
 
    def run(self):
        while True:
            def do(self):
                print("All 1-MIN closes:\r")
                print(self.u.closesT15[-5:])
                print("Past Trades: \r")
                print(c.pasTrades[-10:])
                print("Track Test: \r")
                print(c.trackTest[-10:])
                self.u.do()
                # self.u.geste=True
            
            def on_open(ws):
                self.lock.acquire()
                for kline in client.get_historical_klines_generator(self.u.TRADE_SYMBOL, Client.KLINE_INTERVAL_1MINUTE, "2 days ago"):
                    self.u.closes15.append(float(kline[4]))
                self.u.closes15.pop()
                self.u.closesT15=self.u.closes15
                #do(self)
                print('~~~~~~~OPENED 1-MIN CONNECTION~~~~~~~')
                c.status4=True
                self.lock.release()
                time.sleep(2)
                #code for historical klines looped through array that is received or added to numpy closes
                #global closes.append(float(kline));  for kline in client.gethistorical "4 years ago UTC"
                
                
            def on_close(ws):
                print('~~~~~~~CLOSED 1-MIN CONNECTION~~~~~~~')
                c.status4=False
            def on_message(ws, message):
                self.lock.acquire()
                
                print('['+self.u.TRADE_SYMBOL+'] received 1-MIN message')
                json_message=json.loads(message)
                candle=json_message['k']
                candle_closed=candle['x']
                self.u.close15=candle['c']

                print("Open price: "+candle['o']+" Closing price: "+self.u.close15)
                #image recognition from image to text/numbers
                try:
                
                    self.u.close15=float(self.u.close15)
                    # if now.minute%15==0:
                    #     while not c.MIN15_end:
                    #         time.sleep(1)
                    def meth():
                        longProzent=1.022
                        shortProzent=1.022
                        # else:
                        #     longProzent=1.006
                        #     shortProzent=1.006
                            #we dont need to put close15 variable since we take the one from 1 min

                        self.u.long_position=c.long_position
                        self.u.short_position=c.short_position

                        if self.u.long_position and not c.strupTrend:
                            if self.u.close15/c.opened>longProzent:
                                #sell logic binance
                                order_successful= c.order_sell(self.u.LONG_QUANTITY,self.u.TRADE_SYMBOL)
                                
                                if order_successful:
                                    self.u.closed=self.u.close15
                                    c.closed=self.u.close15
                                    self.u.long_position=False
                                    c.long_position=False
                                    self.u.closedRev=self.u.close15
                                    c.closedRev=self.u.closedRev


                        elif self.u.short_position and not c.strdownTrend:
                            if c.shortOpened/self.u.close15>shortProzent:
                                self.u.SHORT_QUANTITY_END=c.round_up(self.u.STABLE_SHORT/self.u.close15)
                                c.SHORT_QUANTITY_END=self.u.SHORT_QUANTITY_END
                                print("Attempting to exit short position!\r")
                                hoh=c.close_short(self.u.SHORT_QUANTITY_START, self.u.SHORT_QUANTITY_END, self.u.TRADE_SYMBOL, self.u.CRYPT)
                                #market buy then repay
                                if hoh:
                                    self.u.short_position=False
                                    self.u.shortCont=False
                                    self.u.shortClosed=self.u.close15
                                    c.shortClosed=self.u.close15
                                    c.short_position=False
                                    c.shortCont=False
                                    
                                    print("SHORT TRADE FINISHED!\r")
                                    

                    if candle_closed:
                        print("1-MIN candle was closed at {}".format(self.u.close15))
                        self.u.closesT15.append(float(self.u.close15))
                        meth()
                        if not c.usual and c.zctr>9:
                            do(self)
                            c.strl4=self.u.statement15
                        
                        c.MIN5_end=False

                    self.lock.release()
                    time.sleep(0.5)
                except Exception as e:
                    print(e)
                    c.errmsg=e

            if self.death:
                ws.close()
                return

        

            ws=websocket.WebSocketApp(self.SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
            ws.run_forever()  