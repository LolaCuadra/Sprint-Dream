import pygame

pygame.init()

SCREEN_WIDHT = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))

player = pygame.Rect((300, 250, 50, 50))

run = True
while run: 

    pygame.draw.rect(screen, (255, 0, 0), player)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.display.update()

pygame.quit()





