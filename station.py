# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 14:22:59 2019

@author: draz
"""


import numpy as np


class Station:
    
    def __init__(self, power_kw, simulation_time, control):
        """
        Represents the charging points.
        :param power_kw: Power the station charges the vehicle with.
        :type power_kw: float
        :param simulation_time: Total length of the simulation time.
        :type simulation_time: int
        :param control: Control type as per assumptions.
        :type control: str
        """
        self.location = np.random.choice(['ST_', 'ST_', 'ST_'])
        self.station_id = self.location + str(np.random.randint(100, 1000))
        self.type_lp = 'AC'
        self.power_kw = power_kw
        self.power_factor = 1.0
        self.power_min = 0.0001
        self.power_max = self.power_kw
        self.charging_power = 0.0
        self.availability = 1
        self.connected_ev = None
        self.time_start_xcharging = None
        self.load_profile = {'LP_%s' % self.station_id: [0] * simulation_time}
        self.control = control if control is not None else 'UC'
        self.served_evs = 0
        self.occupancy = {'LP_%s' % self.station_id: [0] * simulation_time}
        self.charging_plan = None

    def station_data(self, t=None):
        """
        Print out key values of the instance.
        :param t: Current time step.
        :type t: int
        """
        print('station ID = ', self.station_id, ';',
              'time = ', 'NA' if t is None else t,  ';',
              'charging power = ', self.charging_power, ';',
              'connectedEV = ', self.connected_ev, ';',
              'max. Power = ', self.power_max, ';',
              'availability = ', self.availability)
            
    def assign_ev(self, ev=None, t=None):
        """
        Dock vehicle to the station.
        :param ev: Instance of the :class:`vehicle`
        :param t: Current time step.
        :type t: int
        """
        if ev is None:
            self.availability = 1
        else:
            ev.time_start_xcharging = t
            self.availability = 0
            self.connected_ev = ev
            self.time_start_xcharging = t
            self.served_evs = self.served_evs + 1
            
    def check_power(self):
        """
        Check if the charging power is within its limits and assign accordingly.
        """
        if self.power_min <= self.charging_power <= self.power_max:
            self.charging_power = self.charging_power
        else:
            if self.charging_power < self.power_min:
                self.charging_power = self.power_min
            else:
                self.charging_power = self.power_max
        if self.type_lp == 'AC':
            self.charging_power = self.charging_power
        elif self.type_lp == 'DC':
            self.charging_power = self.charging_power * self.power_factor
        
    def update_availability(self, t=None):
        """
        Disconnect the vehicle if the parking time is over.
        :param t: Current time step.
        :type t: int
        """
        if t is not None and t - self.connected_ev.arrival_time >= self.connected_ev.parking_time * 60:
            self.availability = 1
            self.connected_ev = None
            self.time_start_xcharging = None
            self.power_kw = self.power_max
