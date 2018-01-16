##Stefan Orton-Urbina, 15-112 Term Project Main File
#sortonur
#December 5th, 2017
#This is the main file that you run
#Imports
import pygame
import cv2
import random
import MainSprites
import ArrowGame
import Matches
import BouncyBall
import Rainbow

#THESE 3 SCREENS are just backgrounds with buttons not too complicated
import MainMenu
import Help
import Win

#Sets up the game
pygame.init()
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bartender")

##CHANGE THIS TO THE PATH TO THE IMAGES FOLDER
images = "/Users/stefan/Desktop/GIMP/"


clock = pygame.time.Clock()

#Sets up our font and score
pygame.font.init()
score = 0
scoreText = pygame.font.SysFont("Times",75)

#This is used for gesture recognision

##!!!!!!!!!PUT THE PATH TO THE GESTURE PICTURES HERE!!!!!!!!!!
matches = "/Users/stefan/Desktop/TermProjectStuff/GesturePictures"

#Configures the Camera and its window
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#These determine where on the screen each check should go
checkLocations = {0:[50,150],1:[150,150],2:[250,150],3:[350,150],4:[450,150],5:[550,150]}

#Checks are added to this list when they are generated
checkQueue = []

#Define our coasters and their locations/positions
coaster1 = MainSprites.Coaster([50,430],1)
coaster2 = MainSprites.Coaster([150,430],2)
coaster3 = MainSprites.Coaster([250,430],3)
coaster4 = MainSprites.Coaster([350,430],4)
coaster5 = MainSprites.Coaster([450,430],5)
coaster6 = MainSprites.Coaster([550,430],6)

#Define the highlight and its starting position/coaster
theHighlight = MainSprites.Highlight(1)
theHighlight.setLocation(coaster1)

#This is only true when the mouse is dragging a check
dragging = False


running = True

#This event is put into the queue every 10 seconds in order to spawn a check
addCheckEvent = pygame.USEREVENT
pygame.time.set_timer(addCheckEvent,10000)

#Starts the game by calling the main menu and the info screen if so needed
if MainMenu.main(images) != "Start":
    Help.main(images)

#Reloads the screen and the image in case it is messed up by pygame form another file
image = pygame.image.load(images + "MainBackground.png")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


########################################################
#Below here are functions until we get to the main loop#
########################################################


#This function returns a coaster that is associated with the hand position it detects
def getHandPosition():

    #Gets the frame of when the function is called
    _, frame = cap.read()
    frame = frame[0:240, 0:320]

    #Passes it into the function in the Matches file which returns a string
    gestureDetected = Matches.bestGestureMatch(frame, matches)


    #Based on the string returned, this function determines which coaster to return

    #In this case we return "SEND" because Closed Fist means to send the drink currently highlighted
    if gestureDetected == "ClosedFist":
        return "SEND"
    if gestureDetected == "1Finger":
        return coaster1
    if gestureDetected == "2Fingers":
        return coaster2
    if gestureDetected == "3Fingers":
        return coaster3
    if gestureDetected == "4Fingers":
        return coaster4
    if gestureDetected == "5Fingers":
        return coaster5
    if gestureDetected == "HangLoose":
        return coaster6

