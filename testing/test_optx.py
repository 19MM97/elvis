import input
import vehicle
from events import generate_lp
from optx import opt_charging
import cp

data = input.DataClass()
data.get_defaults()

t_start = data.user_assumptions['opening_hours'][0] * 60
t_end = data.user_assumptions['opening_hours'][-1] * 60

ev = vehicle.Vehicle(t_start, data, 1.0)
ev2 = vehicle.Vehicle(t_start, data, 1.0)

evs = [ev, ev2]
charging_points = generate_lp(2, data.power_cp, data)
for cp in range(len(charging_points)):
    charging_points[cp].assign_ev(evs[cp], t_start)
    evs[cp].xcharging_power = charging_points[cp].power_nominal

x = opt_charging(t_start + 1, data.transformer_preload, charging_points,
                 data.user_assumptions, data.co2_emission, data.energy_price)

print(sum(x[0].chargingPlan))

print()
