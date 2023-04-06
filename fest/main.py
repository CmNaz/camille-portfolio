from bi15 import Bi15
from biHR import BiHR

import threading
import time

#troit again
if __name__ == "__main__":
    # data management
    lock = threading.Lock()

    # create websocket threads
    b15 = Bi15(
        url="wss://stream.binance.com:9443/ws/btcusdt@kline_15m",
        exchange="Binance15",
        lock=lock
    )

    b15.start()

    
    bHR = BiHR(
        url="wss://stream.binance.com:9443/ws/btcusdt@kline_1h",
        exchange="BinanceHR",
        lock=lock
    )
    bHR.start()

    
    
    


    
    
# import threading

# class T1(threading.Thread):
#     def run(self):


# class T2(threading.Thread):
#     def run(self):


# if __name__=="__main__":
#     t1=T1()
#     t1.start()

#     t2=T2()
#     t2.start()
