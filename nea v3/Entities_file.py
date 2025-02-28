import pygame
from queue import PriorityQueue
from Spriteloader import loadSprite_x, loadSprite_y
from game_objects import enemy_group

class Node:
    def __init__(self,x, y):
        self.x = x # X coordinate of the node
        self.y = y # Y coordinate of the node
        self.parent = None # Parent node of the current node
        self.walkable = True # Node is initially walkable
        self.f_score = float("inf") # Sets the f score as infinite initially

    def get_pos(self):
        return self.x, self.y # Returns the x and y coordinates of the node
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y # Checks if the x and y coordinates of the nodes are the same
    
    def __hash__(self):
        return hash((self.x, self.y)) # Returns the hash of the x and y coordinates of the node. This is needed because the node is used in a set
    
    def __lt__(self, other):
        return self.f_score < other.f_score # Compares the f score of the current node with another node

def h_score(pos1, pos2): # Heuristic score
    x1, y1 = pos1
    x2, y2 = pos2

    return abs(x1 - x2) + abs(y1- y2) # Creates an estimate of the distance between the two nodes but it is not the actual distance of the path

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, tilemap, player):
        super().__init__()
        self.spritesheet = pygame.image.load("Sprites/NEA + converted terraria sprites/Enemy converted/NPC_4.png")
        self.image = loadSprite_y(self.spritesheet, 40, 56, 1, 1, False) # Loads the image of the enemy
        self.rect = self.image.get_rect(topleft = (x,y)) # Set the rect of the enemy to the rect of the image
        self.tilemap = tilemap # Initialise the tilemap
        self.player = player # Initalise the player
        self.path = [] # Make the path empty initially
        self.speed = 4
        self.tile_size = 48

        self.health = 3
        self.alive = True

    def take_damage(self, damage): # Function for the enemy to take damage
        self.health -= damage # Reduce the health of the enemy by the damage dealt
        if self.health <= 0:
            self.kill() # Get rid of the sprite if the enemy has no health

    def calculate_path(self):
        start_x = self.rect.x // self.tile_size # Gets the x coordinate of the enemy
        start_y = self.rect.y // self.tile_size # Gets the y coordinate of the enemy

        goal_x = self.player.rect.x // self.tile_size # Gets the x coordinate of the player
        goal_y = self.player.rect.y // self.tile_size # Gets the y coordinate of the player

        start = (start_x, start_y)
        goal = (goal_x, goal_y)

        if start == goal: # If the enemy is on the same tile as the player, end the path calculation
            return
        
        open_set = PriorityQueue() # Creates a priority queue
        open_set.put((0, start)) # Puts the start node into the open set
        came_from = {} # Creates a dictionary to store each previous node
        g_score = {start: 0} # Creates a dictionary to store the G-score of each node. G-score is the cost of the path from the start node to the current node
        f_score = {start: h_score(start, goal)} # Creates a dictionary to store the F-score of each node. F-score is the sum of the G-score and the H-score of the node

        while not open_set.empty(): # While there is still nodes in the open set
            _, current_node = open_set.get() # Gets the current node from the open set

            if current_node == goal: # If the goal is found, reconstruct the path
                self.reconstruct_path(came_from, current_node)
                return # End the calculation if the current node is found
            
            for neighbour in self.get_neighbours(current_node): # For each neighbour of the current node 
                temp_g_score = g_score[current_node] + 1 # Calculate the temporary G-score of the neighbour. This is used to determine if the a different path is shorter than the current one

                if temp_g_score < g_score.get(neighbour, float('inf')): # If the temp G-score is less than the current G-score of the neighbour, it means that the path is shorter
                    came_from[neighbour] = current_node
                    g_score[neighbour] = temp_g_score # Since the temporary G-score is shorter than the current G-score, the temporary G-score becomes the current as we want the shortest path.
                    f_score[neighbour] = g_score[neighbour] + h_score(neighbour, goal) # New F-score is calculated
                    open_set.put((f_score[neighbour], neighbour)) # The neighbour is added to the open set with the updated F-score


    def reconstruct_path(self, came_from, current_node):
        path = [] # Creates a list to store the path
        while current_node in came_from: # While there is still nodes in the came_from dictionary
            path.append(current_node) # Add the current node to the path
            current_node = came_from[current_node] # Move to the previous node
        self.path = path[::-1] # Since the path is from the player to the enemy, reverse it for the path from the enemy to the player
    
    def get_neighbours(self, node):
        x, y = node
        neighbours = [] # List to store the neighbours of the node
        directions = [
            (0, -1), # Up
            (0, 1), # Down
            (-1, 0), # Left
            (1, 0), # Right
        ] # List of directions to check for neighbours

        for self.movement in directions:
            neighbour_coor = (x + self.movement[0]), (y + self.movement[1]) # Calculate the new coordinates of the neighbour
            if self.tilemap.is_walkable(neighbour_coor): # Checks if the node is walkable
                neighbours.append(neighbour_coor) # If the node is walkable, add it to the neighbours list
        return neighbours
    

    def update(self):
        if self not in enemy_group:
            return # Doesn't find the path if the enemy sprite is not there
        if not self.alive: # Doesn't find the path if the enemy is 'dead'
            return
        if (
            not self.path or
            self.path[-1] != (self.player.rect.x // self.tile_size, self.player.rect.y // self.tile_size)
        ): 
            self.calculate_path() # If there is no path or the player has moved, find a new path
        if self.path: # If there is a path
            next_x, next_y = self.path[0] # Get the next node in the path
            target_x = next_x * self.tile_size # Calculate the target x coordinate
            target_y = next_y * self.tile_size # Calculate the target y coordinate

            self.movement = ((target_x - self.rect.x), (target_y - self.rect.y))

            if abs(self.movement[0]) > self.speed: # If the x movement is greater than the speed
                self.rect.x += self.speed if self.movement[0] > 0 else -self.speed # Move the enemy by the speed depending on direction
            elif abs(self.movement[0]) > 0: # If the x movement is less than the speed
                self.rect.x = target_x # Snap the enemy to the target x coordinate
            if abs(self.movement[1]) > self.speed: # If the y movement is greater than the speed
                self.rect.y += self.speed if self.movement[1] > 0 else -self.speed # Move the enemy by the speed depending on direction
            elif abs(self.movement[1]) > 0: # If the y movement is less than the speed
                self.rect.y = target_y # Snap the enemy to the target y coordinate

            if self.rect.x == target_x and self.rect.y == target_y: # If the enemy has reached the target node
                self.path.pop(0) # Remove the target node from the path

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
        self.facing_right = True
        self.is_jump = False
        self.jump_vel = 25
        self.grav = 1
        self.game_over = False

        self.tilemap = tilemap

        self.load_spritesheets()

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

        self.animation_speed = 3 #
        self.frame_counter = 0
        self.is_on_ground = True
        self.jump_count = 2
        self.is_on_wall = False
        self.is_holding_wall = False
        self.has_wall_jumped = False
        self.wall_jump_duration = 15
        self.wall_jump_timer = 0

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
    
    def flip_sprites(self, sprites):
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites]
    
    def load_sprites(self, sprite_sheet, frame_num):
        frame_num = max(frame_num, 1)
        return [loadSprite_x(sprite_sheet, self.width, self.height, i, self.scale_factor, False) for i in range(frame_num)]
    
    def load_spritesheets(self):
        self.walking_spritesheet = pygame.image.load('Sprites/platformer_metroidvania asset pack v1.01/herochar sprites(new)/herochar_run_anim_strip_6.png').convert_alpha()
        self.attacking_spritesheet = pygame.image.load('Sprites/platformer_metroidvania asset pack v1.01/herochar sprites(new)/herochar_sword_attack_anim_strip_4.png').convert_alpha()
        self.idle_spritesheet = pygame.image.load('Sprites/platformer_metroidvania asset pack v1.01/herochar sprites(new)/herochar_idle_anim_strip_4.png').convert_alpha()
        self.jumping_spritesheet = pygame.image.load('Sprites/platformer_metroidvania asset pack v1.01/herochar sprites(new)/herochar_jump_up_anim_strip_3.png').convert_alpha()
        self.falling_spritesheet = pygame.image.load('Sprites/platformer_metroidvania asset pack v1.01/herochar sprites(new)/herochar_jump_down_anim_strip_3.png').convert_alpha()
        
        self.idle = self.load_sprites(self.idle_spritesheet, 3)
        self.walking_right = self.load_sprites(self.walking_spritesheet, 7)
        self.attacking_right = self.load_sprites(self.attacking_spritesheet, 3)
        self.jumping_right = self.load_sprites(self.jumping_spritesheet, 2)
        self.falling_right = self.load_sprites(self.falling_spritesheet, 2)

        self.walking_left = self.flip_sprites(self.walking_right)
        self.attacking_left = self.flip_sprites(self.attacking_right)
        self.jumping_left = self.flip_sprites(self.jumping_right)
        self.falling_left = self.flip_sprites(self.falling_right)

        self.ensure_last_frame(self.idle)
        self.ensure_last_frame(self.walking_right)
        self.ensure_last_frame(self.attacking_right)
   
    def ensure_last_frame(self, sprite_list):
        if not sprite_list[-1]:
            sprite_list[-1] = sprite_list[-2]
    
    def update_animation(self):
        if self.is_attacking: # Checks if the player is attacking
            self.frame_counter += 1 # Increases the frame counter by 1
            if self.frame_counter >= self.animation_speed: # Checks if the frame counter is greater than or equal to the animation speed
                self.frame_counter = 0 # Frame counter is reset
                self.current_frame = (self.current_frame + 1) % len(self.attacking_right) # Changes the current frame to the next frame
            if self.facing_right: # Checks the direction the player is facing
                self.image = self.attacking_right[self.current_frame % len(self.attacking_right)] # Runs the animation for attacking to the right
            else:
                self.image = self.attacking_left[self.current_frame % len(self.attacking_left)] # Runs the animation for attacking to the left
            if self.current_frame == 2: 
                self.check_sword_collision() # Checks for collision with the sword
        elif not self.is_on_ground: # Checks if the player is in the air
            self.frame_counter += 1
            if self.frame_counter >= 5:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.jumping_right)
            # Change the animation to the jumping sprite depending on the direction the player is facing
            if self.movement[1] < 0:
                self.image = self.jumping_right[self.current_frame % len(self.jumping_right)] if self.facing_right else self.jumping_left[self.current_frame % len(self.jumping_left)]
            # Change the animation to the falling sprite depending on the direction the player is facing
            else:
                self.image = self.falling_right[self.current_frame % len(self.falling_right)] if self.facing_right else self.falling_left[self.current_frame % len(self.falling_left)]
        elif self.movement[0] != 0: # Checks if the player is moving horizontally (walking)
            self.frame_counter += 1
            if self.frame_counter >= 5:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.walking_right)
            # Change the animation to the walking sprite depending on the direction the player is facing
            self.image = self.walking_right[self.current_frame % len(self.walking_right)] if self.facing_right else self.walking_left[self.current_frame % len(self.walking_left)]
        else:
            #If no movement is detected, the idle animation runs
            self.frame_counter += 1
            if self.frame_counter >= 5:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.idle)
            self.image = self.idle[self.current_frame % len(self.idle)]

    def input_handling(self, event):
        if self.game_over == False:
            if event.type == pygame.KEYDOWN:
                if not self.dashing:
                    if event.key in [pygame.K_RIGHT, pygame.K_d]: # Checks if the right arrow key or D key are pressed
                        self.movement[0] = self.speed
                        self.facing_right = True
                    elif event.key in [pygame.K_LEFT, pygame.K_a]: # Checks if the left arrow key or A key are pressed
                        self.movement[0] = -self.speed
                        self.facing_right = False

                if event.key == pygame.K_SPACE:
                    if self.is_holding_wall:  # If clinging to the wall, perform wall jump
                        self.wall_jump()
                    else:
                        self.jump()  # Regular jump
                
                elif event.key == pygame.K_q:
                    self.dash()
                elif event.key == pygame.K_e:
                    self.swing_sword()
                elif event.key == pygame.K_z:
                    if self.is_touching_wall() and not self.is_on_ground:
                        self.is_holding_wall = True  # Start clinging to wall

            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_RIGHT, pygame.K_d] and self.movement[0] > 0:
                    self.movement[0] = 0 # Stops the player from moving when the right arrow key or D key are released
                elif event.key in [pygame.K_LEFT, pygame.K_a] and self.movement[0] < 0:
                    self.movement[0] = 0 # Stops the player from moving when the left arrow key or A key are released
                elif event.key == pygame.K_z:
                    self.is_holding_wall = False  # Release from wall if Z is released


    def update(self):
        if self.game_over: # If the game is over
            return  # Don't update the player
        if self.dashing: # Checks if the player is dashing
            self.dash_timer -= 1 # Decrease the dash timer by 1
            if self.dash_timer <= 0: # If the dash timer is less than or equal to 0
                self.dashing = False # Stop the player from dashing
                self.movement[0] = 0 # Stop the player's horizontal movement

        self.rect.x += self.movement[0] # Move the player by the x movement
        self.horizontal_collisions()

        if not self.is_on_ground: # If the player is not on the ground
            self.movement[1] += self.grav # Apply gravity to the player

        self.rect.y += self.movement[1] # Move the player by the y movement
        self.vertical_collisions()
        
        if self.is_attacking: # If the player is attacking
            self.attack_timer -= 1 # Decrease the attack timer by 1
            if self.attack_timer <= 0: # If the attack timer is less than or equal to 0
                self.is_attacking = False # Stop the player from attacking
        self.update_animation() # Update the player's animation
        self.mask = pygame.mask.from_surface(self.image) # Update the player's mask

        if self.dash_cooldown_timer > 0: # If the dash cooldown timer is still running
            self.dash_cooldown_timer -= 1 # Decrease the dash cooldown timer by 1

        if self.is_holding_wall:
            self.hold_onto_wall()
        else:
            self.is_on_wall = False

        if self.is_on_ground: # If the player is on the ground
            self.jump_count = 2 # Reset the jump count
            self.has_wall_jumped = False  # Allow future wall jumps
        if self.wall_jump_timer > 0: # Checks if the timer for the wall jump is more than 0
            self.wall_jump_timer -= 1 # Decrease the timer by 1
            if self.wall_jump_timer == 0: # If the timer is 0
                self.movement[0] = 0 # Stop the horizontal movement in the air
    
    def check_sword_collision(self):
        enemies_hit = pygame.sprite.spritecollide(self, enemy_group, False) # Check for collision with the sword
        for enemy in enemies_hit: # For each enemy hit by the sword
            enemy.take_damage(self.sword_damage) # Deal damage to the enemy
    
    def jump(self):
        if self.jump_count > 0 and not self.has_wall_jumped: # Checks if the user has any jumps left and if they haven't just wall jumped
            self.movement[1] = -self.jump_vel # Moves the player up
            self.jump_count -= 1 # Decreases the jump count by 1
            self.is_jump = True # Sets the player as jumping

    def wall_jump(self):
        if self.is_holding_wall: # Checks if the player is holding onto a wall before wall jumping
            self.movement[0] = -self.speed * 2 if self.facing_right else self.speed * 2  # Push away from the wall
            self.movement[1] = -self.jump_vel  # Jump upwards
            self.is_jump = True
            self.is_holding_wall = False  # Release from wall
            self.is_on_wall = False
            self.has_wall_jumped = True  # Mark that a wall jump happened
            self.wall_jump_timer = self.wall_jump_duration

            
    def hold_onto_wall(self):
        if self.is_touching_wall() and not self.is_on_ground and self.is_holding_wall:
            self.movement[1] = 0  # Prevent falling while holding the wall
            self.is_on_wall = True
            self.movement[0] = 0  # Stop horizontal movement when holding the wall
        else:
            self.is_on_wall = False

    def is_touching_wall(self):
        future_rect_left = self.rect.copy() # Create a copy of the player's rect
        future_rect_left.x -= 1 # Move the rect to the left
        future_rect_right = self.rect.copy() # Create a copy of the player's rect
        future_rect_right.x += 1 # Move the rect to the right

        for _, tile_rect, _ in self.tilemap.tile_list: # For each tile in the tile list
            return future_rect_left.colliderect(tile_rect) or future_rect_right.colliderect(tile_rect) # Check if the player's colliding with the wall
            
    def swing_sword(self): # Function for the player to swing the sword
        self.is_attacking = True # Set the player as attacking
        self.attack_timer = self.attack_cooldown # Set the attack timer to the attack cooldown
 
    def dash(self):
        if (
            not self.dashing and
            self.dash_cooldown_timer == 0
        ): # Check if the player is able to dash
            self.dashing = True # Set the player as dashing
            self.dash_timer = self.dash_duration # Set the dash timer to the dash duration
            self.dash_cooldown_timer = self.dash_cooldown # Set the dash cooldown timer to the dash cooldown
            
            self.movement[0] = -self.dash_speed if not self.facing_right else self.dash_speed # Move the player by the dash speed depending on the direction

    def check_mask_collisions(self, tile_rect, tile_mask):
        offset_x = tile_rect.x - self.rect.x # Calculate the x offset 
        offset_y = tile_rect.y - self.rect.y # Calculate the y offset
        return self.mask.overlap(tile_mask, (offset_x, offset_y)) # Check if the player's mask is overlapping with the tile's mask
    
    def horizontal_collisions(self):
        future_rect = self.rect.copy() # Create a copy of the player's rect
        future_rect.x += self.movement[0] # Move the rect by the x movement

        for _, tile_rect, _ in self.tilemap.tile_list: # For each tile in the tile list
            if future_rect.colliderect(tile_rect): # Check if the player's rect is colliding with the tile's rect
                if self.movement[0] > 0: # If the player is moving right
                    self.rect.right = tile_rect.left # Set the player's right side equal to the tile's left side
                elif self.movement[0] < 0: # If the player is moving left
                    self.rect.left = tile_rect.right # Set the player's left side equal to the tile's right side
                self.movement[0] = 0 # Stop the player's horizontal movement

    def vertical_collisions(self):
        self.is_on_ground = False # Assume the player is not on the ground
        future_rect = self.rect.copy() # Create a copy of the player's rect
        future_rect.y += self.movement[1] # Move the rect by the y movement

        for _, tile_rect, _ in self.tilemap.tile_list: # For each tile in the tile list
            if future_rect.colliderect(tile_rect): # Check if the player's rect is colliding with the tile's rect
                if self.movement[1] > 0:  # Hitting the ground
                    self.rect.bottom = tile_rect.top # Set the player's bottom side equal to the tile's top side
                    self.is_on_ground = True # Set the player as on the ground
                    self.movement[1] = 0 # Stop the player's vertical movement
                    self.jump_count = 2  # Reset jumps when on the ground
                elif self.movement[1] < 0:  # Hitting the bottom of a tile 
                    self.rect.top = tile_rect.bottom # Set the player's top side equal to the tile's bottom side
                    self.movement[1] = 0 # Stop the player's vertical movement

        if not self.is_on_ground: # If the player is not on the ground
            self.movement[1] += self.grav # Apply gravity to the player
            self.movement[1] = min(self.movement[1], 10) # Limit the player's falling speed

    def draw(self, window, camera_x, camera_y): # Draw the player
        self.draw_rect = self.rect.move(-camera_x, -camera_y) # Move the player's rect by the camera's x and y
        window.blit(self.image, self.draw_rect.topleft) # Draw the player's image at the top left of the player's rect
