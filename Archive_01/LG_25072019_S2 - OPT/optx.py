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


def opt_charging(t, trafoPreload, chargingPoints, assumptions, co2_limit):
#    print('_____________________time______________________= ',t)

    tau = 1  # time resolution in minutes 
    hours = list(range(t, (t//1440) * 1440 + assumptions['Open_hours'][-1] * 60//tau))
    power_base = 100 
    energy_price_base = 30
    co2_emission_base = 500
    weights_cost = [1]
    weights_co2 = [0]
    #print(t)
    evs = [s.connectedEV for s in chargingPoints if s.availability == 0]

    data = [ev.__dict__ for ev in evs ]
    data.append({'energy_price': [np.random.uniform(20, 29) for hour in hours],
          'breaker_limit': [trafoPreload[3][hour] * 0.8 - trafoPreload[0][hour]for hour in hours],
               'co2_emissions': [co2_limit[hour] * 1000 for hour in hours]
               })

#    print(data)

    a = len(data[-1]['co2_emissions'])

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
        return model.powerMin[i], model.powerMax[i]
    for hour in hours:
        setattr(model, 'power_' + str(hour), Var(model.EVs, bounds=power_bounds_rule, doc='power given to an EV in kW'))

    #Constraints
    def trafo_limit_rule(model,j):
        return sum(getattr(model,'power_' + str(j))[i] for i in model.EVs) <= model.breaker_limit[j]
    
    model.trafo_limit_rule = Constraint(model.time, rule=trafo_limit_rule)


    # def demand_rule(model, i):
    #
    #     # max_possible = model.parkingTime[i] * model.chargingPower[i] / model.batterySize[i] + model.soc[i]
    #
    #     return sum(getattr(model,'power_' + str(j))[i] for j in model.time) \
    #                        * tau / 60 / model.batterySize[i] + model.soc[i] \
    #                         >= model.soc[i] + 0.05 #aml.Expr_if(model.socTarget[i] <= model.parkingTime[i] * model.chargingPower[i] / model.batterySize[i] + model.soc[i], model.socTarget[i], model.parkingTime[i] * model.chargingPower[i] / model.batterySize[i] + model.soc[i])
    def demand_rule(model, i):
        return sum(getattr(model, 'power_' + str(j))[i] for j in model.time) / 60 /model.batterySize[i] + model.soc[i] >= (model.soc[i] + 0.05)
        #return sum(Ladung per minute)/60 minutes = kWh / batterysize = soc_change + soc_arrival = soc_after charging >= requested soc or max possible soc
    
    model.demand_rule = Constraint(model.EVs, rule=demand_rule)
    #model.demand_rule.pprint()
    #model.soc.pprint()
    # model.demand_rule.pprint()

    kpi = {}
    for w_1, w_2 in zip(weights_cost, weights_co2): 
        def objective_rule(model):
            return sum(w_1 * getattr(model,'power_'+str(j))[i] * model.energy_price[j] / 60 * tau
                       for j in model.time for i in model.EVs )/power_base/energy_price_base + \
                   sum(w_2 * getattr(model,'power_'+str(j))[i] * model.co2_emissions[j] / 60 * tau
                       for j in model.time for i in model.EVs )/power_base/co2_emission_base


        model.objective = Objective(rule=objective_rule, sense=minimize, doc='objective function')
        
        opt = SolverFactory("glpk")
        opt.solve(model)
        
        # print(list(data.keys()))
        day_ahead_plan =pd.DataFrame(0, index= range(t, t+24*60//tau), columns=ev_set + grid_param)

        #print(len(ev_set))

        #check here pls: if Im right then Im taking all values from the variables and check if they are not 0 and there are some that are not.
        #If thats right then our model is probably assigning values but at a time that is not listed because its after the closing time
        for hour in hours:
            # print(list(getattr(model, 'power_' + str(hours[hours.index(hour)])).get_values().values())[0])
            if list(getattr(model, 'power_' + str(hours[hours.index(hour)])).get_values().values())[0] != 0:
                print(hour, list(getattr(model, 'power_' + str(hours[hours.index(hour)])).get_values().values())[0])


        for hour in hours:
            day_ahead_plan.iloc[hours.index(hour)][0:len(ev_set)] = list(getattr(model, 'power_' + str(hour) ).get_values().values())

        day_ahead_plan['total_load'] = day_ahead_plan[ev_set].sum(axis=1)
        #print(day_ahead_plan)
        day_ahead_plan.update({'energy_price': data[-1]['energy_price']})
        day_ahead_plan.update({'co2_emissions': data[-1]['co2_emissions']})
        day_ahead_plan.update({'breaker_limit': data[-1]['breaker_limit']})
        #print(day_ahead_plan)
        # day_ahead_plan['energy_price'][hours] = data[-1]['energy_price']
        # day_ahead_plan['co2_emissions'][hours] = data[-1]['co2_emissions']
        # day_ahead_plan['breaker_limit'][hours] = data[-1]['breaker_limit']
        kpi.update({'Number of EVs%s_%s'%(w_1,w_2): len(ev_set),
                   'Total charging costs in Euro%s_%s'%(w_1,w_2): (day_ahead_plan['total_load'] * day_ahead_plan['energy_price']).sum()/100.0,
                   'Total energy charged in kWh%s_%s'%(w_1,w_2): day_ahead_plan['total_load'].sum(),
                   'Total CO2 emissions in kge%s_%s'%(w_1,w_2): (day_ahead_plan['co2_emissions'] * day_ahead_plan['total_load']).sum()/1000.0,
                   'Average energy price in Euro/kWh%s_%s'%(w_1,w_2): (day_ahead_plan['total_load'] * day_ahead_plan['energy_price']).sum() / day_ahead_plan['total_load'].sum()
                   })
    for s in chargingPoints:
        if s.availability == 0: 
            s.chargingPlan = day_ahead_plan[s.connectedEV.carID]
            # print(day_ahead_plan[s.connectedEV.carID])
        else: continue

    return chargingPoints
#    ax =day_ahead_plan[data['EVs']].plot()
#    ax2 = ax.twinx()
#    day_ahead_plan['energy_price'].plot(ax=ax2)
    

 
