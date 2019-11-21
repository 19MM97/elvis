# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 15:53:58 2019

@author: draz
"""

import scipy.interpolate as interpol
import math
import numpy as np
import pickle
import queue
from chargingpoint import ChargingPoint


def arr_interpol(dis_ev_arr, dis_year, simulation_time):
    """
    Generate arrival times based on data from the input file/ Assumptions.

    :param dis_ev_arr: Hourly arrival distribution for one week. \
    Values from 0 to 1, where 1 means maximum number of arrivals and 0 no arrivals.
    :type dis_ev_arr: list
    :param dis_year: Total amount of car arrivals over simulation time.
    :param dis_year: int
    :param simulation_time: Total simulation time based on chosen time step.
    :type simulation_time: int
    :return: Arrival times.
    :rtype: list
    """
    week_arrivals = []
    nod = 7
    noh = 24
    now = math.ceil(simulation_time // 60 // 24 / 7)
    y = np.array(dis_ev_arr)
    y = np.append([0], y)
    y = np.cumsum(y)
    y = y / y[-1]
    y[0] = 0
    x = np.arange(0, simulation_time + 60, 60)
    f = interpol.interp1d(y, x)

    for W in range(now):
        arrivals = f(np.random.rand((dis_year[W])))
        arrivals = np.sort(arrivals)
        arrivals = np.round(arrivals).astype(int)
        arrivals = arrivals.tolist()
        arrivals = [x + noh * 60 * W * nod for x in arrivals]
        week_arrivals = week_arrivals + arrivals
    print(week_arrivals)
    return week_arrivals


def fix_arrivals(dis_ev_arr, dis_year, simulation_time, fix_key):
    """ Call :mod:`events.arr_interpol` if fix_key is 0 otherwise use saved arrival times.

    :param dis_ev_arr: Hourly arrival distribution for one week. Values from 0 to 1, where 1 means maximum arrivals and\
    0 no arrivals.
    :type dis_ev_arr: list
    :param dis_year: Total amount of car arrivals within simulation time.
    :param dis_year: int
    :param simulation_time: Total simulation time based on chosen time step.
    :type simulation_time: int
    :param fix_key: 1 fixes the assumptions. 0 generates new assumptions every simulation.
    :type fix_key: int
    :return: Arrival times.
    :rtype: list
    """
    if fix_key == 1:
        week_arrivals = arr_interpol(dis_ev_arr, dis_year, simulation_time)
        arr_file = open('arr', 'wb')
        pickle.dump(week_arrivals, arr_file)
        arr_file.close()
    else: 
        arr_file = open('arr', 'rb')
        week_arrivals = pickle.load(arr_file)
        arr_file.close()

    return week_arrivals


def generate_ev(dis_ev_arr, dis_year, simulation_time, fix_key):
    """
    Generate arrival times and a queue for waiting electric vehicles.

    :param dis_ev_arr: Hourly arrival distribution for one week. Values from 0 to 1, where 1 means maximum arrivals and\
    0 no arrivals.
    :type dis_ev_arr: list
    :param dis_year: Total amount of car arrivals over simulation time.
    :type dis_year: int
    :param simulation_time: Total simulation time based on chosen time step.
    :type simulation_time: int
    :param fix_key: 1 fixes the assumptions. 0 generates new assumptions every simulation.
    :type fix_key: int
    :return: Arrival times and queue.
    """
    arrivals = fix_arrivals(dis_ev_arr, dis_year, simulation_time, fix_key)
    ev_queue = queue.Queue(maxsize=5)
    return arrivals, ev_queue


def generate_lp(n, power_kw, simulation_time, control):
    """
    Generate charging points based on assumptions.

    :param n: Amount of charging points.
    :type n: int
    :param power_kw: Specified power of charging points (Assumptions).
    :type power_kw: float
    :param simulation_time: Total simulation time based on chosen time step.
    :type simulation_time: int
    :param control: Control Strategy ('UC', 'FD', 'FCFS', 'WS', 'OPT')
    :type control: str
    :return: Charging points as instance of :class:`station`.
    :rtype: list
    """
    charging_points = []
    for s in range(n):
        charging_points.append(ChargingPoint(power_nominal=power_kw, simulation_time=simulation_time, control=control))

    return charging_points
