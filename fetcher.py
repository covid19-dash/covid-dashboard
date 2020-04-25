"""
Fetch the data from Johns Hopkins' github
"""

import pandas as pd
import urllib

URL_BASE = (
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
    "csse_covid_19_data/csse_covid_19_time_series/"
)
FILENAME_JOHN_HOPKINS = {
    "confirmed": "time_series_covid19_confirmed_global.csv",
    "death": "time_series_covid19_deaths_global.csv",
}

URL_COUNTRY_ISO = (
    "https://gist.githubusercontent.com/tadast/8827699/raw/"
    "7255fdfbf292c592b75cf5f7a19c16ea59735f74/"
    "countries_codes_and_coordinates.csv"
)

MAP_UNMATCHED_COUNTRIES = {
    'Congo (Kinshasa)': "Congo, the Democratic Republic of the",
    "Cote d'Ivoire": "Côte d'Ivoire",
    'Czechia': "Czech Republic",
    'Eswatini': "Swaziland",
    'Holy See': "Italy",
    'Iran': "Iran, Islamic Republic of",
    'Korea, South': "South Korea",
    'Moldova': "Moldova, Republic of",
    'North Macedonia': "Macedonia, the former Yugoslav Republic of",
    'Reunion': "Réunion",
    'Taiwan*': "Taiwan",
    'US': "United States",
    'occupied Palestinian territory': "Palestinian Territory, Occupied",
}

MISSING_COUNTRIES = pd.DataFrame({
    "Country": ["Curacao"],
    "Alpha-2 code": ["CW"],
    "Alpha-3 code": ["CUW"],
    "Numeric code": [531.0],
    "Latitude (average)": [12.169570],
    "Longitude (average)": [-68.990021],
})

UNMATCHED_COUNTRIES = ['Cruise Ship']


def fetch_john_hopkins_data():
    df_covid = {
        key: pd.read_csv(urllib.request.urljoin(URL_BASE, filename))
        for key, filename in FILENAME_JOHN_HOPKINS.items()
    }
    columns_drop = ["Province/State", "Province_State",
                    "Lat", "Long", "Long_", "Population",
                    "UID", "iso2", "iso3", "code3", "FIPS", "Admin2",
                    ]
    for key in df_covid:
        for col in columns_drop:
            if col in df_covid[key].columns:
                df_covid[key] = df_covid[key].drop(columns=[col, ])
        df_covid[key] = df_covid[key].rename(
                            columns={'Country_Region': 'Country/Region'})
    for key in df_covid:
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
