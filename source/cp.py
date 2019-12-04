# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 14:22:59 2019

@author: draz
"""


import numpy as np


class ChargingPoint:
    """
       Represents the charging points.

       :param power_nominal: Power the station charges the vehicle with.
       :type power_nominal: float

       :cvar self.location: Location of the charging point/station. Needs to be adjusted when data can be provided.
       :cvar self.station_id: Identifier for each charging point.
       :cvar self.type_lp: DC or AC charging.
       :cvar self.power_nominal: Nominal power of the charging point.
       :cvar self.power_factor: Power factor (cos(phi)) of the grid.
       :cvar self.power_min: Minimal power the charging point can charge with.
       :cvar self.power_max: Maximal power the charging point can charge with.
       :cvar self.xcharging_power: The charging or discharging power for a specific time step.
       :cvar self.availability: Availability of the charging point (0 ev is connected, 1 no ev is connected).
       :cvar self.connected_ev: ID of the connected ev.
       :cvar self.time_start_xcharging: Time the charging/discharging starts.
       :cvar self.load_profile: Time series data of the charging power.
       :cvar self.control: Control type as per assumptions.
       :cvar self.served_evs: Counter for every connected ev that charged/discharged.
       :cvar self.occupancy: Time series data, 0 for charging point is available and 1 for charging point is used.
       :cvar self.charging plan: Day ahead plan for the charging schedule.
    """
    
    def __init__(self, data, power_nominal):
        self.location = str('latitude, longitude')
        self.station_id = self.location + str(np.random.randint(100, 1000))
        self.type_lp = 'AC'
        self.power_nominal = power_nominal
        self.power_factor = 1.0
        self.power_min = 0.0001
        self.power_max = self.power_nominal
        self.xcharging_power = 0.0
        self.availability = 1
        self.connected_ev = None
        self.time_start_xcharging = None
        self.load_profile = {'LP_%s' % self.station_id: [0] * data.total_simulation_time}
        self.served_evs = 0
        self.occupancy = {'LP_%s' % self.station_id: [0] * data.total_simulation_time}
        self.charging_plan = None

    def station_data(self, t=None):
        """
        Print out key values of the instance.

        :param t: Current time step.
        :type t: int
        """
        print('station ID = ', self.station_id, ';',
              'time = ', 'NA' if t is None else t,  ';',
              'xcharging power = ', self.xcharging_power, ';',
              'connectedEV_soc = ', self.connected_ev.soc if self.connected_ev is not None else "nan", ';',
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
        if self.power_min <= self.xcharging_power <= self.power_max:
            self.xcharging_power = self.xcharging_power
        else:
            if self.xcharging_power < self.power_min:
                self.xcharging_power = self.power_min
            else:
                self.xcharging_power = self.power_max
        if self.type_lp == 'AC':
            self.xcharging_power = self.xcharging_power
        elif self.type_lp == 'DC':
            self.xcharging_power = self.xcharging_power * self.power_factor
        
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
            self.xcharging_power = 0.0
