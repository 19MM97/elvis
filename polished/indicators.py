# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 20:01:37 2018

@author: draz
"""
import numpy as np 


def get_indicators(load_profile, total_load, control):

    hours_station_opened = (load_profile.assumptions['Open_hours'][-1] - load_profile.assumptions['Open_hours'][0]) * \
        load_profile.assumptions['Simulation Zeit (Woche)'] * load_profile.assumptions['Tage der Woche']

    arrived_cars = len(load_profile.arrivals)
    served_cars = load_profile.servedEV
    cars_not_served = len(load_profile.arrivals) - load_profile.servedEV

    total_energy_loaded = total_load['LP_total_load_kW'].sum() / 1000.0 / 60.0

    load_factor_cars = load_profile.servedEV / len(load_profile.arrivals) * 100.0
    load_factor_energy = total_energy_loaded * 1000 / load_profile.powerKw / \
        load_profile.numberOfLp / hours_station_opened * 100.0
    load_factor_time = total_load['LP_occupancy'].sum() / load_profile.numberOfLp / \
        (hours_station_opened * 60.0) * 100.0

    diversity_factor = total_load['LP_total_load_kW'].max() / load_profile.numberOfLp / load_profile.powerKw

    trafo_peak_load = total_load['trafoLoading_kW'].max() / load_profile.trafoPreload[-1][0] * 100.0

    co2_emissions = sum(total_load['LP_total_load_kW'][t] * load_profile.co2Emission[t]
                        for t in range(len(total_load))) / 60.0

    energy_costs = sum((total_load['LP_total_load_kW'][t] / 1000 * load_profile.energyPrice[t])
                       for t in range(len(total_load))) / 60.0
    specific_energy_costs = energy_costs * 100.0 / (total_load['LP_total_load_kW'].sum() / 60.0)
    if load_profile.servedEV != 0:
        satisfaction_factor = len(np.where(np.asanyarray([load_profile.vehicles[ev.carID].soc
                                                         for ev in load_profile.vehicles.values()]) >= 0.9)[0]) \
                          / load_profile.servedEV * 100
    else:
        satisfaction_factor = "no_costumer_served"

    indicators = {
        'ArrivedCars_' + control: arrived_cars,
        'ServedCars._' + control: served_cars,
        'TotalEnergyLoaded(MWh)_' + control: round(total_energy_loaded, 4),
        'CarsNotServed_' + control: cars_not_served,
        'F1_LoadFactorCars(%)_' + control: round(load_factor_cars, 2),
        'F2_LoadFactorEnergy(%)_' + control: round(load_factor_energy, 2),
        'F3_LoadFactorTime(%)_' + control: round(load_factor_time, 2),
        'MaxDiversityFactor' + control: round(diversity_factor, 2),
        'TrafoPeakLoad(%)_'+control: round(trafo_peak_load, 2),
        'CO2Emissions(kge)_' + control: round(co2_emissions, 2),
        'EnergyCosts(Euro)_' + control: round(energy_costs, 2),
        'SpecificEnergyCosts(Euro/kWh)_' + control: round(specific_energy_costs, 2),
        "Zufriedenheit (%)_"+control: satisfaction_factor
        }

    print('Control', control,  "Energy in MWh =", round(np.trapz(total_load['LP_total_load_kW']) / 60000.0, 4),
          indicators['TotalEnergyLoaded(MWh)_' + control])

    indicators.update({'Abfahrtszustand_' + control + "_" + load_profile.vehicles[ev.carID].carID:
                       load_profile.vehicles[ev.carID].soc for ev in load_profile.vehicles.values()})

    return indicators
