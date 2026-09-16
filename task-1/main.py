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


def main():
    activations = get_data("activations_afrr")
    imbalance_volumes = get_data("imbalance_volumes_v2")

    activations = activations[['datetime_from', 'area', 'Upward', 'Downward']]
    imbalance_volumes = imbalance_volumes.rename(columns={"Unnamed: 3": "value"})
    imbalance_volumes = imbalance_volumes[['datetime_from', 'area', 'value']]

    result = pd.merge(
        activations,
        imbalance_volumes,
        on=["datetime_from", "area"],
        how="left",
    )

    print(result)


if __name__ == "__main__":
    main()
