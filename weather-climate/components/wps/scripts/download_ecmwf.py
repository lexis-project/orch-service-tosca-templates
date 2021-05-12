#!/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:16:59 2021

@author: vincenzo.mazzarella
"""
import os
import sys
from datetime import datetime, timedelta
from polytope.api import Client

# Compute the date, as it can be needed to get data before the start date (warmup data)
startDateStr=START_DATE[0:8]
startDate = datetime.strptime(START_DATE, "%Y%m%d%H")
hour=START_DATE[8:10]
period=NUMBER_OF_HOURS[0:2]

# For data assimilation, data from 6 hours before is needed
if WPS_MODE.lower() in ['wrfda', 'warmupda']:
    hours = timedelta(hours=6)
    startDate = startDate - hours
    period = str( int(period) + 6)
    newStartDateStr = startDate.strftime('%Y%m%d%H')
    startDateStr = newStartDateStr[0:8]
    hour = newStartDateStr[8:10]

days = timedelta(days=int(PAST_DAY))
newDate = startDate - days
date = newDate.strftime('%Y%m%d')
year = newDate.strftime('%Y')
month = newDate.strftime('%m')
day = newDate.strftime('%d')

print("Processing request for " + date + " " + hour + " getting data for " + period + " hours")

output_path = OUTPUT_DIRECTORY + '/' + year + '/' + month + '/' + day + '/' + hour + "00"
os.makedirs(output_path, exist_ok=True)

# Replace key and email by your Polytope key and email
c = Client(user_email = EMAIL_ADDRESS, user_key = KEY, quiet = True)

request = {
    'stream': 'oper',
    'levtype': 'sfc',
    'param': '129.128/165.128/166.128/167.128/168.128/172.128/134.128/151.128/235.128/31.128/34.128/141.128/139.128/170.128/183.128/236.128/39.128/40.128/41.128/42.128/33.128',
    'step': '0/to/' + period + '/by/3',
    'time': hour,
    'date': date,
    'grid': '0.1/0.1',
    'repres': 'sh',
    'type': 'fc',
    'class': 'od',
    'expver': '0001',
    'area': '65/-20/23/48',
}

# Retrieve data
c.retrieve('lexis-mars', request, output_path + '/ECMWF_2D_' + date + '.grib' )

request = {
    'stream': 'oper',
    'param': '129.128/130.128/157.128/131.128/132.128',
    'levtype': 'pl',
    'levelist': '10/20/30/50/70/100/150/200/250/300/400/500/600/700/800/850/900/925/950/1000',
    'step': '0/to/' + period + '/by/3',
    'time': hour,
    'date': date,
    'grid': '0.1/0.1',
    'repres': 'sh',
    'type': 'fc',
    'class': 'od',
    'expver': '0001',
    'area': '65/-20/23/48',
}

c.retrieve('lexis-mars', request, output_path + '/ECMWF_3D_' + date + '.grib')

print("ECMWF data downloaded for " + date + " hour " + hour + " over " + period + " hours")
