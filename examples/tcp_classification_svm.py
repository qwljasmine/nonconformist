#!/usr/bin/env python

"""
Example: inductive conformal classification using DecisionTreeClassifier
"""

# Authors: Henrik Linusson

import numpy as np
import pandas as pd

from sklearn.svm import SVC
from sklearn.datasets import load_iris

from nonconformist.base import ClassifierAdapter
from nonconformist.cp import TcpClassifier
from nonconformist.nc import ClassifierNc, MarginErrFunc

# -----------------------------------------------------------------------------
# Setup training, calibration and test indices
# -----------------------------------------------------------------------------
data = load_iris()

idx = np.random.permutation(data.target.size)
train = idx[:int(idx.size / 2)]
test = idx[int(idx.size / 2):]

# -----------------------------------------------------------------------------
# Train and calibrate
# -----------------------------------------------------------------------------
tcp = TcpClassifier(ClassifierNc(ClassifierAdapter(SVC(probability=True)),
                                 MarginErrFunc()))
tcp.fit(data.data[train, :], data.target[train])

# -----------------------------------------------------------------------------
# Predict
# -----------------------------------------------------------------------------
prediction = tcp.predict(data.data[test, :], significance=0.1)
header = np.array(['c0','c1','c2','Truth'])
table = np.vstack([prediction.T, data.target[test]]).T
df = pd.DataFrame(np.vstack([header, table]))
print(df)
