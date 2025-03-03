import pygame

enemy_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()

class Projectiles(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.speed = 5
        self.direction = direction

    def update(self):
        self.rect.x += self.speed * self.direction

    def draw(self, window, camera_x, camera_y):
        self.draw_rect = self.rect.move(-camera_x, -camera_y)
        window.blit(self.image, self.draw_rect.topleft)

    
