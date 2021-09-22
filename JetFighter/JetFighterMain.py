import pygame
import os
pygame.mixer.init()
pygame.font.init()

pygame.display.set_caption("CyberPunk 3077")
WIDTH, HEIGHT = 900, 500
PLAYER, SIZE = 34, 34
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
'''We have now created the window and it's size
Now lets create the background display'''

FPS = 60
HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
VELOCITY = 3 
WHITE = ((255, 255, 255))
BLUE = ((0, 0, 255))
YELLOW = ((255, 255, 0))
YELLOW_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2
MID_BORDER = pygame.Rect((WIDTH/2)-2.5, 0,5, HEIGHT) #this will place a solid line in the middle of the screen


Player_1 = pygame.transform.scale(pygame.image.load(os.path.join('skins', 'player.png')), (PLAYER,SIZE))
P1 = pygame.transform.rotate(Player_1, 270)
Player_2 = pygame.transform.scale(pygame.image.load(os.path.join('skins', 'enemy.png')), (PLAYER,SIZE))
P2 = pygame.transform.rotate(Player_2, 270)
SKY = pygame.transform.scale(pygame.image.load(os.path.join('skins', 'bg.png')), (WIDTH,HEIGHT))
#this will search our folder 'skins' for the file 'bg' to make our background
BULLET_SPEED = 5
BULLET_NUMBER = 5

BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('soundEffects', 'tiro.wav'))
BULLET_DAMAGE_SOUND = pygame.mixer.Sound(os.path.join('soundEffects', 'batida.wav'))


def draw(yellow, blue, yellow_bullets, blue_bullets, yellow_health, blue_health):
    WIN.blit(SKY, (0,0)) 
    pygame.draw.rect(WIN, WHITE, MID_BORDER)
    WIN.blit(P1, (yellow.x, yellow.y))
    WIN.blit(P2, (blue.x, blue.y))
    #pygame starts tracking at the top left with 0,0
    for bullet in blue_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    yellow_health_txt = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    blue_health_txt = HEALTH_FONT.render("Health: " + str(blue_health), 1, WHITE)
    WIN.blit(yellow_health_txt,(10,10))
    WIN.blit(blue_health_txt,(WIDTH - blue_health_txt.get_width() - 10, 10))


    pygame.display.update()

def winner_draw(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() /2 ))
    pygame.display.update()
    pygame.time.delay(5000)




def P1_moves(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0: #LEFT MOVEMENT
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width < MID_BORDER.x: #RIGHT MOVEMENT
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0: #UP MOVEMENT
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT: #DOWN MOVEMENT
        yellow.y += VELOCITY

def P2_moves(keys_pressed, blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - VELOCITY > MID_BORDER.x + MID_BORDER.width: #LEFT MOVEMENT
        blue.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and blue.x + VELOCITY + blue.width < WIDTH: #RIGHT MOVEMENT
        blue.x += VELOCITY
    if keys_pressed[pygame.K_UP] and blue.y - VELOCITY > 0: #UP MOVEMENT
        blue.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and blue.y + VELOCITY + blue.width < HEIGHT: #DOWN MOVEMENT
        blue.y+= VELOCITY 


def bullet_handle(yellow_bullets, blue_bullets, yellow, blue):
    for bullet in yellow_bullets:
        bullet.x += BULLET_SPEED
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
             yellow_bullets.remove(bullet)
    
    for bullet in blue_bullets:
        bullet.x -= BULLET_SPEED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)
    

    


def main():
    yellow = pygame.Rect(200, 250, 32, 32)
    blue = pygame.Rect(650, 250, 32, 32)


    yellow_health = 100
    blue_health = 100


    yellow_bullets = []
    blue_bullets = []

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < BULLET_NUMBER:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2, 8, 5)
                    yellow_bullets.append(bullet)
        #This is how the left jet will fire 
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(blue_bullets) < BULLET_NUMBER:
                    bullet = pygame.Rect(blue.x , blue.y + blue.height//2 -2, 8, 5)
                    blue_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
        
            if event.type == YELLOW_HIT:
                yellow_health -= 10
                BULLET_DAMAGE_SOUND.play()
        
            if event.type == BLUE_HIT:
                blue_health -= 10
                BULLET_DAMAGE_SOUND.play()


        winner_message = ""
        if yellow_health <= 0:
            winner_message = ("Players 2 wins!")
        if blue_health <= 0:
            winner_message = ("Player 1 wins!")
        if winner_message != "":
            winner_draw(winner_message)
            break


        keys_pressed = pygame.key.get_pressed()
        P1_moves(keys_pressed, yellow)
        P2_moves(keys_pressed, blue)
        bullet_handle(yellow_bullets, blue_bullets, yellow, blue)
        draw(yellow, blue, yellow_bullets, blue_bullets, yellow_health, blue_health)
    

if __name__ == "__main__":
    main()
