# -*- coding: utf-8 -*-
"""
Created on Fri Oct  18 13:17:14 2019

@author: draz
"""

import pyomo.environ as  aml
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pandas as pd
import matplotlib
import numpy as np

tau = 60  # time resolution in minutes
N = list(range(0, 1440 // tau))
data = {
    'EVs': ['EV1', 'EV2', 'EV3', 'EV4'],
    'EV1': {'arrival': 10,
            'min': 0,
            'max': 3.7,
            'soc_arr': 0.2,
            'parkingtime': 4,
            'battery_size': 60},
    'EV2': {'arrival': 11,
            'min': 0,
            'max': 3.7,
            'soc_arr': 0.2,
            'parkingtime': 5,
            'battery_size': 40},
    'EV3': {'arrival': 9,
            'min': 0,
            'max': 3.7,
            'soc_arr': 0.10,
            'parkingtime': 7,
            'battery_size': 54},
    'EV4': {'arrival': 12,
            'min': 0,
            'max': 3.7,
            'soc_arr': 0.1,
            'parkingtime': 4,
            'battery_size': 40},
    'parameters': {'energy_price': [np.random.uniform(20, 50) for t in N],
                   'breaker_limit': [np.random.uniform(20, 70) for t in N],
                   'co2_emissions': [np.random.uniform(500, 1100) for t in N]
                   }
}

model = ConcreteModel()
# Set
# Initialize Set containing all EVs
model.EVs = Set(initialize=data['EVs'])
model.time = Set(initialize=N)

# Parameters

# Create a list containing all parameter names
EV_parameters = [list(data['EV1'].keys())[param] for param in range(len(data['EV1']))]

# Add Parameters to the modell containing the data for all EVs
for param in range(len(data['EV1'])):
    setattr(model, EV_parameters[param], Param(model.EVs,
                                               initialize={data['EVs'][i]:
                                                               data[data['EVs'][i]][list(data['EV1'].keys())[param]]
                                                           for i in range(len(data['EVs']))
                                                           }, doc=list(data['EV1'].keys())[param]))

model.breaker_limit = Param(model.time, initialize={N[t]: data['parameters']['breaker_limit'][t] for t in N})
model.energy_price = Param(model.time, initialize={N[t]: data['parameters']['energy_price'][t] for t in N})

#Test SOC - SOC parameter is declared now add the adjustment that the soc is changed if the car is being loaded
for t in N:
    setattr(model, 'soc_'  + str(t), Param(model.EVs,
                                           initialize={EV: data[EV]['soc_arr']
                                                       for EV in model.EVs
                                                       if t >= data[EV]['arrival']
                                                       },
                                           mutable=True,
                                           doc="soc"))


# model.co2_emissions = Param(model.time, initialize={N[t]: data['parameters']['co2_emissions'][t] for t in N})

# Decision variables
def power_bounds_rule(model, i):
     return model.min[i], model.max[i]


for t in N:
    setattr(model, 'power_' + str(t), Var(model.EVs, bounds=power_bounds_rule, initialize=0, doc='max'))


# Constraints
def trafo_limit_rule(model, j):
    return sum(getattr(model, 'power_' + str(j))[i] for i in model.EVs) <= model.breaker_limit[j]


model.trafo_limit_rule = Constraint(model.time, rule=trafo_limit_rule)


def demand_rule(model, i):

    max_possible = data[i]['parkingtime']*data[i]['max'] / data[i]['battery_size'] + data[i]['soc_arr']

    return sum(getattr(model, 'power_' + str(j))[i] for j in model.time) * tau / 60.0 / model.battery_size[i] + \
           model.soc_arr[i] >= min(0.8, max_possible)


model.demand_rule = Constraint(model.EVs, rule=demand_rule)


def unavailable_rule(model, i):

    arr = data[i]['arrival'] * 60 // tau
    dep = arr + data[i]['parkingtime'] * 60 // tau

    return sum(getattr(model, 'power_' + str(j))[i] for j in N[0:N.index(arr)]) + \
           + sum(getattr(model, 'power_' + str(j))[i] for j in N[N.index(dep):len(N)]) \
           == 0


model.unavailable_rule = Constraint(model.EVs, rule=unavailable_rule)


# def co2_rule(model, i):
#    return sum(getattr(model,'power_'+str(j))[i] * model.co2_emissions[j]/(tau/60.0)/1000.0 for j in model.time for i in model.EVs ) <= 70
# model.co2_rule = Constraint(model.EVs, rule=co2_rule)


def objective_rule(model):
    return sum(getattr(model, 'power_' + str(j))[i] * model.energy_price[j] / (tau / 60.0) for j in model.time for i in
               model.EVs)


model.objective = Objective(rule=objective_rule, sense=minimize, doc='objective function')

opt = SolverFactory("glpk")
opt.solve(model)

day_ahead_plan = pd.DataFrame(0, index=range(len(N)), columns=data['EVs'])
for t in N:
    day_ahead_plan.iloc[t] = list(getattr(model, 'power_' + str(t)).get_values().values())
    # day_ahead_plan.iloc[t] = list(getattr(model, 'soc_' + str(t)).get_values().values())

day_ahead_plan['total_load'] = day_ahead_plan[data['EVs']].sum(axis=1)
day_ahead_plan['energy price'] = data['parameters']['energy_price']
day_ahead_plan['co2_emissions'] = data['parameters']['co2_emissions']
day_ahead_plan['breaker_limit'] = data['parameters']['breaker_limit']


summary = {'Number of EVs': len(data['EVs']),
           'Total charging costs in Euro': value(model.objective) / 100.0,
           'Total energy charged in kWh': day_ahead_plan['total_load'].sum(),
           'Total CO2 emissions in kge': day_ahead_plan['co2_emissions'].sum() / 1000.0,
           'Average energy price in Euro/kWh': day_ahead_plan['energy price'].mean(),

          }
print(day_ahead_plan)
ax = day_ahead_plan[data['EVs']].plot()
ax2 = ax.twinx()
day_ahead_plan['energy price'].plot(ax=ax2)
model.unavailable_rule.display()


