"""
Fetch the data from Johns Hopkins' github
"""

import pandas as pd
import urllib
import os
import glob
import numpy as np

URL_BASE = (
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
    "csse_covid_19_data/csse_covid_19_time_series/"
)
FILENAME_JOHN_HOPKINS = {
    "confirmed": "time_series_19-covid-Confirmed.csv",
    "death": "time_series_19-covid-Deaths.csv",
    "recovered": "time_series_19-covid-Recovered.csv",
}

URL_COUNTRY_ISO = (
    "https://gist.githubusercontent.com/tadast/8827699/raw/"
    "7255fdfbf292c592b75cf5f7a19c16ea59735f74/"
    "countries_codes_and_coordinates.csv"
)

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

MISSING_COUNTRIES = pd.DataFrame({
    "Country": ["Curacao"],
    "Alpha-2 code": ["CW"],
    "Alpha-3 code": ["CUW"],
    "Numeric code": [531.0],
    "Latitude (average)": [12.169570],
    "Longitude (average)": [-68.990021],
})

UNMATCHED_COUNTRIES = ['Cruise Ship', 'Others', 'Channel Islands']


def update_data():
    """ Update the data source
    """
    os.chdir('COVID-19')
    try:
        os.system('git pull')
    finally:
        os.chdir('..')


def read_data():
    import data_input
    # The population table we will merge with. We use it to check that
    # the names are properly formatted with their ISO3 code
    population_table = data_input.get_populations()
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
        day_data.columns = [c.lower() for c in day_data.columns]
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
    correspondence = all_days.columns.levels[1].isin(
        population_table['Country'])
    if not correspondence.all():
        missing_countries = all_days.columns.levels[1][np.logical_not(
            correspondence)]
        raise ValueError('The countries below are not recognized\n' 
                         'Pease update the correspondence table %s'
                         % missing_countries)
    return all_days


def fetch_john_hopkins_data():
    df_covid = {
        key: pd.read_csv(urllib.request.urljoin(URL_BASE, filename))
        for key, filename in FILENAME_JOHN_HOPKINS.items()
    }
    columns_drop = ["Province/State", "Lat", "Long"]
    for key in df_covid:
        df_covid[key] = df_covid[key].drop(columns=columns_drop)
        df_covid[key] = df_covid[key].groupby("Country/Region").sum()
        # move each date column as a row entry to get a "date" column instead
        df_covid[key] = df_covid[key].stack().to_frame().reset_index().rename(
            columns={"level_1": "date", 0: "cases"}
        )
        df_covid[key]["date"] = df_covid[key]["date"].apply(
            lambda x: pd.to_datetime(x)
        )
        df_covid[key]["type"] = key
    df_covid = pd.concat(df_covid.values(), ignore_index=True)
    df_covid = df_covid.replace({"Country/Region": MAP_UNMATCHED_COUNTRIES})

    df_countries = pd.read_csv(URL_COUNTRY_ISO)
    for col_name in df_countries.columns:
        df_countries[col_name] = df_countries[col_name].str.strip('. "."')
    float_column = [
        "Numeric code", "Latitude (average)", "Longitude (average)"
    ]
    df_countries[float_column] = df_countries[float_column].astype(float)
    df_countries = pd.concat(
        [df_countries, MISSING_COUNTRIES], ignore_index=True
    )

    df = pd.merge(
        left=df_covid,
        right=df_countries,
        left_on="Country/Region",
        right_on="Country",
        how="inner",
    )

    assert df["Country"].unique().shape[0] >= 143, \
        "Missing countries when making the merge: not enough countries"
    assert 'China' in df["Country"].unique(), \
        "Missing countries when making the merge: China missing"
    assert 'South Korea' in df["Country"].unique(), \
        "Missing countries when making the merge: South Korea missing"

    df = df.rename(
        columns={
            "Country/Region": "name",
            "Country": "country_region",
            "Alpha-3 code": "iso",
            "Latitude (average)": "lat",
            "Longitude (average)": "long",
        }
    )

    return df
