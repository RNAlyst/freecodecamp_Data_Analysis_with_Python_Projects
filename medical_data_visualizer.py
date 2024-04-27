#!/usr/bin/env python

# Modules
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Functions
def goodbad( df: pd.DataFrame(), index: list, treshold: list = [1] ) -> pd.DataFrame():
    '''Turns the values of selected columns in a Pandas DataFrame to good (False) or bad (True).

    :param df: Pandas DataFrame
    :param index: List of indices for the targeted columns
    :param treshold: List of tresholds, if only one treshold is given, it will be used for all columns

    :return: Edited DataFrame
    '''
    if len( treshold ) == 1:
        for i in index:
            df[ i ] = df[ i ] > treshold[0]

    else:
        for i, t in zip( index, treshold ):
            df[ i ] = df[ i ] > treshold[ t ]

    return df

def bool2int( df: pd.DataFrame(), index: list ) -> pd.DataFrame():
    '''Turns the booleans (True and False) of certain columns in a Pandas DataFrame to integers (1 and 0 respectively).

    :param df: Pandas DataFrame
    :param index: List of indices for the column of target

    :return: Edited DataFrame
    '''

    for i in index:
        df[ i ] = df[ i ].astype(int)

    return df

def draw_cat_plot(df: pd.DataFrame() ) -> None:
    '''Shows and saves two bar plots, for cardio = 1 and = 0. Bars for 'active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke' for 0 and 1.'''

    # Convert df to long-form data 
    df_cat = pd.melt( df, id_vars= [ 'cardio' ], value_vars= [ 'active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke' ] )

    # 
    df_cat = df_cat.groupby( [ 'cardio', 'variable', 'value' ] ).size().reset_index( name='total' )
    df_cat[ 'value' ] = df_cat[ 'value' ].astype( str )
    fig = sns.catplot( data=df_cat, kind='bar', x='variable', y='total', hue='value', col='cardio' )
    fig.savefig( 'catplot.png' )
    return fig

def draw_heat_map( df: pd.DataFrame() ) -> None:
    '''Creates a heat map correlating all categories of the medical data.'''
    # Clean the data 
    df_heat = df[
        ( df[ 'ap_lo' ] <= df[ 'ap_hi' ] ) & 
        ( df[ 'height' ] >= df[ 'height' ].quantile( 0.025 ) ) & 
        ( df[ 'height' ] <= df[ 'height' ].quantile( 0.975 ) ) & 
        ( df[ 'weight' ] >= df[ 'weight' ].quantile( 0.025 ) ) & 
        ( df[ 'weight' ] <= df[ 'weight' ].quantile( 0.975 ) ) 
    ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu( corr )


    # Set up the matplotlib figure
    fig, ax =  plt.subplots()
    
    # Draw the heatmap with 'sns.heatmap()'
    ax = sns.heatmap( corr, mask=mask, annot=True, fmt='0.1f', square=True )


    # Do not modify the next two lines
    fig.savefig( 'heatmap.png' )
    return fig

# Code
df = pd.read_csv( 'medical_examination.csv' )
df['overweight'] = df[ 'weight' ] / (df[ 'height' ] / 100 ) ** 2 > 25
df = goodbad( df= df, index= [ 'cholesterol', 'gluc', ], treshold= [ 1 ] )
df = bool2int( df= df, index= ['overweight', 'cholesterol', 'gluc', ] )
draw_cat_plot( df )
draw_heat_map( df )
