#there used to be talib here
import config, math
from binance.client import Client
from binance.enums import *
import numba as nb
import numpy as np

from numpy import diff

# ___library_import_statements___
import pandas as pd


client=Client(config.API_KEY, config.API_SECRET, tld='com')

total=0
pasTrades=[]
trackTest=[]

HR_end=False
MIN15_end=False
MIN5_end=False

#\\\\\\\///////#
strupTrend=False
strdownTrend=False
kdjstrupTrend=False
kdjstrdownTrend=False
kdjupTrend=False

kay=[]
dee=[]
jay=[]
kay_15=[]
dee_15=[]
jay_15=[]
kay_5=[]
dee_5=[]
jay_5=[]

long_position=False
short_position=False

opened=0
closed=None
shortClosed=None
shortOpened=0

upTrend=False
TrUp=False
profitShort=1
profit=1

closedRev=0
openedRev=0

SHORT_QUANTITY_START=0
SHORT_QUANTITY_END=0
LONG_QUANTITY=0

instanceShort=0
instanceLong=0
newShort=False
newLong=False

close15=0
closeHR=0

profitRev=0
shortCont=False
start=False
#///////\\\\\\\#

ex=['BTCUSDT'] #,'ADAUSDT'
crypt=['BTC']
pay='USDT'
ctr=0
xctr=0
zctr=0
viy=[]
xviy=[]
yviy=[]

lowsHR=[]
highsHR=[]
closesTHR_1=[]
rsi6_1=0
rsi12_1=0
rsi24_1=0

lowsHR_2=[]
highsHR_2=[]
closesTHR_2=[]
rsi6_2=0
rsi12_2=0
rsi24_2=0

lows15_5=[]
highs15_5=[]
closesT15_3=[]
rsi6_3=0
rsi12_3=0
rsi24_3=0

strl=""
strl2=""
strl3=""
strl4=""

threadMin=[]
threadHr=[]
thread1MIN=[]
thread5MIN=[]
threadv=[]

norm=True
stochsign=False
usual=True

restart=False
recnt=0

status1=False
status2=False
status3=False
status4=False

change=False

longHalt=0
shortHalt=0
longJatkaa=0
shortJatkaa=0

errmsg=None
def stoch(self, close):
    #loop that checks 24 hours/candles for stochrsi change, if more than 5intersects, then xconditions
    
    x=24
    #9a-7am 22 hours
    global xctr, zctr, norm, stochsign, change, usual, start
    zctr=0
    close1=[]
    while x>=0:
        if x==0:
            close1=close
        else:
            close1=close[:-x]
        series=pd.Series(close1)
        rsi=computeRSI(series, 14)
        fastk, fastd = stochastic(rsi, 14, 3)#, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0

        fastk = [round(x,2) for x in fastk]
        fastd = [round(y,2) for y in fastd]

        print("stochrsi_K: {}".format(fastk[-1:]))
        print("stochrsi_D: {}".format(fastd[-1:]))
        
        fastk=fastk[-1:]
        fastd=fastd[-1:]
        if x==24 and fastk>fastd or not norm and stochsign:
            norm=True
            stochsign=False

        elif x==24 and fastk<fastd or norm and stochsign:
            norm=False
            stochsign=False
        
        if norm and fastk<fastd:
            stochsign=True
            zctr+=1
        if not norm and fastk>fastd:
            stochsign=True
            zctr+=1
        x-=1
    print("ZCTR:")
    print(zctr)
    #NEVERMIND IT'S BACK TO NORMAL
    #YOU SWTICHED TRUE AND FALSE
    if start:
        if zctr>6: #original value was 5
            usual=False
        elif zctr<=6:
            usual=True
        start=False
    
    def stop():
        change=True
        self.u.instanceShort=0
        self.u.instanceLong=0


    if usual:
        if zctr>6:
            if self.u.long_position or self.u.short_position:
                stop()
            usual=False
    elif not usual and xctr>6 and xctr<10:
        if zctr<7:
            if self.u.long_position or self.u.short_position:
                stop()
            usual=True
        elif zctr>9:
            if self.u.long_position or self.u.short_position:
                stop()
            
    elif not usual and xctr > 9:
        if zctr>6 and zctr<10:
            if self.u.long_position or self.u.short_position:
                stop()
        elif zctr<7 :
            if self.u.long_position or self.u.short_position:
                stop()
            usual=True
    xctr=zctr
    
    print("Value of usual: ")
    print(usual)

