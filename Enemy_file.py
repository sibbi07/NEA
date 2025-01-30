import pygame
from queue import PriorityQueue
from Spriteloader import loadSprite_y
from Enemy_AI import Node, h_score

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = pygame.image.load("Sprites/NEA + converted terraria sprites/Enemy converted/NPC_21.png")
        self.image = loadSprite_y(self.spritesheet, 40, 56, 1, 1, False)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.path = []
        self.current_waypoint = 0
        self.node = Node(x, y)

    def calculate_path(self, grid, start, goal):
        open_set = PriorityQueue()
        came_from = {}
        g_score = {self.node: float("inf") for row in grid for node in row}
        g_score[start] = 0
        f_score = {self.node: float("inf") for row in grid for node in row}
        f_score[start] = h_score(start.get_pos(), goal.get_pos())


    def update(self):
        pass

    

enemy_group = pygame.sprite.Group()
