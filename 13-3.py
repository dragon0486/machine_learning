import os
import struct
import numpy as np
from scipy.special import expit
import sys
def load_mnist(path,kind='train'):
    labels_path = os.path.join(path,"%s-labels.idx1-ubyte"%kind)
    images_path = os.path.join(path,"%s-images.idx3-ubyte"%kind)

    with open(labels_path,'rb') as lbpath:
        magic,n = struct.unpack(">II",lbpath.read(8))
        labels = np.fromfile(lbpath,dtype=np.uint8)

    with open(images_path,'rb') as imgpath:
        magic,num,row,cols = struct.unpack(">IIII",imgpath.read(16))
        images = np.fromfile(imgpath,dtype=np.uint8).reshape(len(labels),784)

    return images,labels
X_train,y_train = load_mnist('./',kind='train')
X_test,y_test = load_mnist('./',kind='t10k')

import theano
theano.config.floatX='float32'
X_train = X_train.astype(theano.config.floatX)
X_test = X_test.astype(theano.config.floatX)
from keras.utils import np_utils
# print(y_train[:3])
y_train_ohe = np_utils.to_categorical(y_train)
# print(y_train_ohe[:3])

from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import SGD

np.random.seed(1)
model = Sequential()
model.add(Dense(input_dim=X_train.shape[1],output_dim=50,init='uniform',activation='tanh'))
model.add(Dense(input_dim=50,output_dim=50,init='uniform',activation='tanh'))
model.add(Dense(input_dim=50,output_dim=y_train_ohe.shape[1],init='uniform',activation='softmax'))
sgd = SGD(lr=0.001,decay=1e-7,momentum=.9)
model.compile(loss='categorical_crossentropy',optimizer=sgd)
#
model.fit(X_train,y_train_ohe,nb_epoch=50,batch_size=300,verbose=1,validation_split=0.1)

y_train_pred = model.predict_classes(X_train,verbose=0)
train_acc = np.sum(y_train==y_train_pred,axis=0)/X_train.shape[0]
print(train_acc)
y_test_pred = model.predict_classes(X_test,verbose=0)
train_acc = np.sum(y_test==y_test_pred,axis=0)/X_test.shape[0]
print(train_acc)