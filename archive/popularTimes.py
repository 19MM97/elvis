# -*- coding: utf-8 -*-
"""
Created on Fri May 31 11:07:05 2019

@author: Leo77
"""

import populartimes
import csv

# print(populartimes.get_id('AIzaSyA9HfJMu0p-RYI5uZvF-uaOSsSgPOenAB8', 'ChIJSYuuSx9awokRyrrOFTGg0GY'))

# print(populartimes.get('AIzaSyA9HfJMu0p-RYI5uZvF-uaOSsSgPOenAB8', ['bar'],
#                        (48.132986, 11.566126), (48.142199, 11.580047)))


def popular_time_id(id_):
    """

    :param id_:
    :return:
    """
    data = populartimes.get_id('AIzaSyC5tGMwgvsyi5HZBZ_6bo__KLhBxVEOlGs', id_)

    with open('popularTime.csv', 'a+', newline='', encoding='UTF-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        column_title_row = ['Time', data['name']]
        csv_writer.writerow(column_title_row)
        for i in range(len(data['populartimes'])):
            for j in range(24):
                if j < 10:
                    time = data['populartimes'][i]['name'] + ' 0' + str(j) + ':00'
                else:
                    time = data['populartimes'][i]['name'] + ' ' + str(j) + ':00'
                row = [time, data['populartimes'][i]['data'][j]]
                csv_writer.writerow(row)       
        time_spent = ['Time Spent', str(data['time_spent'][0]) + '~' + str(data['time_spent'][1])]
        csv_writer.writerow(time_spent)
                
#    for key in data.keys():
       

def populartime_position(types, bound_lower, bound_upper):
    """

    :param types:
    :param bound_lower:
    :param bound_upper:
    :return:
    """
    data = populartimes.get('AIzaSyA9HfJMu0p-RYI5uZvF-uaOSsSgPOenAB8', types, bound_lower, bound_upper)

    time_spent = 0
    if len(data) == 0:
        distribution = 0
    else:
        distribution = []
        if len(data) == 1:
            for i in range(len(data['populartimes'])):
                for j in range(len(data['populartimes'][i]['data'])):
                    distribution.append(data['populartimes'][i]['data'][j])
            if 'time_spent' not in data:
                time_spent = 0
            else:
                time_spent = data['time_spent']
        else:
            for i in range(len(data[0]['populartimes'])):
                for j in range(len(data[0]['populartimes'][i]['data'])):
                    distribution.append(data[0]['populartimes'][i]['data'][j])
            if 'time_spent' not in data[0]:
                time_spent = 0
            else:
                time_spent = data[0]['time_spent']
    return distribution, time_spent


''' writing to csv file
    with open('popularTime1.csv', 'a+', newline='',encoding='UTF-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        columnTitleRow = ['Time']
        for i in range(len(data)):
            columnTitleRow.append(data[i]['name'])
        csv_writer.writerow(columnTitleRow)
        for i in range(len(data[0]['populartimes'])):
            for j in range(24):
                if j < 10:
                    time = data[0]['populartimes'][i]['name'] + ' 0' + str(j) + ':00'
                else:
                    time  = data[0]['populartimes'][i]['name'] + ' ' + str(j) + ':00'
                row = [time]
                for k in range(len(data)):
                    row.append(data[k]['populartimes'][i]['data'][j])
                csv_writer.writerow(row)
        time_spent = ['Time Spent']
        for i in range(len(data)):
            if 'time_spent' not in data[i]:
                interval = 'not available'                
            else:
                interval = str(data[i]['time_spent'][0]) + '~' + str(data[i]['time_spent'][1])  
            time_spent.append(interval)
        csv_writer.writerow(time_spent)
'''

# populartime_ID('ChIJSYuuSx9awokRyrrOFTGg0GY')
# populartime_position('ChIJSYuuSx9awokRyrrOFTGg0GY', ['bar'], (48.132986, 11.566126), (48.142199, 11.580047))
