# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 08:43:02 2019

@author: draz
"""
import numpy as np


class Storage:
    """"
    Represents the batteries used in the charging infrastructure.

    :param simulation_time: Current time step.
    :param storage_capacity: Storage capacity in kWh.
    """
    
    def __init__(self, simulation_time, storage_capacity):
        self.location = np.random.choice(['Kaufland', 'Prakhaus', 'Street'])
        self.battery_id = 'storage' + str(self.location)
        self.mode = 0
        self.battery_size = storage_capacity if storage_capacity is not None else 0.0
        self.soc_min = 0.01
        self.power_max = self.battery_size * 0.75
        self.power_min = - self.power_max
        self.eta_c = 1.0
        self.eta_d = 1.0
        self.self_dis = 0.0001
        self.xcharging_capacity = None
        self.soc = 0.5
        self.xcharging_time = None
        self.load_profile = {'LP_%s' % self.battery_id: [0] * simulation_time,
                             'SOC_%s' % self.battery_id: [0] * simulation_time}

    def storage_data(self):
        """
        Print out key values of the instance.
        """
        print('Storage ID = ', self.battery_id, ';',
              'xcharging_power', self.xcharging_capacity,
              'SOC = ', self.soc, ';',
              'Battery Size = ', self.battery_size, ';',
              'Min. Power = ', self.power_min, ';',
              'Max. Power = ', self.power_max, ';',
              'Mode = ', self.mode, ';',
              'Estimated Charging Time= ', self.xcharging_time)

    def xcharge_battery(self):
        """
        Determine the Xcharge power of the battery based on its current SOC and the power needed.
        """
        if self.soc > 0.8 and self.mode == 1:
            self.xcharging_capacity = - 5 * self.xcharging_capacity * (self.soc - 1.0)
        if self.soc < 0.2 and self.mode == 0:
            self.xcharging_capacity = 5 * self.xcharging_capacity * self.soc
        else:
            self.xcharging_capacity = self.xcharging_capacity
        
    def check_power(self):
        """
        Check if the SOC and the charging/discharging capacity are within the limits and Xcharge the battery.
        """
        if self.soc <= self.soc_min and self.mode == 0 or self.soc >= 1.0 and self.mode == 1:
            self.xcharging_capacity = self.self_dis
        else:
            if self.power_min <= self.xcharging_capacity <= self.power_max:
                self.xcharge_battery()
            else:
                if self.xcharging_capacity < self.power_min:
                    self.xcharging_capacity = self.power_min
                    self.xcharge_battery()
                else:
                    if self.xcharging_capacity > self.power_max:
                        self.xcharging_capacity = self.power_max
                        self.xcharge_battery()

    def update_xcharge(self, tau):
        """
        Update the battery SOC according to the power withing the time step. \
        Update the time period the battery can be Xcharged with the current power.

        :param tau: Length of one time step.
        :type tau: float
        """
        e_x_kwh = (self.mode - self.soc) * (1 - self.self_dis) * self.battery_size
        e_x_kwh = e_x_kwh / self.eta_c if self.mode == 1 else e_x_kwh / self.eta_d

        self.xcharging_time = abs(e_x_kwh / self.xcharging_capacity * 60)
        self.soc = (self.battery_size * self.mode - e_x_kwh + self.xcharging_capacity * tau / 60.0) / self.battery_size

        if 1.0 <= self.soc <= self.soc_min:
            self.soc = self.soc

    def update_mode(self):
        """
        Update the charging mode based on the power sign.
        """
        self.mode = 0 if self.xcharging_capacity < 0 else 1  # 0 discharging and 1 for charging
        
    def flip_mode(self):
        """
        Switch the charging mode.
        """
        self.mode = 0 if self.mode == 1 else 0
