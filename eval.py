"""
This script contains x
"""

__author__ = "msalzarulo"

FILES = ["Results.csv",
         "test_truth.csv"]

import pandas as pd
import pickle
import train,test

from sklearn.neural_network import MLPClassifier

train.main()
test.main()

results = pd.read_csv(FILES[0], header=None).values
labels = pd.read_csv(FILES[1], header=None).values

fn = "Trained_model.pkl"
with open(fn, "rb") as fp:
    model = pickle.load(fp)

print(f"FINAL SCORE {sum(results==labels)/results.size}")