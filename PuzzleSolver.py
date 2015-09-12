from os import listdir
from os.path import isfile, join
from PIL import Image
__author__ = 'maakbar'


def getSplittedFiles(mypath): #exlude grayscaled, inversed
    imageFiles = [Image.open(join(mypath,f)) for f in listdir(mypath) if isfile(join(mypath,f))]
    return imageFiles


def getBorder(mypath, filename):
    return Image.open(join(mypath,filename))


def putImageRegion(background, images, region, splittedSize, dimen=(3,3), shifter=(0, 0)):
    if region >= len(images):
        return background
    image = images[region]
    tempPixels = image.load()

    for x in range(image.size[0]):    # for every pixel:
        for y in range(image.size[1]):
            pixels = background.load()
            xpos = x+shifter[0]+((region%dimen[0])*splittedSize[0])
            ypos = y+shifter[1]+((region/dimen[0])*splittedSize[1])
            pixels[xpos,ypos] = tempPixels[x,y]
    background = putImageRegion(background, images, region+1, splittedSize, dimen, shifter)
    return background


# images format in [image, stat]
def solvePuzzle(background, images, level, splittedSize, dimen=(3,3), shifter=(0, 0)):
    for region in xrange(len(images)):
        if region/dimen[0] == level or region/dimen[0] == dimen[1]-(level+1) \
                or region%dimen[0]==level or region%dimen[0]==dimen[0]-(level+1):
            minimum = [region,9999999.9] # default [image, index, score]
            isFound = False
            i = 0
            for image in images:
                xpos = shifter[0]+((region%dimen[0])*splittedSize[0])
                ypos = shifter[1]+((region/dimen[0])*splittedSize[1])
                print 'posisi', region, i
                val = differenceSide(background, image, region/dimen[0] == level, region%dimen[0]==level,
                                     region%dimen[0]==dimen[0]-(level+1), region/dimen[0] == dimen[1]-(level+1),
                                     (xpos, ypos))
                if val < minimum[1]:
                    print minimum[1], val
                    minimum[0] = i
                    minimum[1] = val
                    isFound = True
                i += 1
            if isFound:
                temp = images[region]
                print region, minimum[0]
                images[region] = images[minimum[0]]
                images[minimum[0]] = temp
                # images[region][1] = True
    return images


def differenceSide(background, image, isTop, isLeft, isRight, isBottom, shifter=(0, 0)): #
    value = 0
    print isTop, isLeft, isRight, isBottom
    if isLeft:
        area = 0
        temp = 0
        for i in range(image.size[1]):  #check_left:
            temp += calculateDiff(background, image, 0, i, shifter)
            area += 1
        value += temp/area
    if isRight:
        area = 0
        temp = 0
        for i in range(image.size[1]):  #check_right:
            value += calculateDiff(background, image, image.size[0]-1, i, shifter)
            area += 1
        value += temp/area
    if  isTop:
        area = 0
        temp = 0
        for i in range(image.size[0]):  #check_top:
            value += calculateDiff(background, image, i, 0, shifter)
            area += 1
        value += temp/area
    if isBottom:
        area = 0
        temp = 0
        for i in range(image.size[0]):  #check_bottom:
            value += calculateDiff(background, image, i, image.size[1]-1, shifter)
            area += 1
        value += temp/area
    return value


def calculateDiff(background, image, x, y, shifter):
    background_r, background_g, background_b = background.getpixel((x+shifter[0], y+shifter[1]))
    background_tot = (background_r + background_g + background_b) / 3
    image_r, image_g, image_b = image.getpixel((x, y))
    image_tot = (image_r + image_g + image_b) / 3
    return abs(background_tot - image_tot)