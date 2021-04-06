#!/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:16:59 2021

@author: vincenzo.mazzarella
"""
import sys
from polytope.api import Client

date=DATE[0:8]
hour=DATE[8:10]

print("Processing request for " + date + " " + hour)

# Replace key and email by your Polytope key and email
c = Client(user_email = EMAIL_ADDRESS, user_key = KEY, quiet = True)

request = {
    'stream': 'oper',
    'levtype': 'sfc',
    'param': '129.128/165.128/166.128/167.128/168.128/172.128/134.128/151.128/235.128/31.128/34.128/141.128/139.128/170.128/183.128/236.128/39.128/40.128/41.128/42.128/33.128',
    'step': '0/3/6/9/12/15/18/21/24/27/30/33/36/39/42/45/48/51/54',
    'time': hour,
    'date': date,
    'grid': '0.1/0.1',
    'repres': 'sh',
    'type': 'fc',
    'class': 'od',
    'expver': '0001',
    'area': '62/-23/25/40',

}

# Retrieve data
c.retrieve('lexis-mars', request, OUTPUT_DIRECTORY + '/ECMWF_2D_' + date + '.grib' )

request = {
    'stream': 'oper',
    'param': '129.128/130.128/157.128/131.128/132.128',
    'levtype': 'pl',
    'levelist': '10/20/30/50/70/100/150/200/250/300/400/500/600/700/800/850/900/925/950/1000',
    'step': '0/3/6/9/12/15/18/21/24/27/30/33/36/39/42/45/48/51/54',
    'time': hour,
    'date': date,
    'grid': '0.1/0.1',
    'repres': 'sh',
    'type': 'fc',
    'class': 'od',
    'expver': '0001',
    'area': '62/-23/25/40',

}

c.retrieve('lexis-mars', request, OUTPUT_DIRECTORY + '/ECMWF_3D_' + date + '.grib')

print("ECMWF data downloaded for " + date + " " + hour)
