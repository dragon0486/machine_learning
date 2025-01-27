import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
from sklearn.model_selection import validation_curve
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

df = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data",header=None)
X = df.loc[:,2:].values
y = df.loc[:,1].values
le = LabelEncoder()
y = le.fit_transform(y)
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=0)
pipe_svc = Pipeline([('scl',StandardScaler()),("clf",SVC(random_state=1))])
param_range = [0.0001,0.001,0.01,0.1,1.0,10.0,100.0,1000.0]
param_grid = [{"clf__C":param_range,
               "clf__kernel":['linear']},
              {"clf__C":param_range,"clf__gamma":param_range,"clf__kernel":['rbf']}]
gs = GridSearchCV(estimator=pipe_svc,param_grid=param_grid,cv=10,n_jobs=-1)
gs.fit(X_train,y_train)
# print(gs.best_score_)
# print(gs.best_params_)
clf = gs.best_estimator_
clf.fit(X_train,y_train)
print(clf.score(X_test,y_test))