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
        'Gelad. Energie (MWh)_'+ control: round(totalLoad['LP_total_load_kW'].sum()/60000,2),  #if control != 'WS' else 
#        round((totalLoad['LP_total_load_kW'].sum() + abs(sum([n for n in totalLoad['sotrage_LP'].tolist() if n <0])))/60000,2),
        'F1_Fzg.- Auslastung (%)_'+ control: round(loadProfile.servedEV/len(loadProfile.arrivales)*100, 2),
        'F2_Energ. Auslastung(%)_'+ control: round(np.trapz(totalLoad['LP_total_load_kW'])/loadProfile.power_kw/loadProfile.numberOfLp/loadProfile.simulationTime*100, 2),
#        'F2_Energ. Auslastung(%)':round(np.trapz(totalLoad['LP_total_load_kW'])/loadProfile.power_kw/loadProfile.numberOfLp/loadProfile.simulationTime/len(np.where(loadProfile.disDay['Autos_No']!=0)[0])*len(loadProfile.disDay['Autos_No'])*100,2),
        'F3_Zeitl. Auslastung (%)_'+ control: round(totalLoad['LP_occupancy'].sum()/loadProfile.numberOfLp/loadProfile.simulationTime*100, 2),
        'Max. Gleichzeitigkeitsfaktor_'+ control: round(totalLoad['LP_total_load_kW'].max()/loadProfile.numberOfLp/loadProfile.power_kw, 2),
        'Trafo Spitzenlast (%)_'+control:round(totalLoad['trafoLoading_kW'].max()/630 *100,2) 
#        'Kabelabschnitte Spitzenlast (%)_'+control:round(lineloading.max().max(),2),
#        'Min Spannung (pu)_'+control:round(busvoltge.min().min(),2)    
        }
    
    return indicators
