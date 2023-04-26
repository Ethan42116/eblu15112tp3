#talked to Petros Emmanouilidis, Gongwei Wang, Arnav Sabharwal to brainstorm features and improve user experience

import PIL
import numpy as np
import os, pathlib
from numpy import array
import random
import copy
from cmu_graphics import *
from PIL import Image, ImageFilter,ImageDraw,ImageEnhance,ImageOps
import json
from Image_Functions import alterImage, openImage,convertToAIBasicLab, spaceFinder,spaceFinderFloodFill
from Basic_AI_Lab import emnistAI
from files_navigator import getFileSet  
from equation_generator import getSimpleArithmetic
from AI_Class import AI
from Front_End_Classes_and_Helpers import *
from non_mainpage_classes import*



def onAppStart(app):
    getNegTrainingData(app)
    app.width=1500
    app.height=1500

    app.question=Question() #app.textTop is defined in questions because it depends if the questions is a fraction or not
    
    #the left of the textbox is determined by how long the problem is
    #app.textLeft=200+(len(app.question.problem)+3)*int(app.question.fontSize/2)
    #dimentions of textBox
    app.textDimention=200 

    #gets the blank textbox/whiteboard prepared
    #copied from PIL Image Demo (makeNewImages.py) presented during lecture
    app.image = Image.new('RGB', (app.textDimention*2, app.textDimention), (255,255,255))
    app.draw = ImageDraw.Draw(app.image)
    app.image2=Image.new('RGB', (app.textDimention*2, app.textDimention), (255,255,255))
    app.draw2 = ImageDraw.Draw(app.image2)
    #trains the AI at the start so you don't need to retrain it every time you check answer
    app.ai=AI(True,app.negImages,app.negLabels)
   
    #gets the predicted AI Value, currently blank because you did not feed it anything
    app.predictionValue=np.array([])
    app.predictionValue2=np.array([])
    #sets buttons and features in mainpage 
    app.timer=Timer()
    app.eraser=Eraser()
    app.refresh=Refreshbutton()
    app.check=CheckButton()
    app.output=Result()
    app.reportIssueButton=ReportIssueButton()
    app.scoreBoard=ScoreBoard()
    app.confetti=Confetti(app)
    #app.sound=loadSound("correct.mp3"), does not work will want to fix it in the future

    #sets features in non mainpage up
    app.issuesPage=IssuesPage(app)
    app.backButton=BackToMainPageButton()
    app.instructions=Instructions(app)
    app.prevPageButton= PrevPageButton()
    app.nextPageButton= NextPageButton()
    #draws the blinking buttons on the first instructions page
    app.instructionsEraser=InstructonsEraser()
    app.instructionsRefresh=InstructionsRefresh()
    app.instructionsCheck=InstructionsCheck()
    app.Denominator=None
    app.stepsPerSecond=10
    #variables to keep track of time on each page
    app.mainpage_time=0
    app.frontpage_time=0

def frontpage0_redrawAll(app):
    #draws background
    drawRect(0,0,app.width,app.height,fill=rgb(239,164,139))
    #draws the instructions text and buttons
    app.nextPageButton.drawButton()
    app.instructions.drawPage()
    #draws the flashing buttons
    app.instructionsEraser.drawInstructionsEraser()
    app.instructionsRefresh.drawInstructionsRefresh()
    app.instructionsCheck.drawInstructionsCheck()
    
    

def frontpage1_redrawAll(app):
    #draws background
    drawRect(0,0,app.width,app.height,fill=rgb(239,164,139))
    #draws the instructions text and buttons
    app.nextPageButton.drawButton()
    app.prevPageButton.drawButton()
    app.instructions.drawPage()


def issuespage_redrawAll(app):
    #draws background
    drawRect(0,0,app.width,app.height,fill=rgb(239,164,139))
    app.backButton.drawButton()
    app.issuesPage.drawPage()


