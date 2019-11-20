# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 15:53:58 2019

@author: draz
"""

import scipy.interpolate as interpol
import numpy as np 
import pickle
import math 
import queue
from station import Station


def arr_interpol(dis_day, dis_year, simulation_time):

    week_arrivals = []
    nod = 7
    noh = 24
    now = math.ceil(simulation_time // 60 // 24 / 7)
    y = np.array(dis_day)
    y = np.append([0], y)
    y = np.cumsum(y)
    y = y / y[-1]
    y[0] = 0
    x = np.arange(0, noh * nod * 60 + 60, 60)
    f = interpol.interp1d(y, x)

    for W in range(now):
        arrivals = f(np.random.rand((dis_year[W])))
        arrivals = np.sort(arrivals)
        arrivals = np.round(arrivals).astype(int)
        arrivals = arrivals.tolist()
        arrivals = [x + noh * 60.0 * W * nod for x in arrivals]
        week_arrivals = week_arrivals + arrivals

    return week_arrivals


def fix_arrivals(dis_day, dis_year, simulation_time, fix_key):

    if fix_key == 1:
        week_arrivals = arr_interpol(dis_day, dis_year, simulation_time)
        arr_file = open('arr', 'wb')
        pickle.dump(week_arrivals, arr_file)
        arr_file.close()
    else: 
        arr_file = open('arr', 'rb')
        week_arrivals = pickle.load(arr_file)
        arr_file.close()

    return week_arrivals


def generate_ev(dis_day, dis_year, simulation_time, fix_key):

    arrivals = fix_arrivals(dis_day, dis_year, simulation_time, fix_key)
    ev_queue = queue.Queue(maxsize=5)
    return arrivals, ev_queue


def generate_lp(n, power_kw, simulation_time, control):
    charging_points = []

    for s in range(n):
        charging_points.append(Station(power_kw=power_kw, simulation_time=simulation_time, control=control))

    return charging_points
