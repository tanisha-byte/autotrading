
from datetime import date
import pandas as pd
from datetime import timedelta
import yfinance as yf
import os

ProfitCount = 0
LossCount = 0
TakeProfitPer = 1.6
StopLossPer = 0.6  # ( 1 - 0.4)
ExceptionalProfitPer = 0
ExceptionalLossPer = 0
listofall = []
def checkDateOfWeek(dt):
    """Return the day of the week as an integer, where Monday is 0 and Sunday is 6"""
    return dt.weekday()

def Debu(text):
    print(text)

def monthToNum(shortMonth):
    shortMonth = shortMonth.lower()
    return {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12
    }[shortMonth]


def checkHoliday(dt):
    holidays = pd.read_csv('StockData/NSEHolidays.csv')
    holidaysList = holidays.iloc[:, 0].tolist()
    # holidaysplit = holidays.iloc[0,0].split('-')
    if checkDateOfWeek(dt) == 6 or checkDateOfWeek(dt) == 5:
        return True
    for i in holidaysList:
        ilist = i.split('-')
        if dt == date(int(ilist[2]), monthToNum(ilist[1]), int(ilist[0])):
            return True
    return False


def Buy(data, buyprice, i):
    global ProfitCount
    global LossCount
    global ExceptionalLossPer
    global ExceptionalProfitPer
    for j in range(len(data.iloc[:, 0])-i-1):
        DayTime = str(data.index[i])
        TimeHour = int(DayTime[11:13])
        OpenBuy = data.iloc[i+j, 0]
        HighBuy = data.iloc[i+j, 1]
        LowBuy = data.iloc[i+j, 2]
        CloseBuy = data.iloc[i+j, 3]
        if OpenBuy >= buyprice*TakeProfitPer or HighBuy >= buyprice*TakeProfitPer or CloseBuy >= buyprice*TakeProfitPer:
            SellingPrice = buyprice*TakeProfitPer
            Debu(SellingPrice)
            Profit = SellingPrice - buyprice
            ProfitCount += 1
            break
        elif OpenBuy <= buyprice*StopLossPer or LowBuy <= buyprice*StopLossPer or CloseBuy <= buyprice*StopLossPer:
            Debu(SellingPrice)
            SellingPrice = buyprice*StopLossPer
            Loss = buyprice - SellingPrice
            LossCount += 1
            break
        if TimeHour >= 15:
            if CloseBuy > buyprice:
                Prof = CloseBuy - buyprice
                ExceptionalProfitPer += Prof/buyprice*100
            elif CloseBuy <= buyprice:
                Los = CloseBuy - buyprice
                ExceptionalLossPer += Los/buyprice*100

    Debu("\n")
    Debu(ProfitCount)
    Debu(LossCount)
    Debu(ExceptionalProfitPer)
    Debu(ExceptionalLossPer)

def Sell(data, sellprice, i):
    global ProfitCount
    global LossCount
    global ExceptionalLossPer
    global ExceptionalProfitPer
    for j in range(len(data.iloc[:, 0])-i-1):
        DayTime = str(data.index[i])
        TimeHour = int(DayTime[11:13])
        OpenSell = data.iloc[i+j, 0]
        HighSell = data.iloc[i+j, 1]
        LowSell = data.iloc[i+j, 2]
        CloseSell = data.iloc[i+j, 3]
        if OpenSell <= sellprice*(1-TakeProfitPer) or LowSell <= sellprice*(1-TakeProfitPer) or CloseSell <= sellprice*(1-TakeProfitPer):
            BuyingPrice = sellprice*(1-TakeProfitPer)
            Profit = sellprice-BuyingPrice
            # ProfitPer = (buyprice*TakeProfitPer - buyprice)/buyprice*100
            ProfitCount += 1
            break
        elif OpenSell >= sellprice*(1+1-StopLossPer) or HighSell >= sellprice*(1+1-StopLossPer) or CloseSell >= sellprice*(1+1-StopLossPer):
            BuyingPrice = sellprice*(1+1-StopLossPer)
            Loss = BuyingPrice-sellprice
            # LossPer = (buyprice - SellingPrice)/buyprice*100
            LossCount += 1
            break
        if TimeHour >= 15:
            if CloseSell < sellprice:
                Prof = sellprice - CloseSell 
                ExceptionalProfitPer += Prof/sellprice*100
            elif CloseSell >= sellprice:
                Los = CloseSell - sellprice
                ExceptionalLossPer += Los/sellprice*100
    Debu("\n")
    Debu(ProfitCount)
    Debu(LossCount)
    Debu(ExceptionalProfitPer)
    Debu(ExceptionalLossPer)


def FifteenMinBreakout(data):
    Debu("Inside Fun 15Min breakout")
    OpeningPerEntry = 0.8
    FifHigh = 0
    FifLow = 100000000
    for i in range(9):
        Debu("Inside High Low Loop")
        if data.iloc[i, 1] > FifHigh:
            FifHigh = data.iloc[i, 1]
        elif data.iloc[i, 2] < FifLow:
            FifLow = data.iloc[i, 2]
    if ((FifHigh-FifLow)/FifLow*100) >= OpeningPerEntry:
        for i in range(len(data.iloc[:, 0])):
            Debu("Inside Time Wise Func")
            Open = data.iloc[i, 0]
            High = data.iloc[i, 1]
            Low = data.iloc[i, 2]
            Close = data.iloc[i, 4]
            BenchMarkHigh = FifHigh*1.0015
            BenchMarkLow = FifLow*(1-0.0015)
            DayTime = str(data.index[i])
            TimeHour = int(DayTime[11:13])
            if 12 >= TimeHour >= 9:
                if Open >= BenchMarkHigh or High >= BenchMarkHigh or Close >= BenchMarkHigh:
                    Buy(data, BenchMarkHigh, i)
                    return
                elif Open <= BenchMarkLow or Low <= BenchMarkLow or Close <= BenchMarkLow:
                    Sell(data, BenchMarkLow, i)
                    return
        

Today = date.today()
CompanyNames = pd.read_csv('StockData/CompanyNames.csv')
DaysTobeCounted = 2
for Company in CompanyNames.iloc[:, 0]:
    Debu("------Company name ------"+Company)
    for i in range(DaysTobeCounted):
        Day = Today - i*timedelta(days=1)   # Includeing Today
        Debu(Day)
        # Day = Today - (i+1)*timedelta(days=1)
        if checkHoliday(Day) == False:
            Debu("Not Holiday")
            data = yf.download(tickers=Company, start=Day,
                               period='1d',end=Day+1*timedelta(days=1), interval='2m', index=True)
            FifteenMinBreakout(data)
    Debu("\n")

Debu("\n")
Debu(ProfitCount)
Debu(LossCount)
Debu(ExceptionalProfitPer)
Debu(ExceptionalLossPer)