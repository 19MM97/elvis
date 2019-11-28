import yaml
from datetime import timedelta
import data


class DataClass:
    """
    Data model containing data from user inputs and simulation parameter.

    :cvar self.car_amount: Amount of cars arrinving per week in the simulation instance.
    :type self.amount: int
    :cvar self.power_cp: Power of the charging points.
    :type self.power_cp: float
    :cvar self.amount_cp: Number of charging points for the simulation instance.
    :type self.amount_cp: int
    :cvar self.control: Control strategy for the simulation strategy.
    :type self.control: str
    :cvar self.co2_scenario: CO2 scenario considered in the simulation instance.
    :type self.co2_scenario: int
    :cvar self.co2_scenario: Storage capacity in kWh considered in the simulation instance.
    :type self.co2_scenario: float
    :cvar self.storage_capacity: Capacity of the battery from the charging infrastructure.
    :type self.storage_capacity: float
    :cvar self.total_simulation_time: Amount of time steps in the simulation.
    :type self.total_simulation_time: int
    :cvar self.dis_ev_arr: Distribution of the vehicle arrival as per input file.
    :type self.dis_ev_arr: list
    :cvar self.dis_year: Total amount of car arrivals over simulation time.
    :type self.dis_year: int
    :cvar self.dis_soc: Distribution of the SOC at arrival times of the vehicles.
    :type self.dis_soc: list
    :cvar self.dis_battery_size: Distribution of the battery sizes for the vehicles.
    :type self.dis_battery_size: list
    :cvar self.dis_user_type: Distribution of the user types resulting in different pariking times.
    :type self.dis_user_type: list
    """
    def __init__(self):
        # User input
        self.user_assumptions = read_user_assumptions()

        # Simulation parameters
        self.power_cp = 0
        self.car_amount = 0
        self.amount_cp = 0
        self.control = None
        self.co2_scenario = None
        self.storage_capacity = None

        # Simulation variables
        if self.user_assumptions['Simulation_time_in_weeks'] is not None:
            self.total_simulation_time = self.user_assumptions['Simulation_time_in_weeks'] * 60 * 24 * 7
        else:
            self.total_simulation_time = int(timedelta(weeks=1).total_seconds() // 60)

        # Assumed distributions
        self.dis_ev_arr = None
        self.dis_year = None
        self.dis_soc = None
        self.dis_battery_size = None
        self.dis_user_type = None

        # Time series data
        self.co2_emission = None
        self.energy_price = None
        self.transformer_preload = None

    def get_time_series_data(self):
        """
        Read time series data from input files.
        """
        self.co2_emission = data.get_co2_emission(self.total_simulation_time)[self.co2_scenario]
        self.energy_price = data.get_energy_price(self.total_simulation_time)
        self.transformer_preload = data.preload(self.total_simulation_time)


def read_user_assumptions():
    """
    Read yaml file containing the data specified by the user.
    :return: User input data.
    :rtype: dict
    """
    with open(r'../data/test.yaml', 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)
