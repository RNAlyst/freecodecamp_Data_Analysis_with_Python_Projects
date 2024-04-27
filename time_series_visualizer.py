#!/usr/bin/env python

# Modules
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import calendar

# Import data
df = pd.read_csv( 'fcc-forum-pageviews.csv', index_col= 0 )

# # Turn 2.5% highest and lowest values to NaN
df = df[
        ( df >= df.quantile( 0.025 ) ) & 
        ( df <= df.quantile( 0.975 ) )
    ]
# # Remove NaN
df.dropna(inplace=True)

# # Turn indices to datetimes
df.index = pd.to_datetime(df.index)

# Functions 
def draw_line_plot():
    '''Plots time against daily page views.'''    
    # Create a figure with a specified size
    fig = plt.figure(figsize=(10, 5))

    # Create an axes object associated with the figure
    ax = fig.add_subplot(1, 1, 1)  # 1 row, 1 column, plot number 1

    # Plot data onto the axes
    ax.plot(df.index, df, color='red')

    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    
    return fig

def draw_bar_plot():
    '''Illustrates average page views per day in each month in each year in a barplot.'''
    # constants
    MONTH_ORDER = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    CUSTOM_PALETTE = ['#ff0000', '#ff8000', '#ffff00', '#80ff00', '#00ff00', '#00ff80', '#00ffff', '#0080ff', '#0000ff', '#8000ff', '#ff00ff', '#ff0080', ]  # Rainbow custom palette 
    
    # group df by month
    df_monthly = df.copy()
    df_monthly = df_monthly.groupby(pd.Grouper(freq='M')).mean()

    # add a column with years and months
    df_monthly['Year'] = df_monthly.index.year.astype('category')
    df_monthly['Month'] = df_monthly.index.month.astype('category')

    # turn month number into month name
    df_monthly['Month'] = df_monthly['Month'].map(lambda x: calendar.month_name[x])

    # create and modify barplot
    fig = sns.catplot( data=df_monthly, kind='bar', x='Year', y='value', hue='Month', hue_order=MONTH_ORDER, palette= CUSTOM_PALETTE )
    plt.xlabel('Years') # Adding xlabel
    plt.ylabel('Average Page Views') # Adding ylabel
    plt.show()

    # Save image and return fig
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    '''Illustrates page views per day per year and per month in a boxplot.'''
    # Constants
    MONTH_ORDER = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    CUSTOM_PALETTE = ['#ff0000', '#ff8000', '#ffff00', '#80ff00', '#00ff00', '#00ff80', '#00ffff', '#0080ff', '#0000ff', '#8000ff', '#ff00ff', '#ff0080', ] # Rainbow custom palette

    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Create a figure with two subplots side by side
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Plot the first boxplot on the left subplot
    sns.boxplot(
        data=df_box, 
        x='year', 
        y='value', 
        ax=axes[0],
    )

    # Customize axes and titile
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    axes[0].set_title('Year-wise Box Plot (Trend)')

    # Plot the second boxplot on the right subplot
    sns.boxplot(
        data=df_box, 
        x='month', 
        y='value', 
        ax=axes[1], 
        order= MONTH_ORDER,
        palette= CUSTOM_PALETTE
    )
    # Customize axes and title
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    axes[1].set_title('Month-wise Box Plot (Seasonality)')

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

# Code
if __name__ == '__main__':
    fig_1 = draw_line_plot()
    fig_2 = draw_bar_plot()
    fig_3 = draw_box_plot()
