timeline = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
costs = [3, 3, 2, 2, 1, 1, 2, 2, 3, 0.5]
limit = [3, 2, 4, 3, 2, 2, 0, 1, 2, 1]
soc = {0: 10, 0.1: 10, 0.2: 10, 0.3: 10, 0.4: 10, 0.5: 10, 0.6: 8, 0.7: 8, 0.8: 7, 0.9: 6, 1: 0}

maximal = [10, 9, 8, 7, 5, 5, 4, 3, 2, 4]

dep = 5
maximum = 10
minimum = 2
tank = 300
import pyomo
from pyomo.environ import *
from pyomo.opt import SolverFactory
import numpy as np

model = ConcreteModel()
model.timeline = Set(timeline)


#  model.soc = Var(timeline, doc='SOC', bounds=(0, 1))
# def loading_rule(model, t):
#     print(math.floor(sum(model.loading[i] for i in range(0, t))/tank*100)/100)
#     return minimum, soc[math.floor(sum(model.loading[i] for i in range(0, t))/tank*100)/100]


model.loading = Var(timeline, bounds=(0, 10))


def fillcar_rule(model):
    return sum(model.loading[t] for t in timeline[0:dep]) == min(tank, dep * maximum)


model.fillcar = Constraint(rule=fillcar_rule)


# def loading_rule(model, t):
#     return model.loading[t] <= maximum * ((tank - sum(model.loading[i] for i in timeline[0:t]))/tank)


# model.loadrule = Constraint(timeline, rule=loading_rule)

#
# def soc_limit_rule(model, t):
#     if t == 9:
#         return model.soc[t] == 1
#     else:
#         return Constraint.Skip
#
#
# model.soc_limit = Constraint(timeline, rule=soc_limit_rule)

model.obj = Objective(expr=sum(model.loading[t] * costs[t] for t in timeline), sense=minimize)

opt = SolverFactory("glpk")
opt.solve(model)
model.fillcar.pprint()
# model.loadrule.pprint()
print(model.loading.get_values())

