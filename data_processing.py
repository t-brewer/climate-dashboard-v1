import pandas as pd
from constants import axis_labels

def means_by_date(data, columns):
    # Creates a dataframe that has the mean for each specified column,
    # on a specified date.
    if type(columns) is str:
        columns = [columns]

    g = data.groupby("DATE")
    m = g[columns[0]].mean()

    for c in columns[1:]:
        m = pd.concat([m, g[c].mean()], axis=1)

    m.reset_index(inplace=True)
    m.sort_values(by="DATE", inplace=True)

    return m


def co2_emissions():
    data = pd.read_csv(axis_labels["co2"]["data"])
    data = data[data.entity == "World"]
    data=data[["year", "co2"]]
    return data


def temp_anomaly():
    data = pd.read_csv(axis_labels["anomaly"]["data"], header=4)
    data['year'] = data['Date'].apply(lambda s: int(str(s)[:4]))
    data = data.drop("Date", axis=1)
    data.rename({k: k.lower() for k in data.columns},
                axis=1,
                inplace=True)
    # todo data["anomaly_hotter"] = [ T > 0 for T in data.anomaly]
    return data

def sea_level():
    data = pd.read_csv(axis_labels["sea_level"]["data"])
    data = data[["day", "gsl_average"]]
    data.rename({"gsl_average": "sea_level"}, inplace=True, axis=1)
    data["day"] = pd.to_datetime(data["day"])
    data["year"] = pd.DatetimeIndex(data.day).year
    s = data.groupby("year").mean()
    data = s["sea_level"]
    return data

def get_data():
    co2 = co2_emissions()
    temp = temp_anomaly()
    sea_rise = sea_level()
    data = co2.merge(temp, on="year", how="outer")
    data = data.merge(sea_rise, on="year", how="outer")

    options = [k for k in axis_labels.keys()]
    columns = ["year"] + options
    data = data[columns]
    data["year"] = data["year"].astype(int)
    data.sort_values(by="year", inplace=True)
    return data

def get_delta(data, col, year_min, year_max):
    slice = data[(data.year >= year_min) & (data.year <= year_max)]
    min_vals = slice[slice.year == year_min]
    if len(min_vals) > 1:
        ymin = min_vals[col].mean()
    else:
        ymin = min_vals[col].values[0]

    max_vals = slice[slice.year == year_max]
    if len(max_vals) > 1:
        ymax = max_vals[col].mean()
    else:
        ymax = max_vals[col].values[0]

    return ymax-ymin





################# End Testing Area
