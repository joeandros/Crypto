# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 22:14:38 2017

@author: Joe
"""

import gdax
import numpy as np
import pandas as pd
import datetime
import time
import os
import sys

def updateLatestTick(client, df):
    
    new_df = generateTickDf(client)
    
    if df['Trade Id'][df.shape[0] - 1 ] != new_df['Trade Id'][0]:
        df = df.append(new_df, ignore_index = True)
    
    return df
    
def generateTickDf(client):
    
    latest_tick = client.get_product_ticker('ETH-USD')

    df = pd.DataFrame({'Date': [datetime.datetime.strptime(latest_tick['time'], '%Y-%m-%dT%H:%M:%S.%fZ').date()],
                       'Time': [datetime.datetime.strptime(latest_tick['time'], '%Y-%m-%dT%H:%M:%S.%fZ').time()],
                       'Trade Id': [latest_tick['trade_id']],
                       'Ask': [latest_tick['ask']],
                       'Bid': [latest_tick['bid']],
                       'Price': [latest_tick['price']],
                       'Size': [latest_tick['size']],
                       'Volume': [latest_tick['volume']]
                        })
    
    return df
    
def pullData(client, df, curtime, num_hours, sleep_time):
    
    endtime = curtime + datetime.timedelta(hours = num_hours)
    
    while curtime < endtime:
        
        try:
            df = updateLatestTick(client, df)
            print('Row length:', df.shape[0], 'Current price:', df['Price'][df.shape[0] - 1], 'Time is' + str(curtime))
        except:
            e = sys.exc_info()
            print('Error:', e)
            
        time.sleep(sleep_time)
        print('Pausing for', sleep_time, 'seconds.')
        curtime = datetime.datetime.today()
        
    return df
    

if __name__ == "__main__":
    
    public_client = gdax.PublicClient()
    curdate = datetime.datetime.today()
    
    df = pullData(public_client, generateTickDf(public_client), curdate, 12, 1)
    
    endtime = datetime.datetime.today()

    file_name = str(curdate.year) + '_' + str(curdate.month) + '_' + str(curdate.day) + '__' + str(curdate.hour) + str(curdate.minute) + str(curdate.second) + '_to_' + str(endtime.year) + '_' + str(endtime.month) + '_' + str(endtime.day) + '__' + str(endtime.hour) + str(endtime.minute) + str(endtime.second) + '_eth_data.csv' 
    df.to_csv(file_name, header = True)