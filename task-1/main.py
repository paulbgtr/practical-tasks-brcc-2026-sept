from io import StringIO

import matplotlib.pyplot as plt
import pandas as pd
import requests

API = "https://api-baltic.transparency-dashboard.eu/api/v1/export"


def get_data(id):
    res = requests.get(
        API,
        params={
            "id": id,
            "start_date": "2025-09-22T00:00",
            "end_date": "2025-09-23T00:00",
            "output_time_zone": "EET",
            "output_format": "csv",
        },
    )

    data = StringIO(res.text)

    df = pd.read_csv(
        data,
        sep=";",
        decimal=",",
    )

    return df


def format_tables(df_afrr_raw, df_imbalance_raw):
    df_afrr = df_afrr_raw.rename(columns={"datetime_from": "timestamp"})[
        ["timestamp", "area", "Upward", "Downward"]
    ].copy()

    df_imbalance = df_imbalance_raw.rename(
        columns={"Unnamed: 3": "value", "datetime_from": "timestamp"}
    )[["timestamp", "area", "value"]].copy()

    df_afrr["timestamp"] = pd.to_datetime(df_afrr["timestamp"])
    df_imbalance["timestamp"] = pd.to_datetime(df_imbalance["timestamp"])

    return df_afrr, df_imbalance


def main():
    df_afrr_raw = get_data("activations_afrr")
    df_imbalance_raw = get_data("imbalance_volumes_v2")

    df_afrr, df_imbalance = format_tables(df_afrr_raw, df_imbalance_raw)

    result = pd.merge(
        df_afrr,
        df_imbalance,
        on=["timestamp", "area"],
        how="inner",
    )

    print(result)


if __name__ == "__main__":
    main()
