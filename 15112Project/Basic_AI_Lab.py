#source:https://colab.research.google.com/drive/1NyYH1EPpaJlMBLK0fcKYz4icaD1SNSLK#scrollTo=DWcb4sxAP2lT
#got base code from link above, but modified it to my use
#https://scikit-learn.org/stable/install.html installying sckitlearn
#https://www.youtube.com/watch?v=GvYYFloV0aA&list=PL8dPuuaLjXtO65LeD2p4_Sb5XQ51par_b&ab_channel=CrashCourse important source that gave me basics of character recognition
from PIL import Image, ImageFilter,ImageDraw,ImageEnhance,ImageOps
import PIL
import numpy as np
import random
import copy
from emnist import extract_training_samples 
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml
from sklearn.neural_network import MLPClassifier
#from Term_project_playing_around import X_test,y_test


def emnistAI(X_test,y_test,isEmnist,isSelfTrain,Xtrain,ytrain):
    if isEmnist:
        X, y = extract_training_samples('digits')
    else:
        X,y=Xtrain,ytrain
    


    print(X.shape)
    X=X/255.
    X_test=X_test/255.

    X_train=X[0:90000]
    y_train=y[0:90000]




    #print((XtrainingData).shape)

    X_train = X_train.reshape((X_train.shape)[0],784)
    X_test = X_test.reshape((y_test.shape)[0],784)

    #reshapes from 1d array back to 2d array to image
    #img=Image.fromarray(X_train[500].reshape(28,28))
    #img.show()

    #you need to add 96 to show the right acii values
    #print(str(chr(y_train[500]+96)))
    mlp1 = MLPClassifier(hidden_layer_sizes=(100,100,50,50), max_iter=20, alpha=1e-4,
                            solver='sgd', verbose=10, tol=1e-4, random_state=1,
                            learning_rate_init=.1)



    mlp1.fit(X_train, y_train)
    print("Training set score: %f" % mlp1.score(X_train, y_train))
    print("Test set score: %f" % mlp1.score(X_test, y_test))
    print("wef")
    y_pred = mlp1.predict(X_test)
    if not isEmnist:
        return y_pred
    else:
        y_pred_char=[]
        for i in range(len(y_pred)):
            y_pred_char.append(chr(y_pred[i]+96))
        return(np.array(y_pred_char))





















