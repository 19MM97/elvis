# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 18:17:14 2019

@author: draz
"""

import pyomo.environ as  aml 
from pyomo.environ import *
from pyomo.opt import SolverFactory
import numpy as np 



def opt_lp(data): 
    
    #Creation of a Concrete Model
    model = ConcreteModel()
    
    #Sets 
    model.z = Set(initialize=data['stations_types'], doc='station types')

    #Parameters
    probelm_prameters = [chr(letter) for letter in range(97, 97+len(data['parameters']))]
    
    for param in range(len(data['parameters'])): 
        setattr(model, probelm_prameters[param], Param(model.z, initialize={data['stations_types'][i]: 
           data['parameters'][list(data['parameters'].keys())[param]][i] for i in range(len(data['stations_types']))}, mutable=True, doc=list(data['parameters'].keys())[param]))
    
    def power_bounds_rule(model,i):
        return (3.7, model.a[i])
        
    #Variables
    model.x = Var(model.z, bounds=power_bounds_rule, within=NonNegativeReals, doc='power given to each station')
    
    
    #Constraints
    def trafo_limit_rule(model):
        return sum(model.x[i] * model.e[i]  for i in model.z) <= data['Kraftwerk_limit_kVA']   #trafo limit  in kW
    model.trafo_limit = Constraint(model.z, rule=trafo_limit_rule, doc='transformer limit')
    
#    def weights_rule(model):
#        return model.i[i] + model.j[i] == 1.0   #wieght for each objective
#    model.weights = Constraint(model.z, rule=weights_rule, doc='w1+w1=1')
#
#    def user_demand_rule(model):
#        return sum(model.x[i]  * model.e[i] * model.f[i ] * model.e[i] for i in model.z)/1000 <= data['user_demand_MWh']  #annual demand in MWh
#    model.user_demand = Constraint(model.z, rule=user_demand_rule, doc='annual demand')

 
    def co2_limit_rule(model):
        return sum(model.x[i]/60.0 * model.e[i] * model.d[i] for i in model.z)/1000.0  <= data['co2_limit_ton']/1000.0
    model.CO2limit = Constraint(model.z, rule=co2_limit_rule, doc='co2 emission limit')
  

#Min - w_1 * p(t) * P(t) / P_max(t) * p_max(t) + w_2 * C(t) * P(t) - P_max(t) * C_max(t) 
    ## Objective: maximizing profit
    def objective_rule(model):
        return - sum((model.i[i]  *  model.x[i] * model.c[i] - model.b[i]) / (model.f[i] * model.g[i]) for i in model.z) 
    + sum((model.j[i] * model.d[i] * model.x[i] / model.f[i] / model.h[i] for i in model.z))
#    sum((model.i[i]  *  model.x[i] ( model.c[i] - model.b[i]) / model.f[i] / model.g[i] for i in model.z)) 
#    - sum((model.j[i] * model.d[i] * model.x[i] / model.f[i] / model.h[i] for i in model.z))
    
    model.objective_co2 = Objective(rule=objective_rule, sense=minimize, doc='objective function')
    
    opt = SolverFactory("glpk").solve(model)
    
    return model.x.get_values()


##probelm data
#data = {
#'trafo_limit_kVA': 200, #trafo limit 
#'user_demand_MWh':0.9, #total annual energy demand 
#'co2_limit_ton': 0.4,  #co2 limit per year
#'No_lp': 6, 
#'stations_types': ['Station_1','Station_2','Station_3','Station_4','Station_5', 'Station_6'],   #just names for the types 
#'parameters': {'powers': [3.7, 11, 22, 50, 250, 350], #capacities of the stations 
#'cost_rates': [0.2, 0.2, 0.2, 0.22, 0.35, 0.45], #the costs of the investment levelized 
#'energy_price': [0.3, 0.3, 0.32, 0.5, 0.7, 1.0], #selling price of energy
#'co2_emission': [0.53] * 6,  #emission fo each type
#'operation_hours': [8, 8, 8, 10, 15, 15],    #operational hours of each type
#'gleichzeitigkeitsfaktor': [0.95, 0.775, 1, 0.7603, 1, 1], 
#'lp_each': [1, 3, 2, 2, 0, 0]}}  #concurrency usage of the station 
#


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





chargingPowers = opt_lp(data)

print(chargingPowers)

