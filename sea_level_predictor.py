#!/usr/bin/env python
# Modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Function
def draw_plot( year_threshold: int = 2000, year_predict: int = 2050 ) -> plt.axes:
    '''Illustrates the rise in sea level. 
    
    :param year_treshold: Treshold for the years considered for the second linear regression.
    :param year_predict: Year of which the sea level should be predicted
    :return: Plot illustrating the rise in sea level.'''

    # Read data from file
    df = pd.read_csv( 'epa-sea-level.csv')

    # Create scatter plot
    plt.scatter( x= df['Year'], y= df['CSIRO Adjusted Sea Level'], marker= '.', color= 'black')


    # Create first line of best fit

    # # Determine lowest and highest year of the data
    df_min = df['Year'].min()
    df_max = df['Year'].max()

    # # Linear regression
    params = linregress( x=df['Year'], y=df['CSIRO Adjusted Sea Level' ] )
    slope = params[0]
    intercept = params[1]

    # # Create values of linear regression, predict sea level in 2050
    x = np.arange( df_min, year_predict + 1 )
    y = intercept + slope * x
    sea_level_2050 = round( y.max(), 1 )
    print(f"Based on a linear regression from {df_min} to {df_max}, the sea level will rise to {sea_level_2050} by {year_predict}." )
    # # Plot linear regression
    plt.plot( x, y, ls= '--', color= 'blue')


    # Create second line of best fit

    # # Select data based on treshold
    df_2 = df[ df['Year'] >= year_threshold ]

    # # Determine lowest and highest year of the data
    df_2_min = df_2['Year'].min()
    df_2_max = df_2['Year'].max()

    # # Linear regression
    params_2 = linregress( x=df_2['Year'], y=df_2['CSIRO Adjusted Sea Level' ] )
    slope_2 = params_2[0]
    intercept_2 = params_2[1]

    # # Create values of linear regression, predict sea level in 2050
    x_2 = np.arange(year_threshold, year_predict + 1 )
    y_2 = intercept_2 + slope_2 * x_2
    sea_level_2050_2 = round( y_2.max(), 1 )
    print(f"Based on a linear regression from {df_2_min} to {df_2_max}, the sea level will rise to {sea_level_2050_2} by {year_predict}." )
    # # Plot linear regression
    plt.plot( x_2, y_2, ls= '-.', color= 'orange' )

    # Add labels and title
    plt.legend( ['CSIRO Adjusted Sea Level', 'Linear Regression from 1880 to 2013', 'Linear Regression from 2000 to 2013' ])
    plt.xlabel( 'Year' )
    plt.ylabel( 'Sea Level (inches)' )
    plt.title( 'Rise in Sea Level' )
    
    # Save plot and return data for testing
    plt.savefig('sea_level_plot.png')
    return plt.gca()

# Code
fig = draw_plot()
