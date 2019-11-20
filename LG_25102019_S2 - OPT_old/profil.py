# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 12:42:34 2019

@author: draz
"""

from events import generate_ev, generate_lp
from vehicle import Vehicle
from control import first_come_first_served, discrimination_free, control_with_battery
from optx import opt_charging
from data import preload, get_co2_emission, get_energy_price
import numpy as np 
from datetime import timedelta
from storage import Storage 
import time

get_energy_price (1440)


class ProfileChargingDemand: 
    
    def __init__(self, 
                 assumptions, numberOfLp, 
                 power_kw, 
                 disDay, disYear,
                 control,storageCapacity=None, co2_scenario=None,typeLP=None, 
                 disBatterysize = None, disSoc=None, disUserTyp=None, 
                 trafoPreload=None): 
        self.numberOfLp = numberOfLp
        self.power_kw = power_kw
        self.typeLP = None
        self.control = control
        self.disDay = disDay
        self.disYear = disYear
        self.disBatterysize = disBatterysize
        self.disSoc = disSoc 
        self.disUserTyp = disUserTyp
        self.simulationTime = assumptions['Simulation Zeit (Woche)']
        self.trafoPreload = trafoPreload
        self.co2_emission = None
        self.energy_price = None
        self.assumptions = assumptions
        self.connectedEVs = []
        self.arrivales = None
        self.tau = None
        self.chargingPoints = None
        self.storage = None
        self.storageCapacity = None
        self.servedEV = 0.0
        self.intailsValues(co2_scenario)
        
    def intailsValues(self,c): 
        self.typeLP = 'AC' if self.typeLP == None else 'DC'
        self.simulationTime = int(timedelta(weeks=1).total_seconds()//60) if self.simulationTime == None else self.simulationTime * 60 * 24 * 7
        self.tau = 1 if self.tau == None else self.tau
        self.simulationTime = self.simulationTime 
        self.control = 'UC' if self.control == None else self.control
        self.storage = Storage(self.simulationTime, self.storageCapacity) if self.control == 'WS' else None 
        if self.trafoPreload == None: self.trafoPreload = preload(self.assumptions, self.simulationTime, control=self.control)   
        if self.co2_emission == None and self.control == 'OPT': self.co2_emission = get_co2_emission(self.simulationTime)[c] 
        if self.energy_price == None and self.control == 'OPT': self.energy_price = get_energy_price(self.simulationTime) 
        
    def profileEvLoad(self, fix_key): 
        self.chargingPoints = generate_lp(self.numberOfLp, self.power_kw, self.simulationTime, self.control)
        arrivales, evQueue = generate_ev(self.control, self.disDay, self.disYear, self.simulationTime, fix_key)
        self.arrivales = arrivales if self.arrivales == None else self.arrivales 
        i = 0
        for t in range(0, self.simulationTime, self.tau):
            n = np.where(np.asanyarray(arrivales) == t)[0]
            if t == arrivales[i]: 
                for m in n:
                    if evQueue.full() == False: 
                        ev = Vehicle()
                        ev.initialize_values(t, dis_battery_size=self.disBatterysize, dis_soc=self.disSoc,
                                             dis_user_type=self.disUserTyp)
                        evQueue.put(ev)
                        i = i + 1 if arrivales[m] != arrivales[-1] else 0 
                    else:
                        i = i + 1 if arrivales[m] != arrivales[-1] else 0 
            if t <= self.assumptions['Open_hours'][0] * 60  + t//1440 * 1440  or t >= self.assumptions['Open_hours'][1] * 60  + t//1440 * 1440: 
                 for s in self.chargingPoints: 
#                     print(t,s.availability)
                     s.availability = 1.0
                     s.chargingPower = 0.0
                     s.connectedEV = None 
                 self.connectedEVs.append(0)   
                 continue
            for s in range (len(self.chargingPoints)):
                if self.chargingPoints[s].availability == 1 and evQueue.empty() == False: 
                    ev = evQueue.get()
                    self.chargingPoints[s].assign_ev(ev, t)
                    self.chargingPoints[s].connectedEV.initialize_values(t)
                    self.chargingPoints[s].connectedEV.chargingPower = self.chargingPoints[s].power_kw
                    self.servedEV = self.servedEV + 1
                    if self.control == 'OPT':
                        self.chargingPoints = opt_charging(t, self.trafoPreload, self.chargingPoints, self.assumptions,
                                                           self.co2_emission, self.energy_price)

            self.connectedEVs.append( len([ s.availability for s in self.chargingPoints if s.availability==0]))
            if self.control =='UC':
                chargingpower = self.power_kw
#                print(chargingpower)
            elif self.control == 'FD':
                chargingpower = discrimination_free(t, self.trafoPreload, self.connectedEVs[t])
#                print(chargingpower)         
            elif self.control == 'WS':
                available_from_Trafo, xchargingPower = control_with_battery(t, self.power_kw, self.trafoPreload, self.connectedEVs[t])
                self.storage.xchargingCapacity = xchargingPower
                self.storage.update_mode()
                self.storage.check_power()
                chargingpower = (available_from_Trafo - self.storage.xchargingCapacity)/self.connectedEVs[t] if self.connectedEVs[t] > 0 else 0.0
                self.storage.update_xcharge(t, self.tau)
                self.storage.loadProfile['LP_%s'%self.storage.batteryID][t] = self.storage.xchargingCapacity
                self.storage.loadProfile['SOC_%s'%self.storage.batteryID][t] = self.storage.soc
#            print(self.connectedEVs[t],';', chargingpower, ';', self.control, )
            for s in range(len(self.chargingPoints)):
                if self.control == 'FCFS':
                    chargingLoad = sum([s.loadProfile['LP_%s'%s.stationID][t] for s in self.chargingPoints])
                    chargingpower = first_come_first_served(t, chargingLoad, self.trafoPreload)
                if self.chargingPoints[s].availability == 0: 
                    self.chargingPoints[s].connectedEV.requestedXCapacity = self.chargingPoints[s].connectedEV.powerMax
                    self.chargingPoints[s].chargingPower = self.chargingPoints[s].connectedEV.requestedXCapacity
                    if self.control == 'OPT': 
                         self.chargingPoints[s].chargingPower = self.chargingPoints[s].chargingPlan[t]
                    else:
                         self.chargingPoints[s].chargingPower =  chargingpower
                    self.chargingPoints[s].check_power()
                    self.chargingPoints[s].connectedEV.confirmedXCapacity = self.chargingPoints[s].chargingPower
                    self.chargingPoints[s].connectedEV.check_power()
                    self.chargingPoints[s].connectedEV.timeStartXchaging = self.chargingPoints[s].timeStartXchaging
                    self.chargingPoints[s].connectedEV.update_xcharge(self.tau)
#                    print(self.connectedEVs[t],';', self.chargingPoints[s].connectedEV.confirmedXCapacity)
                    self.chargingPoints[s].loadProfile['LP_%s'%self.chargingPoints[s].stationID][t] = self.chargingPoints[s].connectedEV.confirmedXCapacity
                    self.chargingPoints[s].occupancy['LP_%s'%self.chargingPoints[s].stationID] [t] = 1.0
                    self.chargingPoints[s].update_availability(t)


                
#                self.chargingPoints[s].sationData()

            