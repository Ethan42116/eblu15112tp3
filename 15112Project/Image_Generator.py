
import PIL
import numpy as np
from numpy import array
import random
import copy
from cmu_graphics import *
from PIL import Image, ImageFilter,ImageDraw,ImageEnhance,ImageOps
import json
from Image_Functions import alterImage, openImage

def distance(x1,y1,x2,y2):
    return ((x2-x1)**2+(y2-y1)**2)**.5

def onAppStart(app):
    app.width=1000
    app.height=1000
    app.x=2019
    app.img=None
    app.dropDown=[(650,100+i*75) for i in range(0,5)]
    app.dropDownCircle=[(650-150,100+i*75) for i in range(0,5)]
    app.alter=[0]*5
    app.dropDownTitles=["rotation","blurring","randomlyAlterV2","width mutiplier","height mutiplier"]
    app.previousValue=0
    pass

def redrawAll(app):
    #draws image input box
    drawLabel("press a key to enter image file name",250,160,size=30,fill="darkBlue")
    drawRect(50,200,400,400,fill=None,border="black")
    if app.img!=None:
        drawImage(app.linkName,250,400,align='center', width=app.imgSize[0],height=app.imgSize[1])
        drawLabel("is this image correct?",250,400+app.imgSize[1]/2+30,size=30,fill="darkBlue")
    else:
        drawLabel("no image slected",250,400,size=30,fill="darkBlue")
    
    #draws all dropdowns
    for i in range(len(app.dropDown)):
        dropDownCenter=app.dropDown[i]
        circleCenter=app.dropDownCircle[i]
        drawRect(dropDownCenter[0],dropDownCenter[1],300,30,
        fill=None,border="black",align="center")
        drawCircle(circleCenter[0],circleCenter[1],20,fill="black")
        drawLabel(app.alter[i],dropDownCenter[0]+160,dropDownCenter[1])
        drawLabel(app.dropDownTitles[i],dropDownCenter[0],dropDownCenter[1]-35,size=20)
    
    #draws the convert button
    drawCircle(650,650,75,fill="red")
    
    
def onMouseDrag(app,mouseX,mouseY):
    #checks if you are moving dropdown menu
    for i in range(len(app.dropDownCircle)):
        circleCenter=app.dropDownCircle[i]
        dropDownCenter=app.dropDown[i]

        if distance(mouseX,mouseY,circleCenter[0],circleCenter[1])<=20:
            #checks if mouse is within the dropDown menu
            if dropDownCenter[0]-150<mouseX<dropDownCenter[0]+150:
                app.dropDownCircle[i]=(mouseX,circleCenter[1])
                
                dropDownLeft=dropDownCenter[0]-150
                #subtract mouseX by dropDownLeft to get distance from left edge
                convertX(app,mouseX-dropDownLeft,i)


#converts center coorindates of the dropDown Circle corresponding values
#type = 0 -->rotation
#type = 1 -->blurring
#type = 2 -->randomlyAlterV2
#type = 3 -->width mutiplifer
#type = 4 -->height mutiplier
def convertX(app,circleX,typeChange):
    ratio= circleX/300
    #use int(x*100)/100 to truncate decimal places
    if typeChange==0:
        app.alter[0]= int(ratio*45)
    elif typeChange==1:
        app.alter[1]= int(ratio*6)
    elif typeChange==2:
        app.alter[2]= int(ratio*4)
    #elif typeChange==3:
        #app.alter[3]= int(ratio*4)
    elif typeChange==3:
        app.alter[3]= int(ratio*4)
    else:
        app.alter[4]= int(ratio*4)


        

    
    
    


        
    

    #drawImage("letter-A.png", 200, 230, align='center', width=150, height=150)

def onMousePress(app,mouseX,mouseY):
    #checks if you clicked the big red button
    if distance(mouseX,mouseY,650,650)<75:
        app.img.show()
        #sets current value to previous value, used to ensure images do not overlab after different function calls
        #for more information, please see function documentation
        app.previousValue=alterImage(app.img,app.alter,app.previousValue)
    
#allowd you to input image name at any key press
def onKeyPress(app,key):
    app.linkName=app.getTextInput("Enter name")
    app.img=openImage(app.linkName)
    app.imgSize=(app.img).size
    


def main():
    runApp()

main()
the=10

