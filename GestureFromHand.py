import cv2
import numpy as np
import argparse
refPnt = [0,0]
import math
def getMousePressed(event, x, y, flags, param):
    global refPnt
    if event == cv2.EVENT_LBUTTONUP:
        refPnt = [(y, x)]
        print(refPnt)



def clamp(array):

    result = [0,0,0]
    for i in range(3):
        if i == 0:
            if array[i] > 179:
                result[i] = 179
            elif array[i] < 0:
                result[i] = 0
            else:
                result[i] = array[i]
        else:
            if array[i] > 255:
                result[i] = 255
            elif array[i] < 0:
                result[i] = 0
            else:
                result[i] = array[i]

    return np.array(result)


def distance(points):

    x = abs(points[0][0][0]-points[1][0][0])
    y = abs(points[0][0][1]-points[1][0][1])

    d = (x**2 + y**2)**.5

    return d

def reducePoints(hull):

    result = []
    totalDist = 0

    for i in range(len(hull)-1):
        totalDist += distance([hull[i],hull[i+1]])

    avgDist = totalDist/len(hull)/2

    for i in range(len(hull)-1):
        if distance([hull[i],hull[i+1]]) > avgDist:
            result += [hull[i]]



    return np.array(result)

def color(image):
    blur = cv2.GaussianBlur(image, (3,3), 0)
    deltaR = 15
    deltaG = 135
    deltaB = 120
    maskColor = np.array([112, 200, 100])
    HSV = cv2.cvtColor(blur, cv2.COLOR_RGB2HSV)
    colorDelta = np.array([deltaR, deltaG, deltaB])

    lowerThreshhold = np.subtract(maskColor, colorDelta)
    upperThreshhold = np.add(maskColor, colorDelta)

    lowerThreshhold = clamp(lowerThreshhold)
    upperThreshhold = clamp(upperThreshhold)


    mask = cv2.inRange(HSV, lowerThreshhold, upperThreshhold)
    res = cv2.bitwise_and(blur, blur, mask=mask)
    maskGray = cv2.cvtColor(res, cv2.COLOR_RGB2GRAY)

    return maskGray

def main():
    img = cv2.imread("/Users/stefan/Desktop/TermProjectStuff/GesturePictures/Hand.PNG", -1)
    cv2.namedWindow("Blurred")
    cv2.setMouseCallback("Blurred", getMousePressed)
    deltaR = 5
    deltaG = 151
    deltaB = 89
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    previousRefPnt = [0,0]
    maskColor = np.array([3, 185, 75])
    while True:
        global refPnt

        _, img = cap.read()
        blurredFrame = cv2.GaussianBlur(img, (19, 19),0)
        #blurredFrame = cv2.bilateralFilter(img, 9,100,100)
        cv2.imshow("Blurred",blurredFrame)


        HSVimg = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        if previousRefPnt != refPnt:
            maskColor = HSVimg[refPnt[0]]
            previousRefPnt = refPnt
            print(maskColor)
        cv2.imshow("HSV", HSVimg)
        colorDelta = np.array([deltaR, deltaG, deltaB])
        print(colorDelta)
        print(maskColor)
        lowerThreshhold = np.subtract(maskColor, colorDelta)
        upperThreshhold = np.add(maskColor, colorDelta)

        lowerThreshhold = clamp(lowerThreshhold)
        upperThreshhold = clamp(upperThreshhold)


        mask = cv2.inRange(HSVimg, lowerThreshhold, upperThreshhold)
        #mask = cv2.bitwise_not(mask)
        res = cv2.bitwise_and(blurredFrame, blurredFrame, mask = mask)

        maskGray = cv2.cvtColor(res, cv2.COLOR_RGB2GRAY)


        newFrame, contours, hierarchy = cv2.findContours(maskGray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        maxArea = 0
        besti = 0
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if (area > maxArea):
                maxArea = area
                besti = i
        if len(contours) != 0:
            cnt = contours[besti]

            img2 = cv2.drawContours(newFrame, [cnt], -1, (0, 255, 0), 3)
            hull = cv2.convexHull(cnt)



            #May contain lots of extra points
            hull2 = cv2.convexHull(cnt)

            #Gets rid of extra points
            hull = reducePoints(hull2)




            #         defects = cv2.convexityDefects(cnt, hull)
            cv2.drawContours(img2, [cnt], -1, (188, 255, 0), 3)
            cv2.drawContours(img2, hull, -1, (188, 255, 0), 3)


            cv2.imshow("img", img2)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        if k == ord("k"):
            print("# FINGERS ---->")
            print(len(hull)-2)
        elif k == ord("q"):
            deltaR += 2
        elif k == ord("w"):
            deltaG += 2
        elif k == ord("e"):
            deltaB += 2
        elif k == ord("a"):
            deltaR -= 2
        elif k == ord("s"):
            deltaG -= 2
        elif k == ord("d"):
            deltaB -= 2
        elif k == ord("r"):
            deltaR += 2
            deltaG += 2
            deltaB += 2
        if k == ord("f"):
            deltaR -= 2
            deltaG -= 2
            deltaB -= 2



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Get a Gesture File")
    parser.add_argument("-i", "--image", help="PNG image to process", required=False)
    args = parser.parse_args()
    main()