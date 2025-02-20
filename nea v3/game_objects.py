import pygame

enemy_group = pygame.sprite.Group()

class Portal:
    def __init__(self, x, y, width, height, spawn_x, spawn_y, destination_map, image_path = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.destination_map = destination_map
        self.spawn_pos = (spawn_x, spawn_y)

        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = None

    def check_collision(self, player):
        if self.rect.colliderect(player.rect):
            return True
        return False
    
    def draw(self, window, camera_x, camera_y):
        draw_rect = self.rect.move(-camera_x, -camera_y)
        if self.image:
            window.blit(self.image, draw_rect.topleft)
        else:
            pygame.draw_rect(window, (0, 0, 255), draw_rect, 2)
