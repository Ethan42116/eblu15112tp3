import PIL # source for debugging a bug: https://stackoverflow.com/questions/10748822/img-image-openfp-attributeerror-class-image-has-no-attribute-open
from PIL import Image, ImageFilter,ImageDraw,ImageEnhance,ImageOps
import numpy as np
from numpy import array
import random
import copy
import sys
########################################################################################################################################
########################################################################################################################################
#Here are some more general sources, 
#more specficic sources can be found inside code(usally right above the function the source is related to)


#potential inspirations/readings for it 
#https://stackoverflow.com/questions/46385999/transform-an-image-to-a-bitmap
#https://stackoverflow.com/questions/47909323/how-to-create-bitmap-with-pillow-from-image-without-saving-image
#https://www.geeksforgeeks.org/cropping-an-image-in-a-circular-way-using-python/
#https://www.reddit.com/r/Python/comments/4u7qlu/pillow_vs_opencv/



#readings that taught me how to use PIL and to answer questions
#sources of basic functions such as rotateImage
#https://stackoverflow.com/questions/46385999/transform-an-image-to-a-bitmap
#https://www.tutorialspoint.com/python_pillow/index.html (entire tutorial)
#https://pillow.readthedocs.io/en/stable/index.html (entire documentation)
#https://www.geeksforgeeks.org/python-pil-image-crop-method/# (image cropping)
#https://www.youtube.com/watch?v=6Qs3wObeWwc&ab_channel=CoreySchafer
#https://www.youtube.com/watch?v=5QR-dG68eNE&ab_channel=ClearCode
#https://towardsdatascience.com/image-processing-opencv-vs-pil-a26e9923cdf3
#https://www.geeksforgeeks.org/python-pil-image-resize-method/  (resizing image)
#https://stackoverflow.com/questions/2232742/does-python-pil-resize-maintain-the-aspect-ratio   (resizing image)
#https://www.geeksforgeeks.org/change-the-ratio-between-width-and-height-of-an-image-using-python-pillow/ (resizing image )
#https://stackoverflow.com/questions/10965417/how-to-convert-a-numpy-array-to-pil-image-applying-matplotlib-colormap (converting array to image)
#https://stackoverflow.com/questions/18522295/python-pil-change-greyscale-tif-to-rgb (converting images from one type to another)
# https://stackoverflow.com/questions/44739775/how-to-get-python-pillow-pil-version (getting version of PIL)
# https://stackoverflow.com/questions/55319949/pil-typeerror-cannot-handle-this-data-type :helped fix bug converting array to image (.astype(np.uint8))

#misc: OOP (learned before class covered classes) and debug sources
#https://stackoverflow.com/questions/37837682/python-class-input-argument
#https://www.w3schools.com/python/python_classes.asp
#https://www.freecodecamp.org/news/python-typeerror-int-object-not-subscriptable-solved/#:~:text=Why%20the%20%22TypeError%3A%20%27int,an%20integer%20as%20an%20array
#https://stackoverflow.com/questions/62221258/importing-variables-from-python-script-into-another-script-is-throwing-errors-th
# https://stackoverflow.com/questions/10748822/img-image-openfp-attributeerror-class-image-has-no-attribute-open (werid import error debug)
# https://rednafi.github.io/reflections/modify-iterables-while-iterating-in-python.html to debug modifying while iterating, but don't think I used it extensively
#https://www.freecodecamp.org/news/python-multiline-comment-how-to-comment-out-multiple-lines-in-python/ (how to do mutiline comments)


#numpy sources (mainly about array)
#https://numpy.org/doc/stable/index.html (many pages in numpy docs)
#https://www.scaler.com/topics/length-of-array-in-python/
#https://www.w3schools.com/python/numpy/numpy_creating_arrays.asp
#https://www.w3schools.com/python/numpy/numpy_array_join.asp
#https://www.youtube.com/watch?v=mkbgEvUkSaM
#https://www.youtube.com/watch?v=VhU5o8Yobqc&ab_channel=NareshiTechnologies
#https://www.pluralsight.com/guides/different-ways-create-numpy-arrays
#https://www.geeksforgeeks.org/how-to-append-a-numpy-array-to-an-empty-array-in-python/ (appending array, don't think I used)
#https://www.pluralsight.com/guides/different-ways-create-numpy-arrays 


########################################################################################################################################
########################################################################################################################################




