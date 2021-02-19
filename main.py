# ASU_CSE_PROJECT_TEMPLATE
# ====
# Project 3

import pandas as pd
import sklearn
import pickle

from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
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
        y_val = int(series[meal_ticker])
        tm = series.Date_Time

        # skip this logic on first iteration
        if "tp" in dir() and y_val > 0:
            # meal data tm+2hrs
            if tp - tm > meal_range:
                time = tp - start_meal_delta
                tm_list.append(time)

            # tp if tp>tm and tp<tm+2hrs
            elif tp - tm < meal_range:
                time = tp - start_meal_delta
                tm_list.append(time)

            # tm+2hrs = tm then tm+1.5hrs to tm+4hrs
            elif tp - tm == meal_range:
                time = tp+other_meal_delta
                tm_list.append(time)

            # return error message to console
            else:
                print(f"There is an error @ {series.Date_Time}")

            carb_intake_list.append((y_val, time))

        # assign current time to previous time
        tp = tm
    # this assumes the final tm fits meal data tm+2hrs
    # tm_list.append(tm)

    # build cluster labels
    carb_intake_list.sort(key=lambda x: int(x[0]))
    labels = {}
    count = 0
    high_carb = carb_intake_list[0][0]+20
    label_name = str(count)

    for carb in carb_intake_list:
        if carb[0] < high_carb:
            if label_name in labels:
                labels[label_name].append(carb)
            else:
                labels[label_name] = [carb]
        else:
            count += 1
            high_carb += 20
            label_name = str(count)
            labels[label_name] = [carb]

    meal_window = pd.to_timedelta(2.5, "hours")
    no_meal_window = pd.to_timedelta(2, "hours")
    meal_truth_label = []

    # get meal and no meal data
    # meal data is px Px30
    for time_stamp in tm_list:
        data = CGM_df.loc[CGM_df.Date_Time > time_stamp]
        meal_start = data.Date_Time.min()
        meal_end = meal_start+meal_window
        data = data.loc[data.Date_Time < meal_end]
        meal_data.append(data)
        [meal_truth_label.append(label) for label, items in labels.items() if time_stamp in [x[1] for x in items]]

    # Extract data to expected format
    meal_data = [pd.to_numeric(x[col_of_interest]).values for x in meal_data]
    [print(f" expected 30 got :{len(x)}") for x in meal_data if len(x) != 30]

    # filter out incomplete data
    meal_ind = np.asarray([x for x, y in enumerate(meal_data) if len(y) == 30 and True not in np.isnan(y)])

    # apply filter
    meal = np.asarray(meal_data)[meal_ind]
    meal_truth_label = np.asarray(meal_truth_label)[meal_ind]

    # run k means on meal data
    kmeans_model = KMeans(n_clusters=6)
    kmeans_model = kmeans_model.fit(meal.tolist())
    ky = kmeans_model.labels_

    # run DBSCAN on meal data
    dbscan_model = DBSCAN()
    dbscan_model.fit(meal.tolist())
    dby = dbscan_model.labels_

    # create confusion matrix
    confusion_matrix = build_confusion_matrix(ky, meal_truth_label, labels)
    cluster_means = np.mean(kmeans_model.cluster_centers_, axis=1)

    [sse(x, y) for x, y in zip(confusion_matrix, cluster_means)]

    return

def build_confusion_matrix(ky, meal_truth_label):
    p_labels = np.zeros((ky.max()+1, meal_truth_label.max()+1))

    for y, truth in zip(ky, meal_truth_label.astype(np.uint8)):
        p_labels[y, truth] += 1

    return p_labels

def sse(cluster, mean):
    return sum(map(lambda x: (x-mean)**2, cluster))

def purity():
    return purity

def entropy():
    return entropy


if __name__ == '__main__':
    main()

