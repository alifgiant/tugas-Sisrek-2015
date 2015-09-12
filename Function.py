import os.path
import string
import random
from PuzzleSolver import *
from tkFileDialog import askopenfilename
from PIL import Image

dimens = (3,3)

class Function:
    def __init__(self):
        self.counter = 1
        self.imageAddress = None
        self.imageFile = None
        self.grayscaled = None
        self.inversed = None
        self.images = None
        self.exclude = []
        self.app = None
        self.splitSize = (0,0)
        self.shifter = (0,0)

    def addGUI(self, GUI):
        self.app = GUI

    def showOriginal(self):
        if (self.imageFile!=None):
            self.app.putPhotoOnCanvas(self.imageFile,1)

    def setImageFile(self, image):
        self.imageFile = image

    def cleanMemory(self):
        self.grayscaled = None
        self.inversed = None
        print "cleaning"

    def browseFile(self):
        self.app.parent.withdraw()
        global imageAddress
        imageAddress = askopenfilename()
        self.app.parent.deiconify()
        if (imageAddress!=" " and imageAddress!="" and imageAddress!=None ):
            print("loaded: "+imageAddress)
            self.app.addressViewer.insert(0,imageAddress)
            originalImage = Image.open(imageAddress)
            imageFile = self.app.resizeImage(originalImage)	#resized
            imageFile = self.turn2RGB(imageFile)
            self.setImageFile(imageFile)
            self.saveWorkingImage(imageFile) #save new file
            self.app.putPhotoOnCanvas(imageFile,1) #put image on canvas
            self.cleanMemory()

    @staticmethod
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def saveWorkingImage(self,photo,name="original", splitted=False): #change thisa later to .bmp

        filename = "working"+str(self.counter)+"/_"+name+".bmp"
        while (os.path.isfile(filename) and name=="original"):
            self.counter += 1
            filename = "working"+str(self.counter)+"/_"+name+".bmp"

        path = "working"+str(self.counter)+""
        if not os.path.exists(path):
            os.makedirs(path)
            path += "/splitted"
            os.makedirs(path)

        if splitted:
            filename = "working"+str(self.counter)+"/splitted/_"+name+".bmp"

        photo = self.turn2RGB(photo)
        photo.save(filename)
        print "saved: "+ filename

    def turn2RGB(self, photo):
        if len(photo.split()) == 4:
            # prevent IOError: cannot write mode RGBA as BMP
            r, g, b, a = photo.split()
            photo = Image.merge("RGB", (r, g, b))
        return photo

    def turn2Grayscale(self):
        if (self.grayscaled==None):
            if self.app.mode == 1:
                r,g,b = self.imageFile.split()
            elif self.app.mode == 2:
                r,g,b = self.grayscaled.split()
            elif self.app.mode == 3:
                r,g,b = self.inversed.split()

            tempImg = Image.new('RGB', self.imageFile.size)
            tempPixels = tempImg.load()

            for i in range(self.imageFile.size[0]):    # for every pixel:
                for j in range(self.imageFile.size[1]):
                    #(r,g,b) = originalPixel[i,j]
                    value = (r.getpixel((i,j))+g.getpixel((i,j))+b.getpixel((i,j)))/3
                    tempPixels[i,j] = (value, value, value)
            self.grayscaled = tempImg
            self.saveWorkingImage(self.grayscaled,"grayscaled")
        if(self.grayscaled!=None):
            self.app.putPhotoOnCanvas(self.grayscaled,2)

    def turn2Invers(self):
        if (self.inversed==None):
            if self.app.mode == 1:
                r,g,b = self.imageFile.split()
            elif self.app.mode == 2:
                r,g,b = self.grayscaled.split()
            elif self.app.mode == 3:
                r,g,b = self.inversed.split()

            tempImg = Image.new('RGB', self.imageFile.size)

            tempPixels = tempImg.load()

            for i in range(self.imageFile.size[0]):    # for every pixel:
                for j in range(self.imageFile.size[1]):
                    tempPixels[i,j] = (255-r.getpixel((i,j)), 255-g.getpixel((i,j)), 255-r.getpixel((i,j)))
            self.inversed = tempImg
            self.saveWorkingImage(self.inversed,"inversed")
        if(self.inversed!=None):
            self.app.putPhotoOnCanvas(self.inversed,3)

    def splitImage(self,w=dimens[0],h=dimens[1]):
        working = self.app.photoViewer.background
        if(working!=None):
            #set thickness
            thicknessX = self.imageFile.size[0]/20 #ketebalan 10% dari lebar
            thicknessY = self.imageFile.size[1]/20 #ketebalan 10% dari tinggi
            self.shifter = (thicknessX, thicknessY)

            borderImage = Image.new('RGB', self.imageFile.size, "white")

            centerSize = (self.imageFile.size[0]-(2*thicknessX),self.imageFile.size[1]-(2*thicknessY)) #w,h center image (pixel)

            splittedSize = (int(self.returnValue(centerSize[0],w)),int(self.returnValue(centerSize[1],h))) #rounded
            self.splitSize = splittedSize
            lastSplittedSize = (int(self.getLeftValue(centerSize[0],splittedSize[0],w)) , int(self.getLeftValue(centerSize[1],splittedSize[1],h)))

            splittedImage = []

            for x in xrange(0,w):
                splittedImage.append([])
                for y in xrange(0,h):
                    if (x==w-1) and (y==h-1):
                        splittedImage[x].append(Image.new('RGB', lastSplittedSize, "black"))
                    elif (x==w-1):
                        splittedImage[x].append(Image.new('RGB', (lastSplittedSize[0],splittedSize[1]), "black"))
                    elif (y==h-1):
                        splittedImage[x].append(Image.new('RGB', (splittedSize[0],lastSplittedSize[1],), "black"))
                    else:
                        splittedImage[x].append(Image.new('RGB', splittedSize, "black"))

            print len(splittedImage),' ',len(splittedImage[0])

            for x in range(self.imageFile.size[0]):    # for every pixel:
                for y in range(self.imageFile.size[1]):
                    if self.app.mode == 1:
                        originalPixel = self.imageFile.load()
                    elif self.app.mode == 2:
                        originalPixel = self.grayscaled.load()
                    elif self.app.mode == 3:
                        originalPixel = self.inversed.load()
                    if ((x < thicknessX) or (y < thicknessY) or (x>=(self.imageFile.size[0]-thicknessX)) or (y>=(self.imageFile.size[1]-thicknessY))): #add more pixel to build
                        tempPixels = borderImage.load()
                        tempPixels[x,y] = originalPixel[x,y]
                    else:
                        # if ((x < thicknessX+1) or (y < thicknessY+1) or (x>=(self.imageFile.size[0]-thicknessX)+1) or (y>=(self.imageFile.size[1]-thicknessY+1))):
                        #      tempPixels = borderImage.load()
                        #      tempPixels[x,y] = originalPixel[x,y]
                        tempX = x - thicknessX
                        tempY = y - thicknessY
                        # print tempX/splittedSize[0], ' ', tempY/splittedSize[1]
                        if (tempX/splittedSize[0]<w-1) and (tempY/splittedSize[1]<h-1):
                            tempPixels = splittedImage[tempX/splittedSize[0]][tempY/splittedSize[1]].load()
                            # print  'ini kordinat split ',x%splittedSize[0],y%splittedSize[1],'\n'
                            tempPixels[tempX%splittedSize[0],tempY%splittedSize[1]] = originalPixel[x,y]
                            # print tempX/splittedSize[0], ' ', tempY/splittedSize[1]
                        elif (tempX/splittedSize[0]<w-1):
                            tempPixels = splittedImage[tempX/splittedSize[0]][h-1].load()
                            #splittedSize[0]+x%w is to get last pixel index then add left over
                            tempPixels[tempX%splittedSize[0],tempY%lastSplittedSize[1]] = originalPixel[x,y]
                        elif (tempY/splittedSize[1]<h-1):
                            tempPixels = splittedImage[w-1][tempY/splittedSize[1]].load()
                            #splittedSize[0]+x%w is to get last pixel index then add left over
                            tempPixels[tempX%lastSplittedSize[0],tempY%splittedSize[1]] = originalPixel[x,y]
                        else:
                            #print 'ini last ', w-1, ' ', h-1, '\n'
                            tempPixels = splittedImage[w-1][h-1].load() #index is start from 0 so x-1 to get last index
                            #splittedSize[0]+x%w is to get last pixel index then add left over
                            tempPixels[tempX%lastSplittedSize[0],tempY%lastSplittedSize[1]] = originalPixel[x,y]

            self.saveWorkingImage(borderImage,'borderImage')
            for x in xrange(0,w):
                for y in xrange(0,h):
                    self.saveWorkingImage(splittedImage[x][y],str(self.id_generator()+'_'+str(x)+'_'+str(y)), True)

    def reload(self):
        self.images = getSplittedFiles("working"+str(self.counter)+"/splitted/")

        borderImage = getBorder("working"+str(self.counter)+"/", "_borderImage.bmp")
        borderImage = putImageRegion(borderImage, self.images, 0, self.splitSize, dimens, self.shifter)

        self.app.putPhotoOnCanvas(borderImage, 3)

    def solve(self):
        borderImage = getBorder("working"+str(self.counter)+"/", "_borderImage.bmp")
        # puzzleBox = [[x,False] for x in self.images] #create puzzle box based on image region

        puzzleBox = solvePuzzle(borderImage,self.images, 0, self.splitSize, dimens, self.shifter)

        # after being solved
        # puzzleBox = [x for [x,stat] in puzzleBox]
        # self.images = puzzleBox
        borderImage = putImageRegion(borderImage, puzzleBox, 0, self.splitSize, dimens, self.shifter)
        self.app.putPhotoOnCanvas(borderImage, 3)

    @staticmethod
    def returnValue(numerator, denominator):
        return round(numerator/float(denominator))

    @staticmethod
    def getLeftValue(original, splitted, multiplier):
        return round(splitted - (original - splitted*multiplier))

    def isRGBbased(self):
        typeName = self.imageAddress[-3:]
        if(typeName=="png"):
            return False
        else:
            return True
