"""
Data massaging: prepare the data so that it is easy to plot it.
"""

from fetcher import fetch_john_hopkins_data
import pandas as pd


def tidy_most_recent(df):
    df = df['confirmed'].reset_index().melt(id_vars='date')
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

    # %%
    # The cumulative sum
    df_sum = df_day.groupby([
        'country_region', 'iso', 'type']
    ).transform(lambda x: x.cumsum())['cases']
    df_sum = df_sum.reset_index()
    # %%
    # Switch to wide format (time series)
    data = df_sum.pivot_table(values='cases',
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