def mainpage_redrawAll(app):
    #draws background
    drawRect(0,0,app.width,app.height,fill=rgb(239,164,139))
    
    #draws writing box
    drawImage(CMUImage(app.image),app.textLeft,app.textTop)
    drawRect(app.textLeft,app.textTop,app.textDimention*2,app.textDimention,fill=None,border="black")
    
    
    #draws buttons
    app.question.drawQuestion()
    app.eraser.drawEraser()
    app.refresh.drawRefreshButton()
    app.check.drawCheckButton()
    app.output.drawOutput(app)
    app.scoreBoard.drawScoreBoard()
    app.reportIssueButton.drawReportIssueButton()
    app.timer.drawTimer()
    #if the question is a fraction, draw the fraction parts
    if app.question.isFraction:
        drawLine(app.textLeft-20,app.textTop+app.textDimention+5,app.textLeft+app.textDimention*2+20,app.textTop+app.textDimention+5,fill="black",lineWidth=6)
        drawImage(CMUImage(app.image2),app.textLeft,app.textTop+app.textDimention+10)
        drawRect(app.textLeft,app.textTop+app.textDimention+10,app.textDimention*2,app.textDimention,fill=None,border="black")
    

    
    #drawRect(app.textLeft,app.textTop,app.textDimention,app.textDimention,fill=None,border="black")
    #for position in app.inputSet:
        #drawCircle(position[0],position[1],10,fill="Black")

def mainpage_onMouseDrag(app,mouseX,mouseY):
    #checks to see if mouse is in writing box
    if app.textLeft<=mouseX<app.textLeft+app.textDimention*3 and app.textTop<=mouseY<app.textTop+app.textDimention:
        #draws if eraser is off
        if not (app.eraser).isClicked:
            app.draw.ellipse([(mouseX-10-app.textLeft,mouseY-10-app.textTop),(mouseX+10-app.textLeft,mouseY+10-app.textTop)], width=10, fill=(0, 0, 0))
        #erases if eraser is on
        elif app.eraser.isClicked:
            imgArray=np.array(app.image)
            row=mouseY-app.textTop
            col=mouseX-app.textLeft
            spaceFinderFloodFill(imgArray,row,col,set())
            app.image=Image.fromarray(imgArray.astype(np.uint8))
            app.draw = ImageDraw.Draw(app.image)
        
    #if the question is a fraction, draw the fraction parts
    if app.question.isFraction:
        if app.textLeft<=mouseX<app.textLeft+app.textDimention*3 and app.textTop+app.textDimention+10<=mouseY<app.textTop+2*app.textDimention+10:
        #draws if eraser is off
            if not (app.eraser).isClicked:
                app.draw2.ellipse([(mouseX-10-app.textLeft,mouseY-10-(app.textTop+app.textDimention+10)),(mouseX+10-app.textLeft,mouseY+10-(app.textTop+app.textDimention+10))], width=10, fill=(0, 0, 0))
            #erases if eraser is on
            elif app.eraser.isClicked:
                img2Array=np.array(app.image2)
                row=mouseY-app.textTop-app.textDimention-10
                col=mouseX-app.textLeft
                spaceFinderFloodFill(img2Array,row,col,set())
                app.image2=Image.fromarray(img2Array.astype(np.uint8))
                app.draw2 = ImageDraw.Draw(app.image2)





def mainpage_onMousePress(app,mouseX,mouseY):
    #checks to see which button you clicked
    app.eraser.checkClick(mouseX,mouseY)
    app.refresh.checkClick(app,mouseX,mouseY)
    app.check.checkClick(app,mouseX,mouseY)
    app.reportIssueButton.checkClick(app,mouseX,mouseY)

def frontpage0_onMousePress(app,mouseX,mouseY):
    app.nextPageButton.checkClick(app,mouseX,mouseY)

