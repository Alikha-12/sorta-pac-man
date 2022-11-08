import pygame
import random
from player import Player
from level import *

pygame.init()
game_width = 650
game_height = 750
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True

player = Player()
platforms = []
ladders = []
snakes = []

snake_spawn_timer_max = 100
snake_spawn_timer = snake_spawn_timer_max
max_snakes = 8
chance_to_spawn = 40

current_level = 1
font = pygame.font.SysFont("Default", 40)
next_level_text = font.render("Press Enter for Next Level", True, (0, 0, 0))
restart_text = font.render("Press Enter to Restart", True, (0, 0, 0))
gameover_text = font.render("Game Over", True, (0, 0, 0))

def spawn_snakes():
    global snakes
    for i in range(1, 6):
        if random.randint(0, 100) <= chance_to_spawn:
            if len(snakes) < max_snakes:
                if i % 2 == 0: #even
                    snakes.append(Snake(0, platforms[i].rect.y + 1, 1))
                else: #odd
                    snakes.append(Snake(600, platforms[i].rect.y + 1, -1))
def start():
    global ladders
    ladders = []
    global snakes
    snakes = []
    
    platforms.append(Platform(0, 720, 13))
    for i in range(3):
        platforms.append(Platform(100, 620 -(200 * i), 11))
        platforms.append(Platform(0, 520 - (200 * i), 11))

    for i in range(6):
        l = Ladder(random.randint(100, 550), platforms[i].rect.y, 5)
        while l.rect.collidelist(ladders) > -1:
            l = Ladder(random.randint(100, 550), platforms[i].rect.y, 5)
        ladders.append(l)
    
    player.reset(0,720)

start()


# Main Loop
while running:

    if current_level > 1:
        max_snakes = 14
        snake_spawn_timer_max = max_snakes * 2
        
    max_snakes = 4 + current_level * 2
    snake_spawn_timer_max = (current_level * -2) + 100

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        # Reset the level, for testing
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            start()

    snake_spawn_timer -= 1
    if snake_spawn_timer <= 0:
        spawn_snakes()
        snake_spawn_timer = snake_spawn_timer_max
    
    for p in platforms:
        p.update(screen)
    for l in ladders:
        l.update(screen)
    for s in snakes:
        if s.rect.y > game_height:
            snakes.remove(s)
        else:
            s.update(screen, platforms)

    keys = pygame.key.get_pressed()
    player.update(screen, keys, platforms, ladders, snakes)

    lives_text = font.render("Lives: " + str(player.lives), True, (0, 0, 0))
    screen.blit(lives_text, (0,0))
    level_text = font.render("Levels: " + str(current_level), True, (0, 0, 0))
    screen.blit(level_text, (525,0))

    if player.grounded and player.rect.colliderect(platforms[len(platforms)-1]):
        player.win()

    if not player.alive:
        if player.lives > 0:
            screen.blit(restart_text, (0,50))
            if keys[pygame.K_RETURN]:
                start()
                             
        else:
            screen.blit(gameover_text, (0,50))

    if player.has_won:
        screen.blit(next_level_text, (0,50))
        if keys[pygame.K_RETURN]:
            current_level += 1
            player.lives += 1
                            
    pygame.display.flip()
    clock.tick(50)
    screen.fill((0, 0, 0))
