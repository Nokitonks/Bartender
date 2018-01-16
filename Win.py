
import pygame
#This is the win screen
def main(images):
    pygame.init()
    screen = pygame.display.set_mode([500, 500])
    pygame.display.set_caption("YOU WIN")
    image = pygame.image.load(images + "WinScreen.png")
    clock = pygame.time.Clock()
    Buttons = pygame.sprite.Group()

    playing = True

    while playing:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False



        screen.blit(image,(0,0))
        Buttons.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
