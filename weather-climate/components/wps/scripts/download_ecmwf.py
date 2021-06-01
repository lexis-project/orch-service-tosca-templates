#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:16:59 2021

@author: Vincenzo.Mazzarella
"""

from polytope.api import Client
import threading
import os
import sys
from datetime import datetime, timedelta

initialDateStr=START_DATE[0:8]

print("Processing request for " + initialDateStr + " minus " + PAST_DAY + " day(s)")

initialDate = datetime.strptime(initialDateStr, "%Y%m%d")
pastDays = timedelta(days=int(PAST_DAY))
newDate = initialDate - pastDays
date = newDate.strftime('%Y%m%d')
year = newDate.strftime('%Y')
month = newDate.strftime('%m')
day = newDate.strftime('%d')
hour = "18"
print("Request for " + date)

output_path = OUTPUT_DIRECTORY + '/' + year + '/' + month + '/' + day + '/' + hour + "00"
os.makedirs(output_path, exist_ok=True)

def download_sfc():

 c = Client(user_email = EMAIL_ADDRESS, user_key = KEY, quiet = True)
 request = {
    'stream': 'oper',
    'levtype': 'sfc',
    'param': '129.128/165.128/166.128/167.128/168.128/172.128/134.128/151.128/235.128/31.128/34.128/141.128/139.128/170.128/183.128/236.128/39.128/40.128/41.128/42.128/33.128',
    'step': '6/12/18/24/30/36',
    'time': '12',
    'date': date,
    'repres': 'sh',
    'type': 'fc',
    'class': 'od',
    'grid' : '0.1/0.1',
    'expver': '0001',
    'area': '65/-20/23/48',

 }


# Retrieve data
 c.retrieve('lexis-mars', request, output_path + '/ECMWF_2D_step1.grib')

def download_sfc2():

 c = Client(user_email = EMAIL_ADDRESS, user_key = KEY, quiet = True)
 request = {
    'stream': 'oper',
    'levtype': 'sfc',
    'param': '129.128/165.128/166.128/167.128/168.128/172.128/134.128/151.128/235.128/31.128/34.128/141.128/139.128/170.128/183.128/236.128/39.128/40.128/41.128/42.128/33.128',
    'step': '42/48/54/60/66',
    'time': '12',
    'date': date,
    'repres': 'sh',
    'type': 'fc',
    'class': 'od',
    'grid' : '0.1/0.1',
    'expver': '0001',
    'area': '65/-20/23/48',

 }

 c.retrieve('lexis-mars', request, output_path + '/ECMWF_2D_step2.grib')


def download_pressure():
 c = Client(user_email = EMAIL_ADDRESS, user_key = KEY, quiet = True)
 request = {
    'stream': 'oper',
    'param': '129.128/130.128/157.128/131.128/132.128',
    'levtype': 'pl',
    'levelist': '10/20/30/50/70/100/150/200/250/300/400/500/600/700/800/850/900/925/950/1000',
    'step': '6/12/18/24/30/36',
    'time': '12',
    'date': date,
    'repres': 'sh',
    'type': 'fc',
    'class': 'od',
    'grid' : '0.1/0.1',
    'expver': '0001',
    'area': '65/-20/23/48',

 }

 c.retrieve('lexis-mars', request, output_path + '/ECMWF_3D_step1.grib')


def download_pressure2():
 c = Client(user_email = EMAIL_ADDRESS, user_key = KEY, quiet = True)
 request = {
    'stream': 'oper',
    'param': '129.128/130.128/157.128/131.128/132.128',
    'levtype': 'pl',
    'levelist': '10/20/30/50/70/100/150/200/250/300/400/500/600/700/800/850/900/925/950/1000',
    'step': '42/48/54/60/66',
    'time': '12',
    'date': date,
    'repres': 'sh',
    'type': 'fc',
    'class': 'od',
    'grid' : '0.1/0.1',
    'expver': '0001',
    'area': '65/-20/23/48',

 }

 c.retrieve('lexis-mars', request, output_path + '/ECMWF_3D_step2.grib')


if __name__ == "builtins":


 print("ID of process running main program: {}".format(os.getpid()))

    # print name of main thread
 print("Main thread name: {}".format(threading.current_thread().name))

 t1 = threading.Thread(target=download_sfc, name='t1')
 t2 = threading.Thread(target=download_sfc2, name='t2')
 t3 = threading.Thread(target=download_pressure, name='t3')
 t4 = threading.Thread(target=download_pressure2, name='t4')

 t1.start()
 t2.start()
 t3.start()
 t4.start()

 t1.join()
 t2.join()
 t3.join()
 t4.join()
