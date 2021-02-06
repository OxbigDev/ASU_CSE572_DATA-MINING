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
    tm = "BWZ Carb Input (grams)"

    # Read in the dataframe concatenate date and time cols
    insulin_pump_df = pd.read_csv(FILES[0], parse_dates=[['Date', 'Time']], na_filter=False)
    CGM_df = pd.read_csv(FILES[2], parse_dates=[['Date', 'Time']])

    # extract relevent time stamps
    all_t = insulin_pump_df.loc(insulin_pump_df[tm] != "").Date_time

    # Find time windows follow three scenarios
    meal_range = pd.to_timedelta(2, "hours")
    tm_list = []
    tp_list = []
    other_rule_list = []

    # iterate over the relevent timestamps
    for series in all_t[::-1]:
        tm = series.Date_Time

        # skip this logic on first iteration
        if "tp" in dir():
            # meal data tm+2hrs
            if tp - tm > meal_range:
                tm_list.append(tp)

            # tp if tp>tm and tp<tm+2hrs
            if tp - tm < meal_range:
                tp_list.append(tp)

            # tm+2hrs = tm then tm+1.5hrs to tm+4hrs
            if tp - tm == meal_range:
                other_rule_list.append(tp)

        # assign current time to previous time
        tp = tm
        # this assumes the final tm fits meal data tm+2hrs
        tm_list.append(tm)

    meal_data = CGM_df.loc

    return


if __name__ == "__main__":
    main()