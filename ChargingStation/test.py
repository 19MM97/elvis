
JOBS = {
    'A': {'release': 2, 'duration': 5, 'due': 10},
    'B': {'release': 5, 'duration': 6, 'due': 21},
    'C': {'release': 4, 'duration': 8, 'due': 15},
    'D': {'release': 0, 'duration': 4, 'due': 10},
    'E': {'release': 0, 'duration': 2, 'due':  5},
    'F': {'release': 8, 'duration': 3, 'due': 15},
    'G': {'release': 9, 'duration': 2, 'due': 22},
}

import pyomo.environ as  aml
from pyomo.environ import *
from pyomo.opt import SolverFactory
from pyomo.gdp import *

import numpy as np


def opt_schedule(JOBS):
    # create model
    m = ConcreteModel()

    # index set to simplify notation
    m.J = Set(initialize=JOBS.keys())
    m.PAIRS = Set(initialize=m.J * m.J, dimen=2, filter=lambda m, j, k: j < k)

    # upper bounds on how long it would take to process all jobs
    tmax = max([JOBS[j]['release'] for j in m.J]) + sum([JOBS[j]['duration'] for j in m.J])

    # decision variables
    m.start = Var(m.J, domain=NonNegativeReals, bounds=(0, tmax))
    m.pastdue = Var(m.J, domain=NonNegativeReals, bounds=(0, tmax))
    m.early = Var(m.J, domain=NonNegativeReals, bounds=(0, tmax))

    # additional decision variables for use in the objecive
    m.makespan = Var(domain=NonNegativeReals, bounds=(0, tmax))
    m.maxpastdue = Var(domain=NonNegativeReals, bounds=(0, tmax))
    m.ispastdue = Var(m.J, domain=Binary)

    # objective function
    m.OBJ = Objective(expr=sum([m.pastdue[j] for j in m.J]), sense=minimize)

    # constraints
    m.c1 = Constraint(m.J, rule=lambda m, j: m.start[j] >= JOBS[j]['release'])
    m.c2 = Constraint(m.J, rule=lambda m, j:
    m.start[j] + JOBS[j]['duration'] + m.early[j] == JOBS[j]['due'] + m.pastdue[j])
    m.c3 = Disjunction(m.PAIRS, rule=lambda m, j, k:
    [m.start[j] + JOBS[j]['duration'] <= m.start[k],
     m.start[k] + JOBS[k]['duration'] <= m.start[j]])

    m.c4 = Constraint(m.J, rule=lambda m, j: m.pastdue[j] <= m.maxpastdue)
    m.c5 = Constraint(m.J, rule=lambda m, j: m.start[j] + JOBS[j]['duration'] <= m.makespan)
    m.c6 = Constraint(m.J, rule=lambda m, j: m.pastdue[j] <= tmax * m.ispastdue[j])

    TransformationFactory('gdp.chull').apply_to(m)
    SolverFactory('glpk').solve(m).write()

    SCHEDULE = {}
    for j in m.J:
        SCHEDULE[j] = {'machine': 1, 'start': m.start[j](), 'finish': m.start[j]() + JOBS[j]['duration']}

    return SCHEDULE


SCHEDULE = opt_schedule(JOBS)
print(SCHEDULE)