#====================================================================
def KDJ(self,H, L, C): #LOL NOTHING WRONG WITH SELF JUST GOTTA CHECK FOR IF ELSE IN USUAL
    if usual:
        self.u.kdjstrupTrend=False
        self.u.kdjstrdownTrend=False
    else:
        self.u2.kdjstrupTrend=False
        self.u2.kdjstrdownTrend=False
    
    #L5 = pd.rolling_min(L, 9)
    L5 = L.rolling(9).min()
    #H5 = pd.rolling_max(H, 9)
    H5 = H.rolling(9).max()

    RSV = 100 * ((C - L5) / (H5 - L5)).values

    k0 = 50
    k_out = []
    for j in range(len(RSV)):
        if RSV[j] == RSV[j]: # check for nan
            k0 = 1/3 * RSV[j] + 2/3 * k0
            k_out.append(k0)
        else:
            k_out.append(np.nan)
    k_out=[float(i) for i in k_out]
    k_out=np.asarray(k_out)
    k=float(k_out[-1:])
    k=round(k,2)
    print(type(k))
    print(k_out[-5:])
    
    d0 = 50
    d_out = []
    for j in range(len(RSV)):
        if k_out[j] == k_out[j]:
            d0 =1/3 * k_out[j] + 2/3 * d0
            d_out.append(d0)
        else:
            d_out.append(np.nan)
    d_out=[float(i) for i in d_out]
    d_out=np.asarray(d_out)
    d=float(d_out[-1:])
    d=round(d,2)
    print(type(d))
    print(d_out[-5:])

    J = (3 * np.array(k_out)) - (2 * np.array(d_out))
    j=float(J[-1:])
    j=round(j,2)
    print(type(j))
    print(J[-5:])

    global kdjstrdownTrend, kdjupTrend, kdjstrupTrend, jay,jay_15,jay_5,kay,kay_15,kay_5,dee,dee_15,dee_5,errmsg
    try:
        if not usual:
            if self.u.thread==15:
                jay_15.append(j)
                kay_15.append(k)
                dee_15.append(d)
            
            elif self.u.thread==5:
                jay_5.append(j)
                kay_5.append(k)
                dee_5.append(d)

        else:
            jay.append(j)
            kay.append(k)
            dee.append(d)

        upmid=j-k
        middown=k-d

        if upmid>15 and middown>15:
            kdjupTrend=True
            if usual:
                self.u.kdjstrupTrend=True
            else:
                self.u2.kdjstrupTrend=True
        elif upmid<-15 and middown<-15:
            kdjupTrend=False
            if usual:
                self.u.kdjstrdownTrend=True
            else:
                self.u2.kdjstrdownTrend=True
        else:
            if usual:
                self.u.kdjstrupTrend=False
                self.u.kdjstrdownTrend=False
            else:
                self.u2.kdjstrdownTrend=False
                self.u2.kdjstrupTrend=False
        if usual:
            kdjstrdownTrend=self.u.kdjstrdownTrend
            kdjstrupTrend=self.u.kdjstrupTrend
        else:
            kdjstrdownTrend=self.u2.kdjstrdownTrend
            kdjstrupTrend=self.u2.kdjstrupTrend
        print(kdjstrdownTrend)
        print(kdjstrupTrend)
        print(kdjupTrend)
    
    except Exception as e:
        print("an exception occured - {}".format(e))
        errmsg=e


##################
def KEPP(close):
                
    d=24 #distance
    s=1
    percArr=[]

    while s<25:
        v1=close[0-s]
        v2=close[0-(s+d)]


        if v1>v2:
            perc=round(v1/v2,4)
            percArr.append(perc)
            
        else:
            perc=round(v2/v1,4)
            percArr.append(perc)

        s+=1

    global total
    total=0
    for i in percArr:
        total+=i

    total=float(round(total/24,4))
