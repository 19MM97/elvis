# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 20:01:37 2018

@author: draz
"""
import numpy as np 

def Get_indiciators(loadProfile, totalLoad, control):

    indicators= {
        'Angek. Fzg._'+ control: len(loadProfile.arrivales), 
        'Gelad. Fzg._'+ control: loadProfile.servedEV, 
        'Gelad. Energie (MWh)_'+ control: round(totalLoad['LP_total_load_kW'].sum() / 60000.0,2),  #if control != 'WS' else 
#        round((totalLoad['LP_total_load_kW'].sum() + abs(sum([n for n in totalLoad['sotrage_LP'].tolist() if n <0])))/60000,2),
        'F1_Fzg.- Auslastung (%)_'+ control: round(loadProfile.servedEV/len(loadProfile.arrivales) * 100, 2),
        'F2_Energ. Auslastung(%)_'+ control: round(np.trapz(totalLoad['LP_total_load_kW'])/loadProfile.power_kw/loadProfile.numberOfLp/loadProfile.simulationTime*100, 2),
#        'F2_Energ. Auslastung(%)':round(np.trapz(totalLoad['LP_total_load_kW'])/loadProfile.power_kw/loadProfile.numberOfLp/loadProfile.simulationTime/len(np.where(loadProfile.disDay['Autos_No']!=0)[0])*len(loadProfile.disDay['Autos_No'])*100,2),
        'F3_Zeitl. Auslastung (%)_'+ control: round(totalLoad['LP_occupancy'].sum()/loadProfile.numberOfLp/loadProfile.simulationTime * 100.0, 2),
        'Max. Gleichzeitigkeitsfaktor_'+ control: round(totalLoad['LP_total_load_kW'].max()/loadProfile.numberOfLp/loadProfile.power_kw, 2),
        'Trafo Spitzenlast (%)_'+control:round(totalLoad['trafoLoading_kW'].max()/630 *100,2), 
         'Total charging costs in Euro_'+control: round(sum(totalLoad['LP_total_load_kW'][t]/1000.0/60.0 * loadProfile.energy_price[t] for t in range(len(loadProfile.energy_price))),6),
         'Total CO2 emissions in kge_'+control: round(sum(totalLoad['LP_total_load_kW'][t] * loadProfile.co2_emission[t] for t in range(len(loadProfile.co2_emission))),2),
        'Energy price per kWh' + control: round(round(
                                                sum(loadProfile.energy_price[t] *
                                                    totalLoad['LP_total_load_kW'][t] / 60000.0
                                                    for t in range(len(loadProfile.energy_price))),3) /
                                                round(totalLoad['LP_total_load_kW'].sum() / 60.0, 3),
                                            12)
        }

    # costs = 0
    # energy = 0
    # for t in range(len(loadProfile.energy_price)):
    #     costs += totalLoad['LP_total_load_kW'][t] /1000.0/60.0* loadProfile.energy_price[t]
    #     energy += totalLoad['LP_total_load_kW'][t] / 60.0
    #
    # print(str(costs) + ' in €')
    # print(str(energy) + ' in kWh')
    # print(str(costs/energy) + ' in €/kWh')
    # print('\n___________________________\n')
    #
    # print(str(sum([totalLoad['LP_total_load_kW'][t] / 60.0 / 1000.0 *
    #                                                 loadProfile.energy_price[t]
    #                                                 for t in range(len(loadProfile.energy_price))])) + ' in €')
    # print(str(totalLoad['LP_total_load_kW'].sum() / 60.0) + ' in kWh')
    #
    # print(str(round(round(
    #                                             sum(loadProfile.energy_price[t] *
    #                                                 totalLoad['LP_total_load_kW'][t] / 60000.0
    #                                                 for t in range(len(loadProfile.energy_price))),3) /
    #                                             round(totalLoad['LP_total_load_kW'].sum() / 60.0, 3),
    #                                         12)
    #                                         )
    #       )
    #
    # print(len(loadProfile.energy_price))


    return indicators
