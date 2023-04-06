
import c
import numpy as np
import pandas as pd
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

        self.thread=0

        self.kdjstrupTrend=False
        self.kdjstrdownTrend=False

        self.strupTrend=False
        self.strdownTrend=False

        self.long_position=False
        self.short_position=False

        self.opened=0
        self.closed=None
        self.shortClosed=None
        self.shortOpened=0

        self.upTrend=False
        self.TrUp=False
        self.profitShort=1
        self.profit=1

        self.closedRev=0
        self.openedRev=0

        self.STABLE_SHORT=20*3
        self.STABLE_LONG=20
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

        self.statement15=""


    def do(self):
        #[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]#
        
        self.long_position=c.long_position
        self.short_position=c.short_position

        self.opened=c.opened
        self.closed=c.closed
        self.shortClosed=c.shortClosed
        self.shortOpened=c.shortOpened

        self.profitShort=c.profitShort
        self.profit=c.profit

        self.closedRev=c.closedRev
        self.openedRev=c.openedRev

       
        self.SHORT_QUANTITY_START=c.SHORT_QUANTITY_START
        self.SHORT_QUANTITY_END=c.SHORT_QUANTITY_END
        self.LONG_QUANTITY=c.LONG_QUANTITY

        self.instanceShort=c.instanceShort
        self.instanceLong=c.instanceLong
        self.newShort=c.newShort
        self.newLong=c.newLong

        self.profitRev=c.profitRev
        self.shortCont=c.shortCont
        #[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]#

        # if c.usual:
        c.KEPP(self.closesTHR)
        diffLong=((c.total-1)/2)+c.total
        diffShort=((c.total-1)*2)+1
        longProzent=c.total #1.022
        shortProzent=c.total #1.022
        
            
        longHalt=round(c.total/diffLong,4)     #0.99
        shortHalt=round(c.total/diffShort,4)                          #0.98
        longJatkaa=round(c.total/diffLong,4)    #0.99
        shortJatkaa=round((c.total/diffShort)+0.005,4)                       #0.985
        if shortJatkaa>1:
            shortJatkaa=0.9985
        c.longHalt=longHalt
        c.shortHalt=shortHalt
        c.longJatkaa=longJatkaa
        c.shortJatkaa=shortJatkaa

        # else:
        #     longProzent=1.006
        #     shortProzent=1.006
        #     longHalt=0.994
        #     shortHalt=0.994
        #     longJatkaa=0.994
        #     shortJatkaa=0.994
        
        #if len(closes) > 24:
        self.close15=float(self.close15) #value of self.close15 is not actually a float or int, it is originally a dict so cast it
        np_closes=np.array(self.closesT15)
        series=pd.Series(np_closes)
        # rsi6=talib.RSI(np_closes, 6)
        # rsi12=talib.RSI(np_closes, 12)
        # rsi24=talib.RSI(np_closes, 24)
        rsi6 = c.computeRSI(series, 6 )
        rsi12 = c.computeRSI(series, 12 )
        rsi24 = c.computeRSI(series, 24 )
        print("All {}".format(self.thread)+"-min RSIs Calculated Thus Far:\r")
        print(rsi6[-5:])
        print(rsi12[-5:])
        print(rsi24[-5:])
        last_rsi_6=round(float(rsi6[-1:]), 2)
        last_rsi_12=round(float(rsi12[-1:]), 2)
        last_rsi_24=round(float(rsi24[-1:]), 2)


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

                if self.close15/self.shortClosed<=shortJatkaa and self.strdownTrend and not self.short_position and upmidDistance<-1.5 and middownDistance<-1.5:
                    #enter short
                    self.SHORT_QUANTITY_START=c.round_up(self.STABLE_SHORT/self.close15)
                    self.shortOpened=self.close15
                    hoh=c.open_short(self.STABLE_SHORT,self.SHORT_QUANTITY_START, self.TRADE_SYMBOL, self.CRYPT, self.close15)
                    self.newShort=False
                    if hoh:
                        print("YOU HAVE OPENED A SHORT TRADE\r")
                        self.short_position=True
                        self.shortCont=True
                        self.profitShort=1
                        
                    else:
                        print("YOU HAVE NOT OPENED THE SHORT TRADE ERROR ERROR\r")

            if self.closed!=None:

                if self.closed/self.close15<=longJatkaa and self.strupTrend and not self.long_position and upmidDistance>2 and middownDistance>2:
                    #enter long
                    print("Attempting to enter long position!\r")
                    c.long_buy_hist(last_rsi_6, last_rsi_12, last_rsi_24)
                    
                    self.LONG_QUANTITY=c.round_up(self.STABLE_LONG/self.close15)
                    order_successful= c.order_buy(self.STABLE_LONG, self.LONG_QUANTITY, self.TRADE_SYMBOL)
                
                    if order_successful:
                        self.opened=self.close15
                        self.long_position=True
                        self.newLong=False
                        self.profit=1
                        c.long_buy_conf(last_rsi_6, last_rsi_12, last_rsi_24)


            if (not self.upTrend and self.long_position) or (self.long_position and self.profit<longHalt) or (c.change and self.long_position):
                #get quantity to sell btc amount for quick stop loss
                
                print("STOP LOSS IN LONG POSITION TRIGGERED! CHANGED TO DOWNTREND!\r")
                self.TrUp=False
                hoh=c.stop_loss(self.TrUp, self.SHORT_QUANTITY_START, self.SHORT_QUANTITY_END, self.LONG_QUANTITY, self.TRADE_SYMBOL, self.CRYPT)
                if hoh:
                    c.change=False
                    self.newLong=False
                    self.long_position=False
                    self.strupTrend=False
                    

                
                
            if (self.upTrend and self.short_position) or (self.short_position and self.profitShort<shortHalt) or (c.change and self.short_position):
                
                #give up short position accept defeat buy back with loss and calculate if your money is 1/3 of the asset make sure to research on prices
                print("STOP LOSS IN SHORT POSITION TRIGGERED! CHANGED TO UPTREND\r")
                self.SHORT_QUANTITY_END=c.round_up(self.STABLE_SHORT/self.close15)
                self.TrUp=True
                hoh=c.stop_loss(self.TrUp, self.SHORT_QUANTITY_START, self.SHORT_QUANTITY_END, self.LONG_QUANTITY, self.TRADE_SYMBOL, self.CRYPT)
                if hoh:
                    c.change=False
                    self.newShort=False
                    self.short_position=False
                    self.shortCont=False
                    self.strdownTrend=False


            if (upmidDistance<-1.5 and middownDistance<-1.5 and last_rsi_24<45) or self.newLong:#this newLong is actually useless because of the conditions for profitrev and last rsi
                if self.upTrend and self.instanceLong!=0:
                    if self.long_position:
                        print("It is oversold but you have it already so YEET\r")

                    else:
                        
                        if (self.profitRev>1.03) or (last_rsi_24<43) or (self.newLong):
                            print("Attempting to enter long position!\r")
                            c.long_buy_hist(last_rsi_6, last_rsi_12, last_rsi_24)
                            
                            self.LONG_QUANTITY=c.round_up(self.STABLE_LONG/self.close15)
                            order_successful= c.order_buy(self.STABLE_LONG,self.LONG_QUANTITY, self.TRADE_SYMBOL)
                        
                            if order_successful:
                                self.opened=self.close15
                                self.long_position=True
                                self.newLong=False
                                self.profit=1
                                c.long_buy_conf(last_rsi_6, last_rsi_12, last_rsi_24)
                                

                elif not self.upTrend and self.instanceShort!=0: 
                    if self.short_position:
                        #if last_rsi_6>60
                        
                        if (self.profitShort > shortProzent) or (last_rsi_6<15 and not self.shortCont): #and self.profitShort>1.01
                            self.SHORT_QUANTITY_END=c.round_up(self.STABLE_SHORT/self.close15)
                            print("Attempting to exit short position!\r")
                            hoh=c.close_short(self.SHORT_QUANTITY_START, self.SHORT_QUANTITY_END, self.TRADE_SYMBOL, self.CRYPT)
                            #market buy then repay
                            if hoh:
                                self.short_position=False
                                self.shortCont=False
                                
                                print("SHORT TRADE FINISHED!\r")
                    else:
                        print("Downtrend but still looking for optimal short position!\r") 


            if (upmidDistance>2 and middownDistance>2) or self.newShort: #61
                c.long_sell_hist(last_rsi_6, last_rsi_12, last_rsi_24)
                self.closedRev=self.close15
                
                if (self.upTrend and last_rsi_6>75 and last_rsi_24>60 and self.instanceLong!=0):
                    if self.long_position:
                        print("Overbought! Checking if profitable...\r")
                        
                        
                        if self.profit > longProzent:

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
                        self.SHORT_QUANTITY_START=c.round_up(self.STABLE_SHORT/self.close15)
                        self.shortOpened=self.close15
                        hoh=c.open_short(self.STABLE_SHORT,self.SHORT_QUANTITY_START, self.TRADE_SYMBOL, self.CRYPT, self.close15)
                        self.newShort=False
                        if hoh:
                            print("YOU HAVE OPENED A SHORT TRADE\r")
                            self.short_position=True
                            self.profitShort=1
                            
                        else:
                            print("YOU HAVE NOT OPENED THE SHORT TRADE ERROR ERROR\r")


        c.long_position=self.long_position
        c.short_position=self.short_position

        c.opened=self.opened
        c.closed=self.closed
        c.shortClosed=self.shortClosed
        c.shortOpened=self.shortOpened

        c.profitShort=self.profitShort
        c.profit=self.profit

        c.closedRev=self.closedRev
        c.openedRev=self.openedRev

       
        c.SHORT_QUANTITY_START=self.SHORT_QUANTITY_START
        c.SHORT_QUANTITY_END=self.SHORT_QUANTITY_END
        c.LONG_QUANTITY=self.LONG_QUANTITY

        c.instanceShort=self.instanceShort
        c.instanceLong=self.instanceLong
        c.newShort=self.newShort
        c.newLong=self.newLong

        
        c.profitRev=self.profitRev
        c.shortCont=self.shortCont

        self.statement15=("==================================================================================="
                +"\n\nAll {}".format(self.thread)+"-min RSIs Calculated Thus Far: \n {}".format(self.thread)+"-MIN RSI 6: {}".format(rsi6[-5:])+"\n {}".format(self.thread)+"-MIN RSI 12: {}".format(rsi12[-5:])+"\n {}".format(self.thread)+"-MIN RSI 24: {}".format(rsi24[-5:])
        +"\n\n Current {}".format(self.thread)+"-min RSI 6 is: {}".format(last_rsi_6)+"\nCurrent {}".format(self.thread)+"-min RSI 12 is: {}".format(last_rsi_12)+"\nCurrent {}".format(self.thread)+"-min RSI 24 is: {}".format(last_rsi_24)+"\nValue of UpTrend: {}".format(self.upTrend)
        +"\nValue of Long Position: {}".format(self.long_position)+ "  Long Quantity: {}".format(self.LONG_QUANTITY)+"\nPrice at which position opened in Long: {}".format(self.opened)+"  Price Closed in Long: {}".format(self.closed)
        +"\nValue of Short Position: {}".format(self.short_position)+ "  Short Quantity Start: {}".format(self.SHORT_QUANTITY_START)+" Short Quantity End: {}".format(self.SHORT_QUANTITY_END)
        +"\nPrice at which position opened in Short: {}".format(self.shortOpened)+"  Price Closed in Short: {}".format(self.shortClosed)+"\nNew Short: {}".format(self.newShort)+"        New Long: {}".format(self.newLong)
        +"\nInstance Short: {}".format(self.instanceShort)+"      Instance Long: {}".format(self.instanceLong)
        )
        print("Current {}".format(self.thread)+"-min RSI 6 is: {}".format(last_rsi_6))
        print("Current {}".format(self.thread)+"-min RSI 12 is: {}".format(last_rsi_12))
        print("Current {}".format(self.thread)+"-min RSI 24 is: {}".format(last_rsi_24))
        print("Value of UpTrend: {}".format(self.upTrend))
        print("Value of Long Position: {}".format(self.long_position)+ "  Long Quantity: {}".format(self.LONG_QUANTITY))
        print("Price at which position opened in Long: {}".format(self.opened)+"  Price Closed in Long: {}".format(self.closed) )
        print("Value of Short Position: {}".format(self.short_position)+ "  Short Quantity Start: {}".format(self.SHORT_QUANTITY_START)+" Short Quantity End: {}".format(self.SHORT_QUANTITY_END))
        print("Price at which position opened in Short: {}".format(self.shortOpened)+"  Price Closed in Short: {}".format(self.shortClosed) )
        print("New Short: {}".format(self.newShort)+"        New Long: {}".format(self.newLong))
        print("Instance Short: {}".format(self.instanceShort)+"      Instance Long: {}".format(self.instanceLong))

        
        self.geste=False