##################

def computeRSI (data, time_window):
    diff = data.diff(1).dropna()        # diff in one field(one day)

    #this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff
    
    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[ diff>0 ]
    
    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[ diff < 0 ]
    
    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=time_window-1 so we get decay alpha=1/time_window
    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi

def stochastic(data, window, k_window, d_window=3): #k_windows is 3 for stoch
    
    # input to function is one column from df
    # containing closing price or whatever value we want to extract K and D from
    
    min_val  = data.rolling(window=window, center=False).min()
    max_val = data.rolling(window=window, center=False).max()
    
    stoch = ( (data - min_val) / (max_val - min_val) ) * 100
    
    K = stoch.rolling(window=k_window, center=False).mean() 
    #K = stoch
    
    D = K.rolling(window=d_window, center=False).mean() 


    return K, D

@nb.jit(fastmath=True, nopython=True)   
def calc_rsi( array, deltas, avg_gain, avg_loss, n ):

    # Use Wilder smoothing method
    up   = lambda x:  x if x > 0 else 0
    down = lambda x: -x if x < 0 else 0
    i = n+1
    for d in deltas[n+1:]:
        avg_gain = ((avg_gain * (n-1)) + up(d)) / n
        avg_loss = ((avg_loss * (n-1)) + down(d)) / n
        if avg_loss != 0:
            rs = avg_gain / avg_loss
            array[i] = 100 - (100 / (1 + rs))
        else:
            array[i] = 100
        i += 1

    return array

def get_rsi( array, n = 14 ):   

    deltas = np.append([0],np.diff(array))

    avg_gain =  np.sum(deltas[1:n+1].clip(min=0)) / n
    avg_loss = -np.sum(deltas[1:n+1].clip(max=0)) / n

    array = np.empty(deltas.shape[0])
    array.fill(np.nan)

    array = calc_rsi( array, deltas, avg_gain, avg_loss, n )
    return array

#rsi = get_rsi( array or series, 14 )

def round_up(n, decimals=5): #ATTENTION BTCUSDT WENT FROM LOT SIZE 6 TO 5 IN DECIMALS, THIS WAS PROVEN THROUGH PREVIOUS DATA AND WE MAY NEED TO FIND A SOLID ALGO TO CALCULATE DIFFERENT COIN PAIRINGS
    multiplier = 10 ** decimals
    return round(n * multiplier) / multiplier

def order_buy(cnstprice, quantity, symbol):
    try:
        blance = client.get_asset_balance(asset=pay)
        balnce = blance["free"]
        balnce = float(balnce)

        if balnce > cnstprice:
            print("sending order\r")
            order=client.order_market_buy(symbol=symbol, quantity=quantity)
            print(order)
        else:
            print("LOW BALANCE! INITIATED FEE AVOIDANCE MANUEVER!")
            return False


        
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True 

def order_sell(quantity, symbol):
    try:
        print("sending order\r")
        order=client.order_market_sell(symbol=symbol, quantity=quantity)
        print(order)
        
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True 

def long_buy_hist(j6,j12,j24):
    print("Oversold! Buy! Buy! Buy!\r")
    entranceInfo6="Potential LONG buy at RSI 6: {}".format(j6)
    entranceInfo12="RSI 12: {}".format(j12)
    entranceInfo24="RSI 24: {}".format(j24)
    trackTest.append(entranceInfo6+" "+entranceInfo12+" "+entranceInfo24)

def long_buy_conf(a6,a12,a24):
    print("You have successfully engaged in a LONG position!\r")
    entranceInfo6="Bought at RSI 6: {}".format(a6)
    entranceInfo12="RSI 12: {}".format(a12)
    entranceInfo24="RSI 24: {}".format(a24)
    pasTrades.append(entranceInfo6+" "+entranceInfo12+" "+entranceInfo24)

