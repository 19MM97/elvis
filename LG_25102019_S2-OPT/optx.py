# -*- coding: utf-8 -*-
"""
Created on Fri Oct  18 13:17:14 2019

@author: draz
"""

import pyomo.environ as  aml
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pandas as pd
import pickle
import numpy as np


def opt_charging(t, trafoPreload, chargingPoints, assumptions, co2_emission, energy_price): 
    tau = 1  # time resolution in minutes 
    hours = list(range(t, (t//1440) * 1440 + assumptions['Open_hours'][-1] * 60//tau))
    power_base = 100.0 
    energy_price_base = 0.3
    co2_emission_base = 0.5
    #print(t)
    evs = [s.connectedEV for s in chargingPoints if s.availability == 0]

    data = [ev.__dict__ for ev in evs ]
    data.append({'energy_price': [energy_price[hour] / 1000.0 for hour in hours],
          'breaker_limit': [trafoPreload[3][hour] * 0.8 - trafoPreload[0][hour] for hour in hours],
               'co2_emissions': [co2_emission[hour] for hour in hours]
               })

#    print(data[-1]['energy_price'])
    ev_set = [ev.carID for ev in evs]
    ev_param = list(data[0].keys())
    grid_param = list(data[-1].keys())
    
    #Model
    model = ConcreteModel()
    # Sets
    model.EVs = Set(initialize=ev_set)
    model.time = Set(initialize=hours)
    
    # Parameters
    for param in ev_param:
        setattr(model, param, Param(model.EVs, initialize={ev_set[i]: data[i][param] for i in range(len(ev_set))}, mutable=True, doc=param))
    for param in grid_param:
        setattr(model, param, Param(model.time, initialize={hours[hour]: data[-1][param][hour] for hour in range(len(hours))}, mutable=True, doc=param))

#    model.breaker_limit = Param(model.time, initialize={hours[t]: data['parameters']['breaker_limit'][t] for t in N})
    # Decision variables
    def power_bounds_rule(model, i):
        return model.powerMin[i], model.chargingPower[i]
    for hour in hours:
        setattr(model, 'power_' + str(hour), Var(model.EVs, bounds=power_bounds_rule, doc='power given to an EV in kW'))

    #Constraints
    def trafo_limit_rule(model,j):
        return sum(getattr(model,'power_' + str(j))[i] for i in model.EVs) <= model.breaker_limit[j]
    
    model.trafo_limit_rule = Constraint(model.time, rule=trafo_limit_rule)
    
    def demand_rule(model, i):  
        return sum(getattr(model,'power_' + str(j))[i] for j in model.time) / 60 / model.batterySize[i] + model.soc[i] >= aml.Expr_if(model.socTarget[i] <= model.parkingTime[i] * 
                                            model.chargingPower[i] / model.batterySize[i] + \
                                            model.soc[i], model.socTarget[i], model.parkingTime[i] * 
                                            model.chargingPower[i] / model.batterySize[i] +\
                                            model.soc[i])   
           
    model.demand_rule = Constraint(model.EVs, rule=demand_rule)


    kpi = {}
    for w_1, w_2 in zip(assumptions['cost_weights'], assumptions['co2_weights']): 
        def objective_rule(model):
            return sum(w_1 * getattr(model,'power_'+str(j))[i] * model.energy_price[j] / 60 * tau
                       for j in model.time for i in model.EVs )/power_base/energy_price_base + \
                   sum(w_2 * getattr(model,'power_'+str(j))[i] * model.co2_emissions[j] / 60 * tau
                       for j in model.time for i in model.EVs )/power_base/co2_emission_base


        model.objective = Objective(rule=objective_rule, sense=minimize, doc='objective function')
        
        opt = SolverFactory("glpk")
        opt.solve(model)
        
        day_ahead_plan =pd.DataFrame(0, index= hours, columns=ev_set + grid_param)
        power_24 = []
        for hour in hours:
            power_24.append(list(getattr(model, 'power_' + str(hour) ).get_values().values()))
        day_plan = pd.DataFrame(power_24, index=hours, columns = ev_set )
#        print(day_plan)

        day_ahead_plan.update(day_plan)
        day_ahead_plan.update(pd.DataFrame(data[-1], index=hours, columns = grid_param ))

    for s in chargingPoints:
        if s.availability == 0: 
            s.chargingPlan = day_ahead_plan[s.connectedEV.carID]
        else: continue

    return chargingPoints
#    ax =day_ahead_plan[data['EVs']].plot()
#    ax2 = ax.twinx()
#    day_ahead_plan['energy_price'].plot(ax=ax2)
    

 
