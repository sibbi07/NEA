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

        self.health = 3
        self.alive = True

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

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
        if self not in enemy_group:
            return
        if not self.alive:
            return
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
        self.draw_rect = self.rect.move(-camera_x, -camera_y)
        window.blit(self.image, self.draw_rect.topleft)
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2)  # Draw white rectangle around the player
            

    
class Player:
    def __init__(self, window, tilemap):
        self.width = 16
        self.height = 16
        self.scale_factor = 2.5
        self.current_frame = 0
        self.frame_counter = 0
        self.facing_right = True  # Change to True
        self.is_jump = False
        self.jump_vel = 22
        self.grav = 1
        self.game_over = False

        self.tilemap = tilemap

        self.walking_spritesheet = pygame.image.load('Sprites/platformer_metroidvania asset pack v1.01/herochar sprites(new)/herochar_run_anim_strip_6.png').convert_alpha()
        self.attacking_spritesheet = pygame.image.load('Sprites/Knight 2D Pixel Art/Sprites/without_outline/ATTACK 1.png').convert_alpha()
        self.idle_spritesheet = pygame.image.load('Sprites/platformer_metroidvania asset pack v1.01/herochar sprites(new)/herochar_idle_anim_strip_4.png').convert_alpha()
        self.idle = [
            loadSprite_x(self.idle_spritesheet, self.width, self.height, i, self.scale_factor, False)
            for i in range(3)
        ]
        self.player_walking_left = [
            loadSprite_x(self.walking_spritesheet, self.width, self.height, i, self.scale_factor, False)
            for i in range(7)
        ]
        self.player_walking_right = [pygame.transform.flip(i, True, False) for i in self.player_walking_left]
        
        self.player_attacking_left = [
            loadSprite_x(self.attacking_spritesheet, self.width, self.height, i, self.scale_factor, False) 
            for i in range(5)
        ]
        self.player_attacking_right = [pygame.transform.flip(i, True, False) for i in self.player_attacking_left]
        
        # Ensure the last frame is not empty by repeating the last valid frame
        if not self.idle[-1]:
            self.idle[-1] = self.idle[-2]
        if not self.player_walking_left[-1]:
            self.player_walking_left[-1] = self.player_walking_left[-2]
        if not self.player_attacking_left[-1]:
            self.player_attacking_left[-1] = self.player_attacking_left[-2]

        self.image = self.idle[0]
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = self.tilemap.tilemap_height - self.image.get_height() - 50
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.ground_level = self.calculate_ground_level()

        self.movement = [0, 0] 
        self.speed = 3

        self.dashing = False
        self.dash_speed = 10
        self.dash_duration = 15
        self.dash_cooldown = 30
        self.dash_timer = 0
        self.dash_cooldown_timer = 0

        self.animation_speed = 3
        self.frame_counter = 0
        self.is_on_ground = True
        self.jump_count = 2

        self.mask = pygame.mask.from_surface(self.image)

        while any(self.check_mask_collisions(tile_rect, tile_mask) for _, tile_rect, tile_mask in self.tilemap.tile_list):
            print(f"Player spawned inside a tile at {self.rect.topleft}, moving up...")
            self.rect.y -= 5  # Move the player up to find a valid position

        self.sword_range = 30
        self.attack_cooldown = 30
        self.attack_timer = 0
        self.is_attacking = False
        self.sword_damage = 1

    def calculate_ground_level(self):
        bottom_tiles = [tile_rect.top for _, tile_rect, _ in self.tilemap.tile_list if tile_rect.bottom == self.tilemap.tilemap_height]
        return min(bottom_tiles) if bottom_tiles else self.tilemap.tilemap_height

    def input_handling(self, event):
        if self.game_over == False:
            if event.type == pygame.KEYDOWN: 
                if not self.dashing:
                    if event.key == pygame.K_RIGHT:
                        self.movement[0] = self.speed
                        self.facing_right = True
                    elif event.key == pygame.K_LEFT:
                        self.movement[0] = -self.speed
                        self.facing_right = False
                        
                if event.key == pygame.K_SPACE:
                    self.jump()
                if event.key == pygame.K_q:
                    self.dash()
                if event.key == pygame.MOUSEBUTTONDOWN:
                    self.swing_sword()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    self.movement[0] = 0  

    def update(self):
        if self.game_over:
            return
        
        if self.dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.dashing = False
                self.movement[0] = 0
        
        self.rect.x += self.movement[0]
        self.horizontal_collisions()

        if not self.is_on_ground:
            self.movement[1] += self.grav
        
        self.rect.y += self.movement[1]
        self.vertical_collisions()

        self.update_animation()
        self.mask = pygame.mask.from_surface(self.image)

        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= 1
    
    def update_attack_animation(self):
        if self.facing_right:
            self.image = self.player_attacking_left[self.attack_frame]
        else:
            self.image = self.player_attacking_right[self.attack_frame]

        if self.attack_frame == 2:
            self.check_sword_collision()
    
    def check_sword_collision(self):
        enemies_hit = pygame.sprite.spritecollide(self, enemy_group, False)
        for enemy in enemies_hit:
            enemy.take_damage(self.sword_damage)
    
    def jump(self):
        if self.jump_count > 0:
            self.movement[1] = -self.jump_vel
            self.jump_count -= 1
            self.is_jump = True

    def swing_sword(self):
        self.is_attacking = True
        self.attack_timer = self.attack_cooldown
        self.attack_frame = 0

    def dash(self):
        if (
            not self.dashing and
            self.dash_cooldown_timer == 0
        ):
            self.dashing = True
            self.dash_timer = self.dash_duration
            self.dash_cooldown_timer = self.dash_cooldown
            
            self.movement[0] = -self.dash_speed if not self.facing_right else self.dash_speed

    def check_mask_collisions(self, tile_rect, tile_mask):
        offset_x = tile_rect.x - self.rect.x
        offset_y = tile_rect.y - self.rect.y
        return self.mask.overlap(tile_mask, (offset_x, offset_y))
    
    def horizontal_collisions(self):
        future_rect = self.rect.copy()
        future_rect.x += self.movement[0]

        for _, tile_rect, tile_mask in self.tilemap.tile_list:
            if future_rect.colliderect(tile_rect):
                if self.movement[0] > 0:
                    self.rect.right = tile_rect.left
                elif self.movement[0] < 0:
                    self.rect.left = tile_rect.right
                self.movement[0] = 0

    def vertical_collisions(self):
        self.is_on_ground = False
        future_rect = self.rect.copy()
        future_rect.y += self.movement[1]

        for _, tile_rect, tile_mask in self.tilemap.tile_list:
            if future_rect.colliderect(tile_rect):
                if self.movement[1] > 0:
                    self.rect.bottom = tile_rect.top
                    self.is_on_ground = True
                    self.movement[1] = 0
                    self.jump_count = 2
                elif self.movement[1] < 0:
                    self.rect.top = tile_rect.bottom
                    self.movement[1] = 0
        if not self.is_on_ground:
            self.movement[1] += self.grav
            self.movement[1] = min(self.movement[1], 10)

        if self.is_on_ground and self.movement[0] == 0:
            self.movement[1] = 0

    def update_animation(self):
        self.frame_counter += 1
        if self.frame_counter >= 5:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.player_walking_right)

        if self.movement[0] != 0:
            self.image = self.player_walking_right[self.current_frame] if self.facing_right else self.player_walking_left[self.current_frame]
        else:
            self.image = self.idle[self.current_frame % len(self.idle)] 

    def draw(self, window, camera_x, camera_y):
        self.draw_rect = self.rect.move(-camera_x, -camera_y)
        window.blit(self.image, self.draw_rect.topleft)
