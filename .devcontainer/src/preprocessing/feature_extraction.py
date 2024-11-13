#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 22:18:26 2024

@author: qb
"""
import os
import datetime
import calendar
import pandas as pd
import numpy as np

from arcgis.gis import GIS
from geopy.distance import geodesic

gis = GIS()

class features():
    def __init__(self, weather_obj, sub_station_obj, misc, traffic_path = '', rain_path = '',traffic = False, rain = False):
        self.weather_obj = weather_obj
        self.sub_station_obj = sub_station_obj
        self.misc = misc
        if traffic==True:
            self.traffic_path = traffic_path
        if rain== True:
            self.rain_path = rain_path
    
    #lag features with pm2.5 and pm10
    #traffic features
    #misc features
    
    def weighted_distance(self):
        #weather data weighted distance features
        x_t = pd.read_csv(self.sub_station_obj.path+'/df.csv', parse_dates=['date'])
        stations=x_t['location'].unique()
        latitude,longitude = x_t[['latitude', 'longitude']]
        dfs = []
        for station in stations:
           lat, long = x_t[x_t['location'] == station][['latitude', 'longitude']].iloc[0]
           nearby = os.listdir(self.weather_obj.path+station)
           for near in nearby:
               
              wea = pd.read_csv(self.weather_obj.path+station+'/'+near+'/out/wea.csv', parse_dates=['date'])
              _lat, _long = wea[['latitude', 'longitude']].iloc[0]
              distance =geodesic((_long, _lat), (long, lat)).miles
              #use the inverse distance for each feature from weather data and put back to the training data
              _weights = 1/(distance)**2
              f_dic = pd.DataFrame(columns = ['w_wind_speed', 'temp_avg', 'location', 'date'])
              f_dic['location'] = np.repeat(station, wea.shape[0])
              f_dic['w_wind_speed'] = _weights * wea['wind_speed_avg']
              f_dic['temp_avg'] = _weights * wea['temp_avg']
              f_dic['date'] = wea['date']
              dfs.append(f_dic)
        f = pd.concat(dfs)
        f['day'] = f['date'].dt.day
        f['month'] = f['date'].dt.month
        f['year'] = f['date'].dt.year
        x_t['year'] = x_t['date'].dt.year
        x_t['month'] = x_t['date'].dt.month
        x_t['day'] = x_t['date'].dt.day
        cols = ['location', 'year', 'month', 'day', 'w_wind_speed', 'temp_avg']
        x_t = pd.merge(x_t, f, on=['location', 'year', 'month', 'day'], how='left')
        x_t.drop(columns = ['date_y'], inplace=True)
        x_t.rename(columns = {'date_x':'date'}, inplace=True)
        x_t = x_t.loc[:, ~x_t.columns.str.contains('^Unnamed')]
        x_t.to_csv(self.sub_station_obj.path+'/df.csv')

    def temporal_features(self):
        #time related features
        #further if required adding moving average and seasonality features
        x_t = pd.read_csv(self.sub_station_obj.path+'/df.csv', parse_dates = ['date'])
        def make_lags(ts, lags):
            return pd.concat({f'y_lag_{i}': ts.shift(i)
                              for i in range(1, lags + 1)},axis=1)
        
        x_t.set_index(pd.PeriodIndex(x_t.date, freq="W"),inplace=True)
        x_ = make_lags(x_t.pm25, lags=7)
        lags = [f'y_lag_{i}' for i in range(1,8)]
        x_t[lags] = x_
        x_t.reset_index(inplace=True, drop=True)
        #calulate month of week
        x_t['wom'] = x_t['date'].apply(self.week_of_month)
        x_t.to_csv(self.sub_station_obj.path+'/df.csv')
        
        
    def week_of_month(self,tgtdate):
    
        days_this_month = calendar.mdays[tgtdate.month]
        for i in range(1, days_this_month):
            d = datetime.datetime(tgtdate.year, tgtdate.month, i)
            if d.day - d.weekday() > 0:
                startdate = d
                break
        # now we canuse the modulo 7 appraoch
        return (tgtdate - startdate).days //7 + 1    
        
    
    def traffic_features(self, phi=2):
        '''phi here is distance threshold'''
        t_x = pd.read_csv(self.traffic_path, parse_dates=['start', 'end'])
        x = pd.read_csv(self.sub_station_obj.path+'/df.csv', parse_dates=['date'])
        x['month']= x['date'].dt.month
        x['year'] = x['date'].dt.year
        x['day'] = x['date'].dt.day
        
        t_x['month'] = t_x['start'].dt.month
        t_x['year'] = t_x['start'].dt.year
        t_x['day'] = t_x['start'].dt.day
        
        t_x = t_x[t_x['distance'] <= phi]
        event_count = t_x.groupby(['location', 'year', 'month', 'day'])['event'].apply(lambda x: x.count())
        distances = t_x.groupby(['location','year', 'month','day'])['distance'].mean()
        volume = t_x.groupby(['location','year', 'month','day'])['distance'].mean()
        #please check the correct input to the daya before resetting the index
        x.set_index(['location', 'year', 'month', 'day'], inplace=True)
        x['distance_traffic'] = distances
        x['event_count'] = event_count
        x['volume'] = volume
        x.reset_index(inplace=True)
        #distances
        # event_count = t_x.groupby(['location', 'year', 'month'])['event'].apply(lambda x: x.count())

        x.to_csv(self.sub_station_obj.path+'/df.csv')
                
        
    def rain_features(self, phi=0):
        '''phi here is distance threshold'''
        t_x = pd.read_csv(self.rain_path, parse_dates=['start', 'end'])
        x = pd.read_csv(self.sub_station_obj.path+'/df.csv', parse_dates=['date'])
        x['month']= x['date'].dt.month
        x['year'] = x['date'].dt.year
        x['day'] = x['date'].dt.day
        
        t_x['month'] = t_x['start'].dt.month
        t_x['year'] = t_x['start'].dt.year
        t_x['day'] = t_x['start'].dt.day
        
        t_x = t_x[t_x['distance'] <= phi]
        r_count = t_x.groupby(['location', 'year', 'month', 'day'])['event'].apply(lambda x: x.count())
        distances = t_x.groupby(['location','year', 'month','day'])['distance'].mean()
        volume = t_x.groupby(['location','year', 'month','day'])['distance'].mean()
        #please check the correct input to the daya before resetting the index
        x.set_index(['location', 'year', 'month', 'day'], inplace=True)
        x['r_distance'] = distances
        x['r_count'] = r_count
        x['r_vol'] = volume
        x.reset_index(inplace=True)
        x = x.loc[:, ~x.columns.str.contains('^Unnamed')]
        x.to_csv(self.sub_station_obj.path+'/df.csv')

    
    def mics_features(self):
        eng = pd.read_csv('/home/qb/ML_Group_Assignment/eng.csv')
        eng.set_index('Year', inplace=True)
        x= pd.read_csv(self.sub_station_obj.path+'/df.csv', parse_dates=['date'])
        x['year'] = x['date'].dt.year
        x['energy_consumption'] = eng['energy_consumption']
        
        sc_pr = pd.read_csv('/home/qb/ML_Group_Assignment/s_pr.csv', parse_dates=['date'])
        sc_pr.set_index('date', inplace=True)
        x['industrial_production'] = sc_pr
        x.reset_index(inplace=True)
        x = x.loc[:, ~x.columns.str.contains('^Unnamed')]
        x.to_csv(self.sub_station_obj.path+'/df.csv')
        
        
    
    def pm25_to_aqi(self,pm25_concentration):
            #createing predictive variable

            # Define the PM2.5 breakpoints and corresponding AQI ranges
            breakpoints = [
                (0.0, 12.0, 0, 50),  # Good
                (12.1, 35.4, 51, 100),  # Moderate
                (35.5, 55.4, 101, 150),  # Unhealthy for Sensitive Groups
                (55.5, 150.4, 151, 200),  # Unhealthy
                (150.5, 250.4, 201, 300),  # Very Unhealthy
                (250.5, 500.4, 301, 500)  # Hazardous
            ]
            
            # Find the appropriate breakpoint for the given PM2.5 value
            for low, high, aqi_low, aqi_high in breakpoints:
                if low <= pm25_concentration <= high:
                    # Calculate AQI using the formula
                    aqi = ((aqi_high - aqi_low) / (high - low)) * (pm25_concentration - low) + aqi_low
                    return round(aqi)
                    
            
            # If PM2.5 value is outside the expected range
        # PM2.5 value is outside the valid range for AQI
        
        
    def convert_aqi_to_category(self,aqi):
        if aqi != None:
            if aqi <= 50:
                return 'Good'
            elif aqi <= 100:
                return 'Moderate'
            elif aqi <= 150:
                return 'Unhealthy for Sensitive Groups'
            elif aqi <= 200:
                return 'Unhealthy'
            elif aqi <= 300:
                return 'Very Unhealthy'
            elif aqi <= 500:
                return 'Hazardous'
            else:
                return 'Invalid'  
    
            