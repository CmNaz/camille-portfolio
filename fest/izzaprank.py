import c
import threading
import time
STABLE_LONG=11

TRADE_SYMBOL='BTCUSDT'
close=52200
profitRev=1
last_rsi_24=44
newLong=True

class threadr(threading.Thread):
    def __init__(self):
        super(threadr, self).__init__()

    def run(self):
        if profitRev>1.03 or last_rsi_24<43 or newLong:
            print("Attempting to enter long position!")
            LONG_QUANTITY=c.round_up(STABLE_LONG/close)
            order=c.order_buy(LONG_QUANTITY, TRADE_SYMBOL)

            if order:
                print("THE BUY ORDER IN C WORKS THOUGH!")
                order_n=c.order_sell(LONG_QUANTITY, TRADE_SYMBOL)
                if order_n:
                    print("THE SELL ORDER IN C WORKS THOUGH AS WELL!")


thread1=threadr()
thread1.start()