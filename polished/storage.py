# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 08:43:02 2019

@author: draz
"""
import numpy as np


class Storage:
    
    def __init__(self, simulation_time, storage_capacity):
        self.batteryID = None
        self.location = None
        self.mode = None
        self.batterySize = storage_capacity
        self.socMin = None
        self.powerMin = None  
        self.powerMax = None 
        self.eta_c = None 
        self.eta_d = None
        self.self_dis = None
        self.x_charging_capacity = None
        self.soc = None
        self.xchargingTime = None 
        self.loadProfile = None
        self.initialize_values(simulation_time)
        
    def storage_data(self):
        print("Storage ID = ", self.batteryID, ";",
              "xcharging_power", self.x_charging_capacity,
              "SOC = ", self.soc, ";",
              "Battery Size = ", self.batterySize, ";",
              "Min. Power = ", self.powerMin, ";",
              "Max. Power = ", self.powerMax, ";",
              "Mode = ", self.mode, ";",
              "Estimated Charging Time= ", self.xchargingTime)
        
    def initialize_values(self, simulation_time):
        if self.location is None:
            self.location = np.random.choice(['Kaufland', 'Prakhaus', 'Street'])
        if self.batteryID is None:
            self.batteryID = 'storage' + str(self.location)
        if self.mode is None:
            self.mode = 0
        self.batterySize = 150.0 if self.batterySize is None else self.batterySize  # R1000-UPB4860 Gen2 54.4
        if self.socMin is None:
            self.socMin = 0.01
        if self.soc is None:
            self.soc = 0.5
        if self.powerMax is None:
            self.powerMax = self.batterySize * 0.75
        if self.powerMin is None:
            self.powerMin = - self.powerMax
        if self.x_charging_capacity is None:
            self.x_charging_capacity = None
        if self.self_dis is None:
            self.self_dis = 0.0001
        if self.eta_c is None:
            self.eta_c = 1.0
        if self.eta_d is None:
            self.eta_d = 1.0
        if self.loadProfile is None:
            self.loadProfile = {'LP_%s' % self.batteryID:
                                [0] * simulation_time, 'SOC_%s' % self.batteryID: [0] * simulation_time}

    def xcharge_battery(self):
        if self.soc > 0.8 and self.mode == 1:
            self.x_charging_capacity = - 5 * self.x_charging_capacity * (self.soc - 1.0)
        if self.soc < 0.2 and self.mode == 0:
            self.x_charging_capacity = 5 * self.x_charging_capacity * self.soc
        else:
            self.x_charging_capacity = self.x_charging_capacity
        
    def check_power(self):
        if self.soc <= self.socMin and self.mode == 0 or self.soc >= 1.0 and self.mode == 1:
            self.x_charging_capacity = self.self_dis
        else:
            if self.powerMin <= self.x_charging_capacity <= self.powerMax:
                self.xcharge_battery()
            else:
                if self.x_charging_capacity < self.powerMin:
                    self.x_charging_capacity = self.powerMin
                    self.xcharge_battery()
                else:
                    if self.x_charging_capacity > self.powerMax:
                        self.x_charging_capacity = self.powerMax
                        self.xcharge_battery()

    def update_xcharge(self, tau):
        e_x_kwh = (self.mode - self.soc) * (1 - self.self_dis) * self.batterySize
        e_x_kwh = e_x_kwh / self.eta_c if self.mode == 1 else e_x_kwh / self.eta_d
        self.xchargingTime = abs(e_x_kwh / self.x_charging_capacity * 60)
        self.soc = (self.batterySize * self.mode - e_x_kwh + self.x_charging_capacity * tau / 60.0) / self.batterySize
        if 1.0 <= self.soc <= self.socMin:
            self.soc = self.soc

    def update_mode(self):
        self.mode = 0 if self.x_charging_capacity < 0 else 1  # 0 discharging and 1 for charging
        
    def flip_mode(self):
        self.mode = 0 if self.mode == 1 else 0
