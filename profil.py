# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 12:42:34 2019

@author: draz
"""

from control import first_come_first_served, discrimination_free, control_with_battery
from data import preload, get_co2_emission, get_energy_price
from datetime import timedelta
from events import generate_ev, generate_lp
from optx import opt_charging
from storage import Storage
from vehicle import Vehicle
import numpy as np

# get_energy_price(1440)


class SimulationModel:
    """Simulation instance.

       :param assumptions: Containing all simulation configurations.
       :type assumptions: dict
       :param number_of_lp: Amount of charging points the charging infrastructure has.
       :type number_of_lp: int
       :param power_kw: Power of each charging point in kW.
       :type power_kw: float
       :param dis_ev_arr: Hourly arrival distribution for one week. Values from 0 to 1, where 1 means  \
       arrivals and 0 no arrivals.
       :type dis_ev_arr: list
       :param dis_year: Total amount of car arrivals over simulation time.
       :param dis_year: int
       :param control: Control Strategy ('UC', 'FD', 'FCFS', 'WS', 'OPT')
       :type control: str
       :param storage_capacity: Capacity of the storage (in kW).
       :type storage_capacity: float
       :param co2_scenario: Position of the CO2_Scenario in the scenario list in assumptions.
       :type co2_scenario: int
       :param dis_battery_size: Distribution of the battery sizes specified in the input file.
       :type dis_battery_size: list
       :param dis_soc: Distribution of the soc at the arrival time of the evs as specified in the input file.
       :type dis_soc: list
       :param dis_user_type: Distribution of the user types specified in the input file. Each user type is having a \
       minimal and maximal parking time.
       :type dis_user_type: list
       :param trafo_preload: Preload of the transformer the charging infrastructure is connected to.
       :type trafo_preload: float
        """

    def __init__(self,
                 assumptions, number_of_lp, power_kw, dis_ev_arr, dis_year,
                 control, storage_capacity=None, co2_scenario=None,
                 dis_battery_size=None, dis_soc=None, dis_user_type=None,
                 trafo_preload=None):

        self.number_of_lp = number_of_lp
        self.power_kw = power_kw
        self.type_lp = 'AC'
        self.control = 'UC' if control is None else control
        self.dis_ev_arr = dis_ev_arr
        self.dis_year = dis_year
        self.dis_battery_size = dis_battery_size
        self.dis_soc = dis_soc
        self.dis_user_type = dis_user_type

        if assumptions['Simulation_time_in_weeks'] is None:
            self.simulation_time = int(timedelta(weeks=1).total_seconds() // 60)
        else:
            self.simulation_time = assumptions['Simulation_time_in_weeks'] * 60 * 24 * 7
        if trafo_preload is None:
            self.trafo_preload = preload(self.simulation_time)

        self.co2_emission = get_co2_emission(self.simulation_time)[co2_scenario]
        self.energy_price = get_energy_price(self.simulation_time)
        self.assumptions = assumptions
        self.connected_evs = []
        self.arrivals = None
        self.tau = 1
        self.charging_points = None
        self.vehicles = {}
        self.storage_capacity = storage_capacity
        self.storage = Storage(self.simulation_time, self.storage_capacity) if self.control == 'WS' else None
        self.served_ev = 0.0

    def profile_ev_load(self, fix_key):
        """
        Generate charging points, and arrivals. Assign power to each charging point based on control strategy.

        :param fix_key: 1 fixes the assumptions. 0 generates new assumptions every simulation.
        :type fix_key: int
        """
        self.charging_points = generate_lp(self.number_of_lp, self.power_kw, self.simulation_time, self.control)
        arrivals, ev_queue = generate_ev(self.dis_ev_arr, self.dis_year, self.simulation_time, fix_key)
        self.arrivals = arrivals if self.arrivals is None else self.arrivals

        i = 0
        for t in range(0, self.simulation_time, self.tau):
            n = np.where(np.asanyarray(arrivals) == t)[0]
            if t == arrivals[i]:
                for m in n:
                    if ev_queue.full() is False:
                        ev = Vehicle(t, dis_battery_size=self.dis_battery_size, dis_soc=self.dis_soc,
                                     dis_user_type=self.dis_user_type)
                        ev_queue.put(ev)
                        i += 1 if arrivals[m] != arrivals[-1] else 0
                    else:
                        i += 1 if arrivals[m] != arrivals[-1] else 0

            # If t is outside opening hours disconnect all evs from the charging station and set charging power to 0
            if t <= self.assumptions['opening_hours'][0] * 60 + t // 1440 * 1440 or \
                    t >= self.assumptions['opening_hours'][1] * 60 + t // 1440 * 1440:
                for s in self.charging_points:
                    s.availability = 1.0
                    s.charging_power = 0.0
                    s.connected_ev = None
                    with ev_queue.mutex:
                        ev_queue.queue.clear()
            # Connect ev if possible
            for s in range(len(self.charging_points)):
                if self.charging_points[s].availability == 1 and not ev_queue.empty():
                    ev = ev_queue.get()
                    if t - ev.arrival_time < min(ev.parking_time,
                                                 self.assumptions['opening_hours'][-1] -
                                                 self.assumptions['opening_hours'][0]) * 60:
                        self.charging_points[s].assign_ev(ev, t)
                        self.charging_points[s].connected_ev.charging_power = self.charging_points[s].power_kw
                        self.served_ev += 1
                        self.vehicles.update({ev.car_id: ev})
                        if self.control == 'OPT':
                            self.charging_points = opt_charging(t, self.trafo_preload, self.charging_points,
                                                                self.assumptions,
                                                                self.co2_emission, self.energy_price)

            self.connected_evs.append(len([s.availability for s in self.charging_points if s.availability == 0]))

            # Assign power based on control strategy
            charging_power: float = 0.0
            if self.control == 'UC':
                charging_power = self.power_kw
            elif self.control == 'FD':
                charging_power = discrimination_free(t, self.trafo_preload, self.connected_evs[t])
            elif self.control == 'WS':
                available_from_trafo, xcharging_power = control_with_battery(t, self.power_kw, self.trafo_preload,
                                                                             self.connected_evs[t])

                self.storage.xcharging_capacity = xcharging_power
                self.storage.update_mode()
                self.storage.check_power()
                self.storage.update_xcharge(self.tau)

                if self.connected_evs[t] > 0:
                    charging_power = (available_from_trafo - self.storage.xcharging_capacity) / self.connected_evs[t]
                else:
                    charging_power = 0.0

                self.storage.load_profile['LP_%s' % self.storage.battery_id][t] = self.storage.xcharging_capacity
                self.storage.load_profile['SOC_%s' % self.storage.battery_id][t] = self.storage.soc

            for s in range(len(self.charging_points)):
                if self.control == 'FCFS':
                    charging_load = sum([s.load_profile['LP_%s' % s.station_id][t] for s in self.charging_points])
                    charging_power = first_come_first_served(t, charging_load, self.trafo_preload)

                if self.charging_points[s].availability == 0:
                    self.charging_points[s].connected_ev.requested_xcapacity = \
                        self.charging_points[s].connected_ev.power_max
                    self.charging_points[s].charging_power = self.charging_points[s].connected_ev.requested_xcapacity

                    if self.control == 'OPT':
                        self.charging_points[s].charging_power = self.charging_points[s].chargingPlan[t]
                    else:
                        self.charging_points[s].charging_power = charging_power

                    self.charging_points[s].check_power()
                    self.charging_points[s].connected_ev.xcharging_capacity = self.charging_points[s].charging_power
                    self.charging_points[s].connected_ev.check_power()
                    self.charging_points[s].connected_ev.update_xcharge(tau=self.tau)
                    self.charging_points[s].charging_power = self.charging_points[s].connected_ev.xcharging_capacity
                    self.power_kw = self.charging_points[s].charging_power
                    self.charging_points[s].load_profile['LP_%s' % self.charging_points[s].station_id][t] = \
                        self.charging_points[s].connected_ev.xcharging_capacity
                    self.charging_points[s].occupancy['LP_%s' % self.charging_points[s].station_id][t] = 1.0
                    self.vehicles.update(
                        {self.charging_points[s].connected_ev.car_id: self.charging_points[s].connected_ev})
                    self.charging_points[s].update_availability(t)

                    if self.charging_points[s].availability == 1:
                        self.power_kw = self.charging_points[s].power_max
                    else:
                        self.power_kw = self.power_kw
