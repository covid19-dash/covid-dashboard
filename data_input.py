"""
Data massaging: prepare the data so that it is easy to plot it.
"""

import os
import pickle

import pandas as pd

from fetcher import fetch_john_hopkins_data

def tidy_most_recent(df, column='confirmed'):
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




def get_data():
    """ Download the data and return it as a 'wide' data frame
    """
    df = fetch_john_hopkins_data()
    # The number of reported cases per day, country, and type
    df_day = df.groupby(['country_region', 'iso', 'date', 'type']).sum()

    # Switch to wide format (time series)
    data = df_day.pivot_table(values='cases',
                              columns=['type', 'iso', 'country_region'],
                              index=['date'])
    data = data.fillna(method='ffill')
    data = data.fillna(value=0)

    return data


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

    if not os.path.exists('predictions.pkl'):
        print('Running the model')
        exec_full('modeling.py')
    with open('predictions.pkl', 'rb') as f_pkl:
        df_prediction = pickle.load(f_pkl)
    # MultiIndex does not pickle, hence we need to rebuild it
    for p in df_prediction.values():
        p.columns = pd.MultiIndex.from_tuples(p.columns,
                                              names=('iso', 'country'))
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


def normalize_by_population_wide(df):
    """ Normalize by population the columns of a dataframe with
        column names being the country iso
    """
    pop = get_populations()
    # Grap a series, indexed by "iso"
    pop = pop.rename(dict(ISO3='iso'), axis=1).set_index('iso')['Population']
    # Use the ".div" for the divison because it support explicit
    # alignement
    normalized_df = df.div(pop, level='iso', axis=1)

    return normalized_df

if __name__ == "__main__":
    # Basic code to check that we can still do the entity matching
    # between the different databases
    df = get_data()
    tidy_df = tidy_most_recent(df)
    normalized_values = normalize_by_population(tidy_df)

