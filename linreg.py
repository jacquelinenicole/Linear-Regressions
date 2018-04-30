# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 02:44:56 2018

@author: Jackie

Column    Stat

1         StoreID
2         Date
3         Day of Week
4         Lunch/Dinner
5         Overall Score
6         Wait time
7         Knowledge
8         Friendliness
9         Attentiveness
10        Cleanliness
11        Comfort
12        Problem?
13        Problem Resolution
14        Value
15        Return Likelihood
16        Recommend Likelihood
17        Visit # past 3 months
18        Gender
19        Age Group
20        Income Group
21        RegionId
22        DivisionId
23        Promotion
24        Promotion Year
"""


import numpy as np
import pandas as pd
import math


# create DataFrame
df = pd.read_csv(open("GSS_Experience_Metadata.csv", "rb"))


# y-intercept formula
def get_b(x_sum, y_sum, xs_sum, xy_sum, xsum_squared, sample_size):
    return ((y_sum * xs_sum) - (x_sum * xy_sum))/((sample_size * xs_sum) - xsum_squared)

# slope formula
def get_m(x_sum, y_sum, xs_sum, xy_sum, xsum_squared, sample_size):
    return ((sample_size * xy_sum) - (x_sum * y_sum))/((sample_size * xs_sum) - (xsum_squared))

# r formula
def get_r(x_sum, y_sum, xs_sum, ys_sum, xy_sum, xsum_squared, ysum_squared, sample_size):
    return ((sample_size * xy_sum) - (x_sum * y_sum))/math.sqrt(((sample_size * xs_sum) - (xsum_squared))*((sample_size * ys_sum) - (ysum_squared)))

# gets numbers needed to compute b, m, or r
def format_data(x, y, letter):    
    for i in range(len(x)):
        x[i] = int(x[i])
        y[i] = int(y[i])

    x_y_sum = 0
    x_squared_sum = 0
    y_squared_sum = 0
    
    for i in range(len(x)):
        x_y_sum += (x[i] * y[i])
        y_squared_sum += (y[i]*y[i])
        x_squared_sum += (x[i]*x[i])
        
    if letter == 'b':
        return get_b(sum(x), sum(y), x_squared_sum, x_y_sum, sum(x) * sum(x), len(x))
    
    elif letter == 'm':
        return get_m(sum(x), sum(y), x_squared_sum, x_y_sum, sum(x) * sum(x), len(x))
    
    elif letter == 'r':
        return get_r(sum(x), sum(y), x_squared_sum, y_squared_sum, x_y_sum, sum(x) * sum(x), sum(y) * sum(y), len(x))
    
    else:
        return "Invalid character"
    
def print_helper(col_name, x, y):
    b = format_data(x, y, 'b')
    m = format_data(x, y, 'm')
    r_squared = pow(format_data(x, y, 'r'), 2)
    print("\n-- " + str(col_name) + " --")
    print("Equation: y = " + str(m) + "x + " + str(b))
    print("Coefficient of Determination (r^2): " + str(r_squared))

def get_data(col_name):
    x = []
    y = []
    counter = 0
    
    for row in df[col_name]:
        if row == ' ' or df.iloc[counter, 4] == ' ':
            pass
        
        else:
            x.append(row)
            y.append(df.iloc[counter, 4])
        
        counter += 1
    
    return x, y
    


get_data("Knowledge")
get_data("Friendliness")
get_data("Server Attentiveness")
get_data("Overall Cleanliness")
get_data("Overall Comfort")
get_data("Value for Money")

print_helper(col_name, x, y)