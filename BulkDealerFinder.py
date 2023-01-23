import pandas as pd
import numpy as np
import yfinance as yf

Data = pd.read_csv('StockData/BulkDeals.csv')

dropList = []

for i in range(12275):
    companyName = Data.iloc[i,1]
    companyNameDown = Data.iloc[i+1,1]
    clientName = Data.iloc[i,3]
    clientNameDown = Data.iloc[i+1,3]
    currentDate = Data.iloc[i,0]
    currentDateDown = Data.iloc[i+1,0]
    orderType = Data.iloc[i,4]
    orderTypeDown = Data.iloc[i+1,4]
    if clientName == clientNameDown:
        if currentDate == currentDateDown and companyName == companyNameDown and orderType != orderTypeDown:
            # Data = Data.drop(i)
            # Data = Data.drop(i+1)
            dropList.append(i)
            dropList.append(i+1)

print(dropList)
for i in dropList:
    Data.drop(i , inplace=True)
    
# for i in range(4386):
#     try:
#         Data.iloc[i,7] = yf.Ticker(Data.iloc[i,1] + ".NS").info["marketCap"]
#     except:
#         pass
Data.to_csv("result.csv" , index=False)

# print(Data)