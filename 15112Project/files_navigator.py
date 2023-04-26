import PIL
import numpy as np
from numpy import array
import random
import copy
from cmu_graphics import *
from PIL import Image, ImageFilter,ImageDraw,ImageEnhance,ImageOps
from Image_Functions import alterImage, openImage,convertToAIBasicLab
from Basic_AI_Lab import emnistAI
import os


#sources
#https://en.wikipedia.org/wiki/.DS_Store#:~:text=In%20the%20Apple%20macOS%20operating,Services%20Store%2C%20reflecting%20its%20purpose. 
#https://www.kosbie.net/cmu/spring-20/15-112/notes/notes-recursion-part2.html#fileNavigation
#copied most of code from 15112 notes but modified it to store file name into a set
def getFileSet(path): 
    fileName=set()
    if os.path.isfile(path):
        fileName.add(path)
    else:
        for filename in os.listdir(path):
            fileName=fileName|getFileSet(path + '/' + filename)
    return fileName


        
