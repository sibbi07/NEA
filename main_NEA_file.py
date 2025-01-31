import pygame
import os
import sys
from tilemap import Tilemap, tutorial_tilemap_data
from Player_file import Player
from Enemy_file import Enemy, enemy_group


pygame.init()

class Button:
    def __init__(self, image, x_pos, y_pos, font, text_input, base_colour, alt_colour):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = font
        self.base_colour = base_colour
        self.alt_colour = alt_colour
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        self.text_input = text_input
        self.text = font.render(self.text_input, True, base_colour)
        if self.image is None:
            self.image = self.text
        self.text_rect = self.text.get_rect(center = (x_pos, y_pos))
    
    def update(self, window):
        if self.image is not None:
            window.blit(self.image, self.rect)
        window.blit(self.text, self.text_rect)

    def checkForInput(self, pos):
        if(
            pos[0] in range(self.rect.left, self.rect.right) and
            pos[1] in range(self.rect.top, self.rect.bottom)
        ):
            return True
        return False

    def changeColour(self, pos):
        if(
            pos[0] in range(self.rect.left, self.rect.right) and
            pos[1] in range(self.rect.top, self.rect.bottom)
        ):
            self.text = self.font.render(self.text_input, True, self.alt_colour)
        else:
            self.text = self.font.render(self.text_input, True, self.base_colour)


