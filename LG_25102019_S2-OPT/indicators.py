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
        'F1_Fzg.- Auslastung (%)_'+ control: round(loadProfile.servedEV/len(loadProfile.arrivales) * 100.0, 2),
        'F2_Energ. Auslastung(%)_'+ control: round(round(np.trapz(totalLoad['LP_total_load_kW']), 3)/round(loadProfile.power_kw/loadProfile.numberOfLp, 3)/round(loadProfile.simulationTime,3)*100.0, 2),
#        'F2_Energ. Auslastung(%)':round(np.trapz(totalLoad['LP_total_load_kW'])/loadProfile.power_kw/loadProfile.numberOfLp/loadProfile.simulationTime/len(np.where(loadProfile.disDay['Autos_No']!=0)[0])*len(loadProfile.disDay['Autos_No'])*100,2),
        'F3_Zeitl. Auslastung (%)_'+ control: round(round(totalLoad['LP_occupancy'].sum(),3)/round(loadProfile.numberOfLp,3)/round(loadProfile.simulationTime,3) * 100.0, 2),
        'Max. Gleichzeitigkeitsfaktor_'+ control: round(round(totalLoad['LP_total_load_kW'].max(), 3)/round(loadProfile.numberOfLp/loadProfile.power_kw, 3), 2),
        'Trafo Spitzenlast (%)_'+control:round(round(totalLoad['trafoLoading_kW'].max(), 3) /630.0 *100.0,2),
         'Total charging costs in Euro_'+control: round(sum(round(totalLoad['LP_total_load_kW'][t], 6) /1000.0 / 60 * round(loadProfile.energy_price[t], 6) for t in range(len(totalLoad))),2),
         'Total CO2 emissions in kge_'+control: round(sum(round(totalLoad['LP_total_load_kW'][t], 6) / 60.0 * round(loadProfile.co2_emission[t], 6) for t in range(len(totalLoad))),2),
        'Energy price per kWh_' + control: 0.0
        }

    indicators['Energy price per kWh_' + control] = round(round(indicators['Total charging costs in Euro_'+control], 5) / round((indicators['Gelad. Energie (MWh)_'+ control] * 1000.0), 5), 3)

    print(indicators['Energy price per kWh_' + control], indicators['Total charging costs in Euro_' + control] )

    return indicators