import pygame
#This is the BouncyBall minigame file

def main(images):
    pygame.init()
    pygame.font.init()
    score = 0
    fps = 120
    gravity = 240/fps
    #change the image paths
    image = pygame.image.load(images + "BouncyBallBackground.png")

    scoreText = pygame.font.SysFont("Times", 75)
    scoreScreen = scoreText.render(str(score), False, (0, 0, 0))
    screen = pygame.display.set_mode([500, 500])
    pygame.display.set_caption("BouncyBall")
    clock = pygame.time.Clock()
    allSprites = pygame.sprite.Group()
    missiles = pygame.sprite.Group()
    Balls = pygame.sprite.Group()
    Portals = pygame.sprite.Group()

    #Deals with bouncing pysics of ball
    def applyPhysics(object):

        if object.location[1] >= 450:
            object.velocity *= -1
            object.location[1] = 449

        object.velocity += object.acceleration
        object.location[1] += object.velocity



    class Ball(pygame.sprite.Sprite):
        width = 50
        height = 50
        def __init__(self,location,velocity,acceleration):
            super().__init__(allSprites,Balls)
            self.location = location
            self.velocity = velocity
            self.acceleration = acceleration
            self.image = pygame.image.load("/Users/stefan/Desktop/GIMP/Box.png")
            self.rect = self.image.get_rect()
            self.rect.midbottom = location


        def update(self):
            self.rect.midbottom = self.location

    class Missile(pygame.sprite.Sprite):
        width = 24
        height = 12

        def __init__(self,position,velocity,location):
            super().__init__(allSprites,missiles)
            self.position = position
            self.velocity = velocity
            self.image = pygame.image.load("/Users/stefan/Desktop/GIMP/Bullet.png")
            self.rect = self.image.get_rect()
            self.rect.midright = location
            self.location = location


        def update(self):
            self.location[0] += self.velocity
            self.rect.midright = self.location
            if self.location[0]>550:
                self.kill()

    class Portal(pygame.sprite.Sprite):
        width = 12
        height = 48
        def __init__(self,position,location):
            super().__init__(allSprites,Portals)
            self.position = position
            self.location = location
            self.image = pygame.Surface([self.width,self.height])
            self.image.fill([0,0,255])
            self.rect = self.image.get_rect()
            self.rect.center = location
            self.location = location

    portals = []
    ball1 = Ball([250,100],0,gravity)

    #Removes portals or fires missles based on key pressed
    def keyPressed(event):

        if event.key == pygame.K_f:
            Missile(0,25,[25,100])
        if event.key == pygame.K_d:
            Missile(1,25,[25,250])
        if event.key == pygame.K_s:
            Missile(2,25,[25,400])

        if len(portals) == 0:
            if event.key == pygame.K_j:
                portals.append(Portal(0,[475,100]))
            if event.key == pygame.K_k:
                portals.append(Portal(1,[475,250]))
            if event.key == pygame.K_l:
                portals.append(Portal(2,[475,400]))

    #Gets rid of the portals created
    def keyUp(event):
        if event.key == pygame.K_j:
            for portal in portals:
                if portal.position == 0:
                    portal.kill()
                portals.remove(portal)
        elif event.key == pygame.K_k:
            for portal in portals:
                if portal.position == 1:
                    portal.kill()
                    portals.remove(portal)
        elif event.key == pygame.K_l:
            for portal in portals:
                if portal.position == 2:
                    portal.kill()
                    portals.remove(portal)

    playing = True
    while playing:

        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN:
                keyPressed(event)
            if event.type == pygame.KEYUP:
                keyUp(event)

        #Checks for collisions
        if len (pygame.sprite.groupcollide(Balls,missiles,False,True)) != 0:
            return False

        if len(pygame.sprite.groupcollide(missiles,portals,True,False)) != 0:
            score += 1

        screen.blit(image, (0, 0))
        applyPhysics(ball1)
        allSprites.update()
        allSprites.draw(screen)

        scoreScreen = scoreText.render("Score "+ str(score), False, (255, 255, 255))
        screen.blit(scoreScreen, (100, 50))

        #If you win
        if score >= 5:
            return True
        pygame.display.flip()

if __name__ == "__main__":
    main()