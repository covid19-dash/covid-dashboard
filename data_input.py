"""
Data massaging: prepare the data so that it is easy to plot it.
"""

from fetcher import fetch_john_hopkins_data
import pandas as pd
import os
import pickle

def tidy_most_recent(df, column='active'):
    df = df[column].reset_index().melt(id_vars='date')
    date_max = df['date'].max()
    df = df.query("date == @date_max")
    return df


def get_mapping():
    """ Returns mapping between country names (keys) and ISO codes (values).
    To be used for geo charts.
    """
    df = fetch_john_hopkins_data()
    countries = df['name'].unique()
    # Ugly, could be faster
    mapping = {country: df.query("name == @country")['iso'].unique()[0]
               for country in countries}
    return mapping


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

    # Align columns and compute active cases
    death, recovered = data['death'].align(
        data['recovered'], join='outer', fill_value=0
    )
    inactive = death + recovered
    confirmed, inactive = data['confirmed'].align(
        inactive, join='outer', fill_value=0
    )

    active = confirmed - inactive
    # Add a level
    active = pd.concat(dict(active=active), axis=1)
    active.columns.names = ['type', 'iso', 'country_region']
    data = pd.concat((data, active), axis=1)
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
    mapping = get_mapping()
    df_tidy = tidy_most_recent(df) # most recent date, tidy format (one column for countries)
    df_tidy_table = df_tidy[['country_region', 'value']] # keep only two columns for Dash DataTable

    if not os.path.exists('predictions.pkl'):
        print('Running the model')
        exec_full('modeling.py')
    with open('predictions.pkl', 'rb') as f_pkl:
        df_prediction = pickle.load(f_pkl)
    return df, df_prediction, mapping
