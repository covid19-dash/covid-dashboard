import os
import pandas as pd

URL_BASE = (
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
    "csse_covid_19_data/csse_covid_19_time_series"
)
FILENAME_JOHN_HOPKINS = {
    "confirmed": "time_series_19-covid-Confirmed.csv",
    "deaths": "time_series_19-covid-Deaths.csv",
    "recovered": "time_series_19-covid-Recovered.csv",
}

URL_COUNTRY_ISO = (
    "https://raw.githubusercontent.com/lukes/"
    "ISO-3166-Countries-with-Regional-Codes/master/slim-3/slim-3.csv"
)


def fetch_john_hopkins_data():
    df_covid = {
        key: pd.read_csv(os.path.join(URL_BASE, filename))
        for key, filename in FILENAME_JOHN_HOPKINS.items()
    }
    columns_drop = ["Province/State", "Lat", "Long"]
    for key in df_covid:
        df_covid[key] = df_covid[key].drop(columns=columns_drop)
        df_covid[key] = df_covid[key].groupby("Country/Region").sum()
        df_covid[key] = df_covid[key].stack().to_frame().reset_index().rename(
            columns={"level_1": "date", 0: "cases"}
        )
        df_covid[key]["date"] = df_covid[key]["date"].apply(
            lambda x: pd.to_datetime(x)
        )
        df_covid[key]["type"] = key
    df_covid = pd.concat(df_covid.values(), ignore_index=True)

    return df_covid
