import pandas as pd
import yfinance as yf
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count

x_vals = []
y_vals = []

index = count(start=0,step=1)
data = data = yf.download(tickers='TATAMOTORS.NS',start="2022-01-1",period='1d', interval='2m',index=True)
global ins
ins = 0
print(data)
def animate(i):
    global ins
    x_vals.append(ins)
    y_vals.append(data.iloc[ins,1])
    ins = ins + 1
    if len(y_vals) > 1:
        if (y_vals[-1]-y_vals[-2])/y_vals[-2]*100 > 0.1 or (y_vals[-1]-y_vals[-2])/y_vals[-2]*100 < -0.1:
            print((y_vals[-1]-y_vals[-2])/y_vals[-2]*100)
    
    plt.plot(x_vals,y_vals)

ani = FuncAnimation(plt.gcf(),animate,interval=500)

# plt.tight_layout()
# plt.show(