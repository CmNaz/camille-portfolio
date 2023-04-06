import pandas as pd
import numpy as np
import c, config
from binance.client import Client
from binance.enums import *

client=Client(config.API_KEY, config.API_SECRET, tld='com')
array_high=[41,42,43,44,45,46,47,48,49,50,51,52,53,54,57,45,53,48,42,47,60,50,70]
array_low=[41,42,43,44,45,46,47,43,49,50,51,52,53,54,55,51,45,49,44,47,50,60,70] #1915
array_close=[41,42,43,40,45,46,47,48,49,50,51,52,53,54,55, 43, 55, 42, 40,47,70,60,50] #14
kay=[]
jay=[]
dee=[]

def kdj(array_high, array_low, array_close):
    kdjupTrend=False#
    kdjstrdownTrend=False
    kdjstrupTrend=False
    y=0
    z=0
    global kay, dee
    #kperiods are 14 array start from 0 index
    kperiods=13
    array_highest=[]
    try:
        for x in range(0,len(array_high)-kperiods):
            z=array_high[y]
            for j in range(0,kperiods):
                if(z<array_high[y+1]):
                    z=array_high[y+1]
                y=y+1
            # creating list highest of k periods
            array_highest.append(z)
            y=y-(kperiods-1)
    except Exception as e:
        print(e)
    print("Highest array size",len(array_highest))
    print(array_highest)
    y=0
    z=0
    array_lowest=[]
    for x in range(0,len(array_low)-kperiods):
        z=array_low[y]
        for j in range(0,kperiods):
            if(z>array_low[y+1]):
                z=array_low[y+1]
            y=y+1
        # creating list lowest of k periods
        array_lowest.append(z)
        y=y-(kperiods-1)
    print(len(array_lowest))
    print(array_lowest)

    #KDJ (K line, D line, J line)
    Kvalue=[]
    for x in range(kperiods,len(array_close)):
        k = ((array_close[x]-array_lowest[x-kperiods])*100/(array_highest[x-kperiods]-array_lowest[x-kperiods]))
        Kvalue.append(k)
    print(len(Kvalue))
    print(Kvalue)
    y=0
    # dperiods for calculate d values
    dperiods=3
    Dvalue=[None,None]
    mean=0
    for x in range(0,len(Kvalue)-dperiods+1):
        sum=0
        for j in range(0,dperiods):
            sum=Kvalue[y]+sum
            y=y+1
        mean=sum/dperiods
        # d values for %d line
        Dvalue.append(mean)
        y=y-(dperiods-1)
    print(len(Dvalue))
    print(Dvalue)
    print(mean)
    Jvalue=[None,None]
    for x in range(0,len(Dvalue)-dperiods+1):
        j=(Dvalue[x+2]*3)-(Kvalue[x+2]*2)
        # j values for %j line
        Jvalue.append(j)
    print(len(Jvalue))
    print(Jvalue)
    print(j)

    
    d=mean
    jay.append(j)
    kay.append(k)
    dee.append(d)
    upmid=j-k
    middown=k-d

    if upmid>15 and middown>15:
        kdjupTrend=True
        kdjstrupTrend=True
    if upmid<-15 and middown<-15:
        kdjupTrend=False
        kdjstrdownTrend=True
    else:
        kdjstrdownTrend=False
        kdjstrupTrend=False
    print(kdjstrdownTrend)
    print(kdjstrupTrend)
    print(kdjupTrend)

kdj(array_high,array_low,array_close)





for kline in client.get_historical_klines_generator('BTCUSDT', Client.KLINE_INTERVAL_1HOUR, "3 months ago"):
    c.closesTHR_1.append(float(kline[4]))
    c.highsHR.append(float(kline[2]))
    c.lowsHR.append(float(kline[3]))
    c.closesHR.pop()
    c.highsHR.pop()
    c.lowsHR.pop()
    

#np.array(array_close)
array_high=np.array(c.highsHR)
array_low=np.array(c.lowsHR)
array_low=pd.Series(array_low)
array_high=pd.Series(c.highsHR)
#pd.Series(array_close)
[float(i) for i in c.closesTHR_1]

array_close=c.closesTHR



def KDJ(H, L, C):
    kdjupTrend=False#
    kdjstrdownTrend=False
    kdjstrupTrend=False
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

    
    jay.append(j)
    kay.append(k)
    dee.append(d)
    upmid=j-k
    middown=k-d

    if upmid>15 and middown>15:
        kdjupTrend=True
        kdjstrupTrend=True
    if upmid<-15 and middown<-15:
        kdjupTrend=False
        kdjstrdownTrend=True
    else:
        kdjstrdownTrend=False
        kdjstrupTrend=False
    
    print(kdjstrdownTrend)
    print(kdjstrupTrend)
    print(kdjupTrend)


print(KDJ(array_high, array_low, array_close))