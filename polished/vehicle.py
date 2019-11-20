# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 16:42:23 2019

@author: draz
"""
import numpy as np 
from scipy import stats


class Vehicle:
    
    def __init__(self):
        self.carID = None
        self.arrivalTime = None
        self.parkingTime = None
        self.mode = None
        self.batterySize = None
        self.timeStartXcharging = None
        self.socMin = None
        self.powerMin = None  
        self.powerMax = None 
        self.eta_c = None 
        self.eta_d = None
        self.self_dis = None
        self.requestedXCapacity = None
        self.xchargingCapacity = None
        self.charging_power = None
        self.soc = None
        self.xchargingTime = None
        self.socTarget = None
#        self.intialValues(t)
        
    def ev_data(self):
        print("Car ID = ", self.carID, ";",
              "SOC = ", self.soc, ";",
              "Battery Size = ", self.batterySize, ";",
              "Parking Time = ", self.parkingTime, ";",
              "arrivalTime = ", self.arrivalTime, ";",
              "timeStartXchaging = ", self.timeStartXcharging, ";",
              "Min. Power = ", self.powerMin, ";",
              "Max. Power = ", self.powerMax, ";",
              ";",
              "Requested Capacity= ", self.requestedXCapacity, ";",
              "Received Capacity= ", self.xchargingCapacity, ";",
              "Estimated Charging Time= ", self.xchargingTime,
              "Started Xcharging at: ", self.timeStartXcharging)
        
    def initialize_values(self, t, dis_battery_size=None, dis_soc=None, dis_user_type=None, soc_target=None):
        if dis_battery_size is None:
            self.batterySize = 60.0 
        else: 
            self.batterySize = np.random.choice(dis_battery_size[1],
                                                p=dis_battery_size[3])
        if dis_soc is None:
            self.soc = 0.1
        else: 
            self.soc = np.random.choice(dis_soc[0],
                                        p=dis_soc[2])
        if soc_target is None:
            self.socTarget = 1.0 
        else:
            self.socTarget = soc_target
        if dis_user_type is None:
            self.parkingTime = 1
        else: 
            user_size = []
            for ra in range(len(dis_user_type[1])):
                user_size.append(stats.truncnorm.rvs((dis_user_type[1][ra] - 40) / 10,
                                                     (dis_user_type[2][ra] - 40) / 10, loc=40, scale=10, size=1)[0])
            self.parkingTime = np.random.choice(user_size,
                                                p=dis_user_type[4])
        if self.arrivalTime is None:
            self.arrivalTime = t
        if self.carID is None:
            self.carID = 'ev' + str(self.arrivalTime) + '_' + str(np.random.random_integers(0, 100000000, 1)[0])
        if self.mode is None:
            self.mode = 1
        if self.batterySize is None:
            self.batterySize = 60.0
        if self.socMin is None:
            self.socMin = 0.0
        if self.soc is None:
            self.soc = 0.1
        if self.powerMin is None:
            self.powerMin = 0.0
        if self.powerMax is None:
            self.powerMax = 350.0
        if self.requestedXCapacity is None:
            self.requestedXCapacity = self.powerMax
        if self.xchargingCapacity is None:
            self.xchargingCapacity = 0.01
        if self.self_dis is None:
            self.self_dis = 0.0000001
        if self.eta_c is None:
            self.eta_c = 1.0
        if self.eta_d is None:
            self.eta_d = 1.0

    def xcharge_battery(self):
        if self.soc > 0.8 and self.mode == 1:
            self.xchargingCapacity = - 5 * self.xchargingCapacity * (self.soc - 1.0)
        if self.soc < 0.2 and self.mode == 0:
            self.xchargingCapacity = 5 * self.xchargingCapacity * self.soc
        else:
            self.xchargingCapacity = self.xchargingCapacity

    def check_power(self):
        if self.soc <= self.socMin and self.mode == 0 or self.soc >= 1.0 and self.mode == 1:
            self.xchargingCapacity = self.self_dis
        else:
            if self.powerMin <= self.xchargingCapacity <= self.powerMax:
                self.xcharge_battery()
            else:
                if self.xchargingCapacity < self.powerMin:
                    self.xchargingCapacity = self.powerMin
                    self.xcharge_battery()
                else:
                    if self.xchargingCapacity > self.powerMax:
                        self.xchargingCapacity = self.powerMax
                        self.xcharge_battery()

    def update_xcharge(self, tau):
        e_x_kwh = (self.mode - self.soc) * (1 - self.self_dis) * self.batterySize
        e_x_kwh = e_x_kwh / self.eta_c if self.mode == 1 else e_x_kwh / self.eta_d
        self.xchargingTime = abs(e_x_kwh / self.xchargingCapacity * 60)
        self.soc = (self.batterySize * self.mode - e_x_kwh + self.xchargingCapacity * tau / 60.0) / self.batterySize
        if 1.0 <= self.soc <= self.socMin:
            self.soc = self.soc
