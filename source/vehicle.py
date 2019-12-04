# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 16:42:23 2019

@author: draz
"""

from scipy import stats
import numpy as np


class Vehicle:
    """
    Represents all electric vehicles within the simulation.

    :param t: Current time step.
    :type t: int
    :param soc_target: The SOC of the electric vehicle wants to have when leaving.
    :type soc_target: float

    :cvar self.arrival_time: The arrival time of the vehicle.
    :cvar self.car_id: Identifier of the car.
    :cvar self.parking_time: Parking time in hours.
    :cvar self.mode: Charging: 1 and discharging 0.
    :cvar self.battery_size: Battery capacity in kWh.
    :cvar self.time_start_xcharging: Time the charging/discharging begins.
    :cvar self.soc_min: SOC minimum (0 to 1). Can't be discharged below.
    :cvar self.power_min: Minimal power the car can charge or discharge.
    :cvar self.power_max: Maximal power the car can charge or discharge.
    :cvar self.eta_c: Charging efficiency (0 to 1).
    :cvar self.eta_d: Discharging efficiency (0 to 1.
    :cvar self.self_dis: Self-discharge of the battery in kW.
    :cvar self.requested_xcapacity: The requested power of the car in kW.
    :cvar self.xcharging_power: Power the vehicle is charging/discharging with per time step.
    :cvar self.soc: SOC of the vehicle.
    :cvar self.soc_target: SOC target to be fullfilled while parking time if possible.
    """
    def __init__(self, t, data, soc_target=None):
        self.arrival_time = t
        self.car_id = 'ev' + str(self.arrival_time) + '_' + str(np.random.random_integers(0, 100000000, 1)[0])
        if data.dis_user_type is None:
            self.parking_time = 1
        else:
            user_size = []
            for ra in range(len(data.dis_user_type[1])):
                user_size.append(stats.truncnorm.rvs((data.dis_user_type[1][ra] - 40) / 10,
                                                     (data.dis_user_type[2][ra] - 40) / 10,
                                                     loc=40, scale=10, size=1)[0])

            self.parking_time = np.random.choice(user_size, p=data.dis_user_type[4])

        self.mode = 1
        if data.dis_battery_size is None:
            self.battery_size = 60.0
        else:
            self.battery_size = np.random.choice(data.dis_battery_size[1], p=data.dis_battery_size[3])
        self.time_start_xcharging = None
        self.soc_min = 0.0
        self.power_min = 0.0
        self.power_max = 350.0
        self.eta_c = 1.0
        self.eta_d = 1.0
        self.self_dis = 0.0000001
        self.requested_xcapacity = self.power_max
        self.xcharging_power = 0.0000001
        if data.dis_soc is None:
            self.soc = 0.1
        else:
            self.soc = np.random.choice(data.dis_soc[0], p=data.dis_soc[2])
        self.xcharging_time = None
        if soc_target is None:
            self.soc_target = 1.0
        else:
            self.soc_target = soc_target

    def ev_data(self):
        """Print vehicle data."""
        print('Car ID = ', self.car_id, ';',
              'SOC = ', self.soc, ';',
              'Battery Size = ', self.battery_size, ';',
              'Parking Time = ', self.parking_time, ';',
              'arrivalTime = ', self.arrival_time, ';',
              'timeStartXchaging = ', self.time_start_xcharging, ';',
              'Min. Power = ', self.power_min, ';',
              'Max. Power = ', self.power_max, ';', ';',
              'Requested Capacity= ', self.requested_xcapacity, ';',
              'Received Capacity= ', self.xcharging_power, ';',
              'Estimated Charging Time= ', self.xcharging_time,
              'Started Xcharging at: ', self.time_start_xcharging)

    def xcharge_battery(self):
        """
        Adjusting the charging/discharging capacity based on the current SOC of the vehicle.
        """
        if self.soc > 0.8 and self.mode == 1:
            self.xcharging_power = - 5 * self.xcharging_power * (self.soc - 1.0)
        if self.soc < 0.2 and self.mode == 0:
            self.xcharging_power = 5 * self.xcharging_power * self.soc
        else:
            self.xcharging_power = self.xcharging_power
        return self.xcharging_power

    def check_power(self):
        """
        Check if the SOC and the charging/discharging capacity is within the limits and Xcharge the battery.
        """
        if self.soc <= self.soc_min and self.mode == 0 or self.soc >= 1.0 and self.mode == 1:
            self.xcharging_power = self.self_dis
        else:
            if self.power_min <= self.xcharging_power <= self.power_max:
                self.xcharge_battery()
            else:
                if self.xcharging_power < self.power_min:
                    self.xcharging_power = self.power_min
                    self.xcharge_battery()
                else:
                    if self.xcharging_power > self.power_max:
                        self.xcharging_power = self.power_max
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

        self.xcharging_time = abs(e_x_kwh / self.xcharging_power * 60)
        self.soc = (self.battery_size * self.mode - e_x_kwh + self.xcharging_power * tau / 60.0) / self.battery_size

        if 1.0 <= self.soc <= self.soc_min:
            self.soc = self.soc
