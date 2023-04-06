import c
import threading
import time
STABLE_LONG=11



TRADE_SYMBOL='BTCUSDT'
TRADE_QUANTITY=0
closes15=[]
closesT15=[]
closesHR=[]
closesTHR=[]

in_position=False
long_position=True
short_position=False

opened=0
closed=0
shortClosed=0
shortOpened=0

upTrend=False
profitShort=1
profit=1

closedRev=0
openedRev=0

STABLE_SHORT=20
STABLE_LONG=11
SHORT_QUANTITY_START=0
SHORT_QUANTITY_END=0
LONG_QUANTITY=0

instanceShort=0
instanceLong=0
newShort=False
newLong=False

profitRev=0

TRADE_SYMBOL='BTCUSDT'
close=53100
profitRev=1
last_rsi_24=44
newLong=True




def klez():
    global closes15, in_position, close15, closesT15, closedRev, openedRev, closed, opened, TRADE_QUANTITY, long_position, short_position, upTrend
    global shortClosed, shortOpened, SHORT_QUANTITY_START,SHORT_QUANTITY_END, LONG_QUANTITY, LONG_QUANTITY, profitShort, profit, newShort, newLong
    global profitRev
    last_rsi_6=73
    last_rsi_12=69
    last_rsi_24=44

    close15=53100


    shortClosed=float(close15)
    profitShort=c.round_up(shortOpened/shortClosed)
    closed=float(close15)
    profit=c.round_up(5000/4000)
    SHORT_QUANTITY_END=STABLE_SHORT/close15

    upmidDistance=last_rsi_6 - last_rsi_12
    middownDistance=last_rsi_12 - last_rsi_24

    try:

        if (not upTrend and long_position) or (long_position and profit<0.972):
            #get quantity to sell btc amount for quick stop loss
            
            print("STOP LOSS IN LONG POSITION TRIGGERED! CHANGED TO DOWNTREND!\r")
            hoh=c.stop_loss(upTrend, SHORT_QUANTITY_START, SHORT_QUANTITY_END, LONG_QUANTITY, 'USDT')
            if hoh:
                newLong=False

            
            
        elif (upTrend and short_position) or (short_position and profitShort<0.972):
            
            #give up short position accept defeat buy back with loss and calculate if your money is 1/3 of the asset make sure to research on prices
            print("STOP LOSS IN SHORT POSITION TRIGGERED! CHANGED TO UPTREND\r")
            hoh=c.stop_loss(upTrend, SHORT_QUANTITY_START, SHORT_QUANTITY_END, LONG_QUANTITY, 'BTC')
            if hoh:
                newShort=False
            
        else:



            if (upmidDistance<-1.5 and middownDistance<-1.5 and last_rsi_24<45) or newLong:#this newLong is actually useless because of the conditions for profitrev and last rsi
                if upTrend:
                    if long_position:
                        print("It is oversold but you have it already so YEET\r")

                    else:
                        openedRev=float(close15)
                        profitRev=c.round_up(closedRev/openedRev)
                        if (profitRev>1.03) or (last_rsi_24<43) or (newLong): #TTTTTTTTTAAAAAAAAARRRRRRRRRRRRGGGGGGGGGGGGEEEEEEEEEEETTTTTTTTTTT
                            print("Attempting to enter long position!\r")
                            c.long_buy_hist(last_rsi_6, last_rsi_12, last_rsi_24)
                            
                            LONG_QUANTITY=c.round_up(STABLE_LONG/close15)
                            order_successful= c.order_buy(LONG_QUANTITY, TRADE_SYMBOL)
                        
                            if order_successful:
                                opened=float(close15)
                                long_position=True
                                c.long_buy_conf(last_rsi_6, last_rsi_12, last_rsi_24)
                                

                else: 
                    if short_position:
                        #if last_rsi_6>60
                        if (profitShort > 1.022) or (last_rsi_6<15):
                            print("Attempting to exit short position!\r")
                            hoh=c.close_short(SHORT_QUANTITY_START, SHORT_QUANTITY_END, 'BTC')
                            #market buy then repay
                            if hoh:
                                short_position=False
                                newShort=False
                                print("SHORT TRADE FINISHED!\r")
                    else:
                        print("Downtrend but still looking for optimal short position!\r") 


            if (upmidDistance>2 and middownDistance>2) or newShort: #61
                c.long_sell_hist(last_rsi_6, last_rsi_12, last_rsi_24)
                closedRev=float(close15)
                
                if (upTrend and last_rsi_6>75 and last_rsi_24>60):  
                    if long_position:
                        print("Overbought! Checking if profitable...\r")
                        
                        if profit > 1.03:
                            print("Attempting to exit short position!\r")

                            #sell logic binance
                            order_successful= c.order_sell(LONG_QUANTITY,TRADE_SYMBOL)
                            
                            if order_successful:
                                long_position=False
                                newLong=False
                                c.long_sell_conf(last_rsi_6, last_rsi_12, last_rsi_24)
                        else:
                            print("LIESSS!!!\r")
                        
                    else: 
                        print("It is overbought, but you're not in a position, so YEET!\r")

                if (not upTrend and last_rsi_6>61 and last_rsi_24>48) or (not upTrend and newShort):
                    if short_position:
                        print("Already in short position!\r")

                    else:
                        print("Currently in downtrend and getting potential OPEN SHORT POSITION\r")
                        SHORT_QUANTITY_START=STABLE_SHORT/close15
                        shortOpened=float(close15)
                        hoh=c.open_short(SHORT_QUANTITY_START, 'BTC')
                        if hoh:
                            print("YOU HAVE OPENED A SHORT TRADE\r")
                            short_position=True
                        else:
                            print("YOU HAVE NOT OPENED THE SHORT TRADE ERROR ERROR\r")

            print("Current 15-min RSI 6 is: {}".format(last_rsi_6))
            print("Current 15-min RSI 12 is: {}".format(last_rsi_12))
            print("Current 15-min RSI 24 is: {}".format(last_rsi_24))
            print("Value of UpTrend: {}".format(upTrend))
            print("Value of Long Position: {}".format(long_position)+ "  Long Quantity: {}".format(LONG_QUANTITY))
            print("Price at which position opened in Long: {}".format(opened)+"  Price Closed in Long: {}".format(closed) )
            print("Value of Short Position: {}".format(short_position)+ "  Short Quantity Start: {}".format(SHORT_QUANTITY_START)+" Short Quantity End: {}".format(SHORT_QUANTITY_END))
            print("Price at which position opened in Short: {}".format(shortOpened)+"  Price Closed in Short: {}".format(shortClosed) )
            print("New Short: {}".format(newShort)+"        New Long: {}".format(newLong))
            print("Instance Short: {}".format(instanceShort)+"      Instance Long: {}".format(instanceLong))
    
    except Exception as e:
        print("Exception occured finally: {}".format(e))



class threadr(threading.Thread):
    def __init__(self):
        super(threadr, self).__init__()

    def run(self):
        klez()
        # if profitRev>1.03 or last_rsi_24<43 or newLong:
        #     print("Attempting to enter long position!")
        #     LONG_QUANTITY=c.round_up(STABLE_LONG/close)
        #     order=c.order_buy(LONG_QUANTITY, TRADE_SYMBOL)

        #     if order:
        #         print("THE BUY ORDER IN C WORKS THOUGH!")
        #         order_n=c.order_sell(LONG_QUANTITY, TRADE_SYMBOL)
        #         if order_n:
        #             print("THE SELL ORDER IN C WORKS THOUGH AS WELL!")


thread1=threadr()
thread1.start()
