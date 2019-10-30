import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import RANSACRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_blobs
from matplotlib import cm
from sklearn.metrics import silhouette_samples

np.random.seed(123)
variables = ["x","y","z"]
labels = ["ID_0","ID_1","ID_2","ID_3","ID_4"]
X = np.random.random_sample([5,3])*10
df = pd.DataFrame(X,columns=variables,index=labels)
# print(df)

from scipy.spatial.distance import pdist,squareform
row_dist = pd.DataFrame(squareform(pdist(df,metric='euclidean')),columns=labels,index=labels)
# print(row_dist)

from scipy.cluster.hierarchy import linkage
# row_clusters = linkage(row_dist,method='complete',metric='euclidean')

# row_clusters = linkage(pdist(df,metric='euclidean'),method='complete',metric='euclidean')
#
row_clusters = linkage(df.values,method='complete',metric='euclidean')
row_clusters = pd.DataFrame(row_clusters,columns=['row label 1','row label 2','distance','no.of items in clusters'],
             index=['cluster %d'%(i+1) for i in range(row_clusters.shape[0])])
# print(row_clusters)
from scipy.cluster.hierarchy import dendrogram
#
# row_dendr = dendrogram(row_clusters,labels=labels)
# plt.tight_layout()
# plt.ylabel("Euclidean distance")
# plt.show()

fig = plt.figure(figsize=(8,8))
axd = fig.add_axes([0.09,0.1,0.2,0.6])
row_dendr = dendrogram(row_clusters,orientation='left')
df_rowclust = df.ix[row_dendr['leaves'][::-1]]
axm = fig.add_axes([0.23,0.1,0.6,0.6])
cax = axm.matshow(df_rowclust,interpolation='nearest',cmap='hot_r')
axd.set_xticks([])
axd.set_yticks([])
for i in axd.spines.values():
    i.set_visible(False)
fig.colorbar(cax)
axm.set_xticklabels(['']+list(df_rowclust.columns))
axm.set_yticklabels(['']+list(df_rowclust.index))
plt.show()