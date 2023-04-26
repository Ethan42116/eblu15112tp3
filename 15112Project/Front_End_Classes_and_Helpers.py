#want to put all button classes in textbox test into this file, but CMU graphics does not like it

import numpy as np
from numpy import array
from equation_generator import * 
from cmu_graphics import *
from PIL import Image, ImageFilter,ImageDraw,ImageEnhance,ImageOps
from Image_Functions import alterImage, openImage,convertToAIBasicLab, spaceFinder,spaceFinderFloodFill



def distance(point1,point2):
    return ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**.5

def almostEqual(num1,num2):
    return abs(num1-num2)<0.0001



class Eraser():
    def __init__(self):
        self.isClicked=False
        self.width=200
        self.height=50
        self.left=100
        self.top=510
        self.textSize=20
    #eraser becomes bold when clicked on
    def drawEraser(self):
        if not self.isClicked:
            drawRect(self.left,self.top,self.width,self.height,fill=rgb(219,216,179),border="black",borderWidth=1)
            drawLabel("Eraser",self.left+self.width//2,self.top+self.height//2,size=self.textSize)
        else:
            drawRect(self.left,self.top,self.width,self.height,fill=rgb(219,216,179),border="black",borderWidth=5)
            drawLabel("Eraser",self.left+self.width//2,self.top+self.height//2,bold=True,size=self.textSize)

    def checkClick(self,mouseX,mouseY):
        if self.left<=mouseX<self.left+self.width and self.top<=mouseY<self.top+self.height:
            self.isClicked= not (self.isClicked)

#the button to generate a new problem
class Refreshbutton():
    def __init__(self):
        self.top=600
        self.left=100
        self.width=200
        self.height=100
        self.textSize=20
    
    def drawRefreshButton(self):
        drawRect(self.left,self.top,self.width,self.height,fill=rgb(198,216,175))
        drawLabel("click to do another",self.left,self.top+10,align="left-top",size=self.textSize)
        drawLabel("problem",self.left,self.top+30,align="left-top",size=self.textSize)

    
    def checkClick(self,app,mouseX,mouseY):
        #resets everything once clicked
        if self.left<=mouseX<self.left+self.width and self.top<=mouseY<self.top+self.height:
            app.image=Image.new('RGB', (app.textDimention*2, app.textDimention), (255,255,255))
            app.image2=Image.new('RGB', (app.textDimention*2, app.textDimention), (255,255,255))
            app.draw = ImageDraw.Draw(app.image)
            app.draw2 = ImageDraw.Draw(app.image2)
            app.predictionValue=np.array([])
            app.predictionValue2=np.array([])
            app.question=Question(app.scoreBoard.score//6)
            app.output.updateVal(None)
            app.reportIssueButton.exists=False
            app.timer.resetTime()
            #return True

#a button to check answers
class CheckButton():
    def __init__(self):
        self.center=(400,550)
        self.radius=60
        self.textSize=20
  
    
    def drawCheckButton(self):
        drawCircle(self.center[0],self.center[1],self.radius,fill="red")
        drawLabel("check answer",self.center[0],self.center[1],size=self.textSize)
    
    def checkClick(self,app,mouseX,mouseY):
        if distance((mouseX,mouseY),self.center)<self.radius:
            readWriting(app)
            #if correct, ensure that the scoreboard gets updated and "correct" is displayed
            if getAnswer(app)==app.question.correct:
                app.output.updateVal(True)
                app.reportIssueButton.exists=False
                app.scoreBoard.updateVal(1)
            else:
                #if correct, ensure that the incorrect message is displayed and report issue button is displayed, you will also deduct one point from the scoreboard
                app.output.updateVal(False)
                app.reportIssueButton.exists=True
                app.scoreBoard.updateVal(-1)
            #return True

#the result button class
class Result():
    def __init__(self):
        self.left=500
        self.top=200
        self.isCorrect2=None
        self.value=getAnswer(app) #reads the numbers you just wrote
        print(self.isCorrect2)
    #if the user did do not have answer, don't do anything
    #otherwise says if user is correct or wrong
    def drawOutput(self,app):
        #no answer
        if self.isCorrect2==None:
            return None
        #right answer
        elif self.isCorrect2==True:
            drawLabel("correct",self.left,self.top,size=30)
            #draws confetti if answer is correct
            app.confetti.drawConfetti()

        #wrong answer
        elif self.isCorrect2==False: 
            drawLabel(f"not quite,you wrote {self.value}, but the correct answer is {app.question.correct}",self.left,self.top,size=30)
            
    #updates wether if the user's answer is correct
    def updateVal(self,newCorrect):
        self.isCorrect2=newCorrect
        #ready to draw confetti if answer is correct
        if self.isCorrect2:
            app.confetti.isDraw=True
            app.confetti.spriteCounter=0
        self.value=getAnswer(app)

#the question generated by the equation generator
class Question():
    def __init__(self,level=0):
        #caps level
        self.level=level if level<=2 else 2
        self.textTop=300+50 #the top of the question label
        self.textSize=20


        #generates harder question with increasing difficulty
        if self.level==0:
            self.fontSize=200
            #self.problem,self.correct=getSimpleArithmetic()
            self.problem,self.correct=getSimpleArithmetic()
        elif self.level==1:
            self.fontSize=int(200*9/12)
            self.problem,self.correct=getHarderArithmetic()
        else:
            self.fontSize=int(200*7/12)
            self.problem,self.correct=getHardestArithmetic()
        #checks if answer is a fraction or not and determines how to align the answer textbox
        if not almostEqual(self.correct,(int(self.correct))):
            self.isFraction=True
            app.textTop=300-200-5+50+50
        else:
            self.isFraction=False
            app.textTop=300
        #gets the text left
        app.textLeft=200+(len(self.problem)+3)*int(self.fontSize/2)
    def drawQuestion(self):
        #shrinks font size as question gets harder because question takes up more space
        if self.level==0:
            self.fontSize=200
            drawLabel(self.problem+" = ",100,self.textTop,size=self.fontSize,align="left-top",font="monospace")
        elif self.level==1:
            self.fontSize=int(200*9/12)
            drawLabel(self.problem+" = ",100,self.textTop,size=self.fontSize,align="left-top",font="monospace")
        else:
            self.fontSize=int(200*7/12)
            drawLabel(self.problem+" = ",100,self.textTop,size=self.fontSize,align="left-top",font="monospace")
        #also draws the level display
        drawLabel(f"Level: {self.level+1}",700,50,size=self.textSize,bold=True)

    #updates textLeft when question changes
    def updateTextLeft(self,app):
        app.textLeft=200+(len(self.problem)+3)*int(self.fontSize/2)

#the board keeping track of how much you got right
class ScoreBoard:
    def __init__(self):
        self.score=0
        self.left=100
        self.top=50
        self.boardDimentions=(100,100)
    
    def drawScoreBoard(self):
        drawRect(self.left,self.top,self.boardDimentions[0],self.boardDimentions[1],fill=rgb(232,205,234),borderWidth=2,border="Black")
        drawLabel(f"Score: {self.score}",self.left+self.boardDimentions[0]/2,self.top+self.boardDimentions[1]/2)
    
    def updateVal(self,num):
        if self.score+num>=0:
            self.score+=num

#the buttpon that you click to report a issue with the AI misreading your answer
class ReportIssueButton():
    def __init__(self,exists=False):
        self.left=500
        self.top=100
        self.width=100
        self.height=40
        self.exists=exists
    def drawReportIssueButton(self):
        if self.exists:
            drawRect(self.left,self.top,self.width,self.height,fill=rgb(184,224,166),border="black",borderWidth=1)
            drawLabel("report issue",self.left+self.width//2,self.top+self.height//2)
    
    def checkClick(self,app,mouseX,mouseY):
        if self.exists and self.left<=mouseX<self.left+self.width and self.top<=mouseY<self.top+self.height:
            #switch the screen when clicked
            setActiveScreen('issuespage')


        
    




#gets an answer from raw AI output
def getAnswer(app):
    answer=0
    factor=1

    #converts array to string
    answerString=""

    #handels case of the user writing nothing/not able to be discerned by space finder function
    if len(app.predictionValue)==0:
        return "not valid answer"
    

    for c in app.predictionValue:
        answerString+=c
    
    #converts string to number
    for num in answerString:
        if num=="-":
            factor=-1
        else:
            answer*=10
            answer+=int(num)
    #used array.size because the complier told be so, compiler is source!!!
    #DeprecationWarning: The truth value of an empty array is ambiguous. Returning False, but in future this will result in an error. Use `array.size > 0` to check that an array is not empty.
    if (app.predictionValue2.size)!=0:
        factor2=1
        answerString=""
        #converts array to string
        for c in app.predictionValue2:
            answerString+=c

        demoninator=0
        #converts string to number
        for num in app.predictionValue2:
            if num=="-":
                factor2=-1
            else:
                demoninator*=10
                demoninator+=int(num)
        print(answer/demoninator*factor)
        return answer/demoninator*factor*factor2
    return answer*factor

#converts writing to AI

def readWriting(app):
    testImages=[]
    testLabels=[]
    #gets the list of character images
    app.imgList=spaceFinder(app.image)

    #converts imgList into a format that is suitable for the AI
    for img in app.imgList:
        inputImage=convertToAIBasicLab(img)
        testImages.append(inputImage.tolist())
        #I think you need to include a random label otherwise the AI will break, might be wrong though
        testLabels.append("A")
    testImages=np.array(testImages)
    testLabels=np.array(testLabels)
    #feeds the images into AI
    if len(testImages)>0: #checks that input is not empty
        app.predictionValue=app.ai.readImage(testImages,testLabels) 
    else:
        app.predictionValue=np.array([])
    
    #if the question is a fraction, read the denominator. Everything works exactly like neumerator
    if app.question.isFraction:
        testImages2=[]
        testLabels2=[]
        app.imgList2=spaceFinder(app.image2)
        

        for img2 in app.imgList2:
            inputImage2=convertToAIBasicLab(img2)
            testImages2.append(inputImage2.tolist())
            testLabels2.append("A")
        testImages2=np.array(testImages2)
        testLabels2=np.array(testLabels2)
        if len(testImages2)>0: #checks that input is not empty
            app.predictionValue2=app.ai.readImage(testImages2,testLabels2)
        else:
            app.predictionValue2=np.array([])

#got idea of confetti while brainstorming with Sergio Leal
#source:the kirb class in kirbleBirdStarter.py
class Confetti():
    def __init__(self,app):
        self.size=150
        self.top=app.output.top-100
        self.left=app.output.left+100
        self.isDraw=False
        self.confettiGif=Image.open('confetti.gif')
        self.spriteList=[]
        self.spriteCounter=0
        #puts each frame of confetti into list
        for frameNumber in range(self.confettiGif.n_frames):
            self.confettiGif.seek(frameNumber)
            frame=self.confettiGif.resize((self.size,self.size))
            frame=CMUImage(frame)
            
            self.spriteList.append(frame)
        
    def drawConfetti(self):
        if self.isDraw:
            frame=self.spriteList[self.spriteCounter]
            drawImage(frame,self.left,self.top)
    
    #updates the confetti to ensure animation
    def updateConfetti(self):
        self.spriteCounter=(self.spriteCounter+1)
        if self.spriteCounter>=len(self.spriteList)-6:
            self.isDraw=False

        
        
        
    

    


    

class Timer():
    def __init__(self):
        self.top=50
        self.left=900
        self.time=0
        self.textSize=20
    def drawTimer(self):
        drawLabel(f"time: {self.time}",self.left,self.top,size=self.textSize,bold=True)
    def updateTime(self):
        self.time+=1
    def resetTime(self):
        self.time=0