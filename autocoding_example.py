# -*- coding: utf-8 -*-
"""
Use a previously trained autocoder to assign codes to some new set of data.
In this example we will pretend that the 2013 MSHA data has not yet been coded.

This involves 3 steps:
    1) load the uncoded data
    2) load the previously trained vectorizer(s) and classifier
    3) use the vectorizer(s) and classifier to assign codes to the data
"""

import pandas as pd
import numpy as np
import scipy as sp

from sklearn.externals import joblib

### Read in the uncoded data
df_uncoded = pd.read_excel(r'uncoded.xlsx', converters={'MINE_ID': lambda x: str(x)})

### Load the vectorizer(s) and classifier we previously created
clf = joblib.load(filename='LRclf.pkl')
mine_vectorizer = joblib.load(filename='mine_vectorizer.pkl')
narrative_vectorizer = joblib.load(filename='narrative_vectorizer.pkl')

### Assign codes to the uncoded data
x_mine_uncoded = mine_vectorizer.transform(df_uncoded['MINE_ID'])
x_nar_uncoded = narrative_vectorizer.transform(df_uncoded['NARRATIVE'])
x_uncoded = sp.sparse.hstack((x_mine_uncoded, x_nar_uncoded))
y_predicted_prob = clf.predict_proba(x_uncoded)
max_indices = y_predicted_prob.argmax(axis=1)
predicted_codes = clf.classes_[max_indices]
predicted_prob = y_predicted_prob[np.arange(len(y_predicted_prob)), max_indices]
df_uncoded['Autocoded INJ_BODY_PART_CD'] = predicted_codes
df_uncoded['Autocode Confidence'] = predicted_prob
# Save autocoded data 
df_uncoded.to_excel('autocoded_msha.xlsx', index=False)