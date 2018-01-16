import numpy as np
#This file contains the function that changes a frame to its threshholded image
from Matches import *
refPnt = [0,0]
#Makes sure that the HSV value cant go out of range
def clamp(array):

    result = [0,0,0]

    #For each, makes sure that we dont go over or under
    for i in range(3):
        if i == 0:
            #Max Hue is 179
            if array[i] > 179:
                result[i] = 179
            elif array[i] < 0:
                result[i] = 0
            else:
                result[i] = array[i]
        else:
            #Max value and saturation is 255
            if array[i] > 255:
                result[i] = 255
            elif array[i] < 0:
                result[i] = 0
            else:
                result[i] = array[i]


    return np.array(result)


#Simple distance formula function that takes a numpy array
def distance(points):

    x = abs(points[0][0][0]-points[1][0][0])
    y = abs(points[0][0][1]-points[1][0][1])

    d = (x**2 + y**2)**.5

    return d

#Reduces a array of points into less points in order to try and
#figure out how many fingers are help up
def reducePoints(hull):

    result = []
    totalDist = 0

    #Finds the total distance between all points
    for i in range(len(hull)-1):
        totalDist += distance([hull[i],hull[i+1]])

    #Finds the average and divides it by 2
    avgDist = totalDist/len(hull)/2

    #If two points are farther than avgDist we cut them from hull
    for i in range(len(hull)-1):
        if distance([hull[i],hull[i+1]]) > avgDist:
            result += [hull[i]]
    return np.array(result)


def colorImage(img):

    #Puts a blurr on our frame
    blurredFrame = cv2.GaussianBlur(img, (19, 19), 0)

    #This is the base color we are threshholding from
    maskColor = np.array([110, 131, 169])

    #converts the image to HSV
    HSVimg = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    #If we clicked on a point then we set the maskColor to the color we clicked on
    if refPnt != [0, 0]:
        maskColor = blurredFrame[refPnt[0]]

    #This is how much we allow in our threshhold (Change if need be)
    colorDelta = np.array([9, 81, 155])

    #Determine our bounds
    lowerThreshhold = np.subtract(maskColor, colorDelta)
    upperThreshhold = np.add(maskColor, colorDelta)

    #Make sure that they do not go out of bounds for HSV numbers
    lowerThreshhold = clamp(lowerThreshhold)
    upperThreshhold = clamp(upperThreshhold)

    #We create the mask image from the HSV image and the bounds
    mask = cv2.inRange(HSVimg, lowerThreshhold, upperThreshhold)

    #This uses the mask to create a black and white bitwise frame
    res = cv2.bitwise_and(blurredFrame, blurredFrame, mask=mask)

    #We convert it from RGB to GRAY
    maskGray = cv2.cvtColor(res, cv2.COLOR_RGB2GRAY)

    #We find the contours
    newFrame, contours, hierarchy = cv2.findContours(maskGray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    #This finds the biggest shape of white in the frame
    maxArea = 0
    besti = 0

    #Finds each set of contours and checks if it can beat the max area
    #Works because numpy separates contours that dont connect
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if (area > maxArea):
            maxArea = area
            besti = i

    #Makes sure if nothing is seen that we dont crash
    if len(contours) != 0:
        #makes cnt the contours of the best area
        cnt = contours[besti]

        #Draws them for testing purposes
        img2 = cv2.drawContours(newFrame, [cnt], -1, (0, 255, 0), 3)

        #This didn't pan out to be necessary or efficient in determining
        #How many fingers are held up
        # May contain lots of extra points
        hull2 = cv2.convexHull(cnt)

        # Gets rid of extra points
        hull = reducePoints(hull2)

        #Draws them on the image for testing purposes
        cv2.drawContours(img2, [cnt], -1, (188, 255, 0), 3)
        cv2.drawContours(img2, hull, -1, (188, 255, 0), 3)
        #returns the colored image and contours
        return img2,np.array(cnt)

    return maskGray,[]


#Ignore below, its for testing purposes
if __name__ == "__main__":

    img0 = cv2.imread("/Users/stefan/Desktop/TermProjectStuff/GesturePictures/ClosedFist/Hand0.PNG", -1)
    img1 = cv2.imread("/Users/stefan/Desktop/TermProjectStuff/GesturePictures/1Finger/Hand11.PNG", -1)
    img2 = cv2.imread("/Users/stefan/Desktop/TermProjectStuff/GesturePictures/2Fingers/Hand2.PNG", -1)
    img3 = cv2.imread("/Users/stefan/Desktop/TermProjectStuff/GesturePictures/3Fingers/Hand3.PNG", -1)
    img4 = cv2.imread("/Users/stefan/Desktop/TermProjectStuff/GesturePictures/4Fingers/Hand4.PNG", -1)
    img5 = cv2.imread("/Users/stefan/Desktop/TermProjectStuff/GesturePictures/5Fingers/Hand5.PNG", -1)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    images = [img0,img1,img2,img3,img4,img5]

    while True:

        _, imgBase = cap.read()
        frame = imgBase[0:240, 0:320]
        frame,cntBase = colorImage(frame)
        if len(cntBase) != 0:
            bestMatch = 1
            bestImage = frame
            for image in images:
                curImage, curCnt = colorImage(image)
                curMatch = cv2.matchShapes(cntBase,curCnt,1,0.0)
                if curMatch <= bestMatch:
                    bestMatch = curMatch
                    bestImage = curImage
            cv2.imshow("Best",bestImage)
        cv2.imshow("Base",frame)


        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break