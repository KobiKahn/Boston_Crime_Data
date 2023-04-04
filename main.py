import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# plt.style.use('seaborn')
# plt.style.use('fivethirtyeight')
# plt.style.use('dark_background')
plt.style.use('Solarize_Light2')
import math
import statistics as stats
import random


# FUNCTIONS




# VARIABLES AND STARTING STUFF
crime_df = pd.read_csv('Jacob Kahn - crime.csv', delim_whitespace=False, encoding="latin1")

code_group = list(crime_df['OFFENSE_CODE_GROUP'])

district_crime_dict = {}
crime_list = []
crime_dict = {}
big_crime_dict = {}
i = -1
for district in crime_df['DISTRICT']:
    i += 1
    if district in district_crime_dict.keys():
        district_crime_dict[district].append(code_group[i])
    else:
        district_crime_dict[district] = [(code_group[i])]
    if code_group[i] not in crime_list:
        crime_list.append(code_group[i])
x = 0
crime_num = 0
for key, val in district_crime_dict.items():
    crime_dict = {}
    for crime in crime_list:
        crime_num = district_crime_dict[key].count(crime)
        crime_dict[crime] = crime_num
    big_crime_dict[key] = crime_dict

final_dict = {}
for key1, dict in big_crime_dict.items():
    min_list = []
    for key2, val in dict.items():
        min_list.append(val)
    final_dict[key1] = max(min_list)


print(final_dict)
y = []
x = []

for key, val in final_dict.items():
    x.append(key)
    y.append(val)


plt.scatter(x, y)
plt.show()
# print(big_crime_dict)

