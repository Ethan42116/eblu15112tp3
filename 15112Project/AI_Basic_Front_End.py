#note, this file is not very important, it is mainly used for me to play around with AI and test self training my AI
#used self training for negative numbers
import PIL
import numpy as np
from numpy import array
import random
import copy
from cmu_graphics import *
from PIL import Image, ImageFilter,ImageDraw,ImageEnhance,ImageOps
from Image_Functions import alterImage, openImage,convertToAIBasicLab
from Basic_AI_Lab import emnistAI
from files_navigator import getFileSet  


def distance(x1,y1,x2,y2):
    return ((x2-x1)**2+(y2-y1)**2)**.5

def onAppStart(app):
    app.width=1000
    app.height=1000
    app.x=2019
    app.img=None
    app.predictionValue=None
    app.label=[]
    app.imgList=[]
    app.imgTrainList=[]
    app.labelTrain=[]
    app.havePrediction=False
    app.xTrain=None
    app.yTrain=None
    app.isEnmist=False
    app.isSelfTrain=False

    pass

def redrawAll(app):
    drawLabel("press s to enter testing set",250,120,size=30,fill="darkBlue")
    drawLabel("press k to enter training sets",250,160,size=30,fill="darkBlue")
    
    #draws the prediction box
    drawRect(app.width/2+100,100,300,200,fill=None,border="black")
    if app.havePrediction!=False:
        drawLabel(str(app.predictionValue),app.width/2+250,200,size=30,fill="red")
    else:
        drawLabel("unknown input",app.width/2+250,200,size=30,fill="red")

    #draws the buttons selecting between EMNIST and self training
    drawCircle(675,450,50,fill="green")
    drawLabel("emnist",675,450)
    drawCircle(825,450,50,fill="green")
    drawLabel("self Train",825,450)


    
    #draws the input button
    drawLabel("Press to input to AI",700,550,size=30)
    drawCircle(700,650,75,fill="red")
    
    


def onMousePress(app,mouseX,mouseY):
    testImages=[]
    testLabels=[]
    trainImages=[]
    trainLabels=[]
    #selects how you want to train AI (EMNIST or self training)
    if distance(675,450,mouseX,mouseY)<=50:
        app.isEmnist=True
        app.isSelfTrain=False
    elif distance(825,450,mouseX,mouseY)<=50:
        app.isEmnist=False
        app.isSelfTrain=True
    
    #handles case when you are training with EMNIST
    if distance(700,650,mouseX,mouseY)<=75 and app.isEmnist==True:
        #converts all test images into suitable formats and appends testImages and labels into lists
        for img in app.imgList:
            print(img)
            inputImage=convertToAIBasicLab(img)
            testImages.append(inputImage.tolist())
            testLabels.append(app.label)
        #turns lists into arrays and feed them into AI
        testImages=np.array(testImages)
        testLabels=np.array(testLabels)
        print(testImages,testLabels)
        print(app.yTrain)
        app.predictionValue=emnistAI(testImages,testLabels,app.isEmnist,app.isSelfTrain,app.xTrain,app.yTrain)
        app.havePrediction=True
    
    #handles case for self training
    elif distance(700,650,mouseX,mouseY)<=75 and app.isSelfTrain==True:
        #converts all test images into suitable formats and appends testImages and labels into lists
        for img in app.imgList:
            print(img)
            inputImage=convertToAIBasicLab(img)
            testImages.append(inputImage.tolist())
            testLabels.append(app.label)
        #turns lists into arrays
        testImages=np.array(testImages)
        testLabels=np.array(testLabels)
        print(len(app.imgTrainList),app.imgTrainList)
      
    
        #turns all training images labels into a list
        #imgTrainList is a 2d lists, each row have the same label
        for i in range(len(app.imgTrainList)):
            imgSet=app.imgTrainList[i]
            for img in imgSet:
                inputImage=convertToAIBasicLab(img)
                trainImages.append(inputImage.tolist())
                trainLabels.append(app.labelTrain[i])
         #turns lists into arrays
        app.xTrain=np.array(trainImages)
        app.yTrain=np.array(trainLabels)
        print(trainImages,trainLabels)
        #feeds everything into AI
        app.predictionValue=emnistAI(testImages,testLabels,app.isEmnist,app.isSelfTrain,app.xTrain,app.yTrain)
        app.havePrediction=True

        
    pass


#consulted source below to solve a bug    
#https://en.wikipedia.org/wiki/.DS_Store#:~:text=In%20the%20Apple%20macOS%20operating,Services%20Store%2C%20reflecting%20its%20purpose.
def onKeyPress(app,key):
    
    if key=="s":
        #gets all images in testing folder
        app.linkNames=getFileSet(app.getTextInput("Enter testing set"))
        #adds testing images to imgList
        for linkName in app.linkNames:
            if ".DS_Store" not in linkName: 
                img=openImage(linkName)
                app.imgList.append(img)
        #get the label
        app.label=app.getTextInput("Enter testing label")
    elif key=="k" and app.isSelfTrain==True:
        #gets all images in training folder you kust inputted
        app.linkNames=getFileSet(app.getTextInput("Enter training set"))
        singleFile=[]
        #adds all images to a list singleFile (all images are from one folder/file)
        #note to self, might be able to make singleFile into set in future
        for linkName in app.linkNames:
            if ".DS_Store" not in linkName:
                img=openImage(linkName)
                singleFile.append(img)
        #gets label and adds singleFile to list of training images from different files
        app.imgTrainList.append(singleFile)
        app.labelTrain.append(app.getTextInput("Enter training label"))

    
    


def main():
    runApp()

main()
the=10

