"""
Created on Fri Oct  18 13:17:14 2019

@author: draz
"""

import pyomo.environ as  aml
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pandas as pd
import time
import pickle
import numpy as np
import input


def opt_charging(t, trafoPreload, chargingPoints, assumptions, co2_emission, energy_price, data):
    tau = 1  # time resolution in minutes
    hours = list(range(t, (t // 1440) * 1440 + assumptions['opening_hours'][-1] * 60 // tau))
    power_base = 100.0
    energy_price_base = 0.3
    co2_emission_base = 0.5
    evs = [s.connected_ev for s in chargingPoints if s.availability == 0]
    for ev in evs:
        ev.xcharge_battery()
    data = [ev.__dict__ for ev in evs]
    data.append({'energy_price': [energy_price[hour] / 1000.0 for hour in hours],
                 'breaker_limit': [trafoPreload[data.user_assumptions['trafo_limit']][hour] * 0.8 - trafoPreload[data.user_assumption['preload']][hour] for hour in hours],
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
    for para in ev_param:
        setattr(model, para,
                Param(model.EVs, initialize={ev_set[i]: data[i][para] for i in range(len(ev_set))}, mutable=True,
                      doc=para))
    for param in grid_param:
        setattr(model, param,
                Param(model.time, initialize={hours[hour]: data[-1][param][hour] for hour in range(len(hours))},
                      mutable=True, doc=param))

    def power_bounds_rule(model, i):
        return 0, 11

    for hour in hours:
        setattr(model, 'power_' + str(hour), Var(model.EVs, bounds=power_bounds_rule, doc='power given to an EV in kW'))

    # Constraints
    def trafo_limit_rule(model, j):
        return sum(getattr(model, 'power_' + str(j))[i] for i in model.EVs) <= model.breaker_limit[j]

    model.trafo_limit_rule = Constraint(model.time, rule=trafo_limit_rule)

    def demand_rule(model, i):
        connection_time = min(data[ev_set.index(i)]['parking_time'], len(hours) / 60 * tau)
        # print(connection_time, data[ev_set.index(i)]['arrivalTime'], data[ev_set.index(i)]['timeStartXchaging'], t, (data[ev_set.index(i)]['timeStartXchaging'] - data[ev_set.index(i)]['arrivalTime']) / 60.0 * tau)
        return sum(
            getattr(model, 'power_' + str(j))[i] for j in model.time) / 60 / model.battery_size[i] + model.soc[
                   i] >= aml.Expr_if(
            model.soc_target[i] <= connection_time * 11 / model.battery_size[i] +
            model.soc[i], model.soc_target[i],
            connection_time * 11 / model.battery_size[i] + model.soc[i])

    model.demand_rule = Constraint(model.EVs, rule=demand_rule)

    # for w_1, w_2 in zip(assumptions['cost_weights'], assumptions['co2_weights']):
    w_1 = assumptions['cost_weights'][0]
    w_2 = 1 - w_1

    def objective_rule(model):
        return w_1 * sum(
            getattr(model, 'power_' + str(j))[i] * model.energy_price[j] for j in model.time for i in model.EVs) / (
                       power_base * energy_price_base) + w_2 * sum(
            getattr(model, 'power_' + str(j))[i] * model.co2_emissions[j] for j in model.time for i in model.EVs) / (
                       power_base * co2_emission_base)

    model.objective = Objective(rule=objective_rule, sense=minimize, doc='objective function')

    opt = SolverFactory("glpk")
    opt.solve(model)

    start_time = time.time()
    day_ahead_plan = pd.DataFrame(0, index=hours, columns=ev_set + grid_param)
    power_24 = []
    for hour in hours:
        power_24.append(list(getattr(model, 'power_' + str(hour)).get_values().values()))
    day_plan = pd.DataFrame(power_24, index=hours, columns=ev_set)

    day_ahead_plan.update(day_plan)
    day_ahead_plan.update(pd.DataFrame(data[-1], index=hours, columns=grid_param))

    for s in chargingPoints:
        if s.availability == 0:
            s.charging_plan = day_ahead_plan[s.connected_ev.car_id]
    #
    return chargingPoints, time.time() - start_time

#    ax =day_ahead_plan[data['EVs']].plot()
#    ax2 = ax.twinx()
#    day_ahead_plan['energy_price'].plot(ax=ax2)
