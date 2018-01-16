import cv2
import os
import Threshholding
import numpy as np
#This file has functions that perform the opencv hand matches, you can run it alone for testing purposes

#CallBack function that changes the refPnt
def getMousePressed(event, x, y, flags, param):
    global refPnt
    if event == cv2.EVENT_LBUTTONUP:
        refPnt = [(y, x)]
        print(refPnt)

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


#Where frame is a np array and matches is a path to a folder of pictures
def bestGestureMatch(frame, matches):

    #Gets our baseline for comparison
    imgBase, cntBase = Threshholding.colorImage(frame)
    amountMatchesCnt = {}
    for folder in os.listdir(matches):
        if folder.startswith("."):
            continue
        #The amount that the images in this folder match the frame (averaged)
        avgMatch = 0
        for image in os.listdir(matches + "/" + folder):
            if image.startswith("."):
                continue

            #Gets the actual image from the path
            img = cv2.imread(matches + "/" + folder+ "/" + image )


            #Get the img contours and BW image
            curImage,curCnt = Threshholding.colorImage(img)



            #Gets the comparison number and adds it to avgMatch
            avgMatch +=  cv2.matchShapes(cntBase,curCnt,2,0.0)

       # Divides our average by the amount of stock images in the folder we're checking
        try:
            avgMatch /= len(os.listdir(matches + "/" + folder))
        except:avgMatch /= 1

        #Sets the dictionary entry
        amountMatchesCnt[folder] = avgMatch


    #Finds the lowest match and its associated gesture
    best = 10
    gesture = ""
    for posGesture in amountMatchesCnt:
        if amountMatchesCnt[posGesture] < best and amountMatchesCnt[posGesture] != 0:
            best = amountMatchesCnt[posGesture]
            gesture = posGesture



    return gesture


#This is for testing purposes to see what the camera says
if __name__ == "__main__":

    #MUST CHANGE THESE PATHS OR TESTING WONT WORK
    matches = "/Users/stefan/Desktop/TermProjectStuff/GesturePictures"
    testingFrame = cv2.imread("/Users/stefan/Desktop/TermProjectStuff/GesturePictures/4Fingers/help1.PNG")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    while True:
        _, frame = cap.read()
        frame = frame[0:240,0:320]
        gestureDetected = bestGestureMatch(frame,matches)
        cv2.imshow("Window",frame)

        coloredFrame,_ = Threshholding.colorImage(frame)
        cv2.imshow("Colored",coloredFrame)
        cv2.displayOverlay("Window",gestureDetected)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break