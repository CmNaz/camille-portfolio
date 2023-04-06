

lol={
    "borrowEnabled": "true",
    "marginLevel": "11.64405625",
    "totalAssetOfBtc": "6.82728457",
    "totalLiabilityOfBtc": "0.58633215",
    "totalNetAssetOfBtc": "6.24095242",
    "tradeEnabled": "true",
    "transferEnabled": "true",
    "userAssets": [
        {
            "asset": "BTC",
            "borrowed": "0.00000000",
            "free": "0.00499500",
            "interest": "0.00000000",
            "locked": "0.00000000",
            "netAsset": "0.00499500"
        },
        {
            "asset": "BNB",
            "borrowed": "201.66666672",
            "free": "2346.50000000",
            "interest": "0.00000000",
            "locked": "0.00000000",
            "netAsset": "2144.83333328"
        },
        {
            "asset": "ETH",
            "borrowed": "0.00000000",
            "free": "0.00000000",
            "interest": "0.00000000",
            "locked": "0.00000000",
            "netAsset": "0.00000000"
        },
        {
            "asset": "USDT",
            "borrowed": "0.00000000",
            "free": "0.00000000",
            "interest": "0.00000000",
            "locked": "0.00000000",
            "netAsset": "0.00000000"
        }
    ]
}

print(lol)
print(lol["userAssets"])

eh=lol["userAssets"]


for i in eh:
    if i["asset"]=="BTC":
        print(i["free"])

# import pandas as pd
# import c
# close=
# series=pd.Series(close)
# rsi=c.computeRSI(series, 9)
# fastk, fastd = c.stochastic(rsi, 9)#, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0

# fastk = [round(x,2) for x in fastk]
# fastd = [round(y,2) for y in fastd]

# print("KDJ_K: {}".format(fastk[-1:]))
# print("KDJ_D: {}".format(fastd[-1:]))

# k=fastk[-1:]
# d=fastd[-1:]
# print(type(k))