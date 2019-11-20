# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 12:42:34 2019

@author: draz
"""

from events import generate_ev, generate_lp
from vehicle import Vehicle
from control import first_come_first_served, discrimination_free, control_with_battery
from optx import opt_charging
from data import preload, get_co2_emission, get_energy_price
import numpy as np
from datetime import timedelta
from storage import Storage
# import time

get_energy_price(1440)


class ProfileChargingDemand:

    def __init__(self,
                 assumptions, number_of_lp,
                 power_kw,
                 dis_day, dis_year,
                 control, storage_capacity=None, co2_scenario=None, type_lp=None,
                 dis_battery_size=None, dis_soc=None, dis_user_type=None,
                 trafo_preload=None):
        self.numberOfLp = number_of_lp
        self.powerKw = power_kw
        self.typeLP = type_lp
        self.control = control
        self.disDay = dis_day
        self.disYear = dis_year
        self.disBatterysize = dis_battery_size
        self.disSoc = dis_soc
        self.disUserTyp = dis_user_type
        self.simulationTime = assumptions['Simulation Zeit (Woche)']
        self.trafoPreload = trafo_preload
        self.co2Emission = None
        self.energyPrice = None
        self.assumptions = assumptions
        self.connectedEVs = []
        self.arrivals = None
        self.tau = None
        self.chargingPoints = None
        self.vehicles = {}
        self.storage = None
        self.storageCapacity = storage_capacity
        self.servedEV = 0.0
        self.initialize_values(co2_scenario)

    def initialize_values(self, c):

        self.simulationTime = int(timedelta(weeks=1).total_seconds()//60) \
            if self.simulationTime is None else self.simulationTime * 60 * 24 * 7
        self.tau = 1 if self.tau is None else self.tau
        self.simulationTime = self.simulationTime
        self.control = 'UC' if self.control is None else self.control
        self.storage = Storage(self.simulationTime, self.storageCapacity) if self.control == 'WS' else None
        if self.trafoPreload is None:
            self.trafoPreload = preload(self.simulationTime)
        if self.co2Emission is None:
            self.co2Emission = get_co2_emission(self.simulationTime)[c]
        if self.energyPrice is None:
            self.energyPrice = get_energy_price(self.simulationTime)

    def profile_ev_load(self, fix_key):

        self.chargingPoints = generate_lp(self.numberOfLp, self.powerKw, self.simulationTime, self.control)
        arrivals, ev_queue = generate_ev(self.disDay, self.disYear, self.simulationTime, fix_key)
        self.arrivals = arrivals if self.arrivals is None else self.arrivals
        i = 0

        for t in range(0, 1440, self.tau):
            n = np.where(np.asanyarray(arrivals) == t)[0]
            if t == arrivals[i]:
                for m in n:
                    if ev_queue.full() is False:
                        ev = Vehicle()
                        ev.initialize_values(t, dis_battery_size=self.disBatterysize, dis_soc=self.disSoc,
                                             dis_user_type=self.disUserTyp)
                        ev_queue.put(ev)
                        i += 1 if arrivals[m] != arrivals[-1] else 0
                    else:
                        i += 1 if arrivals[m] != arrivals[-1] else 0

            if t <= self.assumptions['Open_hours'][0] * 60 + t // 1440 * 1440 or \
                    t >= self.assumptions['Open_hours'][1] * 60 + t // 1440 * 1440:
                for s in self.chargingPoints:
                    s.availability = 1.0
                    s.charging_power = 0.0
                    s.connectedEV = None
                    with ev_queue.mutex:
                        ev_queue.queue.clear()

            for s in range(len(self.chargingPoints)):
                if self.chargingPoints[s].availability == 1 and not ev_queue.empty():
                    ev = ev_queue.get()
                    if t - ev.arrivalTime < min(ev.parkingTime,
                                                self.assumptions['Open_hours'][-1] -
                                                self.assumptions['Open_hours'][0]) * 60:
                        self.chargingPoints[s].assign_ev(ev, t)
                        self.chargingPoints[s].connectedEV.charging_power = self.chargingPoints[s].power_kw
                        self.servedEV += 1
                        self.vehicles.update({ev.carID: ev})
                        if self.control == 'OPT':
                            self.chargingPoints = opt_charging(t, self.trafoPreload, self.chargingPoints,
                                                               self.assumptions,
                                                               self.co2Emission, self.energyPrice)

            if self.control == 'UC':
                chargingpower = self.powerKw
#                print(chargingpower)
            self.connectedEVs.append(len([s.availability for s in self.chargingPoints if s.availability == 0]))
            if self.control == 'FD':
                chargingpower = discrimination_free(t, self.trafoPreload, self.connectedEVs[t])
#                print(chargingpower)
            if self.control == 'WS':
                available_from_trafo, x_charging_power = \
                    control_with_battery(t, self.powerKw, self.trafoPreload, self.connectedEVs[t])
                self.storage.x_charging_capacity = x_charging_power
                self.storage.update_mode()
                self.storage.check_power()
                self.storage.update_xcharge(self.tau)
                if self.connectedEVs[t] > 0:
                    chargingpower = (available_from_trafo - self.storage.x_charging_capacity) / self.connectedEVs[t]
                else:
                    chargingpower = 0.0

                self.storage.loadProfile['LP_%s' % self.storage.batteryID][t] = self.storage.x_charging_capacity
                self.storage.loadProfile['SOC_%s' % self.storage.batteryID][t] = self.storage.soc
                # print('Trafo power =======', available_from_trafo)
                # self.storage.storage_data()
            for s in range(len(self.chargingPoints)):
                if self.control == 'FCFS':
                    charging_load = sum([s.loadProfile['LP_%s' % s.stationID][t] for s in self.chargingPoints])
                    chargingpower = first_come_first_served(t, charging_load, self.trafoPreload)
                if self.chargingPoints[s].availability == 0:
                    self.chargingPoints[s].connectedEV.requestedXCapacity = self.chargingPoints[s].connectedEV.powerMax
                    self.chargingPoints[s].charging_power = self.chargingPoints[s].connectedEV.requestedXCapacity
                    if self.control == 'OPT':
                        self.chargingPoints[s].charging_power = self.chargingPoints[s].chargingPlan[t]
                    else:
                        self.chargingPoints[s].charging_power = chargingpower
                    self.chargingPoints[s].check_power()
                    self.chargingPoints[s].connectedEV.xchargingCapacity = self.chargingPoints[s].charging_power
                    self.chargingPoints[s].connectedEV.check_power()
                    self.chargingPoints[s].connectedEV.update_xcharge(tau=self.tau)
                    self.chargingPoints[s].charging_power = self.chargingPoints[s].connectedEV.xchargingCapacity
                    self.powerKw = self.chargingPoints[s].charging_power
                    self.chargingPoints[s].loadProfile['LP_%s' % self.chargingPoints[s].stationID][t] = \
                        self.chargingPoints[s].connectedEV.xchargingCapacity
                    self.chargingPoints[s].occupancy['LP_%s' % self.chargingPoints[s].stationID][t] = 1.0
                    self.vehicles.update({self.chargingPoints[s].connectedEV.carID: self.chargingPoints[s].connectedEV})
                    # self.chargingPoints[s].connectedEV.evData()
                    self.chargingPoints[s].update_availability(t)
                    if self.chargingPoints[s].availability == 1:
                        self.powerKw = self.chargingPoints[s].powerMax
                    else:
                        self.powerKw = self.powerKw
