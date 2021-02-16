# ASU_CSE_PROJECT_TEMPLATE
# ====
# Project 3

import pandas as pd
import sklearn
import pickle

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import KFold, train_test_split
import numpy as np

__author__ = "msalzarulo"

FILES = ["CGMData.csv",
         "InsulinData.csv",
         "Results.csv"]

def main():

    # meal time trigger column (tm)
    meal_ticker = "BWZ Carb Input (grams)"
    # data of interest
    col_of_interest = 'Sensor Glucose (mg/dL)'

    meal_data = []
    no_meal_data = []

    # Read in the dataframe concatenate date and time cols
    insulin_pump_df = pd.read_csv(FILES[1], parse_dates=[['Date', 'Time']], na_filter=False)
    CGM_df = pd.read_csv(FILES[0], parse_dates=[['Date', 'Time']], na_filter=False)
    pd.to_numeric(CGM_df[col_of_interest]).interpolate(inplace=True, limit=3000, limit_direction="both")

    # extract relevent time stamps
    all_t = insulin_pump_df.loc[insulin_pump_df[meal_ticker] != ""]

    # Find time windows follow three scenarios
    meal_range = pd.to_timedelta(2, "hours")
    start_meal_delta = pd.to_timedelta(.5, "hours")
    other_meal_delta = pd.to_timedelta(1.5, "hours")
    tm_list = []
    carb_intake_list = []

    # iterate over the relevent timestamps to get meal times
    for _, series in all_t[::-1].iterrows():
        y_val = series[meal_ticker]
        carb_intake_list.append(y_val) if y_val > 0 else None
        tm = series.Date_Time

        # skip this logic on first iteration
        if "tp" in dir():
            # meal data tm+2hrs
            if tp - tm > meal_range:
                tm_list.append(tp - start_meal_delta)

            # tp if tp>tm and tp<tm+2hrs
            elif tp - tm < meal_range:
                tm_list.append(tp - start_meal_delta)

            # tm+2hrs = tm then tm+1.5hrs to tm+4hrs
            elif tp - tm == meal_range:
                tm_list.append(tp+other_meal_delta)

            # return error message to console
            else:
                print(f"There is an error @ {series.Date_Time}")

        # assign current time to previous time
        tp = tm
    # this assumes the final tm fits meal data tm+2hrs
    tm_list.append(tm)

    meal_window = pd.to_timedelta(2.5, "hours")
    no_meal_window = pd.to_timedelta(2, "hours")

    # get meal and no meal data
    # meal data is px Px30
    for time_stamp in tm_list:
        data = CGM_df.loc[CGM_df.Date_Time > time_stamp]
        meal_start = data.Date_Time.min()
        meal_end = meal_start+meal_window
        data = data.loc[data.Date_Time < meal_end]
        meal_data.append(data)

    # no meal data is Qx24
    max_time_stamp = CGM_df.Date_Time.max()
    window_start = CGM_df.Date_Time.min()
    window_end = window_start + no_meal_window
    last_meal = iter(meal_data)
    c_meal_data = pd.concat(meal_data)
    while window_end < max_time_stamp:

        if window_end not in c_meal_data.Date_Time and window_start not in c_meal_data.Date_Time:
            data = CGM_df.loc[CGM_df.Date_Time > window_start]
            data = data.loc[CGM_df.Date_Time < window_end]
            no_meal_data.append(data)

        else:
            window_end = next(last_meal)[-1]

        window_start = window_end
        window_end = window_start + no_meal_window

    # Extract data to expected format
    no_meal_data = [pd.to_numeric(x[col_of_interest]).values for x in no_meal_data]
    [print(f" expected 24 got :{len(x)}") for x in no_meal_data if len(x) != 24]
    meal_data = [pd.to_numeric(x[col_of_interest]).values for x in meal_data]
    [print(f" expected 30 got :{len(x)}") for x in meal_data if len(x) != 30]

    # filter out incomplete data
    no_meal = [x for x in no_meal_data if len(x) == 24 and True not in np.isnan(x)]
    meal = np.asarray([x[6:] for x in meal_data if len(x) == 30 and True not in np.isnan(x)])

    meal_max = np.max(meal)
    meal_min = np.min(meal)

    n = (meal_max - meal_min) / 20

    # take meal data
    # divide into bins
    # each bin has a label
    # run k means on meal data

    return