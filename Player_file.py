import pygame
from Spriteloader import loadSprite_x
from tilemap import Tilemap, tutorial_tilemap_data
from Enemy_file import enemy_group


class Player:
    def __init__(self, window):
        self.width = 20
        self.height = 30
        self.scale_factor = 2
        self.current_frame = 0
        self.frame_counter = 0
        self.facing_left = False
        self.is_jump = False
        self.jump_vel = 20
        self.grav = 1
        self.game_over = False

        self.map = Tilemap(tutorial_tilemap_data, window)

        
        self.spritesheet = pygame.image.load('Sprites/NEA + converted terraria sprites/Terraria_playable_char.png').convert_alpha()
        self.idle = pygame.image.load('Sprites/NEA + converted terraria sprites/Terraria_idle.png')
        self.idle = pygame.transform.scale(self.idle, (self.width * self.scale_factor, self.height * self.scale_factor))

        self.player_walking_left = [
            loadSprite_x(self.spritesheet, self.width, self.height, i, self.scale_factor, False)
            for i in range(7, 18)
            ]
        
        self.player_walking_right = [
            pygame.transform.flip(i, True, False)
            for i in self.player_walking_left
            ]

        self.image = self.idle
        self.rect = self.image.get_rect()
        self.rect.x = window.get_width() - self.image.get_width() // 2
        self.rect.y = window.get_height() - self.image.get_height() -50
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.ground_level = self.rect.y


        self.movement = [0, 0] 
        #Initialises x and y movement to be 0 in both directions        
        self.speed = 3
        #Movement multiplier

        self.animation_speed = 3
        #The speed for the animation to change
        self.frame_counter = 0
        self.is_on_ground = True
        self.jump_count = 2


    def input_handling(self, event):
        if self.game_over == False:
            if event.type == pygame.KEYDOWN: 
            #Horizontal movement begins if the key is pressed down
                if event.key == pygame.K_RIGHT:
                    self.movement[0] = self.speed
                    #Adding self.speed to the movement
                    self.facing_left = False

                elif event.key == pygame.K_LEFT:
                    self.movement[0] = -self.speed
                    #Subtracting self.speed from the movement
                    self.facing_left = True
            
                if event.key == pygame.K_SPACE:
                    self.jump()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    self.movement[0] = 0  

                #Horizontal movement ends if the key is lifted

    def update(self):
        if self.game_over == False:
            self.rect.x += self.movement[0] 
            #Updates player x position by the value in self.movement[0]
            self.horizontal_collisions()

            if not self.is_on_ground:
                self.movement[1] += self.grav
            
            self.rect.y += self.movement[1]
            self.vertical_collisions()

            if self.is_on_ground and self.jump_count != 2:
                self.jump_count = 2

            self.is_on_ground = False
            for _, tile_rect in self.map.tile_list:
                if(
                    self.rect.bottom == tile_rect.top and
                    self.rect.right > tile_rect.left and
                    self.rect.left < tile_rect.right
                ):
                   if abs(self.rect.bottom - tile_rect.top) < 5:
                        self.is_on_ground = True
                        self.is_jump = False
                        self.jump_count = 2
                        break

            if self.movement[0] != 0:
                self.frame_counter += 1
                if self.frame_counter >= self.animation_speed:
                    self.frame_counter = 0
                    self.current_frame = (self.current_frame + 1) % len(self.player_walking_left)
                if self.facing_left:
                    self.image = self.player_walking_left[self.current_frame]
                else:
                    self.image = self.player_walking_right[self.current_frame]
            else:
                if self.facing_left == True:
                    self.image = self.idle
                else:
                    self.image = pygame.transform.flip(self.idle, True, False)

    
    def jump(self):
        if self.jump_count > 0:
            self.movement[1] = -self.jump_vel
            self.jump_count -= 1
            self.is_jump = True

    def horizontal_collisions(self):
        if self.rect.left + self.movement[0] < 0:
            self.rect.left = 0
            self.movement[0] = 0

        elif self.rect.right + self.movement[0] > self.map.tilemap_width:
            self.rect.right = self.map.tilemap_width
            self.movement[0] = 0
        
        
        for _, tile_rect in self.map.tile_list:
            if self.rect.colliderect(tile_rect):
                if self.movement[0] > 0:
                    self.rect.right = tile_rect.left
                if self.movement[0] < 0:
                    self.rect.left = tile_rect.right 
    
        if pygame.sprite.spritecollide(self, enemy_group, False):
            self.game_over = True
            print(self.game_over)                 

    def vertical_collisions(self):
        self.is_on_ground = False
        for _, tile_rect in self.map.tile_list:
            if self.rect.colliderect(tile_rect):
                if self.movement[1] > 0: 
                    self.rect.bottom = tile_rect.top
                    self.is_on_ground = True
                    self.movement[1] = 0
                    self.is_jump = False
                elif self.movement[1] < 0:
                    self.rect.top = tile_rect.bottom
                    self.movement[1] = 0

        if self.rect.y >= self.ground_level:
            self.rect.y = self.ground_level
            self.is_on_ground = True
            self.movement[1] = 0


    def draw(self, window, camera_x, camera_y):
        self.draw_rect = self.rect.move(-camera_x, -camera_y)
        window.blit(self.image, self.draw_rect.topleft)
        #Draws the image at the newly determined position