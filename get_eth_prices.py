import datetime
import time
import os
import Client as cl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def getTradeDf(client):
    
    trades = client.GetTrades()
    
    price_list = []
    trade_size = []
    timestamp = []
    for trade in trades:
        price_list.append(trade.price)
        trade_size.append(trade.size)
        time = trade.timestamp
        new_time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        timestamp.append(new_time)
    
    df = pd.DataFrame(
                  {'Timestamp':timestamp,
                  'Price':price_list, 
                  'Size':trade_size}
                  )
    
    return df
    
    
def initiateDaily(client):

    curdate = datetime.datetime.today()
    nextday = curdate + datetime.timedelta(days = 1)

    master_df = getTradeDf(client)
    
    while curdate < nextday:
        trades_df = getTradeDf(client)
        
        
        print("old master_df length: ", master_df.shape[0])
        for i in range(0, trades_df.shape[0]-1):
            if (trades_df['Timestamp'][i] == master_df['Timestamp'][master_df.index[-1]]) & (trades_df['Price'][i] == master_df['Price'][master_df.index[-1]]):
                master_df = master_df.append(trades_df.tail(49 - i), ignore_index=True)
            
        print("new master_df length: ", master_df.shape[0])
                
        
        time.sleep(10)
        curdate = datetime.datetime.today()
        print("pausing for 10 sec")
        print("current time difference is ", nextday - curdate)
        
    return master_df


if __name__ == "__main__":  
    
    client = cl.MarketClient("coinbase", "ethusd")
    
    daily_df = initiateDaily(client)
    daily_df.to_csv('eth_prices.csv')
