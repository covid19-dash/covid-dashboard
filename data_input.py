"""
Data massaging: prepare the data so that it is easy to plot it.
"""

from pycovid import pycovid

def tidy_most_recent(df):
    df = df['confirmed'].reset_index().melt(id_vars='date')
    date_max = df['date'].max()
    df = df.query("date == @date_max")
    return df


def get_mapping():
    """ Returns mapping between country names (keys) and ISO codes (values).
    To be used for geo charts.
    """
    df = pycovid.getCovidCases()
    countries = df['name'].unique()
    # Ugly, could be faster
    mapping = {country: df.query("name == @country")['alpha-3'].unique()[0] 
                        for country in countries}
    return mapping


def get_data():
    """ Download the data and return it as a 'wide' data frame
    """
    df = pycovid.getCovidCases()
    df.rename(columns={"alpha-3": "iso"}, inplace=True)
    # The number of reported cases per day, country, and type
    df_day = df.groupby(['country_region', 'iso', 'date', 'type']).sum()

    # %%
    # The cumulative sum
    df_sum = df_day.groupby(['country_region', 'iso', 'type']
                            ).transform(lambda x: x.cumsum())['cases']
    df_sum = df_sum.reset_index()
    # %%
    # Switch to wide format (time series)
    data = df_sum.pivot_table(values='cases',
                              columns=['type', 'iso', 'country_region'],
                              index=['date'])
    data = data.fillna(method='ffill')
    return data

