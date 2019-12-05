import pandas as pd
import error_handling


if __name__ == 'data':
    stations_config = pd.ExcelFile('../data/inputdata.xlsx')
    sheet_names_list = stations_config.sheet_names

    for sheet in sheet_names_list:
        exec('{} = pd.DataFrame(stations_config.parse(sheet_name=sheet) )'.format(sheet))


def input_2_profile_evl(dis_location, data):
    """
    Read the data concerning battery sizes, SOCs, user types, arrival times from input file.
    :param dis_location: Location of the charging infrastructure (according to input file).
    :type dis_location: str
    :param data: Data model from :class:`Daten`.
    :return: Distribution of battery sizes, SOC at arrival, user type, arrival times
    """
    error_handling.check_input_file_cols(globals()['Arr_Typ1'].columns, dis_location, 'arrival distribution')
    data.dis_ev_arr = globals()['Arr_Typ1'][dis_location].tolist()
    data.dis_user_type = [globals()['Ort1'][a].values.tolist() for a in globals()['Ort1'].columns]
    data.dis_soc = [globals()['SOC'][a].values.tolist() for a in globals()['SOC'].columns]
    data.dis_battery_size = [globals()['Batterysize'][a].values.tolist() for a in globals()['Batterysize'].columns]
    data.dis_year = list([data.car_amount] * data.user_assumptions['simulation_time_in_weeks'])


def get_co2_emission(simulation_time, scenarios):
    """
    Read the data concerning CO2 emissions from input file.
    :param simulation_time: Total length of the simulation time.
    :type simulation_time: int
    :param scenarios: CO2 scenarios form user inputs.
    :rtype scenarios: list
    :return: CO2 time series data.
    """
    co2_data = pd.concat([globals()['CO2_Emissions'][0:simulation_time // 60 + 1]], ignore_index=True)

    error_handling.check_input_file_cols(co2_data.columns, scenarios, 'CO2 scenario')

    co2_data = co2_data[scenarios]

    datetime_co2 = pd.date_range('2018-01-01', periods=len(co2_data), freq='H')
    co2_data['Time'] = datetime_co2
    co2_data = co2_data.set_index('Time')
    co2_data = co2_data.resample('T')
    co2_data = co2_data.interpolate(method='linear')
    co2_data = [co2_data[a][:-1].values.tolist() for a in co2_data.columns]
    return co2_data


def get_energy_price(simulation_time):
    """
    Read the data concerning energy prices from input file.
    :param simulation_time: Total length of the simulation time.
    :type simulation_time: int
    :return: Energy price time series data.
    """
    price_data = pd.concat([globals()['Energy_Price'][0:simulation_time // 60 + 1]], ignore_index=True)
    datetime_price = pd.date_range('2018-01-01', periods=len(price_data), freq='H')
    price_data['Time'] = datetime_price
    price_data = price_data.set_index('Time')
    price_data = price_data.resample('T')
    price_data = price_data.interpolate(method='linear')
    price_data = [price_data[a].values.tolist() for a in price_data.columns]
    return price_data[-1][:-1]


def preload(simulation_time):
    """
    Read the data concerning transformer pre-load from input file.
    :param simulation_time: Total length of the simulation time.
    :type simulation_time: int
    :return: Transformer preload time series data.
    :rtype: list
    """
    trafo_preload = globals()['Trafo_Vorbelastung']
    date_time_pre = pd.date_range('2018-01-01', periods=simulation_time // 10 + 1, freq='10T')
    trafo_preload = pd.concat([trafo_preload[0:(len(date_time_pre))]], ignore_index=True)
    trafo_preload['Time'] = date_time_pre
    trafo_preload = trafo_preload.set_index('Time')
    preload_resample = trafo_preload.resample('T')
    preload_resample = preload_resample.interpolate(method='linear')
    trafo_preload = preload_resample[:-1]
    trafo_preload = [trafo_preload[a].values.tolist() for a in trafo_preload.columns]
    return trafo_preload
