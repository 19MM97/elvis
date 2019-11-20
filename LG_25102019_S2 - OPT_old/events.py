# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 15:53:58 2019

@author: draz
"""

import scipy.interpolate as intrpol
import numpy as np 
import pickle
import math 
import queue
from station import Station  
import time 

def Arrinterpol(disDay, disYear, simulationTime):
    week_arrivales = []
    nod = 7
    noh = 24
    now = math.ceil(simulationTime//60//24/7)
    y = np.array(disDay)
    y = np.append([0],y)
    y = np.cumsum(y)
    y = y / y[-1]
    y[0] = 0
    x = np.arange(0,noh*nod*60+60,60)
    f=intrpol.interp1d(y,x)
    for W in range(now):
        arrivales = f(np.random.rand((disYear[W])))
        arrivales = np.sort(arrivales)
        arrivales = np.round(arrivales).astype(int)
        arrivales = arrivales.tolist()
    #    math.ceil(simulationTime//60//nod) 
        arrivales = [x + noh*60*W*nod for x in arrivales] 
        week_arrivales = week_arrivales + arrivales
    return week_arrivales


def FixArrivals (control,disDay,disYear,simulationTime, fix_key):    
    if  fix_key == 1:
        week_arrivales = Arrinterpol(disDay, disYear, simulationTime)
        arr_file = open('arr', 'wb')
        pickle.dump(week_arrivales, arr_file)
        arr_file.close()
    else: 
        arr_file = open('arr', 'rb')
        week_arrivales = pickle.load(arr_file)
        arr_file.close()
    return week_arrivales


def GenerateEV(control, disDay,disYear,simulationTime, fix_key): 
    arrivales = FixArrivals (control,disDay,disYear,simulationTime, fix_key)
#    arrivales = EVArrivlas(disDay,disWeek,disYear,simulationTime)
    evQueue = queue.Queue(maxsize = 3)
    return arrivales, evQueue 

def GenerateLP(N,power_kw,simulationTime, control):
    chargingPoints=[]
    for s in range(N):
         chargingPoints.append(Station(power_kw=power_kw, simulation_time=simulationTime, control=control))
    return chargingPoints 






        
        

