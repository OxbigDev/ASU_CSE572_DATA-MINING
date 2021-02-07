# ASU_CSE_PROJECT_TEMPLATE
# ====
# Project 2

import pandas as pd
import sklearn
import pickle

__author__ = "Mike.Salzarulo"

FILES = ["CGMData.csv",
         "CGM_patient2.csv",
         "InsulinData.csv",
         "Insulin_patient2.csv"]

def main():

    # meal time trigger column (tm)
    meal_ticker = "BWZ Carb Input (grams)"

    # Read in the dataframe concatenate date and time cols
    insulin_pump_df = pd.read_csv(FILES[2], parse_dates=[['Date', 'Time']], na_filter=False)
    CGM_df = pd.read_csv(FILES[0], parse_dates=[['Date', 'Time']])

    # extract relevent time stamps
    all_t = insulin_pump_df.loc[insulin_pump_df[meal_ticker] != ""]

    # Find time windows follow three scenarios
    meal_range = pd.to_timedelta(2, "hours")
    start_meal_delta = pd.to_timedelta(.5, "hours")
    other_meal_delta = pd.to_timedelta(1.5, "hours")
    tm_list = []

    # iterate over the relevent timestamps to get meal times
    for _,series in all_t[::-1].iterrows():
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
    meal_data = []

    # get meal and no meal data
    # meal data is px Px30
    for time_stamp in tm_list:
        data = CGM_df.loc[CGM_df.Date_Time > time_stamp]
        meal_start = data.Date_Time.min()
        meal_end = meal_start+meal_window
        data = data.loc[data.Date_Time < meal_end]
        meal_data.append(data)

    # no meal data is Qx24
    no_meal_data = []
    max_time_stamp = CGM_df.Date_Time.max()
    window_start = CGM_df.Date_Time.min()
    window_end = window_start + no_meal_window
    last_meal = iter(meal_data)
    c_meal_data = pd.concat(meal_data)
    while window_end < max_time_stamp:

        # todo: there is an error somewhere here
        if window_end not in c_meal_data.Date_Time and window_start not in c_meal_data.Date_Time:
            data = CGM_df.loc[CGM_df.Date_Time > window_start]
            data = data.loc[CGM_df.Date_Time < window_end]
            no_meal_data.append(data)

        else:
            window_end = next(last_meal)[-1]

        window_start = window_end
        window_end = window_start + no_meal_window

    pd.concat(no_meal_data).to_csv("no_meal_data.csv")
    pd.concat(meal_data).to_csv("meal_data.csv")

        # interpolate
        # extract features
        # train SVM

    return

# expecting 231 rows in 1 col


if __name__ == "__main__":
    main()