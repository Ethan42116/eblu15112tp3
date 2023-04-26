import numpy as np
from numpy import array
from equation_generator import * 
from cmu_graphics import *
from PIL import Image, ImageFilter,ImageDraw,ImageEnhance,ImageOps


class BackToMainPageButton():
    def __init__(self):
        self.left=500
        self.top=100
        self.width=100
        self.height=40
    def drawButton(self):
        drawRect(self.left,self.top,self.width,self.height,fill=rgb(198,216,175),border="black",borderWidth=1)
        drawLabel("back to mainpage",self.left+self.width//2,self.top+self.height//2)
    def checkClick(self,app,mouseX,mouseY):
        if self.left<=mouseX<self.left+self.width and self.top<=mouseY<self.top+self.height:
            #get draw new screen
            setActiveScreen('mainpage')

class IssuesPage():
    def __init__(self,app):
        self.left=app.width//2
        self.top=400
    def drawPage(self):
        drawLabel("Sorry! Seems like our AI make a mistake! Please take a",self.left,self.top,size=40)
        drawLabel("screenshot of previous page and send it to eblu@andrew.cmu.edu",self.left,self.top+45,size=40)
    








#the front page classes
class FrontPage():
    page=0


class NextPageButton(FrontPage):
    def __init__(self):
        self.left=1200
        self.top=600
        self.width=100
        self.height=40
        
    
    def drawButton(self):
        drawRect(self.left,self.top,self.width,self.height,fill="Green")
        drawLabel("next page",self.left+10,self.top+10,align="left-top",bold=True)
    
    def checkClick(self,app,mouseX,mouseY):
        if self.left<=mouseX<self.left+self.width and self.top<=mouseY<self.top+self.height:
            FrontPage.page+=1
            #gets a new Screen (the next page)
            setActiveScreen(f"frontpage{FrontPage.page}") if FrontPage.page<=1 else setActiveScreen(f"mainpage")
    

class PrevPageButton(FrontPage):
    def __init__(self):
        self.left=200
        self.top=600
        self.width=100
        self.height=40
    
    def drawButton(self):
        drawRect(self.left,self.top,self.width,self.height,fill="Green")
        drawLabel("previous page",self.left+10,self.top+10,align="left-top",bold=True)
    def checkClick(self,app,mouseX,mouseY):
        if self.left<=mouseX<self.left+self.width and self.top<=mouseY<self.top+self.height:
            if FrontPage.page>0:
                FrontPage.page-=1
                #gets a new Screen (the previous page)
                setActiveScreen(f"frontpage{FrontPage.page}") 

class Instructions(FrontPage):
    imagesSize=(300,300)
    negImageLink="neg_Instructions.png"
    oneImageLink="one_Instructions.png"
    #the content of the page
    page0='''Welcome to this math practice app. Let's get started.

    Please write your answer in the textbox on the center right of the screen.

    If you make a mistake, click on the olive eraser button on the left of the screen and drag your mouse on the mistake.



    Click the light green press to do another problem button to do another problem




    To check your answer, click on the red check button on the.




    As you get more answers correct, the problems will get harder. But will stop getting harder once you are doing 3 operations.
        Level 1: no fractions and exponents, one operation
        Level 2: two operations
        Level 3: three operations'''

    page1='''Tips about writing.

        1. In this project, an M is considered a negative sign. This is because the “-” seems to confuse our computer.
        2. Please write your 1 with a tall body and a long base. Our computer sometimes confuses a 1 for a 2. See the picture below for more details.

    '''

    def __init__(self,app):
        self.left=app.width//2
        self.textSize=20
        self.imgTop=300
        
    
    def drawPage(self):
        #draws the first front page
        if FrontPage.page==0:
            top=200
            for line in Instructions.page0.splitlines():
                if "Welcome" not in line: #checks if line is the title/first line of the page or a regular line

                    drawLabel(line,self.left,top,size=self.textSize)
                else:
                    drawLabel(line,self.left,top,size=self.textSize,bold=True)
                top+=20
        #draws the second front page
        if FrontPage.page==1:
            top=200
            for line in Instructions.page1.splitlines():
                if "Tips" not in line: #checks if line is the title/first line of the page or a regular line
                    drawLabel(line,self.left,top,size=self.textSize)
                else:
                    drawLabel(line,self.left,top,size=self.textSize,bold=True)

                top+=20
            #draws the images that are examples
            drawImage(Instructions.negImageLink,200,self.imgTop,width=Instructions.imagesSize[0],height=Instructions.imagesSize[1])
            drawImage(Instructions.oneImageLink,1000,self.imgTop,width=Instructions.imagesSize[0],height=Instructions.imagesSize[1])


class InstructonsEraser():
    def __init__(self):
        self.top=280-25
        self.left=20
        self.width=200
        self.height=50
        self.textSize=20
        self.highlighted=True
    def drawInstructionsEraser(self):
        if not self.highlighted:
            drawRect(self.left,self.top,self.width,self.height,fill=rgb(219,216,179),border="black",borderWidth=1)
            drawLabel("Eraser",self.left+self.width//2,self.top+self.height//2,size=self.textSize)
        else:
            drawRect(self.left,self.top,self.width,self.height,fill=rgb(219,216,179),border="black",borderWidth=5)
            drawLabel("Eraser",self.left+self.width//2,self.top+self.height//2,bold=True,size=self.textSize)

    def updateState(self):
        self.highlighted=not self.highlighted
    
class InstructionsRefresh():
    def __init__(self):
        self.top=200+11*20-100
        self.left=200
        self.width=200
        self.height=80
        self.textSize=20
        self.highlighted=True
    
    def drawInstructionsRefresh(self):
        if self.highlighted:
            drawRect(self.left,self.top,self.width,self.height,fill=rgb(198,216,175),border="black",borderWidth=5)
            
            
        else:
            drawRect(self.left,self.top,self.width,self.height,fill=rgb(198,216,175))

        drawLabel("click to do another",self.left,self.top+10,align="left-top",size=self.textSize)
        drawLabel("problem",self.left,self.top+30,align="left-top",size=self.textSize)
    
    def updateState(self):
        self.highlighted=not self.highlighted


class InstructionsCheck():
    def __init__(self):
        self.center=(20+60+150+200,200+15*20-30)
        self.radius=60
        self.textSize=20
        self.highlighted=True
  
    
    def drawInstructionsCheck(self):
        if self.highlighted:
            drawCircle(self.center[0],self.center[1],self.radius,fill="red",border="black",borderWidth=5)
        else:
            drawCircle(self.center[0],self.center[1],self.radius,fill="red")
        drawLabel("check answer",self.center[0],self.center[1],size=self.textSize)


    def updateState(self):
        self.highlighted=not self.highlighted
    
    

