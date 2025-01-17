import pygame
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

main_sound = pygame.mixer.Sound('assets/sound.mp3')
#ecran et titre
WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Star Wars")

#couleurs 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

METEOR_IMAGE = pygame.image.load(os.path.join('Assets', 'meteor.png'))

LIFEBAR_WIDTH = 200 
LIFEBAR_HEIGHT = 20
BACKGROUND_WIDTH = LIFEBAR_WIDTH 
BACKGROUND_HEIGHT = LIFEBAR_HEIGHT
BORDER_RADIUS = 5

LIFEBAR_COLOR = (0, 255, 0)  # Green = HP
BACKGROUND_COLOR = (255, 0, 0)  # Red


#separation en deux de l'ecran
BORDER = pygame.Rect(WIDTH//2 , 0, 1, HEIGHT)

#bullets and hits 'sounds
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/hitted.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/laser.mp3')


WINNER_FONT = pygame.font.SysFont('Arial', 50)

FPS = 120
VEL = 8
BULLET_VEL = 10
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 95, 70

# yellow_hit , red_hit comme évènement:
WHITE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#Loading spaceships 'images
WHITE_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'Vaisseau_right.png'))
WHITE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    WHITE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'Vaisseau-left.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

#background image
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

# Chargez l'image pour le laser
LASER_IMAGE_rouge = pygame.image.load(os.path.join('Assets', '64.png'))
LASER_IMAGE_blanc = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', '55.png')),180)



# dessine
def draw_window(red, white, red_bullets, white_bullets, red_health, white_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, (0,20,0), BORDER) #dessine la ligne qui sépare

    
#dessine les spaceships:
    WIN.blit(WHITE_SPACESHIP, (white.x, white.y)) 
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # Dessinez l'image pour les lasers rouges
    for bullet in white_bullets:

        laser_x = bullet.x - LASER_IMAGE_rouge.get_width() // 2
        laser_y = bullet.y - LASER_IMAGE_rouge.get_height() // 2
        WIN.blit(LASER_IMAGE_rouge, (laser_x, laser_y))

    # Dessinez l'image pour les lasers blancs
    for bullet in red_bullets:
        
        laser_x = bullet.x - LASER_IMAGE_blanc.get_width() // 2
        laser_y = bullet.y - LASER_IMAGE_blanc.get_height() // 2
        WIN.blit(LASER_IMAGE_blanc, (laser_x, laser_y))
        

    
def draw_lifebars( red_health ,white_health):
    
    pygame.draw.rect(WIN, BACKGROUND_COLOR, (20 , 20, BACKGROUND_WIDTH, BACKGROUND_HEIGHT), border_radius=BORDER_RADIUS)
    lifebar_length_player1 =(white_health / 100) * LIFEBAR_WIDTH
    #print("barre de vie avant ", LIFEBAR_COLOR, " et ",lifebar_length_player1)
    pygame.draw.rect(WIN, LIFEBAR_COLOR, (20, 20, lifebar_length_player1, LIFEBAR_HEIGHT), border_radius=BORDER_RADIUS)
    #print("barre de vie apres ", LIFEBAR_COLOR, " et ",lifebar_length_player1)
    pygame.draw.rect(WIN, BACKGROUND_COLOR, (WIDTH - LIFEBAR_WIDTH, 20 , BACKGROUND_WIDTH, BACKGROUND_HEIGHT), border_radius=BORDER_RADIUS)
    lifebar_length_player2 = (red_health / 100) * LIFEBAR_WIDTH
    pygame.draw.rect(WIN, LIFEBAR_COLOR, (WIDTH - LIFEBAR_WIDTH , 20, lifebar_length_player2, LIFEBAR_HEIGHT), border_radius=BORDER_RADIUS)
    

# assignation touche pour diriger white_spaceship
def white_handle_movement(keys_pressed, white):
    if keys_pressed[pygame.K_q] and white.x - VEL > 0:  # LEFT
        white.x -= VEL
    if keys_pressed[pygame.K_d] and white.x + 2*VEL + white.width < BORDER.x :  # RIGHT
        white.x += VEL
    if keys_pressed[pygame.K_z] and white.y - VEL > 0:  # UP
        white.y -= VEL
    if keys_pressed[pygame.K_s] and white.y + VEL + white.height < HEIGHT - 15:  # DOWN
        white.y += VEL

# assignation touche pour diriger red_spaceship
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > 1.05*(BORDER.x + BORDER.width):  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL

#fonction pour les lasers
def handle_bullets(white_bullets, red_bullets, white, red):
    for bullet in white_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT)) #déclenche l'évènement red_hit
            white_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            white_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if white.colliderect(bullet):
            pygame.event.post(pygame.event.Event(WHITE_HIT))#déclenche l'évènement white_hit
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


# écrire texte winner 
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000)





def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    white = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    white_bullets = []

    red_health = 100
    white_health = 100

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(white_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        white.x + white.width, white.y + white.height//2 - 2, 10, 5)
                    white_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 10
                BULLET_HIT_SOUND.play()

            if event.type == WHITE_HIT:
                white_health -= 10
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health < 0:
            winner_text = "Red Wins!"

        if white_health < 0:
            winner_text = "White Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
        main_sound.play()       

        keys_pressed = pygame.key.get_pressed()
        white_handle_movement(keys_pressed, white)
        red_handle_movement(keys_pressed, red)

        handle_bullets(white_bullets, red_bullets, white, red)

        draw_window(red, white, red_bullets, white_bullets,
                    red_health, white_health)
        draw_lifebars(red_health, white_health)  
        
        pygame.display.flip()

    main()

    


if __name__ == "__main__":
    main()