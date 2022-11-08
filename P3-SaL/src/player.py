import pygame

# Player class
class Player():
    def __init__(self):
        self.image = pygame.image.load('../assets/pac_player_copy.png')
        self.image2 = pygame.image.load('../assets/pac_player_copy.png')
        self.image_in_air = pygame.image.load('../assets/pac_player_copy.png')
        self.image_climb = pygame.image.load('../assets/pac_player_copy.png')
        self.image_climb2 = pygame.image.load('../assets/pac_player_copy.png')
        self.rect = self.image.get_rect()

    
        self.move_speed = 3
        self.y_speed_max = 2
        self.y_speed = 0
        self.jump_power = 5
        
        self.grounded = True
        self.climbing = False

        self.alive = True
        self.lives = 3
        self.has_won = False
        self.kill = False

        self.facing_left = False

        self.animations = {}
        self.animations['walk'] = (self.image, self.image2)
        self.animations['jump'] = (self.image_in_air, self.image_in_air)
        self.animations['climb'] = (self.image_climb, self.image_climb2)

        self.current_animation = self.animations['walk']

        self.animation_timer_max = 10
        self.animation_timer = self.animation_timer_max
        self.animation_frame = 0
        

    def  set_animation(self, animation_name):
        self.current_animation = self.animations[animation_name]

    def bop(self):
        if not self.climbing:
            self.y_speed = -self.jump_power  / 2

    def win(self):
        self.has_won = True
        

    def update(self, screen, keys, platforms, ladders, snakes):
        if not self.alive:
            self.rect.move_ip(0, self.move_speed)
        elif self.has_won:
            #victory pose
            self.image_to_draw = self.image_in_air
        else:
                
            if self.climbing:
                if keys[pygame.K_UP]:
                    self.rect.move_ip(0, -self.move_speed)
                    self.animation_timer -= 1
                if keys[pygame.K_DOWN]:
                    self.rect.move_ip(0, self.move_speed)
                    self.animation_timer -= 1
            else:
                if keys[pygame.K_RIGHT] and self.rect.x < screen.get_width() - self.rect.width:
                    self.rect.move_ip(self.move_speed, 0)
                    self.animation_timer -= 1
                    self.facing_left = False
                    
                if keys[pygame.K_LEFT] and self.rect.x > 0:
                    self.rect.move_ip(-self.move_speed, 0)
                    self.animation_timer -= 1
                    self.facing_left = True
                    
                if keys[pygame.K_SPACE] and self.grounded:
                    self.y_speed = -self.jump_power
                    self.grounded = False

            if not self.grounded and not self.climbing: #falling
                self.set_animation('jump')
                if self.y_speed < self.y_speed_max:
                    self.y_speed += 0.25
            elif not self.climbing: #walking
                self.set_animation('walk')
                self.y_speed = 0
                
            
            hit = self.rect.collidelist(platforms)
            if hit > -1  and not self.climbing:
                if self.rect.bottom < platforms[hit].rect.centery:
                    self.grounded = True
            else:
                self.grounded = False

            for ladder in ladders:
                if self.rect.colliderect(ladder.climb_rect):
                    if (keys[pygame.K_UP] and self.rect.bottom > ladder.climb_rect.bottom) or (keys[pygame.K_DOWN] and self.rect.top < ladder.climb_rect.top):    
                        self.climbing = True
                        self.y_speed = 0
                        self.rect.centerx = ladder.rect.centerx
                        self.set_animation('climb')
                    elif (keys[pygame.K_UP] and self.rect.centery < ladder.climb_rect.top) or (keys[pygame.K_DOWN] and self.rect.bottom > ladder.climb_rect.bottom):
                        self.climbing = False


                
                
            for snake in snakes:
                if self.rect.colliderect(snake.rect):
                    # kill player
                    if self.rect.bottom > snake.rect.centery: #kill player
                        self.alive = False
                        self.lives -= 1
                    else: #killing snakes
                        snake.bop()
                        self.bop()

            self.rect.move_ip(0, self.y_speed)
                
            if self.animation_timer <= 0:
                self.animation_timer = self.animation_timer_max
                self.animation_frame += 1
                if self.animation_frame >= len(self.current_animation):
                    self.animation_frame = 0

            self.image_to_draw = self.current_animation[self.animation_frame]
            if self.facing_left:
                self.image_to_draw = pygame.transform.flip(self.image_to_draw, True, False)
                                
        screen.blit(self.image_to_draw, self.rect)

    def reset(self, x, y):
        self.rect.bottomleft = (x, y)
        self.alive =  True
        self.grounded = True
        self.climbing = False
        self.has_won = False

