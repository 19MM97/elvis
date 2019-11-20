# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 18:17:14 2019

@author: draz
"""

import pyomo.environ as  aml
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pandas as pd

import numpy as np

N = list(range(0, 24))
data = {
    'cars': ['car1', 'car2', 'car3', 'car4'],
    'car1': {'arrival': 10, 'departure': 18, 'min': 1, 'max': 7.4, 'soc_arr': 0.6,
             'parkingtime': 1, 'battery_size': 30},
    'car2': {'arrival': 11, 'departure': 17, 'min': 1, 'max': 7.4, 'soc_arr': 0.50,
             'parkingtime': 2, 'battery_size': 40},
    'car3': {'arrival':  9, 'departure': 19, 'min': 1, 'max': 7.4, 'soc_arr': 0.20,
             'parkingtime': 5, 'battery_size': 50},
    'car4': {'arrival': 12, 'departure': 17, 'min': 1, 'max': 7.4, 'soc_arr': 0.4,
             'parkingtime': 8, 'battery_size': 60},
    'parameters': {'energy_price': [np.random.uniform(0.2, 0.5) for i in N],
                   'max_grid': [np.random.uniform(10, 60) for j in N]
                   }
}

model = ConcreteModel()
# Set
# Initialize Set containing all cars
model.cars = Set(initialize=data['cars'])
model.time = Set(initialize=N)

# Parameters

# Create a list containing all parameter names
car_parameters = [list(data['car1'].keys())[param] for param in range(len(data['car1']))]
# Add Parameters to the modell containing the data for all cars
for param in range(len(data['car1'])):
    setattr(model, car_parameters[param], Param(model.cars,
                                                initialize={data['cars'][i]:
                                                            data[data['cars'][i]][list(data['car1'].keys())[param]]
                                                            for i in range(len(data['cars']))
                                                            }, doc=list(data['car1'].keys())[param]))


model.max_grid = Param(model.time, initialize={N[t]: data['parameters']['max_grid'][t] for t in N})
model.energy_price = Param(model.time, initialize={N[t]: data['parameters']['energy_price'][t] for t in N})

# Add Decision variables
def power_bounds_rule(model, i):
    return model.min[i], model.max[i]

for t in N:
    setattr(model, 'power_'+str(t), Var(model.cars, bounds=power_bounds_rule, doc='max'))

#Constraints
def trafo_limit_rule(model,j):
    return sum(getattr(model,'power_'+str(j))[i] for i in model.cars) <= model.max_grid[j]

model.trafo_limit_rule = Constraint(model.time, rule=trafo_limit_rule)

#def demand_rule(model, i):
#    return sum(getattr(model,'power_'+str(j))[i] for j in model.time) == min((1-model.soc_arr[i]) * model.battery_size[i], model.parkingtime[i] * model.max[i])
#
#model.supply_limit = Constraint(model.cars, rule=demand_rule)


def objective_rule(model):
    return sum(getattr(model,'power_'+str(j))[i] * model.energy_price[j] for j in model.time for i in model.cars )

#model.objective = Objective(expr=objective_rule, sense=minimize)
model.objective = Objective(rule=objective_rule, sense=minimize, doc='objective function')



opt = SolverFactory("glpk")
opt.solve(model)


day_ahead_plan =pd.DataFrame(0, index= range(len(N)), columns= data['cars'])
for t in N: 
     day_ahead_plan.iloc[t] = list(getattr(model, 'power_'+str(t)).get_values().values()) 

day_ahead_plan.plot()