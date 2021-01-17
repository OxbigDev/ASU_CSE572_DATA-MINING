# ASU_CSE_PROJECT_TEMPLATE
# ====
# Project #

__author__ = "Mike.Salzarulo"

import sklearn
import pandas as pd

def preform_desired_mining(df):

    col_of_interest = 'Sensor Glucose (mg/dL)'
    time_inverval = df['Time'].iloc[0] - df['Time'].iloc[1]
    time_delta = df.shape[0] * time_inverval
    time_of_day = []

    # todo: this aint it
    #  This method will not include the times when the levels monitored fall out of hyper glycemia
    #  I'll need to preform a sliding window operation to capture acurate time deltas
    # # hyperglycemia > 180
    # threshold = 180
    # time_delta_hyperglycemia = df.loc[df[col_of_interest] > threshold]['Time'].max() - df.loc[df[col_of_interest] > threshold]['Time'].min()
    #
    # # hyperglycemia critical > 250
    # threshold = 250
    # time_delta_hyperglycemia = df.loc[df[col_of_interest] > threshold]['Time'].max() - df.loc[df[col_of_interest] > threshold]['Time'].min()
    #
    # # primary range 70:180
    # low = 70
    # high = 180
    # time_delta_hyperglycemia = df.loc[df[col_of_interest] > low and df[col_of_interest] < high]['Time'].max() - df.loc[df[col_of_interest] > low and df[col_of_interest] < high]['Time'].min()

    # todo: this needs to be done for three different times of day see line 15
    # hyperglycemia > 180
    threshold = 180
    temp_df = df.loc[df[col_of_interest] > threshold]['Time']
    tot_time_hyperglycemia = temp_df.shape[0] * time_inverval

    # hyperglycemia critical > 250
    threshold = 250
    temp_df = df.loc[df[col_of_interest] > threshold]['Time']
    tot_time_hyperglycemia_crit = temp_df.shape[0] * time_inverval

    # primary range 70:180
    low = 70
    high = 180
    temp_df = df.loc[df[col_of_interest] >= low and df[col_of_interest] <= high]['Time']
    tot_time_primaryrng = temp_df.shape[0] * time_inverval

    # secondary range 70:150
    low = 70
    high = 150
    temp_df = df.loc[df[col_of_interest] >= low and df[col_of_interest] <= high]['Time']
    tot_time_secondaryrng = temp_df.shape[0] * time_inverval

    # hypoglycemia lv 1 70
    threshold = 70
    temp_df = df.loc[df[col_of_interest] < threshold]['Time']
    tot_time_lv1 = temp_df.shape[0] * time_inverval

    # hypoglycemia lv 2 54
    threshold = 54
    temp_df = df.loc[df[col_of_interest] < threshold]['Time']
    tot_time_lv2 = temp_df.shape[0] * time_inverval

    return df

def main():
    """
    main

    :return:
    """

    files = ["Project 1 Student Files/InsulinData.csv",
             "Project 1 Student Files/CGMData.csv"]
    mode_change_trigger = 'AUTO MODE ACTIVE PLGM OFF'

    insulin_pump_df = pd.read_csv(files[0], parse_dates=['Date', 'Time'])
    CGM_df = pd.read_csv(files[1], parse_dates=['Date', 'Time'])

    # a) Percentage time in hyperglycemia(CGM > 180 mg / dL),
    # total time> 180 mg / total recorded time

    # b) percentage of time in hyperglycemia critical(CGM > 250 mg / dL),
    # total time > 250 / total record time

    # c) percentage time in range(CGM >= 70 mg / dL and CGM <= 180 mg / dL),
    # d) percentage time in range secondary(CGM >= 70 mg / dL and CGM <= 150 mg / dL),
    # e) percentage time in hypoglycemia level 1(CGM < 70 mg / dL), and
    # f) percentage time in hypoglycemia level 2(CGM < 54 mg / dL).

    # 18 to be extracted for two modes hence 2x18 matrix

    # figure out where the modes split
    # it's in column Q of insulin pump df
    manual_off_ts = insulin_pump_df.loc[insulin_pump_df['Alarm'] == mode_change_trigger]['Time'].min()

    # todo: need to double check this produced the correct results
    manual_mode_df = CGM_df.loc[CGM_df['Time'] < manual_off_ts]
    auto_mode_df = CGM_df.loc[CGM_df['Time'] >= manual_off_ts]

    preform_desired_mining(manual_mode_df)


    return


if __name__ == "__main__":
    main()