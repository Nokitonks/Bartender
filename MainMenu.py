#This is the main menu
import pygame

def main(images):
    pygame.init()
    screen = pygame.display.set_mode([500, 500])
    pygame.display.set_caption("Main Menu")

    #Change this path
    image = pygame.image.load(images + "/HelpBackground.png")
    clock = pygame.time.Clock()
    Buttons = pygame.sprite.Group()
    class Button(pygame.sprite.Sprite):
        width = 100
        height = 50
        def __init__(self,location,imagePath):
            super().__init__(Buttons)
            self.location = location
            self.image = pygame.image.load(imagePath)
            self.rect = self.image.get_rect()
            self.rect.center = location

    playing = True
    StartButton = Button([250,250],"/Users/stefan/Desktop/GIMP/StartButton.png")
    HelpButton = Button([250,150],"/Users/stefan/Desktop/GIMP/HelpButton.png")
    while playing:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if abs(StartButton.location[0]-pos[0]) < StartButton.width/2\
                    and abs(StartButton.location[1]-pos[1]) < StartButton.height/2:
                    return "Start"
                if abs(HelpButton.location[0]-pos[0]) < HelpButton.width/2\
                    and abs(HelpButton.location[1]-pos[1]) < HelpButton.height/2:
                    return "Help"


        screen.blit(image,(0,0))
        Buttons.draw(screen)
        pygame.display.flip()
