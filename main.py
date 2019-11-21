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


def profile_ev_load(fix_key, assumptions, lp_amount, power, control, car_amount, storage_capacity=None, co2_scenario=None):
    """Initialize the simulation instance and return data of the simulation result.

    :param fix_key: 1 fixes the assumptions. 0 generates new assumptions every simulation.
    :type fix_key: int
    :param assumptions: Containing all simulation configurations.
    :type assumptions: dict
    :param lp_amount: Amount of charging points the charging infrastructure has.
    :type lp_amount: int
    :param power: Power of each charging point in kW.
    :type power: float
    :param control: Control Strategy ('UC', 'FD', 'FCFS', 'WS', 'OPT')
    :type control: str
    :param car_amount: Amount of car arrivals per week.
    :type car_amount: int
    :param storage_capacity: Storage capacity (in kW).
    :type storage_capacity: float
    :param co2_scenario: Position of the CO2_Scenario in the scenario list in assumptions.
    :type co2_scenario: int
    :return: Returning the power curves, the indicators and the the instance of :class:`profil` \
    of the simulation.
    :rtype: tuple
    """
    dis_battery_size, dis_soc, dis_user_type, dis_ev_arr = input_2_profile_evl(assumptions['Arrival_distribution'])
    dis_year = list([car_amount] * assumptions['Simulation_time_in_weeks'])

    total_load = pd.DataFrame()
    df_occupancy = pd.DataFrame()

    indicators = {}

    load_profile = SimulationModel(assumptions, lp_amount, power, dis_ev_arr=dis_ev_arr,
                                   dis_year=dis_year, control=control,
                                   storage_capacity=storage_capacity, co2_scenario=co2_scenario,
                                   dis_battery_size=dis_battery_size, dis_soc=dis_soc,
                                   dis_user_type=dis_user_type)

    load_profile.profile_ev_load(fix_key)

    for s in load_profile.charging_points:
        s.load_profile = pd.DataFrame(s.load_profile)
        s.occupancy = pd.DataFrame(s.occupancy)
        total_load = pd.concat([total_load, s.load_profile], axis=1)
        df_occupancy = pd.concat([df_occupancy, s.occupancy], axis=1)

    total_load['lp_total_load_kW'] = total_load.sum(axis=1)
    total_load['trafo_preload_kW'] = load_profile.trafo_preload[0]
    total_load['lp_occupancy'] = df_occupancy.sum(axis=1)

    if control == 'WS':
        total_load['storage_lp'] = load_profile.storage.load_profile['LP_%s' % load_profile.storage.battery_id]
        total_load[' storage_soc'] = load_profile.storage.load_profile['SOC_%s' % load_profile.storage.battery_id]
        total_load['trafo_loading_kW'] = (total_load['lp_total_load_kW'] + total_load['trafo_preload_kW'] +
                                          total_load['storage_lp'])
    else:
        total_load['trafo_loading_kW'] = total_load['lp_total_load_kW'] + total_load['trafo_preload_kW']

    datetime = pd.date_range('2018-01-01', periods=assumptions['Simulation_time_in_weeks'] * 10080, freq='T')

    total_load['Time'] = datetime
    total_load = total_load.set_index('Time')

    indicators_temp = get_indicators(load_profile, total_load, control)
    indicators.update(indicators_temp)

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'results/')

    output_name = path + 'res_%s_%s_%s_%s_%s_%s.csv' % (car_amount, power, lp_amount, control, co2_scenario, storage_capacity)
    total_load.to_csv(output_name)

    output_name = path + 'indicators_%s_%s_%s_%s_%s_%s.csv' % (car_amount, power, lp_amount, control, co2_scenario, storage_capacity)
    pd.DataFrame.from_dict(indicators, orient='index').to_csv(output_name)

    return total_load, indicators, load_profile


def main():
    """Configure simulation settings. Start simulation for each configuration. Save simulation results."""

    start = time.time()
    assumptions = {
        'Scenario': 'S2',
        'Location': 'Parkhaus/Kaufhaus',
        'Amount_lp': [1],
        'Power_in_kW': [22],
        'Arrival_distribution': 'AutosDiss-supermarket',
        'possible_parking_time': 'Kurz (Normalverteilung, µ=40, σ =10)',
        'Ev_battery_capacity_in_kWh': 'Market Research BEV 2017',
        'Days_per_week': 6,
        'Simulation_time_in_weeks': 1,
        'Preload': 'Station4_1',
        'Control_strategies': ['UC', 'FD', 'FCFS', 'WS', 'OPT'],
        'Storage_capacity': [5],  # R1000-UPB4860 Gen2,
        'Amount_evs': [12],  # per week
        'CO2_Szenario':   ['Referenzszenario',
                           # 'Zukunftsszenario_1',
                           # 'Zukunftsszenario_2',
                           # 'Zukunftsszenario_3',
                           # 'Zukunftsszenario _4',
                           # 'Zunftsszenario _5',
                           # 'Zunftsszenario _6'
                           ],
        'cost_weights': [0.5],
        'co2_weights':  [0.5],
        'opening_hours': [7, 21]
        }

    kpi_s = []
    load_profiles = []
    output = []

    for car_amount in assumptions['Amount_evs']:  # per week
        fix_key = 0  # 1 for fixing the assumptions
        for power in assumptions['Power_in_kW']:
            for lp_amount in assumptions['Amount_lp']:
                for control in assumptions['Control_strategies']:
                    for c02_scenario in range(len(assumptions['CO2_Szenario'])):
                        if control == 'WS':
                            for storage_capacity in assumptions['Storage_capacity']:
                                output = profile_ev_load(fix_key, assumptions, lp_amount, power, control, car_amount,
                                                         storage_capacity, co2_scenario=c02_scenario)
                                kpi_s.append(output[1])
                                load_profiles.append((output[0]))
                                fix_key = 0
                        else:
                            output = profile_ev_load(fix_key, assumptions, lp_amount, power, control, car_amount,
                                                     co2_scenario=c02_scenario)
                            kpi_s.append(output[1])
                            load_profiles.append(output[0])
                            fix_key = 0

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'results/')
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
    df_load_profiles['Energy_price_(Euro/MWh)'] = output[2].energy_price[0:1440]
    df_load_profiles['CO2e(kg/kWh)'] = output[2].co2_emission[0:1440]

    control = 0

    for c in kpi_s_df.columns:
        kpi_s_df[c] = list(kpi_s[control].values())
        control += 1

    kpi_s_df.to_csv('kpi_s.csv')
    df_load_profiles.to_csv('profiles.csv')

    print(time.time()-start)


if __name__ == '__main__':
    main()
