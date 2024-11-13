#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 03:18:26 2024

@author: qb
"""
import pandas as pd 
import numpy as np
import pickle
from prophet import Prophet
from sklearn.impute import KNNImputer
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer
from prophet_missing import fill_missing_values_recursively_with_confidence
from statsmodels.tsa.holtwinters import ExponentialSmoothing

class imputer():
    def __init__(self, weather_obj, substation_obj):
        self.weather_obj = weather_obj
        self.substation_obj = substation_obj
    
    
    #each of the imputatior will have its own function
    def _impute_substation(self, method):
        x_ = pd.read_csv(self.substation_obj.path+'/df.csv')
        #method to impute pm25 one is to regression based methods, 
        #we are not doing for each station seperately as this method is defined and comes from paper
        #(source Tiwari et al 2013)
        if method == 'Tiwari':
            idx = x_[x_['pm25'].isna()].index
            pm10 =  x_['pm10'].loc[idx]
            pm_25 = 0.52 * pm10 + 2.1
            x_.loc[idx, 'pm25'] = pm_25
        if method == 'kumar':
            idx = x_[x_['pm25'].isna()].index
            pm10 =  x_['pm10'].loc[idx]
            pm_25 = 0.63 * pm10 - 1.4
            x_.loc[idx, 'pm25'] = pm_25
        if method == 'USEPA':
            idx = x_[x_['pm25'].isna()].index
            pm10 =  x_['pm10'].loc[idx]
            pm_25 = 0.65 * pm10 - 2.5
            x_.loc[idx, 'pm25'] = pm_25
        #perform exponential moving average to fill in
        if method == 'ema':
            ewm_pm = x_.groupby('location')['pm25'].apply(lambda x: x.ewm(com=0.25).mean())
            #this is risky but it works make sure indexes are correct
            
            x_.loc[x_[x_['pm25'].isna()].index ,'pm25'] = ewm_pm.loc[x_[x_['pm25'].isna()].index]

        x_.to_csv(self.substation_obj.path+'/df.csv')
        
    
    def _missingness_features(self):
        #these feature might have to drop as it might not be missing at random
        #only use despite of tree based models , because xgboost is might find these pattrens on the leafe node of the tree
        x_ = pd.read_csv(self.substation_obj.path+'/df.csv')
        x_['co_fe'] = x_['co'].isna()*1
        x_['so2_fe'] = x_['so2'].isna()*1
        
        x_.to_csv(self.substation_obj.path+'/df.csv')
        
        
    def _iterative_imputation(self, x, test_,name ,y=None, init_startagy='mean'):
        #these imputation methods are mice iterative methods
        #with these methods we will not read data here as it post spltting
        #note that we are voilating the temporal assumptions
        globals()[name]=IterativeImputer(initial_strategy=init_startagy).fit(x, y)
        x=globals()[name].transform(x)
        y=globals()[name].transform(test_)
        
        #make sure the pickle file is the same you pickle on to
        pickle.dump(globals()[name])
        return (x, y)
                
    def prohet_imputer(self, name):
        #we will assume temporal assumption here, #for this to fill in we need to make sure data split without 
        #shuffeling
        #the model is capabale of haneling missing values well lets try// here rn we are not taking data leakage for concern just to make it less comples
        data_=pd.read_csv(self.substation_obj+'/df.csv')
        data = data_[['date', name]].rename(columns = {'date':'ds', name:'y'})
        data.ds= pd.to_datetime(data.ds)
        # Introduce missing values (NaNs) at random places
        np.random.seed(42)  
        # Set seed for reproducibility

        print("Data with missing values:")
        print(data.head(10))  # Check first few rows to verify NaNs

        # Fill missing values recursively using Prophet and get the forecast with confidence intervals
        filled_data, forecast_with_confidence = fill_missing_values_recursively_with_confidence(data)
        # Print the filled data and confidence intervals
        
        return filled_data, forecast_with_confidence
        
    def knn_imputer(self, x, test_, name, n_neighbors,  y=None):
        #x must be train
        globals()[name]  = KNNImputer().knn_imputer(n_neighbors=n_neighbors).fit(x, y)
        x=globals()[name].transform(x)
        y = globals()[name].transform(test_)
        
        pickle.dump(globals()[name])
        
    def exponential_weighted(self):
        #much more simpler methods
        data = pd.read_csv(self.substation_obj+'/df.csv')
        data['day_of_week'] = data['ds'].dt.dayofweek
        # Apply EWMA to each day of the week separately
        data['y_filled'] = data.groupby('day_of_week')['y'].apply(lambda group: group.ewm(span=10, adjust=False).mean())
        
       
        
    def _methods(self, method, name):
        '''list of interpolation methods '''
        '''[quadratic interpolation, linear interpolation bfill, ffill]'''
        #these methods are good only simple time series with no complex trends and seasonalities
        data_ = pd.read_csv(self.substation_obj+'/df.csv')
        data = data_.copy(deep=True)
        if method == 'quadratic interpolation':
            imped = data[name].interpolate(method='quadratic')
            return imped
            
        if method == 'linear interpolation':
            imped = data[name].interpolate(method=='linear')
            return imped
        if method == 'bfill':
            imped = data[name].fillna(method='bfill')
            return imped
        if method == 'ffill':
            imped = data[name].fillna(method='ffill')
            return imped
        
        

