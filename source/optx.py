# -*- coding: utf-8 -*-
"""
Created on Fri Oct  18 13:17:14 2019

@author: draz
"""

import pyomo.environ as aml
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pandas as pd


def opt_charging(t, trafo_preload, charging_points, assumptions, co2_emission, energy_price):
    """
    Linear optimization model for the charging strategy (if control='OPT').

    :param t: Current time step.
    :type t: int
    :param trafo_preload: Transformer preload.
    :type trafo_preload: list
    :param charging_points: Instances from :class:`chargingpoint`.
    :type charging_points: list
    :param assumptions: Simulation configurations.
    :type assumptions: dict
    :param co2_emission: CO2 emissions for the simulation period in kg CO2e/kWh.
    :type co2_emission: list
    :param energy_price: Energy prices for the simulation period in €/MWh.
    :type energy_price: list
    :return: Return charging points (:class:`chargingpoint`) with an updated day ahead charging plan.
    :rtype: list
    """
    tau = 1  # time resolution in minutes 
    hours = list(range(t, (t//1440) * 1440 + assumptions['opening_hours'][-1] * 60//tau))
    power_base = 100.0 
    energy_price_base = 0.3
    co2_emission_base = 0.5

    evs = [s.connected_ev for s in charging_points if s.availability == 0]
    data = [ev.__dict__ for ev in evs]

    data.append({'energy_price': [energy_price[hour] / 1000.0 for hour in hours],
                 'breaker_limit': [trafo_preload[3][hour] * 0.8 -
                                   trafo_preload[assumptions['preload']][hour] for hour in hours],
                 'co2_emissions': [co2_emission[hour] for hour in hours]
                 })
    ev_set = [ev.car_id for ev in evs]
    ev_param = list(data[0].keys())
    grid_param = list(data[-1].keys())

    # Model
    model = ConcreteModel()

    # Sets
    model.EVs = Set(initialize=ev_set)
    model.time = Set(initialize=hours)

    # Parameters
    for parameter in ev_param:
        setattr(model, parameter, Param(model.EVs, initialize={ev_set[i]: data[i][parameter] for i in range(len(ev_set))
                                                               },
                                        mutable=True, doc=parameter))
    for parameter in grid_param:
        setattr(model, parameter, Param(model.time, initialize={hours[hour]: data[-1][parameter][hour]
                                                                for hour in range(len(hours))},
                                        mutable=True, doc=parameter))

    soc = {}
    for ev in model.EVs:
        for time in model.time:
            soc[time, ev] = data[ev_set.index(ev)]['soc']

    def soc_limits_rule(model_in, i, j):
        return 0, 1

    model.soc_temp = Param(model.time, model.EVs, mutable=True, initialize=soc, default=0, rule=soc_limits_rule)

    def update_xcharge(model_in,i, tau):
        """
        Update the battery SOC according to the power within the time step. \
        Update the time period the battery can be Xcharged at the current power.

        :param tau: Length of one time step.
        :type tau: float
        """
        e_x_kwh = (model_in.mode[i] - model_in.soc_temp[i]) * (1 - model_in.self_dis[i]) * model_in.battery_size[i]
        e_x_kwh = e_x_kwh / model_in.eta_c[i] if model_in.mode[i] == 1 else e_x_kwh / model_in.eta_d[i]

        model_in.xcharging_time[i] = abs(e_x_kwh / model_in.xcharging_power[i] * 60)
        model_in.soc_temp[i] = (model_in.battery_size[i] * model_in.mode[i] -
                                e_x_kwh + model_in.xcharging_power[i] * tau / 60.0) / model_in.battery_size[i]


    def xcharge_battery(model_in,i):
        """
        Adjusting the charging/discharging capacity based on the current SOC of the vehicle.
        """
        model_in.xcharging_power[i] = aml.Expr_if(model_in.soc_temp[i] > 0.8,
                                                  - 5 * model_in.xcharging_power[i] * (model_in.soc_temp[i]
                                                  - 1.0), aml.Expr_if(model_in.soc_temp[i] < 0.2, 5 *
                                                  model_in.xcharging_power[i] *
                                                  model_in.soc_temp[i], model_in.xcharging_power[i]))

    def power_bounds_rule(model_in, i, j):
        """
        Define power limits for each car.

        :param model_in: Pyomo optimization model_in.
        :param i: Model instance index.
        :type i: int
        :return: Upper and lower power limits for the charging power.
        """
        return model_in.power_min[j], model_in.xcharging_power[j]

    model.power = Var(model.time, model.EVs, bounds=power_bounds_rule)

    # def adjust_soc(model_in, i, j):
    #     return model_in.soc_temp[i, j] == model_in.soc[j] + sum(model_in.power[time, j] for time in range(hours[0], i)) / \
    #                                    60 / model_in.battery_size[j]
    #
    # model.adjust_soc = Constraint(model.time, model.EVs, rule=adjust_soc)

    # Constraints
    def trafo_limit_rule(model_in, i):
        """
        Limit the total charging power to the maximal transformer load for each time step.

        :param model_in: Pyomo optimization model_in.
        :param j: Model instance index.
        :param j: int
        :return: Maximal charging power.
        """
        return sum(model_in.power[i, j] for j in model_in.EVs) <= model_in.breaker_limit[i]
    
    model.trafo_limit_rule = Constraint(model.time, rule=trafo_limit_rule)

    def demand_rule(model_in, i):
        """
        Adjust vehicle energy demand based on either parking time and maximal charging power or SOC target.

        :param model_in: Pyomo optimization model_in.
        :param i: Model instance index.
        :type i: int
        :return: Energy demand.
        """
        connection_time = min(data[ev_set.index(i)]['parking_time'], len(hours) / 60 * tau)
        return sum(
            model_in.power[j, i] for j in model_in.time) / 60 / model_in.battery_size[i] + \
            model_in.soc[i] >= aml.Expr_if(model_in.soc_target[i] <= connection_time * model_in.xcharging_power[i] /
                                           model_in.battery_size[i] + model_in.soc[i], model_in.soc_target[i],
                                           connection_time * model_in.xcharging_power[i] /
                                           model_in.battery_size[i] + model_in.soc[i])

    model.demand_rule = Constraint(model.EVs, rule=demand_rule)

    w_1 = assumptions['cost_weights'][0]

    def objective_rule(model_in):
        """
        Target function to be minimized or maximized in order to optimize the charging plan.

        :param model_in: Pyomo optimization model_in.
        :return: Target function.
        """
        return w_1 * sum(
            model_in.power[i, j] * model_in.energy_price[i] for i in model_in.time for j in
            model_in.EVs) / (power_base * energy_price_base) + (1 - w_1) * sum(
            model_in.power[i, j] * model_in.co2_emissions[i] for i in model_in.time for j in model_in.EVs) / (
                       power_base * co2_emission_base)

    model.objective = Objective(rule=objective_rule, sense=minimize, doc='objective function')

    opt = SolverFactory('glpk')
    opt.solve(model)

    # model.soc_temp.pprint()
    # model.power.pprint()

    day_ahead_plan = pd.DataFrame(0, index=hours, columns=ev_set + grid_param)

    power_24 = []
    for h in range(len(hours)):
        power_24.append(list(list(model.power.get_values().values())[p * len(hours) + h] for p in range(len(ev_set))))
    day_plan = pd.DataFrame(power_24, index=hours, columns=ev_set)

    day_ahead_plan.update(day_plan)
    day_ahead_plan.update(pd.DataFrame(data[-1], index=hours, columns=grid_param))

    for s in charging_points:
        if s.availability == 0: 
            s.chargingPlan = day_ahead_plan[s.connected_ev.car_id]
            # print("energy planned =", s.chargingPlan.sum() /
            # s.connected_ev.battery_size / 60, ";", 'soc', s.connected_ev.soc)

    return charging_points
