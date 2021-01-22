# ASU_CSE_PROJECT_TEMPLATE
# ====
# Project #

__author__ = "Mike.Salzarulo"

import sklearn
import pandas as pd

def preform_desired_mining(df):
    """
    This function is designed to ingest a pandas dataframe and will calculate the following parameters based on three
    predefined times of day:

        a) Percentage time in hyperglycemia(CGM > 180 mg / dL),
        b) percentage of time in hyperglycemia critical(CGM > 250 mg / dL),
        c) percentage time in range(CGM >= 70 mg / dL and CGM <= 180 mg / dL),
        d) percentage time in range secondary(CGM >= 70 mg / dL and CGM <= 150 mg / dL),
        e) percentage time in hypoglycemia level 1(CGM < 70 mg / dL), and
        f) percentage time in hypoglycemia level 2(CGM < 54 mg / dL).

    :param df:

    :return: list of parameters
    """

    # define function vars
    col_of_interest = 'Sensor Glucose (mg/dL)'
    # Time interval between collections
    time_inverval = df['Date_Time'].iloc[0] - df['Date_Time'].iloc[1]
    # this is the total time in the given mode
    total_time = df.shape[0] * time_inverval
    # This will cover all cases
    time_of_day = 6
    # empty list assignment to place calculated values
    values = []
    # create df to be overwritten each iteration
    time_split_df = df.copy()

    # Begin mining loop
    # The first iteration of the loop does not to any time splitting so to capture 12 am to 12 am
    for split in range(3):
        # This will create a split for 6 AM to midnight given hour 23:59 is midnight
        if split == 1:
            time_split_df = df.loc[df.Date_Time.dt.hour >= time_of_day]

        # This will create a split for midnight to 6 AM given hour 24 is midnight represented by 0
        if split == 2:
            time_split_df = df.loc[df.Date_Time.dt.hour < time_of_day]

        # hyperglycemia > 180
        threshold = 180
        temp_df = time_split_df.loc[time_split_df[col_of_interest] > threshold]
        tot_time_hyperglycemia = temp_df.shape[0] * time_inverval
        values.append(tot_time_hyperglycemia)

        # hyperglycemia critical > 250
        threshold = 250
        temp_df = time_split_df.loc[time_split_df[col_of_interest] > threshold]
        tot_time_hyperglycemia_crit = temp_df.shape[0] * time_inverval
        values.append(tot_time_hyperglycemia_crit)

        # primary range 70:180
        low = 70
        high = 180
        temp_df_highpass = time_split_df.loc[time_split_df[col_of_interest] >= low]
        temp_df = temp_df_highpass.loc[temp_df_highpass[col_of_interest] <= high]
        tot_time_primaryrng = temp_df.shape[0] * time_inverval
        values.append(tot_time_primaryrng)

        # secondary range 70:150
        low = 70
        high = 150
        temp_df_highpass = time_split_df.loc[time_split_df[col_of_interest] >= low]
        temp_df = temp_df_highpass.loc[temp_df_highpass[col_of_interest] <= high]
        tot_time_secondaryrng = temp_df.shape[0] * time_inverval
        values.append(tot_time_secondaryrng)

        # hypoglycemia lv 1 70
        threshold = 70
        temp_df = time_split_df.loc[time_split_df[col_of_interest] < threshold]
        tot_time_lv1 = temp_df.shape[0] * time_inverval
        values.append(tot_time_lv1)

        # hypoglycemia lv 2 54
        threshold = 54
        temp_df = time_split_df.loc[time_split_df[col_of_interest] < threshold]
        tot_time_lv2 = temp_df.shape[0] * time_inverval
        values.append(tot_time_lv2)

    # Here we divide time deltas to get a list of floats
    return [x/total_time for x in values]

def main():
    """
    main

    :return:
    """

    # Define hueristic params
    files = ["Project 1 Student Files/InsulinData.csv",
             "Project 1 Student Files/CGMData.csv",
             "Project 1 Student Files/Results.csv"]
    mode_change_trigger = 'AUTO MODE ACTIVE PLGM OFF'

    # Read in the dataframe concatenate date and time cols
    insulin_pump_df = pd.read_csv(files[0], parse_dates=[['Date', 'Time']])
    CGM_df = pd.read_csv(files[1], parse_dates=[['Date', 'Time']])

    # Find the timestamp for when manual mode is turned off
    manual_off_ts = insulin_pump_df.loc[insulin_pump_df['Alarm'] == mode_change_trigger]['Date_Time'].min()

    # Separate modes where the mode indexed at 0 is manual and the mode indexed at 1 is auto
    modes_dfs = [CGM_df.loc[CGM_df['Date_Time'] < manual_off_ts], CGM_df.loc[CGM_df['Date_Time'] >= manual_off_ts]]

    # manual_mode_calcs = preform_desired_mining(manual_mode_df)
    # auto_mode_calcs = preform_desired_mining(auto_mode_df)

    #todo: read in and update results.csv template
    output_df = pd.read_csv(files[2], index_col=0)
    for i in range(output_df.shape[0]):
        output_df.iloc[i] = preform_desired_mining(modes_dfs[i])

    output_df.to_csv("test_output.csv")

    return


if __name__ == "__main__":
    main()