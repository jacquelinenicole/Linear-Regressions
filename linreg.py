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

import pandas as pd
import math

# create DataFrame
df = pd.read_csv(open("GSS_Experience_Metadata.csv", "rb"))

# y-intercept formula
def get_b(x_sum, y_sum, xs_sum, xy_sum, xsum_squared, sample_size):
    return ((y_sum * xs_sum) - (x_sum * xy_sum))/((sample_size * xs_sum) - xsum_squared)

# regression coefficient formula
def get_m(x_sum, y_sum, xs_sum, xy_sum, xsum_squared, sample_size):
    return ((sample_size * xy_sum) - (x_sum * y_sum))/((sample_size * xs_sum) - (xsum_squared))

# r formula
def get_r(x_sum, y_sum, xs_sum, ys_sum, xy_sum, xsum_squared, ysum_squared, sample_size):
    return ((sample_size * xy_sum) - (x_sum * y_sum))/math.sqrt(((sample_size * xs_sum) - (xsum_squared))*((sample_size * ys_sum) - (ysum_squared)))

# standard error formula
def get_std_err(x, sample_size):
    return get_std_dev(x, sample_size)/math.sqrt(sample_size)

def get_std_dev(x, sample_size):
    mean = get_mean(x, sample_size)
    summed = 0
    
    for data_point in x:
        summed += pow(data_point-mean, 2)
    
    return math.sqrt(summed/(sample_size-1))
    
def get_mean(sample_data, sample_size):
    return sum(sample_data)/sample_size

# gets numbers needed to compute b, m, and r
def format_data(x, y):    
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
        
    return get_b(sum(x), sum(y), x_squared_sum, x_y_sum, sum(x) * sum(x), len(x)), get_m(sum(x), sum(y), x_squared_sum, x_y_sum, sum(x) * sum(x), len(x)), get_r(sum(x), sum(y), x_squared_sum, y_squared_sum, x_y_sum, sum(x) * sum(x), sum(y) * sum(y), len(x))

def print_helper(col_name, x, y):
    b, m, r = format_data(x, y)
    r_squared = pow(r, 2)
    print("\n-- " + str(col_name) + " --")
    
    # rounds numbers so output is easier to read
    m = round(m, 3)
    b = round(b, 3)
    r_squared = round(r_squared, 3)
    
    if b < 0:
        print("Equation: y = " + str(m) + "x - " + str(b*-1))
    else:
        print("Equation: y = " + str(m) + "x + " + str(b))
    
    print("Coefficient of Determination (r^2): " + str(r_squared))
    
def create_data_array(col_name):
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

def multi_create_data_array(x_list, y_loc):
    x = []
    y = []
    
    # columns to check
    cols = [6, 7, 8, 9, 10, 13]
    
    for i in range(len(df[x_list[0]])):
        # if dependent variable was left blank, skip
        if df.iloc[i, y_loc] == ' ':
            continue
        
        # reset
        curr_val = 0
        flag = 0
        
        for col in cols:
            # make sure no column is blank
            if df.iloc[i, col] == ' ':
                flag = 1
                break
            else: 
                curr_val += int(df.iloc[i, col])
        
        # only append scores if all areas were scored
        if flag != 1:
            x.append(curr_val/len(x_list))
            y.append(df.iloc[i, y_loc])
    
    return x, y


columns = ['Knowledge', 'Friendliness', 'Server Attentiveness', 'Overall Cleanliness', 
           'Overall Comfort', 'Value for Money']

# individual regressions
for col in columns:
    x, y = create_data_array(col)
    print_helper(col, x, y)

# combined regression
x, y = multi_create_data_array(columns, 4)
print_helper("Overall", x, y)