def long_sell_hist(k6, k12, k24):
    entranceInfo6="Potential LONG sell at RSI 6: {}".format(k6)
    entranceInfo12="RSI 12: {}".format(k12)
    entranceInfo24="RSI 24: {}".format(k24)
    trackTest.append(entranceInfo6+" "+entranceInfo12+" "+entranceInfo24)

def long_sell_conf(b6, b12, b24):
    print("You have exited your previous LONG position! Searching for a new one...\r")
    entranceInfo6="Sold at RSI 6: {}".format(b6)
    entranceInfo12="RSI 12: {}".format(b12)
    entranceInfo24="RSI 24: {}".format(b24)
    pasTrades.append(entranceInfo6+" "+entranceInfo12+" "+entranceInfo24)
    
def open_short(cnstprice,quantity, symbol, asset, close):
    blance = client.get_margin_account()
    blancet = blance["userAssets"]
    try:
        for i in blancet:
            if i["asset"]==asset:
                balnce=i["free"]
                print(balnce)
        balnce = float(balnce)
    except Exception as e:
        print(e)
    if balnce*close > cnstprice/3:
        non=borrow_margin(quantity, asset)
        if non:
            print("BORROWED BITCOIN SUCCESSFULLY\r")
            print("CONFIRMING SELL...\r")
            nan=margin_sell(quantity, symbol)
            if nan:
                print("SOLD BITCOIN SUCCESS! WAITING FOR BUY BACK OPPORTUNITIES...\r")
                deebts = client.get_max_margin_loan(asset='BNB')
                repay_margin(deebts["amount"], 'BNB')
                return True
            
            else:
                print("JOKE'S ON YOU SELL FAILED\r")
                return False
        
        else:
            print("LOL CAN'T EVEN START THE SHORT POSITION PATHETIC\r")
            return False
    else:
        print("LOW BALANCE! INITIATED FEE AVOIDANCE MANUEVER!")
        return False

def close_short(startquantity, endquantity, symbol, asset):
    non=margin_buy(endquantity, symbol)
    if non:
        print("BUY BACK BITCOIN SUCCESS! WAITING FOR BITCOIN REPAYMENT...\r")
        nan=repay_margin(startquantity, asset)
        if nan:
            print("YOU FRIKKIN DID IT MATE! CHEERS!\r")
            deebts = client.get_max_margin_loan(asset='BNB')
            repay_margin(deebts["amount"], 'BNB')
            return True
        else:
            print("YOU CAN'T ESCAPE! MUST REPAY MANUALLY LOL\r")
            return False
    else:
        print("FAILED TO BUY BACK BITCOIN HUHU\r")
        return False

def margin_sell(quantity, symbol):
    try:
        print("sending order\r")
        order = client.create_margin_order(symbol=symbol,side=SIDE_SELL,type=ORDER_TYPE_MARKET,quantity=quantity)
        print(order)
        
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True 

def margin_buy(quantity, symbol):
    try:
        print("sending order\r")
        order = client.create_margin_order(symbol=symbol,side=SIDE_BUY,type=ORDER_TYPE_MARKET,quantity=quantity)#,isIsolated='TRUE'
        print(order)
        
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True 
    

def borrow_margin(quantity,asset):
    try:
        print("borrowing bitcoin...\r")
        order=client.create_margin_loan(asset=asset, amount=quantity)
        print(order)
        
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True 

def repay_margin(quantity,asset):
    try:
        print("sending order\r")
        order=client.repay_margin_loan(asset=asset, amount=quantity)
        print(order)
        
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True 

def stop_loss(trendUp, startquant, endquant, longquant, symbol, crypt):
    if trendUp:
        print("Trend has turned up while in SHORT position! Initiating stop loss BUY BACK AND REPAY! \r")
        heh=close_short(startquant, endquant, symbol, crypt)
        if heh:
            return True

    else: 
        print("Trend has turned down while in LONG position! Initiating stop loss SELL!\r")
        print("\r")
        heh=order_sell(longquant, symbol)
        if heh:
            return True

#1361+322=1683 lines of code
#1190+150+258=1598 more efficient with more functionalities