# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 11:38:29 2018

@author: draz
"""

from data import input_2_profile_evl
import pandas as pd
from indicators import get_indicators
from profil import SimulationModel
import time


def profile_ev_load(fix_key, assumptions, control, a, n, p, g=None, co2_scenario=None):
    dis_battery_size, dis_soc, dis_user_type, dis_day = input_2_profile_evl(assumptions['Ankunftsverteilung'])
    dis_year = list([a] * assumptions['Simulation Zeit (Woche)'])
    total_load = pd.DataFrame()
    df_occupancy = pd.DataFrame()
    indicators = {}
    load_profile = SimulationModel(assumptions, n, p, dis_ev_arr=dis_day, dis_year=dis_year, control=control,
                                   storage_capacity=g, co2_scenario=co2_scenario,
                                   dis_battery_size=dis_battery_size, dis_soc=dis_soc,
                                   dis_user_type=dis_user_type)

    load_profile.profile_ev_load(fix_key)
    for s in load_profile.charging_points:
        s.loadProfile = pd.DataFrame(s.loadProfile)
        s.occupancy = pd.DataFrame(s.occupancy)
        total_load = pd.concat([total_load, s.loadProfile], axis=1)
        df_occupancy = pd.concat([df_occupancy, s.occupancy], axis=1)

    total_load['LP_total_load_kW'] = total_load.sum(axis=1)
    total_load['trafo_Preload_kW'] = load_profile.trafo_preload[0]
    total_load['LP_occupancy'] = df_occupancy.sum(axis=1)
    if control == 'WS':
        total_load['sotrage_LP'] = load_profile.storage.loadProfile['LP_%s' % load_profile.storage.batteryID]
        total_load[' sotrage_SOC'] = load_profile.storage.loadProfile['SOC_%s' % load_profile.storage.batteryID]

    total_load['trafoLoading_kW'] = \
        total_load['LP_total_load_kW'] + total_load['trafo_Preload_kW'] + total_load['sotrage_LP'] \
        if control == 'WS' \
        else total_load['LP_total_load_kW'] + total_load['trafo_Preload_kW']

    datetime = pd.date_range('2018-01-01', periods=assumptions['Simulation Zeit (Woche)'] * 10080, freq='T')
    total_load['Time'] = datetime
    total_load = total_load.set_index('Time')
    indicators_temp = get_indicators(load_profile, total_load, control)
    indicators.update(indicators_temp)
    total_load.to_csv('LoadProfile_%s_%s_%s_%s_%s_%s.csv' % (a, p, n, control, co2_scenario, g))
    pd.DataFrame.from_dict(indicators, orient="index").to_csv(
        'indicators_%s_%s_%s_%s_%s_%s.csv' % (a, p, n, control, co2_scenario, g))
    return total_load, indicators, load_profile


def main():
    start = time.time()
    assumptions = {
        'Szenario': 'S2',
        'Ort': 'Parkhaus/Kaufhaus',
        'Anzahl-der-Ladepunkte': [1],
        'Leistung-in-kW': [22],
        'Ankunftsverteilung': 'AutosDiss-supermarket',
        'mögliche Standzeit': "Kurz (Normalverteilung, µ=40, σ =10)",
        'Fahrzeugbatteriekapazitiät in kWh': "Market Research BEV 2017",
        'Tage der Woche': 6,
        'Simulation Zeit (Woche)': 1,
        'Vorbelastung': 'Station4_1',
        'ControlStrategies': ['UC', 'FD', 'FCFS', 'WS', 'OPT'],
        'StorageCapacity': [5],  # R1000-UPB4860 Gen2,
        'Anzahl der Autos': [12],
        'CO2_Szenario': ['Referenzszenario',
                         # 'Zukunftsszenario_1',
                         # 'Zukunftsszenario_2',
                         # 'Zukunftsszenario_3',
                         # 'Zukunftsszenario _4',
                         # 'Zunftsszenario _5',
                         # 'Zunftsszenario _6'
                         ],
        'cost_weights': [0.5],
        'co2_weights': [0.5],
        'Open_hours': [7, 21]
    }

    for a in assumptions['Anzahl der Autos']:
        fix_key = 1  # 1 for fixing the assumptions
        for p in assumptions['Leistung-in-kW']:
            for n in assumptions['Anzahl-der-Ladepunkte']:
                for control in assumptions['ControlStrategies']:
                    # if control == 'OPT':
                    for c in range(len(assumptions['CO2_Szenario'])):
                        # x = profile_ev_load(fix_key, co2_scenario=c)
                        # fix_key = 0

                        if control == 'WS':
                            for g in assumptions['StorageCapacity']:
                                x = profile_ev_load(fix_key, assumptions, control, a, n, p, g, c)
                                fix_key = 0
                        else:
                            g = None
                            x = profile_ev_load(fix_key, assumptions, control, a, n, p, g, c)
                            fix_key = 0
    #
    if assumptions['ControlStrategies'] == 'OPT':
        load = x[2]
        power = pd.DataFrame(0, index=range(10080), columns=['price', 'load', 'co2'])
        power['price'] = load.energy_price
        power['co2'] = load.co2_emission
        power['load'] = x[0]['LP_total_load_kW'].tolist()
        ax = power['price'].plot()
        ax2 = ax.twinx()
        power['load'].plot(ax=ax2)
        power.to_csv('power_test_%s.csv' % 1)

    print(time.time() - start)


if __name__ == "__main__":
    for i in range(20):
        main()