class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((720, 576))
        #Creates the window for the game
        
        pygame.display.set_caption("Chronostars")
        #Sets the caption as 'Chronostars'
        
        self.logo_path = os.path.join('Sprites/clock_logo-removebg-preview.png')
        self.logo = pygame.image.load(self.logo_path).convert_alpha()

        self.clock = pygame.time.Clock()


        self.bg_path = os.path.join('Sprites/NEA + converted terraria sprites/NeonVeil/NeonVeilBG13.png')
        self.bg = pygame.image.load(self.bg_path).convert_alpha()

        self.game_over_img = pygame.image.load("maps/game over screens/game over (2).png")
        self.play_button_img = pygame.image.load("buttons/play_button.png")


        self.player = Player(self.window)
        self.map = Tilemap(tutorial_tilemap_data, self.window)

        self.scroll = 0

        self.camera_offset_x = self.player.rect.centerx - (self.window.get_width() // 2)
        self.camera_offset_y = self.player.rect.centery - (self.window.get_height() // 2)


        self.camera_left_limit = self.window.get_width() // 4
        self.camera_right_limit = (self.window.get_width() * 3) // 4
        self.camera_top_limit = self.window.get_height() // 4
        self.camera_bottom_limit = (self.window.get_height() * 3) // 4

        self.main_font = pygame.font.SysFont("broadway", 80)
        self.sub_font = pygame.font.SysFont("broadway", 65)
    
    def draw_grid(self):
        self.tile_size = 48
        
        for line in range(0, self.window.get_width()):
            pygame.draw.line(self.window, (255, 255, 255), (0, line *  self.tile_size), (self.window.get_width(), line * self.tile_size))
        
        for line in range(0, self.window.get_height()):
            pygame.draw.line(self.window, (255, 255, 255), (line *  self.tile_size, 0), (line * self.tile_size, self.window.get_height()))

    def main_menu(self):
        while True:
            self.background = pygame.image.load("maps/game over screens/main menu screen (2).png")
            self.window.blit(self.background, (0, 0))
            self.menu_mouse_pos = pygame.mouse.get_pos()
            self.menu_text = self.main_font.render("CHRONO-", True, (255,194,14))
            self.menu_text_2 = self.main_font.render("STARS", True, (255,194,14))
            self.menu_rect = self.menu_text.get_rect(center= (200, 100))
            self.menu_rect_2 = self.menu_text_2.get_rect(center= (200, 200))
            
            self.play_button = Button(self.play_button_img, 100, 500, self.sub_font, "PLAY", "white", (95, 156, 95))
            self.settings_button = Button(self.play_button_img, 550, 500, self.sub_font, "SETTINGS", "white", (95, 156, 95))

            self.window.blit(self.menu_text, self.menu_rect)
            self.window.blit(self.menu_text_2, self.menu_rect_2)

            for button in [self.play_button, self.settings_button]:
                button.changeColour(self.menu_mouse_pos)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.checkForInput(self.menu_mouse_pos):
                        self.play()
                    if self.settings_button.checkForInput(self.menu_mouse_pos):
                        self.settings()
                    '''if self.quit_button.checkForInput(self.menu_mouse_pos):
                        pygame.quit()
                        sys.exit()'''

            pygame.display.update()
    
    def settings(self):
        while True:
        
            self.settings_mouse_pos = pygame.mouse.get_pos()
            self.window.fill("black")

            self.controls_button = Button(self.play_button_img, 300, 200, self.main_font, "CONTROLS", "white", (95, 156, 95))
            self.music_button = Button(self.play_button_img, 300, 350, self.main_font, "MUSIC", "white", (95, 156, 95))
            self.back_button = Button(self.play_button_img, 300, 500, self.main_font, "BACK", "white", (95, 156, 95))

            for button in [self.controls_button, self.music_button, self.back_button]:
                button.changeColour(self.settings_mouse_pos)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.checkForInput(self.settings_mouse_pos):
                        self.main_menu()

            pygame.display.update()

    def play(self):
        while True:
            pygame.display.set_icon(self.logo)

            bg_x_pos = -self.camera_offset_x // 2 - 1000
            bg_y_pos = -self.camera_offset_y // 2 - 400

            self.update_camera()
            
            if self.player.game_over == False:
                for i in range(0, 2):
                    self.window.blit(self.bg, (self.bg.get_width() * i + self.scroll + bg_x_pos, bg_y_pos))

                if self.player.movement[0] != 0:
                    self.scroll -= self.player.movement[0]

                if abs(self.scroll) > self.bg.get_width():
                    self.scroll = 0

            self.draw_grid()

            self.map.draw(self.window, self.camera_offset_x, self.camera_offset_y)
            #print(self.map.tile_list)

            enemy_group.update()
            if self.player.game_over == False:
                for enemy in enemy_group:
                    # Adjust enemy's position based on camera offset
                    #adjusted_rect = enemy.rect.move(-self.camera_offset_x, -self.camera_offset_y)
                    #self.window.blit(enemy.image, adjusted_rect.topleft)
                    enemy.update()
            
            self.player.update()
            self.player.draw(self.window, self.camera_offset_x, self.camera_offset_y)

            if self.player.game_over == True:
                self.window.blit(self.game_over_img, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    #Game quits when the X is pressed in the top right
                
                self.player.input_handling(event)

            pygame.display.update()
            self.clock.tick(60)
    
    def update_camera(self):
        self.player_centre_x = self.player.rect.centerx
        self.player_centre_y = self.player.rect.centery

        if self.player_centre_x - self.camera_offset_x < self.camera_left_limit:
            self.camera_offset_x = self.player_centre_x - self.camera_left_limit
        elif self.player_centre_x - self.camera_offset_x> self.camera_right_limit:
            self.camera_offset_x = self.player_centre_x - self.camera_right_limit

        if self.player_centre_y - self.camera_offset_y < self.camera_top_limit:
            self.camera_offset_y = self.player_centre_y - self.camera_top_limit
        elif self.player_centre_y - self.camera_offset_y > self.camera_bottom_limit:
            self.camera_offset_y = self.player_centre_y - self.camera_bottom_limit 

        self.camera_offset_x = max(0, min(self.camera_offset_x, self.map.tilemap_width - self.window.get_width()))
        #self.camera_offset_y = max(0, self.camera_offset_y)



if __name__ == "__main__":
    game = Game()
    #Creates a separate instance of the Game class for maintainability

    game.main_menu()
    #Runs the game
