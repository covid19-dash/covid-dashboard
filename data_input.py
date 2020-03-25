"""
Data massaging: prepare the data so that it is easy to plot it.
"""

import os
import pickle
import glob

import numpy as np
import pandas as pd

def tidy_most_recent(df, column='active'):
    df = df[column].reset_index().melt(id_vars='date')
    date_max = df['date'].max()
    df = df.query("date == @date_max")
    return df.sort_values('iso')




MAP_UNMATCHED_COUNTRIES = {
    'Bahamas, The': "Bahamas",
    'The Bahamas': "Bahamas",
    'Congo (Kinshasa)': "Democratic Republic of the Congo",
    "Congo, the Democratic Republic of the":
                            "Democratic Republic of the Congo",
    'Congo (Brazzaville)': 'Republic of the Congo',
    'Cape Verde': 'Cabo Verde',
    "Czech Republic": 'Czechia',
    "Cote d'Ivoire": 'Ivory Coast',
    "Côte d'Ivoire": 'Ivory Coast',
    "Swaziland": 'Eswatini',
    'The Gambia': 'Gambia',
    'Gambia, The': 'Gambia',
    'Hong Kong SAR': "Hong Kong",
    'Holy See': "Italy",
    "Iran, Islamic Republic of": 'Iran',
    'Iran (Islamic Republic of)': "Iran",
    'Korea, South': "South Korea",
    'Republic of Korea': "South Korea",
    'Macau': 'Macao',
    'Macao SAR': 'Macao',
    'Mainland China': 'China',
    "Moldova, Republic of": 'Moldova',
    'Republic of Moldova': "Moldova",
    'Republic of Ireland': 'Ireland',
    "Macedonia, the former Yugoslav Republic of": 'North Macedonia',
    "Réunion": 'Reunion',
    "Russian Federation": "Russia",
    "St. Martin": "Saint Martin",
    'Taiwan*': "Taiwan",
    'Taipei and environs': "Taiwan",
    'Timor-Leste': 'Timor Leste',
    'East Timor': 'Timor Leste',
    'US': "United States",
    'UK': 'United Kingdom',
    'North Ireland': 'United Kingdom',
    'occupied Palestinian territory': "Palestinian Territory",
    'Palestine': "Palestinian Territory",
    'Viet Nam': "Vietnam",
    'Vatican City': 'Vatican',
}

UNMATCHED_COUNTRIES = ['Cruise Ship', 'Others', 'Channel Islands']


def update_data():
    """ Update the data source
    """
    os.chdir('COVID-19')
    try:
        os.system('git pull')
    finally:
        os.chdir('..')


def get_data():
    # The population table we will merge with. We use it to check that
    # the names are properly formatted with their ISO3 code
    population_table = get_populations()
    daily_csvs = glob.glob(
        'COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/*.csv')
    daily_csvs.sort()
    all_days = list()
    for day in daily_csvs:
        day_data = pd.read_csv(day, skipinitialspace=True)
        # Some data wrangling to put in tidy wide form
        day_data = day_data.fillna(value=0)
        if 'Country/Region' in day_data.columns:
            country_column = 'Country/Region'
        else:
            country_column = 'Country_Region'
        day_data = day_data.replace({country_column:
                                     MAP_UNMATCHED_COUNTRIES})
        groupby = day_data.groupby(country_column)
        day_data = groupby['Confirmed', 'Deaths', 'Recovered'].sum()
        day_data.columns = ['confirmed', 'death', 'recovered']
        day_data = day_data.fillna(value=0)
        # Convert to wide with multiindex in column
        day_data = day_data.T.stack().to_frame().T
        for unknown in UNMATCHED_COUNTRIES:
            if unknown in day_data.columns.levels[1]:
                day_data = day_data.drop(unknown, axis=1, level=1)
        # retrieve the date from the filename
        day = pd.to_datetime(os.path.split(day)[-1][:-4])
        day_data['date'] = day
        day_data = day_data.set_index('date')
        all_days.append(day_data)
    all_days = pd.concat(all_days)
    # Check that all countries can be merged with our population table
    countries = all_days.columns.levels[1]
    correspondence = countries.isin(population_table['Country'])
    if not correspondence.all():
        missing_countries = all_days.columns.levels[1][np.logical_not(
            correspondence)]
        raise ValueError('The countries below are not recognized\n'
                         'Pease update the correspondence table %s'
                         % missing_countries)
    population_table = population_table.set_index('Country')
    iso3 = population_table['ISO3'].loc[countries].reset_index()
    iso3.columns = ['iso', 'country_region']
    new_columns = [(kind, p[1]['country_region'], p[1]['iso'])
                   for kind in all_days.columns.levels[0]
                   for p in iso3.iterrows()]
    all_days.columns = pd.MultiIndex.from_tuples(new_columns,
                    names=['type', 'iso', 'country_region'])
    all_days = all_days.fillna(value=0)

    # compute the active cases
    active = all_days['confirmed'] - all_days['death'] - all_days['recovered']
    # Add a level
    active = pd.concat(dict(active=active), axis=1)
    active.columns.names = all_days.columns.names
    all_days = pd.concat((all_days, active), axis=1)
    return all_days


def exec_full(filepath):
    """ Execute a Python file as a script
    """
    global_namespace = {
        "__file__": filepath,
        "__name__": "__main__",
    }
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), global_namespace)


def get_all_data():
    """ Retrieve both the actual data and the predictions from our model.
    """
    df = get_data() # all data
    df_tidy = tidy_most_recent(df) # most recent date, tidy format (one column for countries)
    df_tidy_table = df_tidy[['country_region', 'value']] # keep only two columns for Dash DataTable

    if not os.path.exists('predictions.pkl'):
        print('Running the model')
        exec_full('modeling.py')
    with open('predictions.pkl', 'rb') as f_pkl:
        df_prediction = pickle.load(f_pkl)
    return df, df_prediction


def get_populations():
    """ Load the information that we have about countries """
    pop = pd.read_csv('data/countryInfo.txt', sep='\t', skiprows=50)
    return pop


def normalize_by_population(tidy_df):
    """ Normalize by population the column "value" of a dataframe with
        lines being the country ISO
    """
    pop = get_populations()
    normalized_values = (tidy_df.set_index('iso')['value']
                         / pop.set_index('ISO3')['Population'])

    # NAs appeared because we don't have data for all entries of the pop
    # table
    normalized_values = normalized_values.dropna()
    assert len(normalized_values) == len(tidy_df),\
        ("Not every country in the given dataframe was found in our "
         "database of populations")
    return normalized_values


if __name__ == "__main__":
    # Basic code to check that we can still do the entity matching
    # between the different databases
    df = get_data()
    tidy_df = tidy_most_recent(df)
    normalized_values = normalize_by_population(tidy_df)

