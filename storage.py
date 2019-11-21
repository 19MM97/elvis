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

    :cvar location: Longitude and latitude of the storage. Needs to be adjusted when data is available.
    :cvar battery_id: Identifier of the storage.
    :cvar mode: 0 for discharging, 1 for charging.
    :cvar soc_min: Minimal SOC of the battery, can't be discharged beyond.
    :cvar power_max: Maximum power for charging or discharging.
    :cvar power_min: Minimal power for charging or discharging.
    :cvar eta_c: Efficiency for charging.
    :cvar eta_d: Efficiency for discharging.
    :cvar self_dis: Self-discharge of the battery in kW.
    :cvar xcharging_capacity: Rename to xcharging_power. Power the system is charging or \
    discharging with in each time step.
    :cvar soc: State of charge of the battery (initialized with 0.5).
    :cvar xcharging_time: The time left until the battery is fully charged or discharged based on current power.
    :cvar load_profile: Time series data of the power.
    """
    
    def __init__(self, simulation_time, storage_capacity):
        self.location = 'longitude, latitude'
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
        Update the battery SOC according to the power within the time step. \
        Update the time period the battery can be Xcharged at the current power.

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
