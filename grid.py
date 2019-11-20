# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 16:02:56 2019

@author: draz
"""
# This code models the lighting grid of in several streets in Berlin Adlershof As part of the Flexnet4E-mobility project

import pandapower as pp
import numpy as np
from pandapower.plotting.plotly import simple_plotly
import pandas as pd 


class Grid:
    
    def __init__(self, lps, totalLoad): 
        self.lineloading = None
        self.trafoloading = None
        self.busvoltage = None
        self.net_lighting_lv = None
        self.totalLoad = totalLoad
        self.lps = lps
        self.model_lv_grid()
        self.indexTime()
        
    def indexTime(self): 
        self.lineloading = pd.DataFrame(index=range(len(self.totalLoad)), columns=range(len(self.net_lighting_lv.line)))
        self.trafoloading = pd.DataFrame(index=range(len(self.totalLoad)), columns=range(len(self.net_lighting_lv.trafo)))
        self.busvoltage = pd.DataFrame(index=range(len(self.totalLoad)), columns=range(len(self.net_lighting_lv.bus)))
        for L in range(len(self.net_lighting_lv.line)):
            self.lineloading.rename(columns={self.lineloading.columns[L]: self.net_lighting_lv.line['name'][L]}, inplace=True)
        for tr in range(len(self.net_lighting_lv.trafo)):
            self.trafoloading.rename(columns={self.trafoloading.columns[tr]: self.net_lighting_lv.trafo['name'][tr]}, inplace=True)                 
        for b in range(len(self.net_lighting_lv.bus)):
            self.busvoltage.rename(columns={self.busvoltage.columns[b]: self.net_lighting_lv.bus['name'][b]}, inplace=True)
        datetime = pd.date_range(start='2018-01-01', periods=len(self.totalLoad), freq='H') 
        self.busvoltage['Time'] = datetime
        self.lineloading['Time'] = datetime
        self.trafoloading['Time'] = datetime
        self.busvoltage = self.busvoltage.set_index('Time')
        self.lineloading = self.lineloading.set_index('Time')
        self.trafoloading = self.trafoloading.set_index('Time')
        
    def model_lv_grid(self):
        self.net_lighting_lv = pp.create_empty_network()
        #cable data #150mm^2 AL
        line_data = {
            'c_nf_per_km': 0.0, 'r_ohm_per_km': 0.2647,
            'x_ohm_per_km': 0.0823, 'max_i_ka': 1.0,
            'type': 'cs'
            }
        pp.create_std_type(self.net_lighting_lv, line_data, name='UGlight', element='line')        
        buses_20kv = ['bus_st20', 'bus_st521','bus_st518']
        
        # Busses
        for bus in buses_20kv: 
            pp.create_bus(self.net_lighting_lv, name=bus+'_mv', vn_kv=20.0, type='b', zone='Ernst_Augstin_Str')
        for bus in buses_20kv: 
            pp.create_bus(self.net_lighting_lv, name=bus+'_lv', vn_kv=0.4, type='b', zone='Ernst_Augstin_Str')
            

        for  node in range(6,52): 
            pp.create_bus(self.net_lighting_lv, name='Bus%s'%node, vn_kv=.4, type='m', zone='Ernst_Augstin_Str')
            pp.create_load(self.net_lighting_lv, node, p_mw=0.001, q_mvar=0.0, name='Lamp_at_node%s'%node)    
      
        # Trafos
        for tr in range(3):
            pp.create_transformer_from_parameters(self.net_lighting_lv, tr, tr+3, sn_mva=0.5, vn_hv_kv=20.0,
                                                  vn_lv_kv=0.4, vkr_percent=1.0, vk_percent=4.123106,
                                                  pfe_kw=0.0, i0_percent=0.0, shift_degree=30.0,
                                                  tap_pos=0.0, name=' Trafo Bus%s-Bus%s'%(tr,tr+2))
            
            pp.create_load_from_cosphi(self.net_lighting_lv, 
                                       tr+3, sn_mva=0.0, cos_phi=0.95, 
                                       name='Trafo_preload_'+buses_20kv[tr], mode='ind')
            pp.create_ext_grid(self.net_lighting_lv, tr, vm_pu=1.0, va_degree=0.0, s_sc_max_mva=100.0,
                               s_sc_min_mva=100.0, rx_max=1.0, rx_min=1.0)
            lv_buses = [4,5] 
            
        for bus in range(3,len(self.net_lighting_lv.bus)):
            if bus in lv_buses: continue
            if bus == 3:
                pp.create_line(self.net_lighting_lv, 3, 6, length_km=0.035, std_type='UGlight', name='Line Trafo520-Bus6')
                continue
            elif bus == 38 :
                pp.create_line(self.net_lighting_lv, 38, 4, length_km=0.035, std_type='UGlight', name='Line Bus38-Trafo521')
                pp.create_line(self.net_lighting_lv, 4,39, length_km=0.035, std_type='UGlight', name='Line Trafo521-Bus39')
                continue
            elif bus == 43: 
                pp.create_line(self.net_lighting_lv, 43, 5, length_km=0.035, std_type='UGlight', name='Line Bus43-Trafo518')
                pp.create_line(self.net_lighting_lv, 5, 44, length_km=0.035, std_type='UGlight', name='Line Trafo518-Bus44')
                continue
            elif bus == 51:
                pp.create_line(self.net_lighting_lv, 51, 3, length_km=0.035, std_type='UGlight', name='Line Bus51-Trafo520')
                continue
                
            pp.create_line(self.net_lighting_lv, bus, bus+1, length_km=0.035, std_type='UGlight', name='Line Bus%s-Bus%s'%(bus,bus+1))    
            
       #EV loads
        for  lp in range(self.lps): 
            pp.create_load(self.net_lighting_lv, np.random.randint(0,len(self.net_lighting_lv.bus)), p_mw= 0.0, q_mvar= 0.0, name='Lp_%s'%lp)
    
    def runpp(self):
        for t in range(len(self.totalLoad)):
            for lp in range(self.lps):
                self.net_lighting_lv.load[-self.lps:].iloc[lp,2] = self.totalLoad.iloc[t,lp]/1000 *0.95
                self.net_lighting_lv.load[-self.lps:].iloc[lp,3] = self.totalLoad.iloc[t,lp]/1000 * np.sin(np.arccos(0.95))
                for load in range(len(self.net_lighting_lv.trafo)): 
                    self.net_lighting_lv.load['p_mw'][load+46] = self.totalLoad['Trafo_Preload'][t]/1000 *0.95
                    self.net_lighting_lv.load['q_mvar'][load+46] = self.totalLoad['Trafo_Preload'][t]/1000 * np.sin(np.arccos(0.95))
            pp.runpp(self.net_lighting_lv)
            self.lineloading.iloc[t] = self.net_lighting_lv.res_line['loading_percent'].values 
            self.trafoloading.iloc[t] = self.net_lighting_lv.res_trafo['loading_percent'].values 
            self.busvoltage.iloc[t] = self.net_lighting_lv.res_bus['vm_pu'].values 
#        simple_plotly(self.net_lighting_lv)


#for t in range(len(net_lighting_lv.bus[net_lighting_lv.bus['name'].str.match('Bus4')])): 
#     net_lighting_lv.bus[net_lighting_lv.bus['name'].str.match('Bus4')]['vn_kv'][t] = 20
