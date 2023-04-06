import websocket, json, pprint #there used to be talib here
import config, c, math
from binance.client import Client
from binance.enums import *
import numba as nb
import numpy as np
import threading
import time
from xuslov import viye

# SOCKET="wss://stream.binance.com:9443/ws/btcusdt@kline_15m"
# SOCKET2="wss://stream.binance.com:9443/ws/btcusdt@kline_1h"
#self.SOCKET="wss://stream.binance.com:9443/ws/"+self.u.TRADE_SYMBOL+"@kline_15m"
#Everytime the market normalizes i.e. the 6,12,24 rsis are around 50, that is the most optimal starting point



threadMin=[]
threadHr=[]
threadv=[]

client=Client(config.API_KEY, config.API_SECRET, tld='com')

ex=['BTCUSDT'] #,'ADAUSDT'
crypt=['BTC']
ctr=0
viy=[]

#change variables from main.py then just keep getting info from there when required by other .py files
class biHR(threading.Thread):
    def __init__(self,u):
        super(biHR, self).__init__()
        self.lock=threading.Lock()
        self.u=u
        self.SOCKET="wss://stream.binance.com:9443/ws/"+self.u.TRADE_SYMBOL.lower()+"@kline_5m"
        
    def run(self):
        def do(self):
            
            print("All 1-hour closes:\r\r")
            print(self.u.closesTHR[-5:])
            print("Past Trades: \r\r")
            print(c.pasTrades)
            print("Track Test: \r\r")
            print(c.trackTest)

            #if len(closes) > 24:
            np_closes=np.array(self.u.closesTHR)
            # rsi6=talib.RSI(np_closes, 6)
            # rsi12=talib.RSI(np_closes, 12)
            # rsi24=talib.RSI(np_closes, 24)
            rsi6 = c.get_rsi(np_closes, 6 )
            rsi12 = c.get_rsi(np_closes, 12 )
            rsi24 = c.get_rsi(np_closes, 24 )
            print("All 1-hour RSIs Calculated Thus Far:\r")
            print(rsi6[-5:])
            print(rsi12[-5:])
            print(rsi24[-5:])
            last_rsi_6=rsi6[-1]
            last_rsi_12=rsi12[-1]
            last_rsi_24=rsi24[-1]
            print("Current 1-hour RSI 6 is: {}".format(last_rsi_6))
            print("Current 1-hour RSI 12 is: {}".format(last_rsi_12))
            print("Current 1-hour RSI 24 is: {}".format(last_rsi_24))

            upmidDistance=last_rsi_6 - last_rsi_12
            middownDistance=last_rsi_12 - last_rsi_24

            if upmidDistance>2 and middownDistance>2:
                self.u.upTrend=True
                self.u.instanceShort=0
                self.u.instanceLong+=1
                self.u.strupTrend=True
                if self.u.instanceLong==1:
                    self.u.newLong=True
                    self.u.shortClosed=None
                    
                
            elif upmidDistance<-2 and middownDistance<-2:
                self.u.upTrend=False
                self.u.instanceLong=0
                self.u.instanceShort+=1
                self.u.strdownTrend=True
                if self.u.instanceShort==1:
                    self.u.newShort=True
                    self.u.closed=None
                    

            else:
                self.u.strdownTrend=False
                self.u.strupTrend=False
        
        def on_openHR(w):
            self.lock.acquire()
            for kline in client.get_historical_klines_generator(self.u.TRADE_SYMBOL, Client.KLINE_INTERVAL_5MINUTE, "2 days ago"):
                self.u.closesHR.append(float(kline[4]))
            self.u.closesHR.pop()
            self.u.closesTHR=self.u.closesHR
            do(self)
            self.lock.release()
            time.sleep(2)

            print('opened hour connection')

        def on_closeHR(w):
            print('closed hour connection')

        def on_messageHR(w, msg):
            self.lock.acquire()
            print('['+self.u.TRADE_SYMBOL+'] received hourly message')
            
            json_message=json.loads(msg)
            
            candle=json_message['k']
            candle_closed=candle['x']
            self.u.closeHR=candle['c']

            print("Open price: "+candle['o']+" Closing price: "+self.u.closeHR)

            if candle_closed:
                #image recognition from image to text/numbers
                print("1-hour candle was closed at {}".format(self.u.closeHR))
                self.u.closesTHR.append(float(self.u.closeHR))
                do(self)
            self.lock.release()
                
                

        w=websocket.WebSocketApp(self.SOCKET, on_open=on_openHR, on_close=on_closeHR, on_message=on_messageHR)
        w.run_forever()
        #upTrend, instanceShort, instanceLong, newLong, newShort, close15, closesT15,

class bi15(threading.Thread):
    def __init__(self,u):
        super(bi15, self).__init__()
        self.lock=threading.Lock()
        self.u=u
        self.SOCKET="wss://stream.binance.com:9443/ws/"+self.u.TRADE_SYMBOL.lower()+"@kline_1m"


    def run(self):
        def do(self):
            print("All 15-min closes:\r")
            print(self.u.closesT15[-5:])
            print("Past Trades: \r")
            print(c.pasTrades[-10:])
            print("Track Test: \r")
            print(c.trackTest[-10:])
            self.u.geste=True
        
        def on_open(ws):
            self.lock.acquire()
            for kline in client.get_historical_klines_generator(self.u.TRADE_SYMBOL, Client.KLINE_INTERVAL_1MINUTE, "2 days ago"):
                self.u.closes15.append(float(kline[4]))
            self.u.closes15.pop()
            self.u.closesT15=self.u.closes15
            do(self)
            self.lock.release()
            time.sleep(2)
            #code for historical klines looped through array that is received or added to numpy closes
            #global closes.append(float(kline));  for kline in client.gethistorical "4 years ago UTC"
            print('opened connection')
        def on_close(ws):
            print('closed connection')
        def on_message(ws, message):
            self.lock.acquire()
            print('['+self.u.TRADE_SYMBOL+'] received message')
            json_message=json.loads(message)
            candle=json_message['k']
            candle_closed=candle['x']
            self.u.close15=candle['c']

            print("Open price: "+candle['o']+" Closing price: "+self.u.close15)
            #image recognition from image to text/numbers
            
            

            if candle_closed:
                print("15-min candle was closed at {}".format(self.u.close15))
                self.u.closesT15.append(float(self.u.close15))
                do(self)

            self.lock.release()



        ws=websocket.WebSocketApp(self.SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
        ws.run_forever()               

class pint(threading.Thread):
    def __init__(self,u,symbol,crypt):
        super(pint, self).__init__()
        self.lock=threading.Lock()
        self.u=u
        self.u.TRADE_SYMBOL=symbol
        self.u.CRYPT=crypt
        

    def run(self):
        while True:
            if self.u.geste:
                self.u.do()


# thread1=biHR()
# thread2=bi15()
# thread3=pint()

# thread1.start()
# thread2.start()
# thread3.start()

for i in ex:

    # viy[ctr]=viye()
    viy.append(viye())
    threadv.append(pint(viy[ctr],i,crypt[ctr]))
    threadv[ctr].start()

    threadHr.append(biHR(viy[ctr]))
    threadMin.append(bi15(viy[ctr]))
    

    threadHr[ctr].start()
    threadMin[ctr].start()
    ctr+=1
    