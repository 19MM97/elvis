import pandas as pd 



stationconfig = pd.ExcelFile("inputdata.xlsx")
Sheet_names_list = stationconfig.sheet_names

for sheet in Sheet_names_list: exec('{} = pd.DataFrame(stationconfig.parse(sheet_name=sheet) )'.format(sheet))
#trafo_vorbelastung = pd.ExcelFile("preload.xlsx")
#Sheet_names_list = trafo_vorbelastung.sheet_names
#for sheet in Sheet_names_list: exec('{} = pd.DataFrame(trafo_vorbelastung.parse(sheet_name=sheet) )'.format(sheet))

def Input2profileEVL(disLocation):
    disDay = Arr_Typ1[disLocation].tolist()
    disUserTyp = [Ort1[a].values.tolist() for a in Ort1.columns]
    disSoc = [SOC[a].values.tolist() for a in SOC.columns]
    disBatterysize =[Batterysize[a].values.tolist() for a in Batterysize.columns]
    return disBatterysize, disSoc, disUserTyp, disDay


def co2_emission(simulationTime):
    co2_data = pd.concat([CO2_Emissions [0:simulationTime//60+1]] ,ignore_index=True)
    datetime_co2 = pd.date_range('2018-01-01',periods= len(co2_data), freq='H')
    co2_data['Time'] = datetime_co2 
    co2_data = co2_data.set_index('Time')
    co2_data = co2_data.resample('T')
    co2_data = co2_data.interpolate(method='linear')
    co2_data = [co2_data[a].values.tolist() for a in co2_data.columns]
    return co2_data[:-1]


#def Vorbelastung(simulationTime, control):
#    if control == 'UC': 
#        datetimepre = pd.date_range('2018-01-01', periods=simulationTime//10+1, freq='10T') 
#        vorbelastung = pd.concat([pre_load[0:(len(datetimepre))]], ignore_index=True)
#        vorbelastung['Time'] = datetimepre
#        vorbelastung = vorbelastung.set_index('Time') 
#        vorbelastung_resample = vorbelastung.resample('T')
#        vorbelastung_resample = vorbelastung_resample.interpolate(method='linear')
#        vorbelastung = vorbelastung_resample [:-1] 
#        vorbelastung.to_pickle("./vorbelastung.pkl")
#    else: 
#        vorbelastung = pd.read_pickle("./vorbelastung.pkl")
#    return  vorbelastung


def vorbelastung(assumptions, simulationTime, control):
    pre_load = Trafo_Vorbelastung
    datetimepre=pd.date_range('2018-01-01',periods=simulationTime//10+1, freq='10T') 
    vorbelastung = pd.concat([pre_load [0:(len(datetimepre))]]*1,ignore_index=True)
#    vorbelastung = vorbelastung[:-51]
    vorbelastung['Time'] = datetimepre
    vorbelastung = vorbelastung.set_index('Time') 
    vorbelastung_resample=vorbelastung.resample('T')
    vorbelastung_resample = vorbelastung_resample.interpolate(method='linear')
    vorbelastung = vorbelastung_resample [:-1]
    vorbelastung = [vorbelastung[a].values.tolist() for a in vorbelastung.columns]
#    vorbelastung.to_dict('list')
    return  vorbelastung

