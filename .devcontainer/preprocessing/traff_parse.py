#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 12:30:02 2024

@author: qb
"""

import argostranslate.package
import argostranslate.translate

import pandas as pd
import numpy as np
from googletrans import Translator
from tqdm import tqdm
import re

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
years = np.arange(2017, 2024)
events = ['event'+str(e) for e in years]

prefix = '/home/qb/ML_Group_Assignment//traffic_data/'
x = []
for e in events:
    globals()[e] = pd.read_csv(prefix+e+'.csv')
    globals()[e]['event_year'] = e 
    x.append(globals()[e])

x = pd.concat(x)
x.reset_index(inplace=True)

_res=pd.DataFrame(columns = ['title', 'description'])


def translate_(data):

    from_code = "th"
    to_code = "en"
    idx =data.index.tolist()
    # Download and install Argos Translate package
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())
    global _res
    # Translate
    for i in tqdm(range(data.shape[0])):
        titile_trans = argostranslate.translate.translate(data['title'].loc[idx[i]], from_code, to_code)
        des_trans = argostranslate.translate.translate(data['description'].loc[idx[i]], from_code, to_code)
        _res =pd.concat([_res,pd.DataFrame({'title':titile_trans, 'description':des_trans}, index=[idx[i]])])

x_ = x[x['title_en'].isna()]
translator = Translator()
translate_(x_[['title', 'description']].dropna())
    