# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 12:42:34 2019

@author: draz
"""

from control import first_come_first_served, discrimination_free, control_with_battery
from events import generate_ev, generate_lp
from optx import opt_charging
from storage import Storage
from vehicle import Vehicle
import numpy as np
import time


class SimulationModel:
    """
        Simulation instance.

        :param data: Data model from :class:`Daten`.

        :cvar self.number_of_lp: Number of charging points for the simulation.
        :cvar self.power_nominal: Nominal power of the charging points.
        :cvar self.type_lp: AC or DC charging for the charging points.
        :cvar self.connected_evs: Time series data with the amount of connected vehicles for every time step.
        :cvar self.arrivals: List of all times a car arrives.
        :cvar self.tau: Length of a time step in minutes.
        :cvar self.charging_points: List containing all charging points as instances of :class:`chargingpoint`.
        :cvar self.vehicles: Dictionary containing all connected ev IDs with their instance of :class:`vehicle`.
        :cvar self.storage_capacity: Capacity of the battery of the station in kWh.
        :cvar self.storage: Instance of :class:`storage`.
        :cvar self.served_ev: Counter of all vehicles connected and charged.
    """

    def __init__(self, data):

        self.number_of_lp = data.amount_cp
        self.power_nominal = data.power_cp
        self.xcharging_power = self.power_nominal
        self.type_lp = 'AC'

        self.connected_evs = []
        self.arrivals = None
        self.tau = 1
        self.charging_points = None
        self.vehicles = {}
        self.storage_capacity = data.storage_capacity
        self.storage = Storage(data.total_simulation_time, self.storage_capacity) if data.control == 'WS' else None
        self.served_ev = 0.0

    def profile_ev_load(self, fix_key, data):
        """
        Generate charging points, and arrivals. Assign power to each charging point based on control strategy.

        :param data: Data model from class :class:
        :param fix_key: 1 fixes the assumptions. 0 generates new assumptions every simulation.
        :type fix_key: int
        """
        self.charging_points = generate_lp(self.number_of_lp, self.power_nominal, data)
        arrivals, ev_queue = generate_ev(data.dis_ev_arr, data.dis_year, data.total_simulation_time, fix_key)
        self.arrivals = arrivals if self.arrivals is None else self.arrivals

        i = 0
        for t in range(0, data.total_simulation_time, self.tau):
            n = np.where(np.asanyarray(arrivals) == t)[0]
            if t == arrivals[i]:
                for m in n:
                    if ev_queue.full() is False:
                        ev = Vehicle(t, data)
                        ev_queue.put(ev)
                        i += 1 if arrivals[m] != arrivals[-1] else 0
                    else:
                        i += 1 if arrivals[m] != arrivals[-1] else 0

            # If t is outside opening hours disconnect all evs from the charging station and set charging power to 0
            if t <= data.user_assumptions['opening_hours'][0] * 60 + t // 1440 * 1440 or \
                    t >= data.user_assumptions['opening_hours'][1] * 60 + t // 1440 * 1440:
                for s in self.charging_points:
                    s.availability = 1.0
                    s.xcharging_power = 0.0
                    s.connected_ev = None
                    with ev_queue.mutex:
                        ev_queue.queue.clear()
            # Connect ev if possible
            for s in range(len(self.charging_points)):
                if self.charging_points[s].availability == 1 and not ev_queue.empty():
                    ev = ev_queue.get()
                    if t - ev.arrival_time < min(ev.parking_time,
                                                 data.user_assumptions['opening_hours'][-1] -
                                                 data.user_assumptions['opening_hours'][0]) * 60:
                        self.charging_points[s].assign_ev(ev, t)
                        self.charging_points[s].connected_ev.xcharging_power = self.charging_points[s].power_nominal
                        self.served_ev += 1
                        self.vehicles.update({ev.car_id: ev})
                        if data.control == 'OPT':
                            self.charging_points = opt_charging(t, data.transformer_preload, self.charging_points,
                                                                data.user_assumptions,
                                                                data.co2_emission, data.energy_price)

            self.connected_evs.append(len([s.availability for s in self.charging_points if s.availability == 0]))
            connected_load = sum(
                [s.load_profile['LP_%s' % s.station_id][t-1] for s in self.charging_points])

            # Assign power based on control strategy
            xcharging_power: float = 0.0
            if data.control == 'UC':
                xcharging_power = self.power_nominal
            elif data.control == 'DF':
                xcharging_power = discrimination_free(t, data.transformer_preload, self.connected_evs[t],
                                                      data.user_assumptions['preload'])

            elif data.control == 'WS':
                available_from_trafo, xcharging_power = control_with_battery(t, connected_load,
                                                                             data.transformer_preload,
                                                                             data.user_assumptions['preload'])

                self.storage.xcharging_power = xcharging_power
                self.storage.update_mode()
                self.storage.check_power()
                self.storage.update_xcharge(self.tau)

                if self.connected_evs[t] > 0:
                   xcharging_power = (available_from_trafo - self.storage.xcharging_power) / self.connected_evs[t]
                else:
                   xcharging_power = 0.0

                self.storage.load_profile['LP_%s' % self.storage.battery_id][t] = self.storage.xcharging_power
                self.storage.load_profile['SOC_%s' % self.storage.battery_id][t] = self.storage.soc

            for s in range(len(self.charging_points)):
                if data.control == 'FCFS':
                    connected_load = sum([s.xcharging_power for s in self.charging_points])
                    xcharging_power = first_come_first_served(t, connected_load, data.transformer_preload,
                                                              data.user_assumptions['preload'])

                if self.charging_points[s].availability == 0:
                    if data.control == 'OPT':
                        self.charging_points[s].xcharging_power = self.charging_points[s].chargingPlan[t]
                    else:
                        self.charging_points[s].xcharging_power = xcharging_power
                    self.charging_points[s].check_power()
                    self.charging_points[s].connected_ev.xcharging_power = self.charging_points[s].xcharging_power
                    self.charging_points[s].connected_ev.check_power()
                    self.charging_points[s].connected_ev.update_xcharge(self.tau)
                    self.charging_points[s].xcharging_power = self.charging_points[s].connected_ev.xcharging_power
                    self.xcharging_power = self.charging_points[s].xcharging_power
                    self.charging_points[s].load_profile['LP_%s' % self.charging_points[s].station_id][t] = \
                        self.charging_points[s].connected_ev.xcharging_power
                    # self.charging_points[s].station_data(t)
                    # time.sleep(0.5)
                    self.charging_points[s].occupancy['LP_%s' % self.charging_points[s].station_id][t] = 1.0
                    self.vehicles.update(
                        {self.charging_points[s].connected_ev.car_id: self.charging_points[s].connected_ev})
                    self.charging_points[s].update_availability(t)