def rotateImage(img,angle):
    return img.rotate(angle,fillcolor=(255,255,255))
    #add expand to prevent losing image information
    #add somthing that can crop the image back to original size??

def imageScale(img,num):
    return ImageOps.scale(image=img,factor=num)

def reSize(img,newSize):
    img=img.resize(newSize,Image.LANCZOS)
    return img

#inspiration from Petros Emmanduidalis 
#also inspiration from https://stackoverflow.com/questions/46385999/transform-an-image-to-a-bitmap
#takes in a image and randomly removes some parts of the image to distort it
def randomlyAlterV2(img):



    img=copy.deepcopy(img)
    imgArray=np.array(img)
    rows,cols=len(imgArray),len(imgArray[0])
    

    target=random.randrange(1,2)
    count=0
    while count<target:
        #gets random pixel
        randRow=int(random.random()*rows)#might need to fix to include inclsivity
        randCol=int(random.random()*cols)#might need to fix to include inclsivity
        currentPixel=imgArray[randRow][randCol]
        sumPixel=sum(currentPixel)
        #checks if it is dark pixel
        if sumPixel<(255*1.5):
            count+=1
            
            edge=set([(randRow,randCol)])
            #imgArray=removePixel(imgArray,0,randRow,randCol)
            #darkPixelsSet=set()
            #countDarkPixels(copy.deepcopy(imgArray),randRow,randCol,darkPixelsSet)
            #numDarkPixels=len(darkPixelsSet)
            #print (numDarkPixels,"test")
            darkPixels=set()
            countDarkPixels(imgArray,randRow,randCol,darkPixels)
            print(len(darkPixels),"pixels")
            print(len(imgArray),len(imgArray[0]))

            removePixelV2(imgArray,edge,1,len(darkPixels)//9)

            
        
    return Image.fromarray(imgArray)

#learned about this in 112 floodfilling notes(forgot what year it is) and Dr. Taylor, (did directly not copy code, but used floodfilling, which I learned in this class)
#counts the dark pixels in a single character, have some problems that need fixing
def countDarkPixels(imgArray,darkPixelRow,darkPixelCol,searched):
    rows,cols=len(imgArray),len(imgArray[0])
    if 0<darkPixelRow<rows and 0<darkPixelCol<cols and sum(imgArray[darkPixelRow][darkPixelCol])<255*3*.7 and (darkPixelRow,darkPixelCol) not in searched:
        
        searched.add((darkPixelRow,darkPixelCol))
        countDarkPixels(imgArray,darkPixelRow+1,darkPixelCol,searched)
        countDarkPixels(imgArray,darkPixelRow-1,darkPixelCol,searched)
        countDarkPixels(imgArray,darkPixelRow,darkPixelCol+1,searched)
        countDarkPixels(imgArray,darkPixelRow,darkPixelCol-1,searched)


#source/inspirations for removePixelV2
#used description of algorithim and specifically anmation at 5:23 for learn about specific floodfill algorithm of video below
#did not really use the code they provided in video, made my own code
#https://www.youtube.com/watch?v=VuiXOc81UDM&ab_channel=Insidecode
#used old 15112 recursion notes to get inspitation on how to implement something similar to BFS search (I think it is mazer solver, but not entirely sure)
#https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/ to learn more, but did not really use
#https://www.youtube.com/watch?v=pcKY4hjDrxk&ab_channel=AbdulBari to learn about BFS in general
#https://www.youtube.com/watch?v=lyVRSBFVQQM&ab_channel=KindsonTheGenius to learn about BFS in general

#In general, I am pretty sure that I used the sources to learn about bfs and how it works, but I implement the code myself
#removes a count number of pixels around edge
#removes target number pixels from the image using a special type of floodfilling
def removePixelV2(imgArray,edge,count,target):

    rows,cols=len(imgArray),len(imgArray[0])
    #target=int(rows*cols/200)
    
    oldLen=len(edge)
    oldEdge=copy.deepcopy(edge)
    for pixel in oldEdge:
        #gets pixels around pixel
        for i in range(-1,2):
            col=pixel[1]+i
            for j in range(2):
                row=pixel[0]+j
                #checks if pixel around pixel is outside of image
                if row>0 and row<rows and col>0 and col<cols:
                    currentPixel=(row,col)
                    #checks if currentPixel is already counted
                    if currentPixel not in edge:
                        #checks if currentPixel is a dark pixel and if you have not reached target
                        if sum(imgArray[row][col])<255*3*.7 and count<target:
                            imgArray[row][col]=[255, 255, 255]
                            edge.add(currentPixel)
                            count+=1
                            
                        else:
                            print(sum(imgArray[row][col]))
                    else:
                        #imgArray[row][col]=[130, 5, 1]
                        pass
    
    #keep running as long as you have not floodfilled everything and you have not reached target
    if len(edge)!=oldLen and count<target:
        removePixelV2(imgArray,edge,count,target)
    


                            
                          





#low num grey, high num high vibrance (note to self)
def enhanceColors(img,num):
    blurColor=ImageEnhance.Color(img)
    return blurColor.enhance(num)


def enhanceSharpness(img,num):
    sharp=ImageEnhance.Sharpness(img)
    return sharp.enhance(num)


# source: https://stackoverflow.com/questions/4142687/using-pythons-pil-how-do-i-enhance-the-contrast-saturation-of-an-image
def enhanceContrast(img,num):
    sharp=ImageEnhance.Contrast(img)
    return sharp.enhance(num)

def enhanceBrightness(img,num):
    sharp=ImageEnhance.Brightness(img)
    return sharp.enhance(num)








#blur functions
def simpleBlur(img):
    return img.filter(ImageFilter.BLUR)

def boxBlur(img,radius):
    return img.filter(ImageFilter.BoxBlur(radius))

def guassianBlur(img,radius):
    return img.filter(ImageFilter.GaussianBlur(radius))

#https://www.geeksforgeeks.org/python-pil-image-crop-method/
def cropImage(img,position):
    return img.crop(position)



#convertis to bitmap
def getBitMap(img):
    bitImg=img.convert("1")
    return bitImg
#note: Image.tobitmap(name='image') might work better?


def getGreyScale(img):
    greyImg=img.convert('L')
    return greyImg

#sources
#https://stackoverflow.com/questions/17506163/how-to-convert-a-boolean-array-to-an-int-array
#https://www.youtube.com/watch?v=6nGCGYWMObE&list=PL8dPuuaLjXtO65LeD2p4_Sb5XQ51par_b&index=6&ab_channel=CrashCourse
#converts image to a format(array) that can be read by AI
def convertToAIBasicLab(img):
    img2=PIL.ImageOps.invert(img)
    img2=getGreyScale(img2)
    img2=reSize(img2,(28,28)) 
    return np.array(img2,dtype=int)

#https://stackoverflow.com/questions/18522295/python-pil-change-greyscale-tif-to-rgb
#ensure that image always has RGB (255,255,255)
#will lose color of image
def openImage(name):
    img = Image.open(name)
    img = getGreyScale(img)
    img = img.convert('RGB')
    return img

#takes in a image and instructions (list alter) on how to alter it and performs instructions
#have some issues that I have not fully discover, but it feels werid to use and need more tuning
def alterImage(img,alter,prevValue):
    imgSize=img.size
    rotateAngle=alter[0]
    blurCoefficient=alter[1]
    randomAlterV2=alter[2]
    
    widthMutiplier=alter[3]
    heightMutiplier=alter[4]
    #set value to prevValue so that image names do not overlap when calling function mutiple times
    imgNum=prevValue

    for i in range(-rotateAngle*2,rotateAngle*2,1): #mutiply by 2 to give the effect of for i in range(-rotateAngle,rotateAngle,0.5)
        img2=rotateImage(img,i/2)
        #print("running")
        for k in range(0,randomAlterV2+1):
            if k==0:
                img3=copy.deepcopy(img2)
            else:
                img3=randomlyAlterV2(img2)
        
            #print("running2")
            for j in range(0,blurCoefficient+1):
                #print("running2")
                if j==0:
                    img4=copy.deepcopy(img3)
                else:
                    img4=guassianBlur(img3,j)
                for l in range(1,widthMutiplier+1):
                    img5=reSize(img4,(imgSize[0]*l,imgSize[1]))
                    #print('running4')
                    for m in range(1,heightMutiplier+1):
                        #print('running5')
                        img5Size=img5.size
                        img6=reSize(img5,(img5Size[0],img5Size[1]*m))
                        #img6.show()
                        imgName="training"+str(imgNum)+".png"
                        imgNum+=1
                        img6.save(imgName)
        
    return imgNum
                        

#takes in a image, detects individual characters in image, removes individual characters and outputs them as their own image
#output is all black and white
#indivual characters must intersection line y=img.height//2 to work
def spaceFinder(img):
    #ensures image is right size (might not be nessary but afriad changing will break something)
    #img=img.resize((28*3,28))
    imgSize=img.size
    factor=img.size[1]/100
    img=reSize(img,(int(imgSize[0]/factor),int(imgSize[1]/factor)))
    imgArray=np.array(img)


    midIndex=len(imgArray)//2


    imgList=[]
    #loops through all x values in y==img.height//2
    for col in range(len(imgArray[midIndex])):
        print(col)
        print((imgArray[midIndex][col]))
        
        #checks if it is a dark pixels
        if sum(imgArray[midIndex][col])<255*3*.7:
            searched=set()
            #removes all dark pixels in the same character as current dark pixel and stores pixels locations in set
            spaceFinderFloodFill(imgArray,midIndex,col,searched)
            #img3=Image.fromarray(imgArray.astype(np.uint8))
            #print(img3.getpixel((14,midIndex)),"this is pixel")
            #img3.putpixel( (14,midIndex), (255,0,0))
            #img3.show()

            #creates a new image from pixel locations
            if len(searched)>1:
                    character=createFromSet(searched)
                    imgList.append(character)
    return imgList


#learned about this in 112 floodfilling notes(forgot what year it is) and Dr. Taylor (did directly not copy code, but used floodfilling, which I learned in this class)
#removes all dark pixels in the same character as current dark pixel and stores pixels locations in set
def spaceFinderFloodFill(imgArray,row,col,searched):
    rows,cols=len(imgArray),len(imgArray[0])
    
    #checks if you are searching a new spot inside the image
    #checks if the pixel you are at is a dark pixel
    if 0<=row<rows and 0<=col<cols and sum(imgArray[row][col])<255*3*.7 and (row,col) not in searched:
        #changes dark pixel to light pixel and saves it's location in image
        imgArray[row][col]=[255,255,255]
        print(row,col,imgArray[row][col])
        searched.add((row,col))
        #Image.fromarray(imgArray.astype(np.uint8)).show()
        spaceFinderFloodFill(imgArray,row+1,col,searched)
        spaceFinderFloodFill(imgArray,row-1,col,searched)
        spaceFinderFloodFill(imgArray,row,col+1,searched)
        spaceFinderFloodFill(imgArray,row,col-1,searched)

        
#https://stackoverflow.com/questions/43121880/systemerror-tile-cannot-extend-outside-image-in-pil-during-save-image helped me diagnose a bug
#creates image from a set of locations that will be the dark pixels of the locations
def createFromSet(searched):
    minX=None
    maxX=None
    minY=None
    maxY=None
    
    for y,x in searched:
        if minX==None or x<minX:
            minX=x
        if maxX==None or x>maxX:
            maxX=x
        if minY==None or y<minY:
            minY=y
        if maxY==None or y>maxY:
            maxY=y
    #gets base dimentions of image
    imgSize=(int((maxY-minY)),int((maxX-minX)))
    if imgSize[0]==0 or imgSize[1]==0:
        return None
    print(imgSize)
    imgList=[]

    #creates a empty light that will be new image
    for row in range(imgSize[0]):
        imgListRow=[]
        for col in range(imgSize[1]):
            imgListRow.append(0)
        imgList.append(imgListRow)

    
    
    #fills in the image list with pixels
    for row in range(0,imgSize[0]):
        #imgListRow=[]
        for col in range(0,imgSize[1]):
            shifted=(row+minY,col+minX)
            if shifted in searched:
                imgList[row][col]=(0,0,0)
            else:
                imgList[row][col]=(255,255,255)
        #imgList.append(imgListRow)
    padding=(imgSize[0]//4,imgSize[1]//4)
    #adds padding on top and bottem
    for i in range(0,padding[0]):
        rowList=[(255,255,255)]*imgSize[1]
        imgList.insert(0,rowList)
        imgList.append([(255,255,255)]*imgSize[1])

    #adding padding on sides
    rowPadding=[(255,255,255)]*padding[1]
    for rowList in imgList:
        rowList.extend(rowPadding)
        for i in range(len(rowPadding)):
            rowList.insert(0,(255,255,255))

    return Image.fromarray(np.array(imgList).astype(np.uint8)) #https://stackoverflow.com/questions/55319949/pil-typeerror-cannot-handle-this-data-type 


            
        

    


#source to increase recursion limit
#https://stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-in-python-and-how-to-increase-it
sys.setrecursionlimit(6000*2)



        


    











