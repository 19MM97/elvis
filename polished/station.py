# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 14:22:59 2019

@author: draz
"""


import numpy as np 
# import pandas as pd


class Station:
    
    def __init__(self, power_kw, simulation_time, control):
        self.location = None
        self.stationID = None
        self.type_lp = None
        self.power_kw = power_kw
        self.powerFactor = None 
        self.powerMin = None 
        self.powerMax = None 
        self.charging_power = None
        self.availability = None 
        self.connectedEV = None
        self.timeStartXchaging = None 
        self.loadProfile = None
        self.control = control
        self.servedEVs = None
        self.occupancy = None
        self.chargingPlan = None
        self.initialize_values(simulation_time)
        
    def station_data(self, t=None):
        print("station ID = ", self.stationID, ";",
              "time = ", 'NA' if t is None else t,  ";",
              "charging power = ", self.charging_power, ";",
              'connectedEV = ', self.connectedEV, ';',
              "max. Power = ", self.powerMax, ";",
              "availability = ", self.availability)
    
    def initialize_values(self, simulation_time):
        if self.type_lp is None:
            self.type_lp = 'AC'
        if self.charging_power is None:
            self.charging_power = 0.0
        if self.powerMax is None:
            self.powerMax = self.power_kw
        if self.availability is None:
            self.availability = 1
        if self.location is None:
            self.location = np.random.choice(['ST_', 'ST_', 'ST_'])
        if self.powerMin is None:
            self.powerMin = 0.0001
        if self.powerFactor is None:
            self.powerFactor = 1.0
        if self.stationID is None:
            self.stationID = self.location + str(np.random.randint(100, 1000))
        if self.loadProfile is None:
            self.loadProfile = {'LP_%s' % self.stationID: [0] * simulation_time}
#            datetime = pd.date_range('2018-01-01', periods=simulationTime, freq='T') 
#            self.loadProfile['Time'] = datetime
#            self.loadProfile = self.loadProfile.set_index('Time') 
        if self.control is None:
            self.control = 'UC'
        self.servedEVs = 0 if self.servedEVs is None else self.servedEVs
        if self.occupancy is None:
            self.occupancy = {'LP_%s' % self.stationID: [0] * simulation_time}
#            datetime = pd.date_range('2018-01-01', periods=simulationTime, freq='T') 
#            self.occupancy['Time'] = datetime
#            self.occupancy = self.occupancy.set_index('Time') 
            
    def assign_ev(self, ev=None, t=None):
        if ev is None:
            self.availability = 1
        else:
            ev.timeStartXcharging = t
            self.availability = 0
            self.connectedEV = ev
            self.timeStartXchaging = t
            self.servedEVs = self.servedEVs + 1
            
    def check_power(self):
        if self.powerMin <= self.charging_power <= self.powerMax:
            self.charging_power = self.charging_power
        else:
            if self.charging_power < self.powerMin:
                self.charging_power = self.powerMin
            else:
                self.charging_power = self.powerMax
        if self.type_lp == 'AC':
            self.charging_power = self.charging_power
        elif self.type_lp == 'DC':
            self.charging_power = self.charging_power * self.powerFactor
        
    def update_availability(self, t=None):
        if t is not None and t - self.connectedEV.arrivalTime >= self.connectedEV.parkingTime * 60:
            self.availability = 1
            self.connectedEV = None
            self.timeStartXchaging = None
            self.power_kw = self.powerMax
