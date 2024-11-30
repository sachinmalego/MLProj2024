#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 12:08:29 2024

@author: qb
"""
import pandas as pd
import numpy as np

from arcgis.geocoding import geocode
from arcgis.gis import GIS
from arcgis.geometry import Point
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pyarrow.parquet as pq
import pyarrow as pq

gis = GIS()

def get_lat_long_by_state(location):
    if location  != None or location != '' :
        geolocator = Nominatim(user_agent="myGeopyApp/1.0")
        esrihq = geocode(location)
        if esrihq != None:
            latitude, longitude = esrihq[0]['location']['x'], esrihq[0]['location']['y']
            return latitude, longitude
        
        
years = np.arange(2017, 2024)
events = ['event'+str(e) for e in years]
locations = ['samut-prakan', 'chulalongkorn-hospital', 'samut-sakhon', 'thonburi-power',]


prefix = '/home/qb/ML_Group_Assignment'
# x = []
# for e in events:
#     globals()[e] = pd.read_csv(prefix+e+'.csv')
#     globals()[e]['event_year'] = e 
#     x.append(globals()[e])

x=pd.read_csv('{}/p_traffic_.csv'.format(prefix))

# x = pd.concat(x)
# x.reset_index(inplace=True)

x['start'] = pd.to_datetime(x['start'])
x['stop'] = pd.to_datetime(x['stop'])

x['volume'] = x[['start', 'stop']].apply(lambda x: pd.Timedelta(x['stop'] - x['start']).seconds/(60*60*24), axis=1)

x['year']=x['event_year'].apply(lambda x: x[-4:]).astype('int')
x_ = x[['title_en', 'description_en']].dropna()
#find the keywords
keywords = ['Rain', 'rain']

poss_idxs = []
for k in keywords:
    poss_idxs.append(x_[x_['title_en'].str.contains(k)].index)
    


# print(x.loc[poss_idxs[0]])
    
#todo conversion, keyword search fire, traffic, find nerest location to stations, merging, bulding baseline model
    
base=pd.DataFrame(columns=['station', 'latitude', 'longitude', 'distance', 'event', 'year', 'title', 'volume', 'start', 'end'])

for i,loc in enumerate(locations):
    for j, k in enumerate(keywords):
        longitude, latitude = get_lat_long_by_state(loc)
        distance =x.loc[poss_idxs[j]].apply(lambda c: geodesic((c['latitude'], c['longitude']), (latitude, longitude)).miles, axis=1)
    
        #for traffic get all co-ordinates how far is the traffic from our base sensory location
        latitude=x.loc[poss_idxs[j]]['latitude']
        longitude=x.loc[poss_idxs[j]]['longitude']
        year=x.loc[poss_idxs[j]]['year']
        event =np.repeat(k, poss_idxs[j].shape[0]).tolist()
        station=np.repeat(loc, poss_idxs[j].shape[0]).tolist()
        title = x.loc[poss_idxs[j]]['title_en']
        volume = x.loc[poss_idxs[j]]['volume']
        start = x.loc[poss_idxs[j]]['start']
        end = x.loc[poss_idxs[j]]['stop']
        
        base_=pd.DataFrame({'location':loc, 'latitude':latitude, 
                      'longitude':longitude, 'year': year, 
                      'event':event, 'station':station, 'distance':distance, 'title':title, 'volume':volume, 'start':start, 'end':end})
        base = pd.concat([base, base_])
        
        
base.to_csv('rain_base.csv')        
# base = pd.DataFrame(base)

    

    

