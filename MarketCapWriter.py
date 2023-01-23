import pandas as pd
import numpy as np
import yfinance as yf

Data = pd.read_csv('result.csv')
marketCap = 0
try:
    marketCap = yf.Ticker(Data.iloc[1,1] + ".NS").info["marketCap"]
except:
    pass
for i in range(4383):
    if Data.iloc[i+1,1] == Data.iloc[i,1]:
        Data.iloc[i,7] == marketCap
        Data.iloc[i+1,7] == marketCap
    else:
        try:
            marketCap = yf.Ticker(Data.iloc[i+1,1] + ".NS").info["marketCap"]
        except:
            pass
        Data.iloc[i+1,7] == marketCap


Data.to_csv("MarkCapResult.csv")    