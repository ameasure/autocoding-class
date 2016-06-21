# -*- coding: utf-8 -*-
"""
Code to train and save an "autocoder" for future use. It consists of 5 steps:
    1) read in the data we will use to train and evaluate our model
    2) vectorize our data
    3) fit a logistic regression model to the data
    4) evaluate the model
    5) save the model for future use
"""

# import the libraries we will use
from __future__ import print_function
import scipy as sp
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, f1_score
from sklearn.externals import joblib

### Read in the data we will use to train and evaluate our model
# We also convert the MINE_ID column to a string so we can later use it as an
# input in a CountVectorizer.
df = pd.read_excel(r'training.xlsx', converters={'MINE_ID': lambda x: str(x)})
# split the data into separate test and validation sets based on year
df_training = df[df['YEAR'] <= 2011]
df_validation = df[df['YEAR'] == 2012]

### Convert the raw input data into vectors ###
mine_vectorizer = CountVectorizer()
mine_vectorizer.fit(df_training['MINE_ID'])
x_mine_training = mine_vectorizer.transform(df_training['MINE_ID'])

narrative_vectorizer = CountVectorizer(min_df=5, ngram_range=(1,2))
narrative_vectorizer.fit(df_training['NARRATIVE'])
x_nar_training = narrative_vectorizer.transform(df_training['NARRATIVE'])
# Note: we must always hstack these matrices in the same order in the future
x_training = sp.sparse.hstack((x_mine_training, x_nar_training))

### Train a logisticRegression model on our vectorized training data
y_training = df_training['INJ_BODY_PART_CD']
clf = LogisticRegression(C=1)
clf.fit(x_training, y_training)

### Evaluate our model against the validation data
x_mine_validation = mine_vectorizer.transform(df_validation['MINE_ID'])
x_nar_validation = narrative_vectorizer.transform(df_validation['NARRATIVE'])
x_validation = sp.sparse.hstack((x_mine_validation, x_nar_validation))

y_validation_predictions = clf.predict(x_validation)
# Compare the predicted codes to the correct codes to evaluate our model
y_validation = df_validation['INJ_BODY_PART_CD']
accuracy = accuracy_score(y_validation, y_validation_predictions)
macro_f1 = f1_score(y_validation, y_validation_predictions, average='macro', 
                    labels=set(y_training + y_validation))
print('accuracy = %s' % (accuracy))
print('macro f1 score = %s' % (macro_f1))

### Save the model and vectorizers for future use ###
joblib.dump(clf, filename='LRclf.pkl')
joblib.dump(mine_vectorizer, filename='mine_vectorizer.pkl')
joblib.dump(narrative_vectorizer, filename='narrative_vectorizer.pkl')