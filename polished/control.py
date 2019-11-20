# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 17:25:16 2019

@author: draz
"""

import numpy as np


def discrimination_free(t, trafo_preload, n_ev):
    limit = trafo_preload[3][t] * 0.8 - trafo_preload[0][t]  # 0 for station 4.1, 1 for station 5.1 and 2 for new trafo
    #    print(limit)
    #    print(trafoLoading['TrafoLoading'][t])
    power = limit / n_ev if n_ev > 0 else 0
    #    print(t,power,N_EV)
    #    time.sleep(0.5)
    return power


def first_come_first_served(t, charging_load, trafo_preload):
    return trafo_preload[3][t] * 0.8 - trafo_preload[0][t] - charging_load


def control_with_battery(t, p, trafo_preload, n_ev):
    limit = trafo_preload[3][t] * 0.8 - trafo_preload[0][t]

    power_from_trafo = limit
    xcharging_power = limit - p * n_ev

    return power_from_trafo, xcharging_power


def opt_charging(t, p, trafo_preload, n_ev, co2_limit):
    data = {'Kraftwerk_limit_kVA': trafo_preload[3][t] * 0.8 - trafo_preload[0][t],
            'user_demand_MWh': None,
            'co2_limit_ton': 1.0,
            'stations_types': ['Station_1'],
            'parameters': {
                'powers': [p],
                'cost_rates': [0.25],
                'energy_price': [np.random.uniform(0.39, 0.50)],
                'co2_emission': [co2_limit[t]],
                'lp_each': [n_ev],
                'base_power': [350],
                'base_cost': [0.28],
                'base_bmission': [1],
                'wieght_cost': [0.3],
                'wieght_co2': [0.7]
            }}
    return list(opt_lp(data).values())
