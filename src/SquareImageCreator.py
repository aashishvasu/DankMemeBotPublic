#Aashish Vasudevan
# A class which houses functions for image manipulation related things

from colorthief import ColorThief
import PIL
import os

class SquareImageCreator():
    
    #The main instance of this class
    sqImgC = 'ty'

     #Initialize this class
    def __init__(self):
        pass

    #Returns an image squared and coloured
    def GetSquaredImage(self, imagePath):
        #Open image
        from PIL import Image;

        img = ''
        if(os.path.exists(imagePath)):
            img = Image.open(imagePath)

        #Get pixels
        w, h = img.size

        #Set width and height to be the same for square images
        if(w<h):
            w = h
        else:
            h = w

        #Calculate color from color thief
        clr = ColorThief(imagePath);
        dominantColor = clr.get_color(quality=10)

        print(dominantColor)

    def CreateImageOfSizeAndColour(self, w, h, color):
        pass


sq = SquareImageCreator()
sq.GetSquaredImage('D:/Test/dmb/src/temp.png')