#This is called if a key is pressed and returns a increase of score
def keyPressed(event):


    #If space is pressed we call the getHandPosition() to determine our hand gesture
    if event.key == pygame.K_SPACE:
        coasterDetected = getHandPosition()

        #This is when hand position is closed first
        if coasterDetected == "SEND":

            #Determines if the coaster highlighted has a drink that is full
            for coaster in MainSprites.Coasters:
                if theHighlight.position == coaster.position \
                        and coaster.full == True:
                    if coaster.drink.filledAmount >= 100:

                        #If it is...
                        coaster.full = False
                        coaster.drink.kill()
                        coaster.filledBar.kill()
                        coaster.drink = None
                        return 5

        #Moves the highlight based on which coaster is returned from above
        elif coasterDetected == coaster1:
            theHighlight.position = 1
            theHighlight.setLocation(coasterDetected)
        elif coasterDetected == coaster2:
            theHighlight.position = 2
            theHighlight.setLocation(coasterDetected)
        elif coasterDetected == coaster3:
            theHighlight.position = 3
            theHighlight.setLocation(coasterDetected)
        elif coasterDetected == coaster4:
            theHighlight.position = 4
            theHighlight.setLocation(coasterDetected)
        elif coasterDetected == coaster5:
            theHighlight.position = 5
            theHighlight.setLocation(coasterDetected)
        elif coasterDetected == coaster6:
            theHighlight.position = 6
            theHighlight.setLocation(coasterDetected)


    #If up is pressed
    if event.key == pygame.K_UP:

        #Determines if highlighted coaster has a drink and plays the game
         for coaster in MainSprites.Coasters:
            if coaster.full == True and coaster.position == theHighlight.position:

                if coaster.drink.type == "Martini" :

                    #This calls the minigame associated with each drink and adds to the drink if
                    #you win the minigame
                    if ArrowGame.main(images):
                        coaster.drink.filledAmount += 50
                        coaster.filledBar.amount = (coaster.drink.filledAmount/\
                            coaster.drink.capacity * 50)

                if coaster.drink.type == "Cosmo" :
                    if BouncyBall.main(images):
                        coaster.drink.filledAmount += 50
                        coaster.filledBar.amount = (coaster.drink.filledAmount/\
                            coaster.drink.capacity * 50)

                if coaster.drink.type == "TequilaSunrise" :
                    if Rainbow.main(images):
                        coaster.drink.filledAmount += 50
                        coaster.filledBar.amount = (coaster.drink.filledAmount/\
                            coaster.drink.capacity * 50)


    ##THESE ARE ONLY TO BE USED IF OPENCV STUFF DOESNT WORK##
    if event.key == pygame.K_RIGHT:
        if theHighlight.position < 6:
            theHighlight.position += 1
            for coaster in MainSprites.Coasters:
                if theHighlight.position == coaster.position:
                    theHighlight.setLocation(coaster)

    if event.key == pygame.K_LEFT:
        if theHighlight.position > 1:
            theHighlight.position -= 1
            for coaster in MainSprites.Coasters:
                if theHighlight.position == coaster.position:
                    theHighlight.setLocation(coaster)

    if event.key == pygame.K_DOWN:
        for coaster in MainSprites.Coasters:
            if theHighlight.position == coaster.position\
                and coaster.full == True:
                if coaster.drink.filledAmount >= 100:
                    coaster.full = False
                    coaster.drink.kill()
                    coaster.filledBar.kill()
                    coaster.drink = None
                    return 5
    return 0
    ###########################################################


    #Calls all the draw functions on all groups
def drawAll():
    MainSprites.allSprites.draw(screen)
    MainSprites.Coasters.draw(screen)
    MainSprites.bars.draw(screen)
    MainSprites.Drinks.draw(screen)
    MainSprites.Checks.draw(screen)


#Helper function for determining which check the user just clicked on
#returns that check
def getCheckClickedOn(event):

    mousePos = pygame.mouse.get_pos()
    for check in MainSprites.Checks:
        if abs(mousePos[0] - check.rect.centerx) < check.rect.width/2\
                and abs(mousePos[1] - check.rect.centery) < check.rect.height/2:
            return check
    return None

#Function that is called every 10 seconds to add a check to the game
def addCheck():


    for i in range(len(checkLocations)):
        #Only the position is represented in check queue
        if i in checkQueue:
            continue

        #If the position inst in checkQueue then we had a check with a random type
        checkQueue.append(i)
        x = random.sample(["Cosmo","Martini","TequilaSunrise"],1)
        checkQueue.append(MainSprites.Check(checkLocations[i],checkLocations[i],i,x[0]))
        return False

    #If all positions are filled, we end the game
    return True

