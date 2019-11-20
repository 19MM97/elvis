# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 08:43:02 2019

@author: draz
"""
import numpy as np
import pandas as pd
import time 


class Storage:
    
    def __init__(self, simulationTime, storageCapacity): 
        self.batteryID = None
        self.location = None
        self.mode = None
        self.batterySize = storageCapacity
        self.socMin = None
        self.powerMin = None  
        self.powerMax = None 
        self.eta_c = None 
        self.eta_d = None
        self.slef_dis = None
        self.xchargingCapacity = None 
        self.soc = None
        self.xchargingTime = None 
        self.loadProfile = None
        self.intialValues(simulationTime)
        
    def storage_data(self):
        print ("Storage ID = ", self.batteryID, ";",  
               "SOC = ",  self.soc, ";",  
               "Battery Size = ", self.batterySize, ";", 
               "Parking Time = ", self.parkingTime, ";",  
               "Min. Power = ", self.powerMin, ";",  
               "Max. Power = ", self.powerMax, ";",  
               ";", 
               "Requested Capacity= ", self.requestedXCapacity, ";", 
               "Received Capacity= " , self.xchargingCapacity, ";", 
               "Estimated Charging Time= ", self.chargingTime)
        
    def intialValues(self, simulationTime):
        if self.location == None: self.location = np.random.choice(['Kaufland', 'Prakhaus', 'Street'])
        if self.batteryID == None: self.batteryID = 'storage' + str(self.location)
        if self.mode == None: self.mode == 0
        self.batterySize = 150.0 if self.batterySize == None else self.batterySize #R1000-UPB4860 Gen2 54.4
        if self.socMin == None: self.socMin = 0.01
        if self.soc == None: self.soc = 0.5
        if self.powerMax == None: self.powerMax = self.batterySize * 0.75
        if self.powerMin == None: self.powerMin = - self.powerMax
        if self.xchargingCapacity == None: self.xchargingCapacity = 0.0
        if self.slef_dis == None: self.slef_dis = 0.0001
        if self.eta_c == None: self.eta_c = 1.0
        if self.eta_d == None: self.eta_d = 1.0
        if self.loadProfile == None: 
            self.loadProfile = {'LP_%s'%self.batteryID: [0 for v in range (simulationTime)], 'SOC_%s'%self.batteryID: [0 for v in range (simulationTime)]}
#            self.loadProfile = pd.DataFrame(0.0, index = range(simulationTime), columns = {'LP_%s'%self.batteryID, 'SOC_%s'%self.batteryID})
#            datetime = pd.date_range('2018-01-01', periods=simulationTime, freq='T') 
#            self.loadProfile['Time'] = datetime
#            self.loadProfile = self.loadProfile.set_index('Time') 
        
    def checkPower(self):
        if  self.soc <= self.socMin and self.mode == 0 or self.soc >= 1.0 and self.mode == 1:
            self.xchargingCapacity = self.slef_dis * self.soc * self.batterySize
        else:
            if self.powerMin <= self.xchargingCapacity <= self.powerMax: 
                self.xchargingCapacity = self.xchargingCapacity
            else:
                if self.xchargingCapacity < self.powerMin:
                    self.xchargingCapacity = self.powerMin
                else: 
                    if self.xchargingCapacity > self.powerMax:
                        self.xchargingCapacity = self.powerMax

            
        
        
    def updateXcharge(self, t, tau): 
        e_x_kwh = (self.mode-self.soc) * (1-self.slef_dis) * self.batterySize 
        e_x_kwh = e_x_kwh * self.eta_c if self.mode == 1 else e_x_kwh / self.eta_d 
        self.xchargingTime = abs(e_x_kwh / self.xchargingCapacity * 60)
        self.soc = (self.batterySize * self.mode - e_x_kwh + self.xchargingCapacity * tau/60.0) / self.batterySize
        if 1.0 <= self.soc <= self.socMin:
            self.soc = self.soc
        else:
            if self.soc > 1.0:
                self.soc = 1.0
            else: 
                if self.soc <= self.socMin:
                    self.soc = self.socMin

           
    def updateMode(self):
        self.mode  = 0 if self.xchargingCapacity < 0 else 1 #0 discharging and 1 for charging 
        
    def flipMode(self): 
        self.mode= 0 if self.mode ==1 else 0 

        
              