# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 16:42:23 2019

@author: draz
"""
import numpy as np 
from scipy  import stats

class Vehicle:
    
    def __init__(self):
        self.carID = None
        self.arrivalTime = None
        self.parkingTime = None
        self.mode = None
        self.batterySize = None
        self.timeStartXchaging = None
        self.socMin = None
        self.powerMin = None  
        self.powerMax = None 
        self.eta_c = None 
        self.eta_d = None
        self.slef_dis = None
        self.requestedXCapacity = None
        self.confirmedXCapacity = None
        self.chargingPower = None
        self.soc = None
        self.xchargingTime = None
        self.socTarget = None
#        self.intialValues(t)
        
    def evData(self):
        print ("Car ID = ", self.carID, ";",  
               "SOC = ",  self.soc, ";",  
               "Battery Size = ", self.batterySize, ";", 
               "Parking Time = ", self.parkingTime, ";",  
               "Min. Power = ", self.powerMin, ";",  
               "Max. Power = ", self.powerMax, ";",  
               ";", 
               "Requested Capacity= ", self.requestedCapacity, ";", 
               "Received Capacity= ", self.receivedCapacity, ";", 
               "Estimated Charging Time= ", self.xchargingTime)
        
    def intialValues(self,t , m, disBatterysize=None, disSoc=None, disUserTyp=None, socTarget=None):
        if disBatterysize is None: 
            self.batterySize = 60.0 
        else: 
            self.batterySize = np.random.choice(disBatterysize[1], 
                                                p=disBatterysize[3])
        if disSoc is None: 
            self.soc = 0.1
        else: 
            self.soc = np.random.choice(disSoc[0], 
                                        p = disSoc[2])  
        if socTarget is None:
            self.socTarget = 1.0 
        else:  self.socTarget = socTarget
        if disUserTyp is None: 
            self.parkingTime = 1
        else: 
            Usersize=[]
            for ra in range(len(disUserTyp[1])):
#                Usersize.append(np.random.uniform(disUserType['Von [Std]'][ra], 
#                                                  disUserType['Bis [Std]'][ra]))
                 Usersize.append(stats.truncnorm.rvs((disUserTyp[1][ra]-40)/10, 
                                                  (disUserTyp[2][ra]-40)/10, loc=40, scale=10, size=1)[0])   
            self.parkingTime = np.random.choice(Usersize, 
                                                p=disUserTyp[4])
        if self.arrivalTime == None: self.arrivalTime = t
        if self.carID == None: self.carID = 'ev' + str(self.arrivalTime) + '_' + str(m)
        if self.mode == None: self.mode = 1
        if self.batterySize == None: self.batterySize = 60.0 
        if self.socMin == None: self.socMin = 0.0
        if self.soc == None: self.soc = 0.1
        if self.powerMin == None: self.powerMin = 0.0 
        if self.powerMax == None: self.powerMax = 350.0
        if self.requestedXCapacity == None: self.requestedXCapacity = self.powerMax
        if self.confirmedXCapacity == None: self.confirmedXCapacity = 0.01
        if self.slef_dis == None: self.slef_dis = 0.001
        if self.eta_c == None: self.eta_c = 1.0 
        if self.eta_d == None: self.eta_d = 1.0

    def checkPower(self):        
        if self.powerMin <= self.confirmedXCapacity <= self.powerMax: 
            self.confirmedXCapacity = self.confirmedXCapacity
        elif self.confirmedXCapacity < self.powerMin: 
            self.confirmedXCapacity = 0.0
        elif self.confirmedXCapacity > self.powerMax: 
            self.confirmedXCapacity = self.powerMax
        
    def updateXcharge(self, tau): 
        e_b_kwh = self.mode * (1-self.soc) * (1-self.slef_dis) * self.batterySize 
        e_b_kwh = e_b_kwh * self.eta_c if self.mode == 1 else e_b_kwh / self.eta_d       
        e_p_kwh = self.mode * self.parkingTime * self.confirmedXCapacity * (1-self.slef_dis) 
        e_p_kwh = e_p_kwh * self.eta_c if self.mode == 1 else e_p_kwh / self.eta_d         
        e_x_kwh = e_b_kwh  if e_p_kwh >= e_b_kwh  else e_p_kwh
        
        self.xchargingTime = e_x_kwh / self.confirmedXCapacity * 60        
        self.soc = (self.batterySize - e_b_kwh + self.confirmedXCapacity*tau/60.0) / self.batterySize
        self.confirmedXCapacity = self.slef_dis * self.soc *self.batterySize if 1.0 <= self.soc <= self.socMin else self.confirmedXCapacity
  
    

        
              
