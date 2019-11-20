# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 14:22:59 2019

@author: draz
"""


import numpy as np 
import pandas as pd


class Station:
    
    def __init__(self, power_kw, simulationTime, control): 
        self.location = None
        self.stationID = None
        self.typeLP = None
        self.power_kw = power_kw
        self.powerFactor = None 
        self.powerMin = None 
        self.powerMax = None 
        self.chargingPower = None
        self.availability = None 
        self.connectedEV = None
        self.timeStartXchaging = None 
        self.loadProfile = None
        self.control = control
        self.servedEVs = None
        self.occupancy = None
        self.chargingPlan = None
        self.intialValues (simulationTime)   
        
    def sationData(self):
        print ("station ID = ", self.stationID , ";",  
               "Charging Power = " , self.chargingPower, ";", 
               'ConnectedEV = ', self.connectedEV,';', 
               "Max. Power = " , self.powerMax, ";", 
               "availability = " , self.availability)
    
    def intialValues(self, simulationTime): 
        if self.typeLP == None: self.typeLP = 'AC'
        if self.chargingPower == None: self.chargingPower = 0.0
        if self.powerMax == None: self.powerMax = self.power_kw
        if self.availability == None: self.availability = 1
        if self.location == None: self.location = np.random.choice(['ST_', 'ST_', 'ST_'])
        if self.powerMin == None: self.powerMin = 0.001 
        if self.powerFactor == None: self.powerFactor = 1.0
        if self.stationID == None: self.stationID = self.location + str(np.random.randint(100, 1000))
        if self.loadProfile == None: 
            self.loadProfile = {'LP_%s'%self.stationID: [0 for v in range (simulationTime)]}
#            datetime = pd.date_range('2018-01-01', periods=simulationTime, freq='T') 
#            self.loadProfile['Time'] = datetime
#            self.loadProfile = self.loadProfile.set_index('Time') 
        if self.control == None: self.control = 'UC'
        self.servedEVs = 0 if self.servedEVs ==  None else self.servedEVs 
        if self.occupancy == None: 
            self.occupancy = {'LP_%s'%self.stationID: [0 for v in range (simulationTime)]}
#            datetime = pd.date_range('2018-01-01', periods=simulationTime, freq='T') 
#            self.occupancy['Time'] = datetime
#            self.occupancy = self.occupancy.set_index('Time') 
            
    def assignEv (self, ev = None, t = None):
         if ev == None: 
             self.availability = 1   
         else: 
             self.availability = 0
             self.connectedEV = ev 
             self.timeStartXchaging = t 
             self.servedEVs = self.servedEVs + 1
            
    def checkPower(self):
#        self.chargingPower = self.chargingPower if self.powerMin <= self.chargingPower <= self.powerMax else self.powerMin if self.chargingPower < self.powerMin else self.powerMax   
        if self.powerMin <= self.chargingPower <= self.powerMax:
            self.chargingPower = self.chargingPower
        else:
            if self.chargingPower < self.powerMin:
                self.chargingPower = self.powerMin
            else:
                self.chargingPower = self.powerMax  
        if self.typeLP == 'AC': 
            self.chargingPower = self.chargingPower 
        elif self.typeLP == 'DC': 
            self.chargingPower = self.chargingPower * self.powerFactor
        
    def updateAvailability(self, t = None):
        if t == None: 
            t = 0
        else:
            if t-self.connectedEV.timeStartXchaging > self.connectedEV.xchargingTime: 
               self.availability = 1
               self.connectedEV = None 
               self.timeStartXchaging = None 
    
    def updateChargingPlan(self, optimal_plan): 
        self.chargingPlan = optimal_plan


            
 
        

        
        
        
