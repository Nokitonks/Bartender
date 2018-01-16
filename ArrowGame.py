import pygame
import random
#This is the file that runs the Arrow Minigame

def main(images):

    score = 0
    pygame.init()
    pygame.font.init()
    scoreText = pygame.font.SysFont("Times",75)
    scoreScreen = scoreText.render("Score: "+ str(score), False,(0,0,0))
    screen = pygame.display.set_mode([500,500])
    image = pygame.image.load(images + "ArrowGameBackground.png")
    screen.blit(image,(0,0))
    pygame.display.set_caption("ARROWS")
    clock = pygame.time.Clock()

    allSprites = pygame.sprite.Group()

    arrowQueueLocations = {3:[75,250],2:[125,250],1:[175,250],0:[225,250]}
    arrowQueue = []

    class Arrow(pygame.sprite.Sprite):

        def __init__(self, direction, position, group, location):
            super().__init__(group)
            self.direction = direction
            self.position = position
            if direction == "Down":
                self.image = pygame.image.load(images + "ArrowDown.png")
            elif direction == "Right":
                self.image = pygame.image.load(images + "ArrowRight.png")
            elif direction == "Up":
                self.image = pygame.image.load(images + "ArrowUp.png")
            self.rect = self.image.get_rect()
            self.rect.center = location

        def update(self, QueueLocations):
            self.rect.center = QueueLocations[self.position]
    def keyPressed(event,score):
        for arrow in arrowQueue:
            if arrow.position == 0:
                arrowToDestroy = arrow

        if event.key == pygame.K_UP:
            if arrowToDestroy.direction == "Up":
                arrowToDestroy.kill()
                arrowQueue.remove(arrowToDestroy)
                for arrow in arrowQueue:
                    arrow.position -= 1
                allSprites.update(arrowQueueLocations)
                return score+1

        if event.key == pygame.K_RIGHT:
            if arrowToDestroy.direction == "Right":
                arrowToDestroy.kill()
                arrowQueue.remove(arrowToDestroy)
                for arrow in arrowQueue:
                    arrow.position -= 1
                allSprites.update(arrowQueueLocations)
                return score + 1
        if event.key == pygame.K_DOWN:

            if arrowToDestroy.direction == "Down":
                arrowToDestroy.kill()
                arrowQueue.remove(arrowToDestroy)
                for arrow in arrowQueue:
                    arrow.position -= 1
                allSprites.update(arrowQueueLocations)
                return score + 1
        return -1

    def addArrows():
        x = len(arrowQueueLocations) - len(arrowQueue)

        for i in range(3,3-x,-1):
            direction = random.sample(["Up","Down","Right"],1)
            arrow = Arrow(direction[0],i, allSprites,arrowQueueLocations[i])
            arrowQueue.insert(0,arrow)
            allSprites.update(arrowQueueLocations)

    playing = True

    while playing:
        clock.tick(60)
        addArrows()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN:
                newScore = 0
                newScore += keyPressed(event,score)
                if newScore == -1:
                    return False
                score = newScore

        screen.blit(image, (0, 0))
        allSprites.draw(screen)

        scoreScreen = scoreText.render("Score: "+ str(score), False,(0,0,0))
        screen.blit(scoreScreen,(100,50))
        pygame.display.flip()

        if score >= 5:
            playing = False
    return True

if __name__ == "__main__":
    main()
