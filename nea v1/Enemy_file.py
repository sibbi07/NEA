import pygame
from queue import PriorityQueue
from Spriteloader import loadSprite_y
from Enemy_AI import Node, h_score
from Player_file import Player

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, window):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = pygame.image.load("Sprites/NEA + converted terraria sprites/Enemy converted/NPC_21.png")
        self.image = loadSprite_y(self.spritesheet, 40, 56, 1, 1, False)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tile_size = 48
        self.map_width = 40
        self.map_height = 30
        self.path = []
        self.current_pos = 0
        self.grid_x = x // self.tile_size
        self.grid_y = y // self.tile_size
        self.node = Node(x, y)
        self.player = Player(window)

    def calculate_path(self, grid, start, goal):
        start = grid[self.grid_y][self.grid_x]
        goal = grid[self.player.rect.y][self.player.rect.x]
        
        open_set = PriorityQueue()
        open_set.put((f_score[start], start))
        came_from = {}
        
        g_score = {node: float("inf") for row in grid for node in row}
        g_score[start] = 0

        f_score = {node: float("inf") for row in grid for node in row}
        f_score[start] = h_score(start.get_pos(), goal.get_pos())

        while not open_set.empty():
            _, current_node = open_set.get()

            if current_node == goal:
                self.path = self.reconstruct_path(came_from, current_node)
                return
            
            for neighbour in self.get_neighbours(grid, current_node):
                temp_g_score = g_score[current_node] + 1
                came_from[neighbour] = current_node
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = g_score[neighbour] + h_score(neighbour, goal)
                open_set.put((f_score[neighbour], neighbour))

        self.path = []

    def move_towards_player(self):
        if self.path:
            next_node = self.path.pop(0) # Moves to the next node in the path by popping the current one out
            self.rect.x = next_node.x * self.tile_size
            self.rect.y = next_node.y * self.tile_size
            self.grid_x, self.grid_y = next_node.x, next_node.y

    def reconstruct_path(self, came_from, current_node):
        while current_node in came_from:
            self.path.append(current_node)
            current_node = came_from[current_node]
        return self.path
    
    def get_neighbours(self, grid, node):
        self.neighbours = []
        self.directions = [
            (0, -1), # Up
            (0, 1), # Down
            (-1, 0), # Left
            (1, 0), # Right
        ]

        for dx, dy in self.directions:
            neighbour_x = node.x + dx
            neighbour_y = node.y + dy

            if(
                0 <= neighbour_y < len(grid) and
                0 <= neighbour_x < len(grid[0])
            ):
                neighbour = grid[neighbour_y][neighbour_x]

                if neighbour.walkable:
                    self.neighbours.append(neighbour)
        return self.neighbours

    def update(self):
        if(
            not self.path or
            self.current_pos >= len(self.path)
        ):
            self.move_towards_player()
        

enemy_group = pygame.sprite.Group()
