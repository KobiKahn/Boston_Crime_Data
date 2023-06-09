import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import folium
from collections import OrderedDict
# plt.style.use('seaborn')
# plt.style.use('fivethirtyeight')
# plt.style.use('dark_background')
plt.style.use('Solarize_Light2')
import math
import statistics as stats
import random


# FUNCTIONS

def month_crimes(year):
    # GET THE CORRECT DATAFRAME FOR THAT YEAR AND EACH MONTH
    year_df = crime_df
    i_list = crime_df.index[crime_df['YEAR'] != year].tolist()
    year_df = year_df.drop(i_list)
    year_df = year_df.reset_index()
    month_dict = {}
    i = -1
    for month in year_df['MONTH']:
        i += 1
        if month not in month_dict.keys():
            month_dict[month] = []
        month_dict[month].append(i)

    # SORT THE MONTH DICTIONARY BY KEYS
    month_keys = list(month_dict.keys())
    month_keys.sort()
    month_dict = {i: month_dict[i] for i in month_keys}

    # GRAPH THE MONTH AND GET X AND Y VARIABLES
    month_count = []
    final_dict = {}

    for key, val in month_dict.items():
        week_dict = {'Sunday': 0, 'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0}
        month_count.append(len(month_dict[key]))
        for i in val:
            D_O_W = year_df.loc[i, 'DAY_OF_WEEK']
            week_dict[D_O_W] += 1
        final_dict[key] = week_dict
    # print(final_dict)
    for key, dict in final_dict.items():
        name = f'CRIMES COMMITTED PER DAY IN MONTH #{key}'
        week_list = []
        key_list = []
        for key, val in dict.items():
            week_list.append(val)
            key_list.append(key)
        graph_bar(key_list, week_list, name)
    graph_bar(month_keys, month_count, f'CRIMES COMMITTED EVERY MONTH FOR {year}')


def graph_bar(x_list, y_list, name):
    plt.rcParams["figure.figsize"] = (10, 5)
    x = np.arange(len(x_list))
    plt.bar(x, y_list)
    plt.xticks(x, x_list)
    plt.title(name)
    plt.show()


def top_5(key_district):
    boston_districts = {'Downtown': 'A1', 'Charleston': 'A15',
                        'East Boston': 'A7', 'Roxbury': 'B2',
                        'Mattapan': 'B3', 'South Boston': 'C6',
                        'Dorchester': 'C11', 'South End': 'D4',
                        'Brighton': 'D14', 'West Roxbury': 'E5',
                        'Jamaica Plain': 'E13', 'Hyde Park': 'E18'}
    district = boston_districts[key_district]
    offense_df = crime_df
    i_list = offense_df.index[offense_df['DISTRICT'] != district].tolist()
    spec_df = offense_df
    spec_df = spec_df.drop(i_list)
    spec_df = spec_df.reset_index()
    crime_list = spec_df['OFFENSE_CODE_GROUP']
    crime_dict = {}
    for crime in crime_list:
        if crime in crime_dict.keys():
            crime_dict[crime] += 1
        else:
            crime_dict[crime] = 0
    # {k: v for k, v in sorted(crime_dict.items(), key=lambda item: item[1])}
    crime_dict = dict(sorted(crime_dict.items(), key=lambda item: item[1]))
    top_5_crimes = list(crime_dict)[-5:]
    top_5_crimes = ', '.join(top_5_crimes)
    print(f'THE TOP 5 CRIMES IN {key_district} ARE: {top_5_crimes}')
    # print(crime_dict)



def plot_map(district, crime, all=False):
    boston_districts = {'Downtown': 'A1', 'Charleston': 'A15',
                        'East Boston': 'A7', 'Roxbury': 'B2',
                        'Mattapan': 'B3', 'South Boston': 'C6',
                        'Dorchester': 'C11', 'South End': 'D4',
                        'Brighton': 'D14', 'West Roxbury': 'E5',
                        'Jamaica Plain': 'E13', 'Hyde Park': 'E18'}
    offense_df = crime_df[crime_df['OFFENSE_CODE_GROUP'] == crime]
    if all:
        lat_list = list(offense_df['Lat'].dropna())
        long_list = list(offense_df['Long'].dropna())
        type_list = list(offense_df['OFFENSE_DESCRIPTION'])
    else:
        spec_df = offense_df
        key_district = boston_districts[district]
        i_list = offense_df.index[offense_df['DISTRICT'] != key_district].tolist()
        spec_df = spec_df.drop(i_list)
        spec_df = spec_df.reset_index()
        lat_list = list(spec_df['Lat'].dropna())
        long_list = list(spec_df['Long'].dropna())
        type_list = list(spec_df['OFFENSE_DESCRIPTION'])

    m = folium.Map([42.32, -71.0589], zoom_start=12)
    for val in range(len(lat_list)):
        folium.Marker(location=(lat_list[val], long_list[val]), popup=type_list[val]).add_to(m)
    m.save('index.html')

# VARIABLES AND STARTING STUFF
crime_df = pd.read_csv('Jacob Kahn - crime.csv', delim_whitespace=False, encoding="latin1")
code_group = list(crime_df['OFFENSE_CODE_GROUP'])
# month_crimes(2017)

#########################
# PROJECT TWO OF PLOTTING##
##########################
plot_map('Jamaica Plain', 'Other')


# FIND TOP 5 CRIMES IN EACH DISTRICT
top_5('Jamaica Plain')



