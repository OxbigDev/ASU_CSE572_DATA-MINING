# ASU_CSE_PROJECT_TEMPLATE
# ====
# Project 2

__author__ = "Mike.Salzarulo"

FILES = ["test.csv",
         'Trained_model.pkl',
         'results.csv']

import pandas as pd
import pickle
from sklearn.neural_network import MLPClassifier

def main():

    data = pd.read_csv(FILES[0], header=None).values

    with open(FILES[1], "rb") as fp:
        model = pickle.load(fp)

    predictions = model.predict(data)

    pd.DataFrame(predictions, index=None, columns=None).to_csv(FILES[2], header=False, index=False, index_label=False)

    return


if __name__ == "__main__":
    main()