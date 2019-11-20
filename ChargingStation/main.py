# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 18:17:14 2019

@author: draz
"""

import pyomo.environ as  aml
from pyomo.environ import *
from pyomo.opt import SolverFactory

import numpy as np

N = list(range(0, 24))
data = {
    'cars': ['car1', 'car2', 'car3', 'car4'],
    'car1': {'arrival': 10, 'departure': 18, 'min': 1, 'max': 10, 'SOC_arr': 0.25,
             'SOC_dep': 0.8, 'battery_size': 30},
    'car2': {'arrival': 11, 'departure': 17, 'min': 1, 'max': 10, 'SOC_arr': 0.50,
             'SOC_dep': 1.0, 'battery_size': 40},
    'car3': {'arrival':  9, 'departure': 19, 'min': 1, 'max': 10, 'SOC_arr': 0.20,
             'SOC_dep': 1.0, 'battery_size': 50},
    'car4': {'arrival': 12, 'departure': 17, 'min': 1, 'max': 10, 'SOC_arr': 0.25,
             'SOC_dep': 0.9, 'battery_size': 60},
    'parameters': {'energy_price': [np.random.uniform(0.39, 0.5) for i in range(0, 24)],
                   'max_grid': [np.random.uniform(0, 60) for j in range(0, 24)]
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


# Add Decision variables
def power_bounds_rule(model, i):
    return model.min[i], model.max[i]


for time_steps in N:
    setattr(model, 'power_' + str(time_steps), Var(model.cars, bounds=power_bounds_rule, doc='max'))

# model.power = Var(model.time)

model.max_grid = Param(model.time, initialize={N[i]: data['parameters']['max_grid'][i] for i in N})
model.energy_price = Param(model.time, initialize={N[i]: data['parameters']['energy_price'][i] for i in N})

def power_bounds_rule(model, i):
    return model.min[i], model.max[i]


# model.power = Var(model.cars, bounds=power_bounds_rule, within=NonNegativeReals,
#                   doc='power given to each car')


def energy_demand_rule(model, i):
    return (model.SOC_dep[i] - model.SOC_arr[i]) * model.battery_size[i]  # / (model.departure[i] - model.arrival[i])


model.energy_demand = Var(model.cars, rule=energy_demand_rule)


def objective_rule(j, costs):
    print(j)
    result = sum(getattr(model, 'power_' + str(j))) * costs


model.obj = Objective(expr=sum(objective_rule(i, model.energy_price[i]) for i in model.time),
                      sense=maximize)


def supply_limit_rule(model, j):
    return sum(model.power[i] for i in model.cars) <= model.max_grid[j]


model.supply_limit = Constraint(model.time, rule=supply_limit_rule)


opt = SolverFactory("glpk")
opt.solve(model)

print(model.power.get_values())




#     # Parameters
#     probelm_prameters = [chr(letter) for letter in range(97, 97 + len(data['parameters']))]
#
#     for param in range(len(data['parameters'])):
#         setattr(model, probelm_prameters[param], Param(model.z, initialize={data['stations_types'][i]:
#                                                                                 data['parameters'][
#                                                                                     list(data['parameters'].keys())[
#                                                                                         param]][i] for i in
#                                                                             range(len(data['stations_types']))},
#                                                        mutable=True, doc=list(data['parameters'].keys())[param]))






# # model.max_grid = Param([data[power] for power in data['parameters']['energy_price']])
# model.power = Var(within=NonNegativeReals)
# model.costs = Param(data['parameters']['energy_price'])
# model.obj = Objective(expr=sum(model.power * model.costs[i] for i in len(data['parameters']['energy_price'])),
#                       sense=minimize)
# model.con1 = Constraint(model.power[i] <= data['parameters'][i] for i in len(data['parameters']['energy_price']))


#model.con1 = Constraint(expr=model.power <= max_grid for gmodel.x )
#model.z = Set(initialize=data)

data = {'Kraftwerk_limit_kVA': 100,
        'user_demand_MWh': None,
        'co2_limit_ton': 4.0,
        'stations_types': ['Station_1'],
        'parameters': {
            'powers': [50],
            'cost_rates': [0.3],
            'energy_price': [np.random.uniform(0.39, 0.50)],
            'co2_emission': [1],
            'lp_each': [15],
            'base_power': [350],
            'base_cost': [0.28],
            'base_bmission': [1],
            'wieght_cost': [0.3],
            'wieght_co2': [0.7]
        }}

# # Parameters
# problem_params = [param for param in data['parameters']]
#
# print(problem_params)
#
# def opt_lp(data):
#     # Creation of a Concrete Model
#     model = ConcreteModel()
#
#     # Sets
#     model.z = Set(initialize=data['stations_types'], doc='station types')
#
#     # Parameters
#     probelm_prameters = [chr(letter) for letter in range(97, 97 + len(data['parameters']))]
#
#     for param in range(len(data['parameters'])):
#         setattr(model, probelm_prameters[param], Param(model.z, initialize={data['stations_types'][i]:
#                                                                                 data['parameters'][
#                                                                                     list(data['parameters'].keys())[
#                                                                                         param]][i] for i in
#                                                                             range(len(data['stations_types']))},
#                                                        mutable=True, doc=list(data['parameters'].keys())[param]))
#     model.b.pprint()
#
#     def power_bounds_rule(model, i):
#         return (3.7, model.a[i])
#
#     # Variables
#     model.x = Var(model.z, bounds=power_bounds_rule, within=NonNegativeReals, doc='power given to each station')
#
#     # Constraints
#     def trafo_limit_rule(model):
#         return sum(model.x[i] * model.e[i] for i in model.z) <= data['Kraftwerk_limit_kVA']  # trafo limit  in kW
#
#     model.trafo_limit = Constraint(model.z, rule=trafo_limit_rule, doc='transformer limit')
#
#     #    def weights_rule(model):
#     #        return model.i[i] + model.j[i] == 1.0   #wieght for each objective
#     #    model.weights = Constraint(model.z, rule=weights_rule, doc='w1+w1=1')
#     #
#     #    def user_demand_rule(model):
#     #        return sum(model.x[i]  * model.e[i] * model.f[i ] * model.e[i] for i in model.z)/1000 <= data['user_demand_MWh']  #annual demand in MWh
#     #    model.user_demand = Constraint(model.z, rule=user_demand_rule, doc='annual demand')
#
#     def co2_limit_rule(model):
#         return sum(model.x[i] / 60.0 * model.e[i] * model.d[i] for i in model.z) / 1000.0 <= data[
#             'co2_limit_ton'] / 1000.0
#
#     model.CO2limit = Constraint(model.z, rule=co2_limit_rule, doc='co2 emission limit')
#
#     # Min - w_1 * p(t) * P(t) / P_max(t) * p_max(t) + w_2 * C(t) * P(t) - P_max(t) * C_max(t)
#     # Objective: maximizing profit
#     def objective_rule(model):
#         return - sum((model.i[i] * model.x[i] * model.c[i] - model.b[i]) / (model.f[i] * model.g[i]) for i in model.z)
#
#     + sum((model.j[i] * model.d[i] * model.x[i] / model.f[i] / model.h[i] for i in model.z))
#     #    sum((model.i[i]  *  model.x[i] ( model.c[i] - model.b[i]) / model.f[i] / model.g[i] for i in model.z))
#     #    - sum((model.j[i] * model.d[i] * model.x[i] / model.f[i] / model.h[i] for i in model.z))
#
#     model.objective_co2 = Objective(rule=objective_rule, sense=minimize, doc='objective function')
#
#     opt = SolverFactory("glpk")
#     opt.solve(model)
#
#     return model.x.get_values()
#
# #
# # ##probelm data
# # # data = {
# # # 'trafo_limit_kVA': 200, #trafo limit
# # # 'user_demand_MWh':0.9, #total annual energy demand
# # # 'co2_limit_ton': 0.4,  #co2 limit per year
# # # 'No_lp': 6,
# # # 'stations_types': ['Station_1','Station_2','Station_3','Station_4','Station_5', 'Station_6'],   #just names for the types
# # # 'parameters': {'powers': [3.7, 11, 22, 50, 250, 350], #capacities of the stations
# # # 'cost_rates': [0.2, 0.2, 0.2, 0.22, 0.35, 0.45], #the costs of the investment levelized
# # # 'energy_price': [0.3, 0.3, 0.32, 0.5, 0.7, 1.0], #selling price of energy
# # # 'co2_emission': [0.53] * 6,  #emission fo each type
# # # 'operation_hours': [8, 8, 8, 10, 15, 15],    #operational hours of each type
# # # 'gleichzeitigkeitsfaktor': [0.95, 0.775, 1, 0.7603, 1, 1],
# # # 'lp_each': [1, 3, 2, 2, 0, 0]}}  #concurrency usage of the station
# # #
# #
# #
# data = {'Kraftwerk_limit_kVA': 100,
#         'user_demand_MWh': None,
#         'co2_limit_ton': 4.0,
#         'stations_types': ['Station_1'],
#         'parameters': {
#             'powers': [50],
#             'cost_rates': [0.3],
#             'energy_price': [np.random.uniform(0.39, 0.50)],
#             'co2_emission': [1],
#             'lp_each': [15],
#             'base_power': [350],
#             'base_cost': [0.28],
#             'base_bmission': [1],
#             'wieght_cost': [0.3],
#             'wieght_co2': [0.7]
#         }}
#
# chargingPowers = opt_lp(data)
#
# print(chargingPowers)

