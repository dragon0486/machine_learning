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
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix,precision_score,recall_score,f1_score,make_scorer
from sklearn.metrics import roc_curve,auc
from scipy import interp

df = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data",header=None)
X = df.loc[:,2:].values
y = df.loc[:,1].values
le = LabelEncoder()
y = le.fit_transform(y)
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=0)
X_train2 =X_train[:,[4,14]]
cv = StratifiedKFold(n_splits=3,random_state=1)
fig = plt.figure(figsize=(7,5))
mean_tpr = 0.0
mean_fpr = np.linspace(0,1,100)
all_tpr = []
pipe_lr = Pipeline([('scl',StandardScaler()),("clf",LogisticRegression(random_state=0,penalty='l2'))])
for i ,(train,test) in enumerate(cv.split(X_train2,y_train)):
    probas = pipe_lr.fit(X_train2[train],y_train[train]).predict_proba(X_train2[test])
    fpr,tpr,thresholds = roc_curve(y_train[test],probas[:,1],pos_label=1)
    mean_tpr += interp(mean_fpr,fpr,tpr)
    mean_tpr[0] = 0.0
    roc_auc = auc(fpr,tpr)
    plt.plot(fpr,tpr,lw=1,label="ROC fold %d (area = %0.2f)" %(i+1,roc_auc))
plt.plot([0,1],[0,1],linestyle="--",color=(0.6,0.6,0.6),label="random guessing")
mean_tpr /= len(list(cv.split(X_train2,y_train)))
mean_tpr[-1]=1.0
mean_auc = auc(mean_fpr,mean_tpr)
plt.plot(mean_fpr,mean_tpr,'k--',label="mean ROC (area=%0.2f)" % mean_auc,lw=2)
plt.plot([0,0,1],[0,1,1],lw=2,linestyle=":",color="black",label="perfect performance")
plt.xlim([-0.05,1.05])
plt.ylim([-0.05,1.05])
plt.xlabel("false positive rate")
plt.ylabel("true positive rate")
plt.title("Receiver Operator Characteristic")
plt.legend(loc="lower right")
plt.show()