import pygame
import json
from game_objects import enemy_group, Portal

tile_size = 48
ground_level = 466 


class Tilemap():
    def __init__(self, map_file, window, player=None):
        self.tile_list = []
        self.enemy_pos = []
        self.window = window
        self.player = player
        self.portals = []

        try:
            with open(map_file) as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading tilemap: {e}")
            self.data = {"layers": []}

        if not self.data.get("layers"):
            print("No layers found in the tilemap data.")
            return
        
        self.tileset_first_grid = self.data["tilesets"][0]["firstgid"]
        self.load_tiles()
        self.load_enemies()

        if self.data["layers"]:
            self.tilemap_width = self.data["layers"][0]["width"] * tile_size
            self.tilemap_height = self.data["layers"][0]["height"] * tile_size
        else:
            self.tilemap_width = 0
            self.tilemap_height = 0

        self.load_portals()

    def load_tiles(self):
        for layer in self.data["layers"]:
            if layer["type"] == "tilelayer":
                for y in range(layer["height"]):
                    for x in range(layer["width"]):
                        tile_id = layer["data"][y * layer["width"] + x]
                        if tile_id > 0:
                            self.add_tile(tile_id, x, y)

    def add_tile(self, tile_id, x, y):
        tutorial_tile_image_map = {
        1: "maps/individual tiles/block_(2).png",
        2: "maps/individual tiles/grass block (1).png",
        3: "maps/individual tiles/block_(3).png",
        5: "maps/individual tiles/block_(4).png"
        }                        

        tile_path = tutorial_tile_image_map.get(tile_id - self.tileset_first_grid + 1)
        if tile_path:
            image = pygame.image.load(tile_path).convert_alpha()
            image = pygame.transform.scale(image, (tile_size, tile_size))
            image_rect = image.get_rect(topleft = (x * tile_size, y * tile_size))
            image_mask = pygame.mask.from_surface(image)

            self.tile_list.append((image, image_rect, image_mask))

    def load_enemies(self):
        for layer in self.data["layers"]:
            if layer["type"] == "objectgroup" and layer["name"] == "Enemies":
                for obj in layer["objects"]:
                    self.enemy_pos.append((obj["x"], obj["y"]))
    
    def load_portals(self):
        portal_spawn_positions = []
        for layer in self.data["layers"]:
            if layer["type"] == "tilelayer":
                for y in range(layer["height"]):
                    for x in range(layer["width"]):
                        tile_id = layer["data"][y * layer["width"] + x]
                        if tile_id == 5:
                            portal_x = x * tile_size
                            portal_y = y * tile_size - tile_size
                            portal_spawn_positions.append((portal_x, portal_y))
        
        for x, y in portal_spawn_positions:
            portal = Portal(
                x,
                y,
                tile_size,
                tile_size,
                "next_map.tmj",
                x,
                y,
                "maps/individual tiles/portal frame 1.png"
            )
        self.portals.append(portal)

    def set_entities(self, player):
        self.player = player

        from Entities_file import Enemy
        for enemy_x, enemy_y in self.enemy_pos:
            enemy = Enemy(enemy_x, enemy_y, self, player)
            enemy_group.add(enemy)

    def draw(self, window, camera_x_offset, camera_y_offset):
        for img, img_rect, _ in self.tile_list:
            window.blit(img, img_rect.move(-camera_x_offset, -camera_y_offset))

        for portal in self.portals:
            portal.draw(self.window, camera_x_offset, camera_y_offset)

    def is_walkable(self, pos):
        x, y = pos
        for _, tile_rect, _ in self.tile_list:
            if tile_rect.collidepoint(x * tile_size, y * tile_size):
                return False
        return True

    def make_grid(self):
        from Entities_file import Node
        grid_width = self.data["width"]
        grid_height = self.data["height"]
        grid = [[Node(x,  y) for x in range(grid_width)] for y in range(grid_height)]

        for _, tile_rect in self.tile_list:
            x = tile_rect.x // tile_size
            y = tile_rect.x // tile_size
            if (
                0 <= y < grid_height and
                0 <= x < grid_width
            ):
                grid[y][x].walkable = False
        return grid
