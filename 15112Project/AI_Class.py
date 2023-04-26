#IMPORANT!!!!! READ BELOW
#source code:https://colab.research.google.com/drive/1NyYH1EPpaJlMBLK0fcKYz4icaD1SNSLK#scrollTo=DWcb4sxAP2lT !!!!!!!!!
#got base code from link above, but modified it to my use and also turned it into class so that I don't need to retrain AI every time I have it read something
#https://scikit-learn.org/stable/install.html installying sckitlearn
#https://www.youtube.com/watch?v=GvYYFloV0aA&list=PL8dPuuaLjXtO65LeD2p4_Sb5XQ51par_b&ab_channel=CrashCourse important source that gave me basics of character recognition (the whole video sereies)
from PIL import Image, ImageFilter,ImageDraw,ImageEnhance,ImageOps
import PIL
import numpy as np
import random
import copy
from emnist import extract_training_samples 
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml
from sklearn.neural_network import MLPClassifier

class AI():
    def __init__(self,isEmnist,externalTrainingImages=None,externalTrainingLabels=None):
        if isEmnist:
            X, y = extract_training_samples('digits')
            X=X/255.

            #converts each pixel value to be between 0 and 1
            externalTrainingImages=externalTrainingImages/255.
 
            #gets the training data
            trainingImages=X[0:90000]
            trainingLabels=y[0:90000]
            #sources about concatenating arrays
            #https://pythonguides.com/python-numpy-concatenate/#:~:text=concatenate.-,To%20concatenate%20two%20arrays%20either%20row%2Dwise%20or%20column%2Dwise,join%20the%20column%2Dwise%20elements.
            #https://www.w3schools.com/python/numpy/numpy_array_join.asp
            #https://www.w3schools.com/python/numpy/trypython.asp?filename=demo_numpy_array_join2

            #combines the database data with the data I self trained
            trainingImages=np.concatenate((trainingImages,externalTrainingImages),axis=0)
            trainingLabels=np.concatenate((trainingLabels,externalTrainingLabels),axis=0)
            
            trainingImages = trainingImages.reshape((trainingImages.shape)[0],784)
            self.mlp1 = MLPClassifier(hidden_layer_sizes=(100,100,50,50), max_iter=20, alpha=1e-4,
                            solver='sgd', verbose=10, tol=1e-4, random_state=1,
                            learning_rate_init=.1)
            (self.mlp1).fit(trainingImages, trainingLabels)
    #feed images for AI to read, might be able to remove testlabels in future but not entirely sure
    def readImage(self,testImages,testLabels):
        testImages=testImages/255.
        testImages = testImages.reshape((testLabels.shape)[0],784)
        prediction = self.mlp1.predict(testImages)
        return prediction

            

