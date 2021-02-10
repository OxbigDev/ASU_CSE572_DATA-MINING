# ASU_CSE_PROJECT_TEMPLATE
# ====
# Project 2

__author__ = "Mike.Salzarulo"

FILES = ["test.csv",
         'Trained_model.pkl',
         'Result.csv']

import pandas as pd
import pickle
import numpy as np

def main():

    data = pd.read_csv(FILES[0], header=None).values
    data = feature_extraction(data[:,:24])

    with open(FILES[1], "rb") as fp:
        model = pickle.load(fp)

    predictions = model.predict(data)

    pd.DataFrame(predictions, index=None, columns=None).to_csv(FILES[2], header=False, index=False, index_label=False)

    return

def feature_extraction(data):

    samples = []
    for i, sample in enumerate(data):
        mean = np.mean(sample)
        std = np.std(sample)
        fft = np.fft.fft(sample)
        real = np.real(fft)
        angle = np.angle(fft)
        dsample = np.gradient(sample)
        d2sample = np.gradient(sample, edge_order=2)
        samples.append(np.append(sample, (mean, std, *real, *angle, *dsample, *d2sample)))

    data = np.asarray(samples)

    return data


if __name__ == "__main__":
    main()