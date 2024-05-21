import pygame

pygame.init()

#dimmention fenetre
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

#fenetre
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("son de l'espace")

background_music = "sound.mp3"

pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
pygame.quit()