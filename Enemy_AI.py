import pygame

class Node:
    def __init__(self,x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.walkable = True

    def get_pos(self):
        return self.x, self.y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

def h_score(n1, n2):
    x1, y1 = n1
    x2, y2 = n2

    return abs(x1 - x2) + abs(y1- y2)