#This function simply puts a drink on a coaster depending on type of check
def putDrink(coaster, type):

    if type == "Martini":
        coaster.drink = MainSprites.Martini(coaster.rect.center,50)
        coaster.filledBar = MainSprites.filledBar(coaster.rect.center,\
                                            coaster.drink.filledAmount/coaster.drink.capacity*50)
    if type == "Cosmo":
        coaster.drink = MainSprites.Cosmo(coaster.rect.center,50)
        coaster.filledBar = MainSprites.filledBar(coaster.rect.center,\
                                               coaster.drink.filledAmount/coaster.drink.capacity*50)
    if type == "TequilaSunrise":
        coaster.drink = MainSprites.TequilaSunrise(coaster.rect.center,50)
        coaster.filledBar = MainSprites.filledBar(coaster.rect.center,\
                                               coaster.drink.filledAmount/coaster.drink.capacity*50)



#MAIN GAME LOOP
while running:

    # keep loop running at the right speed
    clock.tick(65)

    # Process input (events)
    for event in pygame.event.get():

        #Quits the game if necessary
        if event.type == addCheckEvent:

            #Quits game if we cant add any more checks
            if addCheck():
                running = False

        # check for closing window
        if event.type == pygame.QUIT:
            running = False

        #Calls the keypressed and updates the score
        if event.type == pygame.KEYDOWN:
            score += keyPressed(event)

            #Resets the screen and font b/c we called a diff pygame window and i dont want it to screw up
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.font.init()
            scoreText = pygame.font.SysFont("Times", 75)

        #Determines what check is clicked on when mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            checkOn = getCheckClickedOn(event)
            if checkOn != None:
                dragging = True

        #Determines if we've dragged a check to a coaster or not
        if event.type == pygame.MOUSEBUTTONUP:
            if checkOn != None:

                #Goes through to check every coaster
                for coaster in MainSprites.Coasters:
                    if abs(pygame.mouse.get_pos()[0] - coaster.rect.centerx)<10:
                        if abs(pygame.mouse.get_pos()[1] - coaster.rect.centery)<60:

                            #If check is being dropped on a coaster
                            if coaster.full == False:
                                if checkOn.type == "Martini":
                                    if ArrowGame.main(images):

                                        # Puts a drink on that coaster of the type of check
                                        putDrink(coaster, checkOn.type)

                                        # Gets rid of the check
                                        checkOn.kill()
                                        checkQueue.remove(checkOn.position)
                                        coaster.full = True

                                if checkOn.type == "TequilaSunrise":
                                    if Rainbow.main(images):

                                        # Puts a drink on that coaster of the type of check
                                        putDrink(coaster, checkOn.type)

                                        # Gets rid of the check
                                        checkOn.kill()
                                        checkQueue.remove(checkOn.position)
                                        coaster.full = True

                                if checkOn.type == "Cosmo":
                                    if BouncyBall.main(images):
                                        # Puts a drink on that coaster of the type of check
                                        putDrink(coaster, checkOn.type)

                                        # Gets rid of the check
                                        checkOn.kill()
                                        checkQueue.remove(checkOn.position)
                                        coaster.full = True

                                #Again idk why but this is necessary or it friks up
                                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                                pygame.font.init()
                                scoreText = pygame.font.SysFont("Times", 75)

                #If we didnt drop a check on a coaster, it snaps back
                checkOn.rect.center = checkOn.home
                checkOn = None
                dragging = False

    #If we're dragging then we update the check we clicked on
    if dragging == True:
        checkOn.rect.center = pygame.mouse.get_pos()

    #Re-render our text incase score changed
    scoreScreen = scoreText.render(str(score), False, (255, 255, 255))

    #Update
    MainSprites.bars.update()

    # Draws everything
    screen.blit(image,[0,0])
    drawAll()
    screen.blit(scoreScreen, (300, 25))
    pygame.display.flip()

    #Shows the camera
    _, frame = cap.read()
    frame = frame[0:240, 0:320]
    cv2.imshow("Camera",frame)

    #If we've won we stop running
    if score >=30:
        running = False

#And we call the win screen
Win.main(images)
pygame.quit()