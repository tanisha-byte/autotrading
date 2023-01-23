# from nsepy import get_history
import pandas as pd
from datetime import date
import numpy as np
import yfinance as yf
from matplotlib import pyplot as plt
import os
from string import digits

#Interval required 5 minutes
# data = yf.download(tickers='Nifty50.NS', period='1d', interval='1m',index=True)
# print(data)
# dateyo = pd.date_range(start='2022-03-25 9:15:00+5:30',end='2022-03-25 3:30:00+5:30',freq='1min')
# print(data.iloc[0:70])
# print(dateyo)
# print(data.loc[["Datetime"],:])
# print(data.iloc[:,0])
# data.to_csv('lk.csv')f        
# plt.plot(data.index,data.Open)
# plt.show()

def ReadLastDate(filename):
    count=len(open(filename).readlines())
    df =pd.read_csv(filename, skiprows=range(2,count-1), header=0)
    return df
def RemoveDigits(string):
    remove_digits = str.maketrans('', '', digits)
    res = string.translate(remove_digits)
    return res

CompanyNames = pd.read_csv('StockData/CompanyNames.csv')
TotalCompany = 0
CompanyDataList = os.listdir(os.getcwd()+"/StockData") 
# CompanyDataListNoDates = []

# for i in CompanyDataList:
#     x = RemoveDigits(i)
#     x.replace('-','')
#     CompanyDataListNoDates.append(x)

for Company in CompanyNames.iloc[:,0]:
    if Company in CompanyDataListNoDates:
        # data = pd.read_csv("StockData/"+Company)
        # LastDate = ReadLastDate("StockData/"+Company).index
        # LastDate = 
        # data = yf.download(tickers=Company,start=LastDate[0], end=date.today(), interval='1m',index=True)

    else:
        data = yf.download(tickers=Company,start="2015-01-01", end=date.today(), interval='1m',index=True)
        CompanyFileName = "StockData/"+Company+date.today()
        data.to_csv(CompanyFileName)
    
    TotalCompany += 1

