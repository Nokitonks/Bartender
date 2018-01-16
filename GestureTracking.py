import cv2
import numpy as np
import colorsys
refPnt = [0,0]

def getMousePressed(event, x, y, flags, param):
    global refPnt
    if event == cv2.EVENT_LBUTTONUP:
        refPnt = [(y, x)]
        print(refPnt)
    pass

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

def main():
    cv2.namedWindow("Blurred")
    cv2.setMouseCallback("Blurred", getMousePressed)

    global refPnt
    cap = cv2.VideoCapture(0)

    deltaR = 20
    deltaG = 108
    deltaB = 118

    while(1):

        # Take each frame
        _, frame = cap.read()

        blurredFrame = cv2.GaussianBlur(frame, (3,3), 0)
        cv2.imshow("Blurred",blurredFrame)
        maskColor = np.array([112,66,26])
        print(maskColor)
        HSVimg = cv2.cvtColor(blurredFrame, cv2.COLOR_RGB2HSV)

        if refPnt != [0,0]:
            maskColor = HSVimg[refPnt[0]]


        colorDelta = np.array([deltaR, deltaG, deltaB])

        lowerThreshhold = np.subtract(maskColor, colorDelta)
        upperThreshhold = np.add(maskColor, colorDelta)

        lowerThreshhold = clamp(lowerThreshhold)
        upperThreshhold = clamp(upperThreshhold)


        mask = cv2.inRange(HSVimg, lowerThreshhold, upperThreshhold)

        cv2.imshow("BlurrMask", mask)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        if k == ord("q"):
            deltaR += 2
        if k == ord("w"):
            deltaG += 2
        if k == ord("e"):
            deltaB += 2
        if k == ord("a"):
            deltaR -= 2
        if k == ord("s"):
            deltaG -= 2
        if k == ord("d"):
            deltaB -= 2
        if k == ord("r"):
            deltaR += 2
            deltaG += 2
            deltaB += 2
        if k == ord("f"):
            deltaR -= 2
            deltaG -= 2
            deltaB -= 2




    cv2.destroyAllWindows()

if __name__ == "__main__": main()
