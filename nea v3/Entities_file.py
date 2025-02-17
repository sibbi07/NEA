import pygame
from queue import PriorityQueue
from Spriteloader import loadSprite_x, loadSprite_y
from game_objects import enemy_group

class Node:
    def __init__(self,x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.walkable = True
        self.f_score = float("inf")

    def get_pos(self):
        return self.x, self.y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __lt__(self, other):
        return self.f_score < other.f_score

def h_score(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2

    return abs(x1 - x2) + abs(y1- y2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, tilemap, player):
        super().__init__()
        self.spritesheet = pygame.image.load("Sprites/NEA + converted terraria sprites/Enemy converted/NPC_21.png")
        self.image = loadSprite_y(self.spritesheet, 40, 56, 1, 1, False)
        self.rect = self.image.get_rect(topleft = (x,y))
        self.tilemap = tilemap
        self.player = player
        self.path = []
        self.speed = 2
        self.tile_size = 48

    def calculate_path(self):
        start_x = self.rect.x // self.tile_size
        start_y = self.rect.y // self.tile_size

        goal_x = self.player.rect.x // self.tile_size
        goal_y = self.player.rect.y // self.tile_size

        start = (start_x, start_y)
        goal = (goal_x, goal_y)

        if start == goal:
            return
        
        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: h_score(start, goal)}

        while not open_set.empty():
            _, current_node = open_set.get()

            if current_node == goal:
                self.reconstruct_path(came_from, current_node)
                return
            
            for neighbour in self.get_neighbours(current_node):
                temp_g_score = g_score[current_node] + 1

                if temp_g_score < g_score.get(neighbour, float('inf')):
                    came_from[neighbour] = current_node
                    g_score[neighbour] = temp_g_score
                    f_score[neighbour] = g_score[neighbour] + h_score(neighbour, goal)
                    open_set.put((f_score[neighbour], neighbour))


    def reconstruct_path(self, came_from, current_node):
        path = []
        while current_node in came_from:
            path.append(current_node)
            current_node = came_from[current_node]
        self.path = path[::-1]
    
    def get_neighbours(self, node):
        x, y = node
        neighbours = []
        directions = [
            (0, -1), # Up
            (0, 1), # Down
            (-1, 0), # Left
            (1, 0), # Right
        ]

        for dx, dy in directions:
            new_cor = (x + dx), (y + dy)
            if self.tilemap.is_walkable(new_cor):
                neighbours.append(new_cor)
        return neighbours
    

    def update(self):
        if (
            not self.path or
            self.path[-1] != (self.player.rect.x // self.tile_size, self.player.rect.y // self.tile_size)
        ):
            self.calculate_path()
        if self.path:
            next_x, next_y = self.path[0]
            target_x = next_x * self.tile_size
            target_y = next_y * self.tile_size

            dx = target_x - self.rect.x
            dy = target_y - self.rect.y

            if abs(dx) > self.speed:
                self.rect.x += self.speed if dx > 0 else -self.speed
            elif abs(dx) > 0:
                self.rect.x = target_x
            if abs(dy) > 0:
                self.rect.y += self.speed if dy > 0 else -self.speed
            elif abs(dy) > 0:
                self.rect.y = target_y

            if self.rect.x == target_x and self.rect.y == target_y:
                self.path.pop(0)

    def draw(self, window, camera_x, camera_y):
        window.blit(self.image, self.rect.move(-camera_x, -camera_y))
            

    
class Player:
    def __init__(self, window, tilemap):
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

        self.tilemap = tilemap

        
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

        self.mask = pygame.mask.from_surface(self.image)

        while any(self.check_mask_collisions(tile_rect, tile_mask) for _, tile_rect, tile_mask in self.tilemap.tile_list):
            print(f"Player spawned inside a tile at {self.rect.topleft}, moving up...")
            self.rect.y -= 5  # Move the player up to find a valid position


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
            '''for _, tile_rect in self.tilemap.tile_list:
                if(
                    self.rect.bottom == tile_rect.top and
                    self.rect.right > tile_rect.left and
                    self.rect.left < tile_rect.right
                ):
                   if abs(self.rect.bottom - tile_rect.top) < 5:
                        self.is_on_ground = True
                        self.is_jump = False
                        self.jump_count = 2
                        break'''
            for _, tile_rect, tile_mask in self.tilemap.tile_list:
                if self.check_mask_collisions(tile_rect, tile_mask):
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
            
            self.mask = pygame.mask.from_surface(self.image)

    
    def jump(self):
        if self.jump_count > 0:
            self.movement[1] = -self.jump_vel
            self.jump_count -= 1
            self.is_jump = True

    def check_mask_collisions(self, tile_rect, tile_mask):
        offset_x = tile_rect.x - self.rect.x
        offset_y = tile_rect.y - self.rect.y
        return self.mask.overlap(tile_mask, (offset_x, offset_y))
    
    def horizontal_collisions(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.movement[0] = 0

        elif self.rect.right + self.movement[0] > self.tilemap.tilemap_width:
            self.rect.right = self.tilemap.tilemap_width
            self.movement[0] = 0
        
        
        for _, tile_rect, tile_mask in self.tilemap.tile_list:
            if self.check_mask_collisions(tile_rect, tile_mask):
                if self.movement[0] > 0:
                    self.rect.right = tile_rect.left
                if self.movement[0] < 0:
                    self.rect.left = tile_rect.right 
    
        if pygame.sprite.spritecollide(self, enemy_group, False):
            self.game_over = True
            print(self.game_over)                 

    def vertical_collisions(self):
        self.is_on_ground = False
        for _, tile_rect, tile_mask in self.tilemap.tile_list:
            if self.check_mask_collisions(tile_rect, tile_mask):
                if self.movement[1] > 0: 
                    self.rect.bottom = tile_rect.top
                    self.is_on_ground = True
                    self.movement[1] = 0
                    self.is_jump = False
                elif self.movement[1] < 0:
                    self.rect.top = tile_rect.bottom + 1
                    self.movement[1] = 0

        if self.rect.y >= self.ground_level:
            self.rect.y = self.ground_level
            self.is_on_ground = True
            self.movement[1] = 0


    def draw(self, window, camera_x, camera_y):
        self.draw_rect = self.rect.move(-camera_x, -camera_y)
        window.blit(self.image, self.draw_rect.topleft)
        #Draws the image at the newly determined position
