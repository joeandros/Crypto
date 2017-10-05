# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 18:28:05 2017

@author: Joe
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np


def appendMovingAvg(df, step=10):
    
    moving_avg = [0] * (step + 1)
    for i in range(step, df.shape[0]-1):
        moving_avg.append(np.mean(df['Price'][i-step:i]))
    
    df['Moving Average'] = moving_avg

    return df

def makeMAPlot(df):
    
    y_lower = np.floor(min(df['Price']))
    y_upper = np.ceil(max(df['Price']))
    
    plt.ylim(y_lower, y_upper)
    plt.plot(df['Price'])
    plt.plot(df['Moving Average'])
    plt.show()
    

if __name__ == '__main__':
    
    os.chdir("C:/Users/Joe/Dropbox/Crypto/Gdax")
    data = pd.read_csv('2017.10.04_eth.csv')
    df['Price'] = df['Price'].astype(float)

    makeMAPlot(appendMovingAvg(data, step=200))
