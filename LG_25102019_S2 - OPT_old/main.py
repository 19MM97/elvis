# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 11:38:29 2018

@author: draz
"""


from data import input_2_profile_evl  
import pandas as pd
from indicators import get_indicators
#from slides import GetSlides 
from profil import SimulationModel 
import time
import numpy as np
#from popularTimes import popularTimes 

start = time.time()
assumptions = { 
    'Szenario': 'S2', 
    'Ort': 'Parkhaus/Kaufhaus', 
    'Anzahl-der-Ladepunkte': [2],
    'Leistung-in-kW': [3.7], 
    'Ankunftsverteilung' : 'AutosDiss-supermarket',
    'mögliche Standzeit': "Kurz (Normalverteilung, µ=40, σ =10)",
    'Fahrzeugbatteriekapazitiät in kWh': "Market Research BEV 2017",
    'Tage der Woche': 6,
    'Simulation Zeit (Woche)': 1, 
    'Vorbelastung': 'Station4_1', 
    'ControlStrategies':['OPT'],
    'StorageCapacity': [150], #R1000-UPB4860 Gen2,
    'Anzahl der Autos': [150],
    'CO2_Szenario':   ['Referenzszenario'
#                       'Zukunftsszenario_1', 	
#                       'Zukunftsszenario_2', 
#                       'Zukunftsszenario_3', 
#                       'Zukunftsszenario _4',
#                       'Zunftsszenario _5',
#                       'Zunftsszenario _6'
                                    ],
    'cost_weights': [1],
    'co2_weights' :  [0],
    'Open_hours': [7,21]
    }
#mode = 'manuel'
#

#if mode == 'auto': 
#    Batterysize_arr, SOC_arr, Usergrouptype, Daytype= Input2profileEVL(Day_arr = 'Arr_Typ1', 
#                                                                            Week_arr='Week_Typ1', Year_arr = 'Year_Typ1', ParkingPattern='Ort1')
#    disDay, parkingTime = popularTimes.populartime_position(["Parkhaus"], (48.132986, 11.566126), (48.142199, 11.580047))
#    
#else: 

disBatterysize, disSoc, disUserTyp, disDay = input_2_profile_evl(assumptions['Ankunftsverteilung'])

s2 = time.time()


def profile_ev_load(fix_key, g=None, co2_scenario=None):
    disYear = list([a] * assumptions['Simulation Zeit (Woche)'])
    totalLoad=pd.DataFrame()
    df_occupancy=pd.DataFrame()
    indicators = {}
    loadProfile=SimulationModel(assumptions, n, P, dis_ev_arr=disDay,
                                dis_year=disYear, control=control, storage_capacity=g, co2_scenario=co2_scenario,
                                dis_battery_size=disBatterysize, dis_soc=disSoc, dis_user_type=disUserTyp)
    loadProfile.profile_ev_load(fix_key)
    for s in loadProfile.charging_points:
        s.loadProfile = pd.DataFrame(s.loadProfile)
        s.occupancy = pd.DataFrame (s.occupancy)
        totalLoad = pd.concat([totalLoad, s.loadProfile], axis=1)
        df_occupancy = pd.concat([df_occupancy, s.occupancy], axis=1)
    
       
    totalLoad['LP_total_load_kW'] = totalLoad.sum(axis=1)
    totalLoad['trafo_Preload_kW'] = loadProfile.trafo_preload[0]
    totalLoad['LP_occupancy'] = df_occupancy.sum(axis=1)       
    if control == 'WS': 
        totalLoad['sotrage_LP'] = loadProfile.storage.loadProfile['LP_%s'%loadProfile.storage.batteryID] 
        totalLoad[' sotrage_SOC'] = loadProfile.storage.loadProfile['SOC_%s'%loadProfile.storage.batteryID]
    
    
    totalLoad['trafoLoading_kW'] = totalLoad['LP_total_load_kW'] + totalLoad['trafo_Preload_kW'] + totalLoad['sotrage_LP'] if control == 'WS' else totalLoad['LP_total_load_kW'] +  totalLoad['trafo_Preload_kW']
        
    datetime = pd.date_range('2018-01-01', periods=assumptions['Simulation Zeit (Woche)'] * 10080, freq='T')
    totalLoad['Time'] = datetime
    totalLoad = totalLoad.set_index('Time')
    indicators_temp= get_indicators(loadProfile, totalLoad, control)
    indicators.update(indicators_temp)
    totalLoad.to_csv('LoadProfile_%s_%s_%s_%s_%s_%s.csv'%(a, P, n, control,c, g))
    pd.DataFrame.from_dict(indicators, orient="index").to_csv('indicators_%s_%s_%s_%s_%s_%s.csv'%(a, P, n, control,assumptions['CO2_Szenario'][c], g))
    return totalLoad, indicators, loadProfile


for a in assumptions['Anzahl der Autos']:
    fix_key = 1 # 1 for fixign the assumptions 
    for P in assumptions['Leistung-in-kW']: 
        for n in assumptions['Anzahl-der-Ladepunkte']:
                for control in assumptions['ControlStrategies']: 
                        if control == 'OPT':
                            for c in range(len(assumptions['CO2_Szenario'])):
                                profile_ev_load(fix_key,co2_scenario=c)
                                fix_key = 0
                        elif control== 'WS': 
                            for g in assumptions['StorageCapacity']: 
                                profile_ev_load(fix_key)
                                fix_key = 0
                        else: 
                            profile_ev_load(fix_key)
                            fix_key = 0
#                    

end = time.time()
print(end-start)