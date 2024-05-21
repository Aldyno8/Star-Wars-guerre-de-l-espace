import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 1, HEIGHT) 

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 8
BULLET_VEL = 6
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 100, 85

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'Vaisseau_right.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)
vaisseau_jaune_rect = YELLOW_SPACESHIP.get_rect()
vaisseau_jaune_rect.x = 00
vaisseau_jaune_rect.y = 250

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'Vaisseau-left.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)
vaiseau_rouge_rect = YELLOW_SPACESHIP.get_rect()
vaiseau_rouge_rect.x = 800
vaiseau_rouge_rect.y = 250

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))



def draw_window( red_bullets, yellow_bullets, red_health, yellow_health, laser, laser_rect):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render( "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # Dessine les navettes 
    WIN.blit(YELLOW_SPACESHIP, (vaisseau_jaune_rect.x, vaisseau_jaune_rect.y))
    WIN.blit(RED_SPACESHIP, (vaiseau_rouge_rect.x, vaiseau_rouge_rect.y))

    for bullet in red_bullets:
        WIN.blit(laser, (laser_rect.x , laser_rect.y))

    for bullet in yellow_bullets:
         WIN.blit(laser, (laser_rect.x ,laser_rect.y-20))

    pygame.display.update()


# Deplacement de la navette jaune 
def yellow_handle_movement(keys_pressed, vaisseau_jaune_rect):
    if keys_pressed[pygame.K_q] and vaisseau_jaune_rect.x - VEL > 0:  # LEFT
        vaisseau_jaune_rect.x -= VEL
        print("Deplacement vers le gauche")
    if keys_pressed[pygame.K_d] and vaisseau_jaune_rect.x + VEL + vaisseau_jaune_rect.width < BORDER.x:  # RIGHT
        vaisseau_jaune_rect.x += VEL
        print("Deplacement vers la droite")
    if keys_pressed[pygame.K_z] and vaisseau_jaune_rect.y - VEL > 0:  # UP
        vaisseau_jaune_rect.y -= VEL
        print("Deplacement vers le haut")
    if keys_pressed[pygame.K_s] and vaisseau_jaune_rect.y + VEL + vaisseau_jaune_rect.height < HEIGHT - 15:  # DOWN
        vaisseau_jaune_rect.y += VEL
        print("Deplacement vers le bas")

#Deplacement de la navette rouge

def red_handle_movement(keys_pressed, vaiseau_rouge_rect):
        if keys_pressed[pygame.K_LEFT] and vaiseau_rouge_rect.x - VEL > BORDER.x + BORDER.width:  # LEFT
            vaiseau_rouge_rect.x -= VEL
            print("Deplacement vers la gauche")
        if keys_pressed[pygame.K_RIGHT] and vaiseau_rouge_rect.x + VEL + vaiseau_rouge_rect.width < WIDTH:  # RIGHT
            vaiseau_rouge_rect.x += VEL
            print("Deplacement vers la droite")
        if keys_pressed[pygame.K_UP] and vaiseau_rouge_rect.y - VEL > 0:  # UP
            vaiseau_rouge_rect.y -= VEL
            print("Deplacement vers le haut")
        if keys_pressed[pygame.K_DOWN] and vaiseau_rouge_rect.y + VEL + vaiseau_rouge_rect.height < HEIGHT - 15:  # DOWN
            vaiseau_rouge_rect.y += VEL
            print("Deplacement vers le bas")

# Deplacement des lasers
def handle_bullets(yellow_bullets, red_bullets, yellow, red, laser_rect):   
    for laser in yellow_bullets:
        laser_rect.x += BULLET_VEL 
        print(f"la position du laser est de  {laser_rect.x}")
        if red.colliderect(laser_rect):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(laser) 
        elif laser_rect.x > WIDTH:
            yellow_bullets.remove(laser)

    for laser in red_bullets:
        laser_rect.x -= BULLET_VEL
        print(f"la position du laser est de  {laser_rect.x}")
        if yellow.colliderect(laser_rect):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(laser)
        elif laser_rect.x < 0:
            red_bullets.remove(laser)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        laser = pygame.image.load(os.path.join('Assets', '55.png'))
        laser_rect = laser.get_rect()
        laser_rect.x = vaisseau_jaune_rect.x + 100
        laser_rect.y= vaisseau_jaune_rect.x
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLETS:
                    print(f"`({vaisseau_jaune_rect.x}, {vaisseau_jaune_rect.y})")
                    yellow_bullets.append(laser)
                    BULLET_FIRE_SOUND.play()
                    print("PLAY")
                    

                if event.key == pygame.K_KP_0 and len(red_bullets) < MAX_BULLETS:
                    red_bullets.append(laser)
                    print(len(red_bullets))
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play() 

        winner_text = ""
        if red_health <= 0:
            winner_text = "Red Wins!"

        if yellow_health <= 0:
            winner_text = "White Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, vaisseau_jaune_rect)
        red_handle_movement(keys_pressed, vaiseau_rouge_rect)

        handle_bullets(yellow_bullets, red_bullets, yellow, red, laser_rect)

        draw_window( red_bullets, yellow_bullets, red_health, yellow_health, laser, laser_rect)

    main()


if __name__ == "__main__":
    main()
