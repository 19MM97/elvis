# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 17:25:16 2019

@author: draz
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 13:50:28 2018

@author: draz
"""
from opt import opt_lp 
import numpy as np
import time 

def free_discriminat(t, trafoPreload, N_EV):
    limit = trafoPreload[3][t] * 0.8 - trafoPreload[0][t] #0 for station 4.1, 1 for station 5.1 and 2 for new trafo
#    print(limit)
#    print(trafoLoading['TrafoLoading'][t])
    power = limit / N_EV if N_EV > 0 else 0 
#    print(t,power,N_EV)
#    time.sleep(0.5)
    return power 

def fisrt_come_first_serve(t, chargingLoad, trafoPreload): 
#    lpPreload = 0.0 
#    lpPreload = sum([(s.loadProfile['LP_%s'%s.stationID][t]) for s in chargingPoints]) 
#    limit = trafoPreload[0][t] * 0.8 - trafoPreload[1][t] - lpPreload
#    power = 0.00 if limit <= 0.0 else limit 
    return trafoPreload[3][t] * 0.8 - trafoPreload[0][t] - chargingLoad

def contro_lwithBattery(t, P, trafoPreload,  N_EV): 
#    lpPreload = 0.0
#    power = chargingPoints[0].powerMax 
#    lpPreload = sum([(s.loadProfile['LP_%s'%s.stationID][t]) for s in chargingPoints]) 
    limit = trafoPreload[3][t] * 0.8 - trafoPreload[0][t]
    
    powerFromTrafo = limit  
    xchargingPower = limit -  P * N_EV
#    limits = [ powerFromTrafo, xchargingCapacity]
    return powerFromTrafo, xchargingPower

def opt_charging(t, P, trafoPreload, N_EV, co2_limit): 
    data = {'Kraftwerk_limit_kVA': trafoPreload[3][t] * 0.8 - trafoPreload[0][t], 
    'user_demand_MWh': None, 
    'co2_limit_ton': 1.0, 
    'stations_types': ['Station_1'], 
    'parameters': {
            'powers': [P],
            'cost_rates': [0.25], 
            'energy_price': [np.random.uniform(0.39, 0.50)], 
            'co2_emission': [co2_limit[t]],  
            'lp_each': [N_EV], 
            'base_power': [350],
            'base_cost': [0.28],
            'base_bmission': [1], 
            'wieght_cost': [0.3], 
            'wieght_co2': [0.7]
            }}
    return list(opt_lp(data).values())
