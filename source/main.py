# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 11:38:29 2018

@author: draz
"""


from data import input_2_profile_evl
from indicators import get_indicators
import os
import pandas as pd
from plots import get_plots
from profil import SimulationModel
import time
import Daten
import sys


def profile_ev_load(fix_key, assumptions, data):
    """Initialize the simulation instance and return data of the simulation result.

    :param fix_key: 1 fixes the assumptions. 0 generates new assumptions every simulation.
    :type fix_key: int
    :param assumptions: Containing all simulation configurations.
    :type assumptions: dict
    :param data: Instance of :class:`Daten` containing all simulation parameters and user assumptions.
    :return: Returning the power curves, the indicators and the the instance of :class:`profil` \
    of the simulation.
    :rtype: tuple
    """
    input_2_profile_evl(assumptions['Arrival_distribution'], data)

    total_load = pd.DataFrame()
    df_occupancy = pd.DataFrame()

    indicators = {}
    data.get_time_series_data()
    load_profile = SimulationModel(data)

    load_profile.profile_ev_load(fix_key, data)

    for s in load_profile.charging_points:
        s.load_profile = pd.DataFrame(s.load_profile)
        s.occupancy = pd.DataFrame(s.occupancy)
        total_load = pd.concat([total_load, s.load_profile], axis=1)
        df_occupancy = pd.concat([df_occupancy, s.occupancy], axis=1)

    total_load['lp_total_load_kW'] = total_load.sum(axis=1)
    total_load['trafo_preload_kW'] = data.transformer_preload[0]
    total_load['lp_occupancy'] = df_occupancy.sum(axis=1)

    if data.control == 'WS':
        total_load['storage_lp'] = load_profile.storage.load_profile['LP_%s' % load_profile.storage.battery_id]
        total_load[' storage_soc'] = load_profile.storage.load_profile['SOC_%s' % load_profile.storage.battery_id]
        total_load['trafo_loading_kW'] = (total_load['lp_total_load_kW'] + total_load['trafo_preload_kW'] +
                                          total_load['storage_lp'])
    else:
        total_load['trafo_loading_kW'] = total_load['lp_total_load_kW'] + total_load['trafo_preload_kW']

    datetime = pd.date_range('2018-01-01', periods=assumptions['Simulation_time_in_weeks'] * 10080, freq='T')

    total_load['Time'] = datetime
    total_load = total_load.set_index('Time')

    indicators_temp = get_indicators(load_profile, total_load, data)
    indicators.update(indicators_temp)

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../results/')
    output_name = path + 'res_%s_%s_%s_%s_%s_%s.csv' % (data.car_amount, data.power_cp, data.amount_cp, data.control,
                                                        data.co2_scenario, data.storage_capacity)
    total_load.to_csv(output_name)

    output_name = path + 'indicators_%s_%s_%s_%s_%s_%s.csv' % (data.car_amount, data.power_cp, data.amount_cp,
                                                               data.control, data.co2_scenario, data.storage_capacity)
    pd.DataFrame.from_dict(indicators, orient='index').to_csv(output_name)

    return total_load, indicators, load_profile


def main():
    """Configure simulation settings. Start simulation for each configuration. Save simulation results."""

    start = time.time()
    data = Daten.DataClass()
    assumptions = data.user_assumptions

    kpi_s = []
    load_profiles = []
    output = []

    for car_amount in assumptions['Amount_evs']:  # per week
        data.car_amount = car_amount
        fix_key = 0  # 1 for fixing the assumptions
        for power in assumptions['Power_in_kW']:
            data.power_cp = power
            for lp_amount in assumptions['Amount_lp']:
                data.amount_cp = lp_amount
                for control in assumptions['Control_strategies']:
                    data.control = control
                    for c02_scenario in range(len(assumptions['CO2_Szenario'])):
                        data.co2_scenario = c02_scenario
                        if control == 'WS':
                            for storage_capacity in assumptions['Storage_capacity']:
                                data.storage_capacity = storage_capacity
                                output = profile_ev_load(fix_key, assumptions, data)
                                kpi_s.append(output[1])
                                load_profiles.append((output[0]))
                                fix_key = 0
                        else:
                            output = profile_ev_load(fix_key, assumptions, data)
                            kpi_s.append(output[1])
                            load_profiles.append(output[0])
                            fix_key = 0

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../results/')
    get_plots(path, list(output[1].keys()))

    kpi_s_df = pd.DataFrame(0, index=output[1].keys(),
                            columns=['Uncontrolled',
                                     'First Come, First Served'	,
                                     'Discrimintation Free',
                                     'With Battery',
                                     'Cost optimized'])

    df_load_profiles = pd.DataFrame(0, index=range(1440), columns=['Uncontrolled', 'First Come, First Served',
                                                                   'Discrimintation Free', 'With Battery',
                                                                   'Cost optimized'])

    df = {}
    for df, col in zip(load_profiles, df_load_profiles.columns):

        df_load_profiles[col] = list(df['lp_total_load_kW'][0:1440])
        df_load_profiles[col+'trafo_load'] = list(df['trafo_loading_kW'][0:1440])

    df_load_profiles['Preload'] = list(df['trafo_preload_kW'][0:1440])
    df_load_profiles['Energy_price_(Euro/MWh)'] = data.energy_price[0:1440]
    df_load_profiles['CO2e(kg/kWh)'] = data.co2_emission[0:1440]

    control = 0

    for c in kpi_s_df.columns:
        kpi_s_df[c] = list(kpi_s[control].values())
        control += 1

    kpi_s_df.to_csv('kpi_s.csv')
    df_load_profiles.to_csv('profiles.csv')

    print(time.time()-start)


if __name__ == '__main__':
    sys.path.append('./source')
    main()
