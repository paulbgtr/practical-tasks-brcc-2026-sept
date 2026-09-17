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


def print_summary(df):
    summary = df.groupby("area").agg(
        total_imbalance=("value", lambda x: x.abs().sum()),
        total_activation=("net_afrr", lambda x: x.abs().sum()),
    )
    summary["coverage_pct"] = (
        summary["total_activation"] / summary["total_imbalance"] * 100
    ).round(1)
    print(summary.round(2))


def plot_area(ax_raw, ax_derived, df, area):
    d = df[df["area"] == area].sort_values("timestamp")

    ax_raw.plot(d["timestamp"], d["value"], label="Imbalance", color="black")
    ax_raw.plot(d["timestamp"], d["Upward"], label="aFRR Upward", color="green")
    ax_raw.plot(d["timestamp"], d["Downward"], label="aFRR Downward", color="red")
    ax_raw.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    ax_raw.set_title(f"{area} — raw")
    ax_raw.legend(loc="upper right", fontsize=8)

    ax_derived.plot(
        d["timestamp"], d["net_afrr"], label="Net aFRR (Down-Up)", color="blue"
    )
    ax_derived.plot(
        d["timestamp"], d["residual"], label="Residual", color="purple", linestyle=":"
    )
    ax_derived.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    ax_derived.set_title(f"{area} — derived")
    ax_derived.legend(loc="upper right", fontsize=8)


def plug_metrics(df):
    df["net_afrr"] = df["Downward"] - df["Upward"]
    df["residual"] = df["value"] - df["net_afrr"]
    df["residual_ratio"] = df["residual"] / df["value"].replace(0, pd.NA)
    return df

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

    result = plug_metrics(result)
    print_summary(result)

    areas = sorted(result["area"].unique())

    fig, axes = plt.subplots(
        nrows=len(areas),
        ncols=2,
        figsize=(16, 4 * len(areas)),
        sharex=True,
    )

    for row, area in zip(axes, areas):
        ax_raw, ax_derived = row
        plot_area(ax_raw, ax_derived, result, area)

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
