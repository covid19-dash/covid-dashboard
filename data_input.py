"""
Data massaging: prepare the data so that it is easy to plot it.
"""

from pycovid import pycovid

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

