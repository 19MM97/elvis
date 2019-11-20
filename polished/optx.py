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
    tau = 1  # tau = 1 for time resolution in minutes
    hours = list(range(t, (t//1440) * 1440 + assumptions['Open_hours'][-1] * 60//tau))
    power_base = 100.0 
    energy_price_base = 0.3
    co2_emission_base = 0.5
    evs = [s.connectedEV for s in charging_points if s.availability == 0]
    data = [ev.__dict__ for ev in evs]
    data.append({'energy_price': [energy_price[hour] / 1000.0 for hour in hours],
                 'breaker_limit': [trafo_preload[3][hour] * 0.8 - trafo_preload[0][hour] for hour in hours],
                 'co2_emissions': [co2_emission[hour] for hour in hours]
                 })
    ev_set = [ev.carID for ev in evs]
    ev_param = list(data[0].keys())
    grid_param = list(data[-1].keys())
    
    # Model
    model = ConcreteModel()
    # Sets
    model.EVs = Set(initialize=ev_set)
    model.time = Set(initialize=hours)
    # Parameters
    for parameter in ev_param:
        setattr(model, parameter, Param(model.EVs, initialize={ev_set[i]: data[i][parameter]
                for i in range(len(ev_set))}, mutable=True, doc=parameter))

    for parameter in grid_param:
        setattr(model, parameter, Param(model.time, initialize={hours[hour]: data[-1][parameter][hour]
                for hour in range(len(hours))}, mutable=True, doc=parameter))

    def power_bounds_rule(self, i):
        return self.powerMin[i], self.charging_power[i]

    for hour in hours:
        setattr(model, 'power_' + str(hour), Var(model.EVs, bounds=power_bounds_rule, doc='power given to an EV in kW'))

    # Constraints
    def trafo_limit_rule(self, j):
        return sum(getattr(self, 'power_' + str(j))[i] for i in self.EVs) <= model.breaker_limit[j]
    
    model.trafo_limit_rule = Constraint(model.time, rule=trafo_limit_rule)
    
    def demand_rule(self, i):
        connection_time = min(data[ev_set.index(i)]['parkingTime'], len(hours) / 60 * tau)
        return sum(
            getattr(self, 'power_' + str(j))[i] for j in self.time) / 60 / self.batterySize[i] + self.soc[i]\
            >= aml.Expr_if(self.socTarget[i] <= connection_time * self.charging_power[i] / self.batterySize[i] +
                           self.soc[i], self.socTarget[i], connection_time * self.charging_power[i] /
                           self.batterySize[i] + self.soc[i])

    model.demand_rule = Constraint(model.EVs, rule=demand_rule)

    w_1 = assumptions['cost_weights'][0]
    w_2 = assumptions['co2_weights'][-1]

    def objective_rule(self):
        return w_1 * sum(
            getattr(self, 'power_' + str(j))[i] * self.energy_price[j] for j in self.time for i in self.EVs) / (
                    power_base * energy_price_base) + w_2 * sum(
            getattr(self, 'power_' + str(j))[i] * self.co2_emissions[j] for j in self.time for i in self.EVs) / (
                    power_base * co2_emission_base)

    model.objective = Objective(rule=objective_rule, sense=minimize, doc='objective function')

    opt = SolverFactory("glpk")
    opt.solve(model)

    day_ahead_plan = pd.DataFrame(0, index=hours, columns=ev_set + grid_param)
    power_24 = []
    for hour in hours:
        power_24.append(list(getattr(model, 'power_' + str(hour)).get_values().values()))
    day_plan = pd.DataFrame(power_24, index=hours, columns=ev_set)

    day_ahead_plan.update(day_plan)
    day_ahead_plan.update(pd.DataFrame(data[-1], index=hours, columns=grid_param))

    for s in charging_points:
        if s.availability == 0: 
            s.chargingPlan = day_ahead_plan[s.connectedEV.carID]
    return charging_points
