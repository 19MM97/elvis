# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 17:25:16 2019

@author: draz
"""


def discrimination_free(t, trafo_preload, n_ev, tr):
    """
    Define the charging power per charging point.

    :param t: Current time step.
    :type t: int
    :param trafo_preload: Time series data of the transformer preload.
    :type trafo_preload: list
    :param n_ev: Amount of connected vehicles.
    :type n_ev: int
    :type tr: Referring to the station in the grid model.
    :rtype tr: int
    :return: Power with which each charging point can charge.
    """
    limit = trafo_preload[3][t] * 0.8 - trafo_preload[tr][t]  # 0 for station 4.1, 1 for station 5.1 and 2 for new trafo
    power = limit / n_ev if n_ev > 0 else 0
    return power 


def first_come_first_served(t, connected_load, trafo_preload, tr):
    """
    Calculate the maximal charging power depending on the transformer pre-load \
    and the power of the other charging points.

    :param t: Current time step.
    :type t: int
    :param connected_load: Sum of the powers of the other charging points that are already assigned.
    :type connected_load: float
    :param trafo_preload: Time series data of the transformer preload and maximal load.
    :type trafo_preload: list
    :type tr: Referring to the station in the grid model.
    :rtype tr: int
    :return: Maximal possible charging power.
    """
    # trafo_preload[3] = maximal transformer load, trafo_preload[0] = current preload.
    return trafo_preload[3][t] * 0.8 - trafo_preload[tr][t] - connected_load


def control_with_battery(t, connected_load, trafo_preload, tr):
    """
    Calculate maximal power possible from the transformer and the sum of the power of all charging points with a
    connected vehicle.

    :param t: Current time step.
    :type t: int
    :param connected_load: Power of each charging point in kW.
    :type connected_load: float
    :param trafo_preload: Time series data of the transformer preload and maximal load.
    :type trafo_preload: list
    :type tr: Referring to the station in the grid model.
    :rtype tr: int
    :return: Maximal power possible from the transformer. \
             Sum of the powers of all charging points with connected vehicle.
    """
    limit = trafo_preload[3][t] * 0.8 - trafo_preload[tr][t]
    
    power_from_trafo = limit
    xcharging_power = limit - connected_load

    return power_from_trafo, xcharging_power
