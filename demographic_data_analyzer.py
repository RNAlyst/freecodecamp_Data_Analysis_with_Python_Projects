#!/usr/bin/env python

# Modules
import pandas as pd
import sys
import os

# Functions
def calculate_demographic_data( print_data: bool = True, filepath: str = "adult.data.csv", sep: str = ',' ) -> dict:
    '''
    Calculates the following parameters from a given filename with demographic data.
    
    :param:
    print_data      bool if calculates parameters should be printed
    filepath        path leading to the csv file with the demographic data
    sep             separator in the csv file

    :return:
    dict{
        'race_count':               # Pandas Series with number of each race
        'average_age_men':          # Average age of men
        'percentage_bachelors':     # Percentage with Bachelors degrees
        'higher_education_rich':    # Percentage with higher education that earn >50K
        'lower_education_rich':     # Percentage without higher education that earn >50K
        'min_work_hours':           # Min work time in hrs per week
        'rich_percentage':          # Percentage of rich among those who work fewest hours
        'highest_earning_country':              # Country with highest percentage of rich people
        'highest_earning_country_percentage':   # Highest percentage of rich people among all countries
        'top_IN_occupation':                    # Top occupation of rich people in India
    }
    '''
    # Read data from file
    df = pd.read_csv( filepath, sep= sep)

    # Total number of entries
    tot = df.shape[0]

    # Pandas Series with number of each race
    race_count = df['race'].value_counts()

    # Average age of men
    average_age_men = round( df[df['sex'] == 'Male']['age'].mean(), 1 )

    # Percentage of people with a Bachelor's degrees
    percentage_bachelors = round( df['education'].value_counts()['Bachelors'] / tot * 100, 1 )

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # maks for with and without `Bachelors`, `Masters`, or `Doctorate`
    mask_higher_education = (df['education'] == 'Bachelors') | (df['education'] == 'Masters') | (df['education'] == 'Doctorate' )
    mask_lower_education = (df['education'] != 'Bachelors') & (df['education'] != 'Masters') & (df['education'] != 'Doctorate' )

    # Percentage with or without higher education that earn >50K
    df_rich = df[ df['salary'] == '>50K' ]
    higher_education_rich = round( df_rich['education'][ mask_higher_education].shape[0] / tot * 100, 1 )
    lower_education_rich = round( df_rich['education'][mask_lower_education].shape[0] / tot * 100, 1 )

    # Min work time in hrs per week
    min_work_hours = df['hours-per-week'].min()

    # Percentage of rich among those who work fewest hours
    num_min_workers = df['hours-per-week'][ df['hours-per-week'] == min_work_hours ].shape[0]
    num_min_workers_rich = df_rich[ df_rich['hours-per-week'] == min_work_hours ].shape[0]
    rich_percentage = round( num_min_workers_rich / num_min_workers * 100, 1 )

    # Country with highest percentage of rich people and Highest percentage of rich people among all countries
    rich_ratio = df_rich['native-country'].value_counts() / df['native-country'].value_counts()
    highest_earning_country = rich_ratio.idxmax()
    highest_earning_country_percentage = round( rich_ratio.max() * 100, 1 )

    # Top occupation of rich people in India
    top_IN_occupation = df_rich[ df_rich['native-country'] == 'India' ]['occupation'].value_counts().idxmax()

    # Optional print-out
    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations of rich people in India:", top_IN_occupation)

    # Return
    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

def dict2csv( dictionary: dict ) -> None:
    '''
    Saves a dictionary to a csv output file.

    :param dictionary: dictionary
    :return: None
    '''
    df = pd.DataFrame( dictionary, index= [0] )

    i = 1
    while True:
        try:
            df.to_csv(f"output_{i}_demographic_data_analyzer.csv", index=False)
            break
        except PermissionError:
            i += 1

# Main
if __name__ == '__main__':

    if len(sys.argv)!= 2:
        print("Usage: python myscript.py <filename>")

    elif not os.path.isfile(sys.argv[1]):
        print(f"Error: The file '{sys.argv[1]}' does not exist.")

    else:
        dict2csv( calculate_demographic_data() )
