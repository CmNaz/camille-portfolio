
import c
import numpy as np
#viye()
#upTrend, instanceShort, instanceLong, newLong, newShort, close15, closesT15,
#either pass these through the method as dependencies or just use main import
#k.closesT15.append(float(close15))
#okay fuck it you really do have to change the variables from main


#
#if candle_closed: 
#u.closesT15=closesT15
#if hr candle_closed:
#u.upTrend=True


#this class as a thread is while True: call this class sleep(60)


class viye:
    def __init__(self):
        self.TRADE_SYMBOL=''
        self.CRYPT=''

        self.strupTrend=False
        self.strdownTrend=False

        self.long_position=False
        self.short_position=False

        self.opened=0
        self.closed=None
        self.shortClosed=None
        self.shortOpened=0

        self.upTrend=False
        self.profitShort=1
        self.profit=1

        self.closedRev=0
        self.openedRev=0

        #self.STABLE_SHORT=20 DONT NEED THIS ANYMO
        self.STABLE_LONG=11
        self.SHORT_QUANTITY_START=0
        self.SHORT_QUANTITY_END=0
        self.LONG_QUANTITY=0

        self.instanceShort=0
        self.instanceLong=0
        self.newShort=False
        self.newLong=False

        self.close15=0
        self.closeHR=0
        self.closes15=[]
        self.closesT15=[]
        self.closesHR=[]
        self.closesTHR=[]
        self.profitRev=0
        self.shortCont=False
        self.geste=False #after if geste: , put geste=False at the end


    def do(self):
    #if len(closes) > 24:
        self.close15=float(self.close15) #value of self.close15 is not actually a float or int, it is originally a dict so cast it
        np_closes=np.array(self.closesT15)
        # rsi6=talib.RSI(np_closes, 6)
        # rsi12=talib.RSI(np_closes, 12)
        # rsi24=talib.RSI(np_closes, 24)
        rsi6 = c.get_rsi(np_closes, 6 )
        rsi12 = c.get_rsi(np_closes, 12 )
        rsi24 = c.get_rsi(np_closes, 24 )
        print("All 15-min RSIs Calculated Thus Far:\r")
        print(rsi6)
        print(rsi12)
        print(rsi24)
        last_rsi_6=rsi6[-1]
        last_rsi_12=rsi12[-1]
        last_rsi_24=rsi24[-1]

        print("------EXECUTING MINUTE VIYE------")
        

        upmidDistance=last_rsi_6 - last_rsi_12
        middownDistance=last_rsi_12 - last_rsi_24


        if self.close15!=0:
            if self.short_position:
                self.shortClosed=self.close15
                self.profitShort=c.round_up(self.shortOpened/self.shortClosed)

            if self.long_position:
                self.closed=self.close15
                self.profit=c.round_up(self.closed/self.opened)

                if self.closedRev!=0:
                    self.openedRev=self.close15
                    self.profitRev=c.round_up(self.closedRev/self.openedRev)
            
            if self.shortClosed!=None:

                if self.close15/self.shortClosed<=0.985 and self.strdownTrend and not self.short_position and upmidDistance<-1.5 and middownDistance<-1.5:
                    #enter short
                    #sell logic binance
                    order_successful= c.order_sell(self.LONG_QUANTITY,self.TRADE_SYMBOL)
                    
                    if order_successful:
                        self.long_position=False
                        self.shortCont=True
                        
                        c.long_sell_conf(last_rsi_6, last_rsi_12, last_rsi_24)
                        
                    else:
                        print("YOU HAVE NOT OPENED THE SHORT TRADE ERROR ERROR\r")

            if self.closed!=None:

                if self.closed/self.close15<=0.99 and self.strupTrend and not self.long_position and upmidDistance>2 and middownDistance>2:
                    #enter long
                    print("Attempting to enter long position!\r")
                    c.long_buy_hist(last_rsi_6, last_rsi_12, last_rsi_24)
                    
                    self.LONG_QUANTITY=c.round_up(self.STABLE_LONG/self.close15)
                    order_successful= c.order_buy(self.LONG_QUANTITY, self.TRADE_SYMBOL)
                
                    if order_successful:
                        self.opened=self.close15
                        self.long_position=True
                        self.newLong=False
                        c.long_buy_conf(last_rsi_6, last_rsi_12, last_rsi_24)


            if (not self.upTrend and self.long_position) or (self.long_position and self.profit<0.972):
                #get quantity to sell btc amount for quick stop loss
                
                print("STOP LOSS IN LONG POSITION TRIGGERED! CHANGED TO DOWNTREND!\r")
                #sell logic binance
                order_successful= c.order_sell(self.LONG_QUANTITY,self.TRADE_SYMBOL)
                
                if order_successful:
                    self.long_position=False
                    self.newLong=False
                    
                    c.long_sell_conf(last_rsi_6, last_rsi_12, last_rsi_24)

                
                
            if (self.upTrend and self.short_position) or (self.short_position and self.profitShort<0.972):
                
                #give up short position accept defeat buy back with loss and calculate if your money is 1/3 of the asset make sure to research on prices
                print("STOP LOSS IN SHORT POSITION TRIGGERED! CHANGED TO UPTREND\r")
                self.LONG_QUANTITY=c.round_up(self.STABLE_LONG/self.close15)
                order_successful= c.order_buy(self.LONG_QUANTITY, self.TRADE_SYMBOL)
            
                if order_successful:
                    self.newShort=False
                    self.shortCont=False
                    self.short_position=False


            if (upmidDistance<-1.5 and middownDistance<-1.5 and last_rsi_24<45) or self.newLong:#this newLong is actually useless because of the conditions for profitrev and last rsi
                if self.upTrend and self.instanceLong!=0:
                    if self.long_position:
                        print("It is oversold but you have it already so YEET\r")

                    else:
                        
                        if (self.profitRev>1.03) or (last_rsi_24<43) or (self.newLong):
                            print("Attempting to enter long position!\r")
                            c.long_buy_hist(last_rsi_6, last_rsi_12, last_rsi_24)
                            
                            self.LONG_QUANTITY=c.round_up(self.STABLE_LONG/self.close15)
                            order_successful= c.order_buy(self.LONG_QUANTITY, self.TRADE_SYMBOL)
                        
                            if order_successful:
                                self.opened=self.close15
                                self.long_position=True
                                self.newLong=False
                                c.long_buy_conf(last_rsi_6, last_rsi_12, last_rsi_24)
                                

                elif not self.upTrend and self.instanceShort!=0: 
                    if self.short_position:
                        #if last_rsi_6>60
                        
                        if (self.profitShort > 1.022) or (last_rsi_6<15 and not self.shortCont):
                            
                            self.LONG_QUANTITY=c.round_up(self.STABLE_LONG/self.close15)
                            order_successful= c.order_buy(self.LONG_QUANTITY, self.TRADE_SYMBOL)
                        
                            if order_successful:
                                self.shortCont=False
                                self.short_position=False
                                print("SHORT TRADE FINISHED!\r")
                    else:
                        print("Downtrend but still looking for optimal short position!\r") 


            if (upmidDistance>2 and middownDistance>2) or self.newShort: #61
                c.long_sell_hist(last_rsi_6, last_rsi_12, last_rsi_24)
                self.closedRev=self.close15
                
                if (self.upTrend and last_rsi_6>75 and last_rsi_24>60 and self.instanceLong!=0):
                    if self.long_position:
                        print("Overbought! Checking if profitable...\r")
                        
                        
                        if self.profit > 1.03:
                            print("Attempting to exit long position!\r")

                            #sell logic binance
                            order_successful= c.order_sell(self.LONG_QUANTITY,self.TRADE_SYMBOL)
                            
                            if order_successful:
                                self.long_position=False
                                
                                c.long_sell_conf(last_rsi_6, last_rsi_12, last_rsi_24)
                        else:
                            print("LIESSS!!!\r")
                        
                    else: 
                        print("It is overbought, but you're not in a position, so YEET!\r")

                if (not self.upTrend and last_rsi_6>61 and last_rsi_24>48 and self.instanceShort!=0) or (not self.upTrend and self.newShort):
                    if self.short_position:
                        print("Already in short position!\r")

                    else:
                        print("Currently in downtrend and getting potential OPEN SHORT POSITION\r")
                        #sell logic binance
                        order_successful= c.order_sell(self.LONG_QUANTITY,self.TRADE_SYMBOL)
                        
                        if order_successful:
                            print("YOU HAVE OPENED A SHORT TRADE")
                            self.shortOpened=self.close15
                            self.short_position=True
                            self.newShort=False
                        else:
                            print("YOU HAVE NOT OPENED THE SHORT TRADE ERROR ERROR\r")

        print("Current 15-min RSI 6 is: {}".format(last_rsi_6))
        print("Current 15-min RSI 12 is: {}".format(last_rsi_12))
        print("Current 15-min RSI 24 is: {}".format(last_rsi_24))
        print("Value of UpTrend: {}".format(self.upTrend))
        print("Value of Long Position: {}".format(self.long_position)+ "  Long Quantity: {}".format(self.LONG_QUANTITY))
        print("Price at which position opened in Long: {}".format(self.opened)+"  Price Closed in Long: {}".format(self.closed) )
        print("Value of Short Position: {}".format(self.short_position)+ "  Short Quantity Start: {}".format(self.SHORT_QUANTITY_START)+" Short Quantity End: {}".format(self.SHORT_QUANTITY_END))
        print("Price at which position opened in Short: {}".format(self.shortOpened)+"  Price Closed in Short: {}".format(self.shortClosed) )
        print("New Short: {}".format(self.newShort)+"        New Long: {}".format(self.newLong))
        print("Instance Short: {}".format(self.instanceShort)+"      Instance Long: {}".format(self.instanceLong))

        self.geste=False