def frontpage1_onMousePress(app,mouseX,mouseY):
    app.prevPageButton.checkClick(app,mouseX,mouseY)
    app.nextPageButton.checkClick(app,mouseX,mouseY)

def issuespage_onMousePress(app,mouseX,mouseY):
    app.backButton.checkClick(app,mouseX,mouseY)



def mainpage_onStep(app):
    app.mainpage_time+=1
    if app.mainpage_time%10==0:
        #updates timer every second
        app.timer.updateTime()
    #updates confetti every frame
    app.confetti.updateConfetti()

#allows the buttons in the first instructions page to flash every second
def frontpage0_onStep(app):
    app.frontpage_time+=1
    if app.frontpage_time%10==0:
        app.instructionsEraser.updateState()
        app.instructionsRefresh.updateState()
        app.instructionsCheck.updateState()
        

    


#mainly for testing, 
def mainpage_onKeyPress(app,key):
    #converts writing to AI, just there for testing purposes
    if key=="k":
        testImages=[]
        testLabels=[]
        app.imgList=spaceFinder(app.image)
        #print(len(app.imgList))

        for img in app.imgList:
            inputImage=convertToAIBasicLab(img)
            #print(inputImage.astype(np.uint8))
            Image.fromarray(inputImage.astype(np.uint8)).show()
            testImages.append(inputImage.tolist())
            testLabels.append("A")
        testImages=np.array(testImages)
        testLabels=np.array(testLabels)
        #app.predictionValue=emnistAI(testImages,testLabels,True,False,None,None)
        app.predictionValue=app.ai.readImage(testImages,testLabels)
        print(app.predictionValue)
        
        #if the question is a fraction, read the denominator
        if app.question.isFraction:
            testImages2=[]
            testLabels2=[]
            app.image2.save("debug.png")
            app.imgList2=spaceFinder(app.image2)
            

            for img2 in app.imgList2:
                inputImage2=convertToAIBasicLab(img2)
                Image.fromarray(inputImage2.astype(np.uint8)).show()
                testImages2.append(inputImage2.tolist())
                testLabels2.append("A")
            testImages2=np.array(testImages2)
            testLabels2=np.array(testLabels2)
            #app.predictionValue=emnistAI(testImages,testLabels,True,False,None,None)
            app.predictionValue2=app.ai.readImage(testImages2,testLabels2)
            print(app.predictionValue2)




#handles converting the file of all negative training images to data that can be fed to AI            
#https://stackoverflow.com/questions/52977871/concatenate-3-d-arrays-python concatenating 3d arrays            
def getNegTrainingData(app):
    app.negImages=[]
    #gets all images in negvals folder in a set
    app.negImagesNames=getFileSet("negVals")
    #gets lable of each image
    #note to self, need to fix bug, negImagesNames might have DS_Store
    app.negLabels=np.array(["-"]*len(app.negImagesNames))
        #adds all images to a list singleFile (all images are from one folder/file)
        #note to self, might be able to make singleFile into set in future
    for linkName in app.negImagesNames:
        #source about strange .DS_Store file in my image set
        ##https://en.wikipedia.org/wiki/.DS_Store#:~:text=In%20the%20Apple%20macOS%20operating,Services%20Store%2C%20reflecting%20its%20purpose. 
        #Source to help understand what DS_Store is (help me know what was breaking my code)
        if ".DS_Store" not in linkName:
            img=openImage(linkName)
            img=convertToAIBasicLab(img)
            app.negImages.append(img)
    app.negImages=np.array(app.negImages)

#source: copied from soundTest.py from the TAs
def loadSound(relativePath):
    # Convert to absolute path (because pathlib.Path only takes absolute paths)
    absolutePath = os.path.abspath(relativePath)
    # Get local file URL
    url = pathlib.Path(absolutePath).as_uri()
    # Load Sound file from local URL
    return Sound(url)


def main():
    runAppWithScreens(initialScreen='frontpage0')
main()

