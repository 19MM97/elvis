import pandas as pd

if __name__ == '__main__':
    stations_config = pd.ExcelFile('inputdata.xlsx')
    sheet_names_list = stations_config.sheet_names

    for sheet in sheet_names_list:
        exec('{} = pd.DataFrame(stations_config.parse(sheet_name=sheet) )'.format(sheet))


def input_2_profile_evl(dis_location):
    """
    Read the data specified in the input file.

    :param dis_location: Location of the charging infrastructure from input.
    :type dis_location: str
    :return: Distribution of battery sizes, SOC at arrival, user type, arrival times
    """
    dis_ev_arr = globals()['Arr_Typ1'][dis_location].tolist()
    dis_user_type = [globals()['Ort1'][a].values.tolist() for a in globals()['Ort1'].columns]
    dis_soc = [globals()['SOC'][a].values.tolist() for a in globals()['SOC'].columns]
    dis_battery_size = [globals()['Batterysize'][a].values.tolist() for a in globals()['Batterysize'].columns]
    return dis_battery_size, dis_soc, dis_user_type, dis_ev_arr


def get_co2_emission(simulation_time):
    """
    Read the data specified in the input file.

    :param simulation_time: Total length of the simulation time.
    :type simulation_time: int
    :return: CO2 time series data.
    """
    co2_data = pd.concat([globals()['CO2_Emissions'][0:simulation_time // 60 + 1]], ignore_index=True)
    datetime_co2 = pd.date_range('2018-01-01', periods=len(co2_data), freq='H')
    co2_data['Time'] = datetime_co2 
    co2_data = co2_data.set_index('Time')
    co2_data = co2_data.resample('T')
    co2_data = co2_data.interpolate(method='linear')
    co2_data = [co2_data[a][:-1].values.tolist() for a in co2_data.columns]
    return co2_data


def get_energy_price(simulation_time):
    """
    Read the data specified in the input file.

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
    Read the data specified in the input file.

    :param simulation_time: Total length of the simulation time.
    :type simulation_time: int
    :return: Transformer preload time series data.
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
