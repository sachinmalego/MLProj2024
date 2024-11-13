#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 16:48:52 2024

@author: qb
"""

import os
import glob
import pandas as pd 
import numpy as np 
import dask as dd 
from arcgis.gis import GIS
import traffic_process
from arcgis.geocoding import geocode

from geopy.geocoders import Nominatim

#the whole process of clearning merging will be run in parallel
gis = GIS()

class preprocess_:
    def __init__(self, path='./', cleaning=False):
        
        '''path is the path of the file you are create for each file we will create seprate object 
        each object have separate preprocessing that is why we have seperate path here'''
        if cleaning:
            self.path = path
            #add the base station location here
            self.locations = ['samut-prakan', 'chulalongkorn-hospital', 'samut-sakhon', 'thonburi-power-sub-station-bangkok']

    
    def _clean_(self , type_):
        if type_=='train':
            cols = ['pm25','pm10', 'o3', 'no2','so2','co']
            df = pd.read_csv(self.path+'/'+'df.csv')
            df.rename(columns={' pm25':'pm25', 
                              ' pm10':'pm10', 
                              ' o3':'o3',
                              ' no2':'no2', 
                              ' so2':'so2', 
                              ' co':'co'}, inplace=True)
            df[cols]=df[cols].apply(lambda x: x.replace(' ', np.NAN), axis=1)
            #type conversion
            df[cols].apply(lambda x: x.astype(float), axis=0)
            stations = df['location'].unique()
            dic = {'location':[], 'latitude':[], 'longitude':[]}
            for station in stations:
                lat,long=traffic_process.get_lat_long_by_state(station)
                dic['location'].append(station)
                dic['latitude'].append(lat)
                dic['longitude'].append(long)
            dic = pd.DataFrame(dic)
            df.set_index('location', inplace=True)
            dic.set_index('location', inplace=True)
            df[['latitude', 'longitude']] = dic[['latitude', 'longitude']]
            df.reset_index(inplace=True)
            df.to_csv(self.path+'/'+'df.csv')
    
        elif type_=='weather':
           stations = []
           #make date columns and extract the coordinates
           for loc in self.locations: 
               prefix = self.path+loc
               #right now we are observing only single input station 
               name = os.listdir(prefix)
               wea = pd.read_csv(prefix+'/'+name[0]+'/out/wea.csv')
               wea['date'] = np.NAN
               for day in range(wea.shape[0]):
                   wea.loc[day, 'date'] = pd.to_datetime(wea[['year', 'month']].assign(day=day+1),  format='%Y%m%d', errors='coerce').loc[day]
                  
              # getting co-ordinates for the locations     
            #clean the weatherdataset
                #put it in the list in case we have more than one stations
               stations.append(wea['weather_station'].unique())
               stations=np.array(stations).flatten()
               #get all the weather stations
               for station in stations:
                   wea[['latitude', 'longitude']] = traffic_process.get_lat_long_by_state(station)
               stations = []
            #write the dataframe
               wea.to_csv(prefix+'/'+name[0]+'/out/wea.csv')
               
        elif type_ == 'traffic':
            pass
        elif type_ == 'misc':
            pass

        
    def read_data(self, type_):
        if type_ == 'train':
            df = []
            for location in self.locations:
                globals()[location] = pd.read_csv(self.path+'/'+location+'.csv')
                globals()[location]['location'] = location 
                df.append(globals()[location])
            df=pd.concat(df)
            df.to_csv(self.path+'/df.csv')
                
        elif type_=='weather':
            for location in self.locations:
                prefix = self.path+location
                name_nearby = os.listdir(prefix)
                #we will have all the concatinated file
                for name in name_nearby:
                    #read all the csv file inside the location
                    temp = pd.concat([pd.read_csv(f) for f in glob.glob(prefix+'/'+name+'/*.csv')])
                    globals()[name] = temp
                    #pass the name of each weather station
                    globals()[name]['weather_station'] = name
                
                #write the data frame to the same folder
                    
                    dir_ = prefix+'/'+name+'/'
                    os.chdir(dir_)
                    if not os.path.exists('out'):
                            os.makedirs('out')
                            globals()[name].to_csv('out/wea.csv')
                    else:
                        globals()[name].to_csv('out/wea.csv')
            #update the path
            return                 
                    
        elif type_ == 'traffic':
            pass
        
        
        elif type_ == 'misc':
            sc_pr = pd.read_csv(self.path+'/'+'sc_pr.csv')
            sc_pr.rename(columns = {'w_0':'date', 'w_1':'price'}, inplace=True)
            sc_pr.drop(columns = {'Unnamed: 0'}, inplace =True)
            sc_pr.to_csv(self.path+'/'+'s_pr.csv', index = None)
            
            energy = pd.read_csv(self.path+'/'+'per-capita-energy-use.csv')
            energy = energy[energy['Entity'] == 'Thailand']
            energy.set_index('Year', inplace=True)
            years = np.arange(2017, 2024)
            eng = energy.loc[years]
            eng.rename(columns={'Primary energy consumption per capita (kWh/person)':'energy_consumption'}, inplace=True)
            eng.reset_index(inplace=True)
            eng.to_csv(self.path+'/'+'eng.csv', index=None)
            
           #read the weather dataset
                
        
    
    
        

        