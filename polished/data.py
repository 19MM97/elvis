import pandas as pd


station_config = pd.ExcelFile("inputdata.xlsx")
Sheet_names_list = station_config.sheet_names

for sheet in Sheet_names_list:
    exec('{} = pd.DataFrame(station_config.parse(sheet_name=sheet) )'.format(sheet))


def input_2_profile_evl(dis_location):

    dis_day = Arr_Typ1[dis_location].tolist()
    dis_user_type = [Ort1[a].values.tolist() for a in Ort1.columns]
    dis_soc = [SOC[a].values.tolist() for a in SOC.columns]
    dis_battery_size = [Batterysize[a].values.tolist() for a in Batterysize.columns]
    return dis_battery_size, dis_soc, dis_user_type, dis_day


def get_co2_emission(simulation_time):

    co2_data = pd.concat([CO2_Emissions[0:simulation_time // 60 + 1]], ignore_index=True)
    datetime_co2 = pd.date_range('2018-01-01', periods=len(co2_data), freq='H')
    co2_data['Time'] = datetime_co2
    co2_data = co2_data.set_index('Time')
    co2_data = co2_data.resample('T')
    co2_data = co2_data.interpolate(method='linear')
    co2_data = [co2_data[a][:-1].values.tolist() for a in co2_data.columns]

    return co2_data


def get_energy_price(simulation_time):

    price_data = pd.concat([Energy_Price[0:simulation_time // 60 + 1]], ignore_index=True)
    datetime_price = pd.date_range('2018-01-01', periods=len(price_data), freq='H')
    price_data['Time'] = datetime_price
    price_data = price_data.set_index('Time')
    price_data = price_data.resample('T')
    price_data = price_data.interpolate(method='linear')
    price_data = [price_data[a].values.tolist() for a in price_data.columns]

    return price_data[0][:-1]


def vorbelastung(simulation_time):

    pre_load = Trafo_Vorbelastung
    datetimepre = pd.date_range('2018-01-01', periods=simulation_time // 10 + 1, freq='10T')
    vorbelastung = pd.concat([pre_load[0:(len(datetimepre))]], ignore_index=True)
    vorbelastung['Time'] = datetimepre
    vorbelastung = vorbelastung.set_index('Time')
    vorbelastung_resample = vorbelastung.resample('T')
    vorbelastung_resample = vorbelastung_resample.interpolate(method='linear')
    vorbelastung = vorbelastung_resample[:-1]
    vorbelastung = [vorbelastung[a].values.tolist() for a in vorbelastung.columns]

    return vorbelastung
