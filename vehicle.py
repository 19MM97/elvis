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
    :param dis_battery_size: Distribution of the battery sizes according to the input file.
    :type dis_battery_size: list
    :param dis_soc: Distribution of the soc at the arrival time of the evs according to the input file.
    :type dis_soc: list
    :param dis_user_type: Distribution of the user types according to the input file. \
    Each user type is having a minimal and maximal parking time.
    :type dis_user_type: list
    :param soc_target: The SOC of the electric vehicle wants to have when leaving.
    :type soc_target: float

    :cvar arrival_time: The arrival time of the vehicle.
    :cvar car_id: Identifier of the car.
    :cvar parking_time: Parking time in hours.
    :cvar mode: Charging: 1 and discharging 0.
    :cvar battery_size: Battery capacity in kWh.
    :cvar time_start_xcharging: Time the charging/discharging begins.
    :cvar soc_min: SOC minimum (0 to 1). Can't be discharged below.
    :cvar power_min: Minimal power the car can charge or discharge.
    :cvar power_max: Maximal power the car can charge or discharge.
    :cvar eta_c: Charging efficiency (0 to 1).
    :cvar eta_d: Discharging efficiency (0 to 1.
    :cvar self_dis: Self-discharge of the battery in kW.
    :cvar requested_xcapacity: The requested power of the car in kW.
    :cvar xcharging_power: Power the vehicle is charging/discharging with per time step.
    :cvar soc: SOC of the vehicle.
    :cvar soc_target: SOC target to be fullfilled while parking time if possible.
    """
    def __init__(self, t, dis_battery_size=None, dis_soc=None, dis_user_type=None, soc_target=None):
        self.arrival_time = t
        self.car_id = 'ev' + str(self.arrival_time) + '_' + str(np.random.random_integers(0, 100000000, 1)[0])
        if dis_user_type is None:
            self.parking_time = 1
        else:
            user_size = []
            for ra in range(len(dis_user_type[1])):
                user_size.append(stats.truncnorm.rvs((dis_user_type[1][ra] - 40) / 10,
                                                     (dis_user_type[2][ra] - 40) / 10, loc=40, scale=10, size=1)[0])

            self.parking_time = np.random.choice(user_size, p=dis_user_type[4])

        self.mode = 1
        if dis_battery_size is None:
            self.battery_size = 60.0
        else:
            self.battery_size = np.random.choice(dis_battery_size[1], p=dis_battery_size[3])
        self.time_start_xcharging = None
        self.soc_min = 0.0
        self.power_min = 0.0
        self.power_max = 350.0
        self.eta_c = 1.0
        self.eta_d = 1.0
        self.self_dis = 0.0000001
        self.requested_xcapacity = self.power_max
        self.xcharging_power = 0.01
        if dis_soc is None:
            self.soc = 0.1
        else:
            self.soc = np.random.choice(dis_soc[0], p=dis_soc[2])
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
