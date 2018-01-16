import pygame
import random
#This is the rainbow minigame file
def main(images):
    pygame.init()
    pygame.font.init()
    score = 0
    fps = 60
    speed = 5
    #Change this path
    image = pygame.image.load(images + "/RainbowBackground.png")
    scoreText = pygame.font.SysFont("Times", 75)
    scoreScreen = scoreText.render(str(score), False, (0, 0, 0))
    screen = pygame.display.set_mode([500, 500])
    pygame.display.set_caption("Rainbow")
    clock = pygame.time.Clock()
    Stars = pygame.sprite.Group()
    Points = pygame.sprite.Group()
    Blocks = pygame.sprite.Group()

    class Star(pygame.sprite.Sprite):


        def __init__(self,location,direction):
            super().__init__(Stars)
            self.location = location
            self.direction = direction
            self.image = pygame.image.load(images + "Star.png")
            self.rect = self.image.get_rect()
            self.rect.center = location

        #Moves the star depending on its direction
        def update(self):
            workingLocation = [0,0]
            workingLocation[0] = self.rect.center[0] + self.direction[0]
            workingLocation[1] = self.rect.center[1] + self.direction[1]
            self.rect.center = workingLocation
            self.location = workingLocation




    class Point(pygame.sprite.Sprite):
        width = 5
        height = 5
        def __init__(self,location):
            super().__init__(Points)
            self.location = location
            self.image = pygame.Surface([self.width, self.height])
            self.image.fill([0, 255, 255])
            self.rect = self.image.get_rect()
            self.rect.center = location

    def drawRainbow(screen,loc1,loc2):

        pygame.draw.line(screen,[0,255,0],loc1,loc2,1)

    #Draws lines inbetween points and stars
    def drawLines(points,Stars,screen):
        for point in points:
            for Star in Stars:
                if point.location[0] == Star.rect.center[0]:
                    drawRainbow(screen,point.location,Star.rect.center)
                if point.location[1] == Star.rect.center[1]:
                    drawRainbow(screen, point.location, Star.rect.center)
            for point2 in points:
                if point.location == point2.location:
                    continue
                if point.location[0] == point2.location[0]:
                    drawRainbow(screen, point.location, point2.location)
                if point.location[1] == point2.location[1]:
                    drawRainbow(screen, point.location, point2.location)

    class Block(pygame.sprite.Sprite):

        def __init__(self,location,size=[50,50]):
            super().__init__(Blocks)
            self.width = size[0]
            self.height = size[1]
            self.location = location
            self.image = pygame.Surface([self.width, self.height])
            self.image.fill([153, 102, 51])
            self.rect = self.image.get_rect()
            self.rect.center = location

    def keyDown(event):

        #This is the complicated split
        if event.key == pygame.K_SPACE:
            counter = 0
            locations = []
            dir = [0,0]

            #Completely emptys the Stars and then recreates it with appropriate stars
            for star in Stars:
                Point(star.location)
                counter += 1
                locations.append(star.location)
                dir = star.direction

            if len(Stars) < 5 or dir[1] == 0:
                Stars.empty()

                if dir[1] == 0:
                    for i in range(counter):
                        Star(locations[i],[0,speed])
                else:
                    for i in range(counter):
                        Star(locations[i],[speed,0])
                        Star(locations[i],[-1*speed,0])

    #Randomly puts in the  blocks
    def addRandoRocks():

        for i in range(15):
            location = [0,0]
            location[0] = random.randint(10,490)
            location[1] = random.randint(10,490)
            width = random.randint(10,25)
            size = [width,width]

            Block(location,size)



    playing = True

    StartingStar = Star([250,0],[0,speed])
    StartingPoint = Point([250,0])
    StartingBlock = Block([250,250])
    splits = 0
    addRandoRocks()
    while playing:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN:

                if splits <=7:
                    keyDown(event)
                if event.key == pygame.K_SPACE:
                    splits += 1

        screen.fill([150, 150, 167])


        Stars.update()

        #Determines how many starts fell and starts the game again
        for star in Stars:
            if star.location[1] > 500:
                score += 1
                star.kill()

        if len(Stars) == 0:
            Points.empty()
            StartingStar = Star([250, 0], [0, speed])
            StartingPoint = Point([250, 0])
            Blocks.empty()
            addRandoRocks()
            splits = 0
        screen.blit(image, (0, 0))
        drawLines(Points, Stars, screen)
        Points.draw(screen)
        Blocks.draw(screen)
        Stars.draw(screen)
        pygame.sprite.groupcollide(Stars,Blocks,True,False)

        #returns false if at any time there are 0 stars
        if len(Stars) == 0:
            return False
        scoreScreen = scoreText.render(str(score), False, (0, 0, 0))
        screen.blit(scoreScreen, (250, 50))
        pygame.display.flip()
        if score >=10:
            return True

if __name__ == "__main__":
    main()