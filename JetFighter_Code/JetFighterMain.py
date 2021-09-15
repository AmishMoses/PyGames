import pygame
import os 


pygame.display.set_caption("CyberPunk 3077")
WIDTH, HEIGHT = 900, 500
PLAYER, SIZE = 34, 34
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
'''We have now created the window and it's size
Now lets create the background display'''

FPS = 60
VELOCITY = 3 
WHITE = ((255, 255, 255))
MID_BORDER = pygame.Rect((WIDTH/2)-2.5, 0,5, HEIGHT) #this will place a solid line in the middle of the screen


Player_1 = pygame.transform.scale(pygame.image.load(os.path.join('skins', 'player.png')), (PLAYER,SIZE))
P1 = pygame.transform.rotate(Player_1, 270)
Player_2 = pygame.transform.scale(pygame.image.load(os.path.join('skins', 'enemy.png')), (PLAYER,SIZE))
P2 = pygame.transform.rotate(Player_2, 270)
SKY = pygame.transform.scale(pygame.image.load(os.path.join('skins', 'bg.png')), (WIDTH,HEIGHT))
#this will search our folder 'skins' for the file 'bg' to make our background

def draw(yellow, blue):
    WIN.blit(SKY, (0,0)) 
    pygame.draw.rect(WIN, WHITE, MID_BORDER)
    WIN.blit(P1, (yellow.x, yellow.y))
    WIN.blit(P2, (blue.x, blue.y))
    #pygame starts tracking at the top left with 0,0
    pygame.display.update()

def P1_moves(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0: #LEFT
        yellow.x -= VELOCITY
    


def main():
    yellow = pygame.Rect(200, 250, 32, 32)
    blue = pygame.Rect(650, 250, 32, 32)

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys_pressed = pygame.key.get_pressed()
        P1_moves(keys_pressed, yellow)
        draw(yellow, blue)
    pygame.quit()

if __name__ == "__main__":
    main()
