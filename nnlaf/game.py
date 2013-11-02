import pygame

from rect import Rect
from controller import Controller


class MainMenu:
    def __init__(self, game):
        self.game = game
        self.core = self.game.core
        self.screen = self.core.screen

        self.font = self.core.get_font("font_8bit_operator_white.png")
        
        screen_w, screen_h = self.screen.get_size()

        self.w = 320
        self.h = 240
        self.x = (screen_w - self.w) // 2
        self.y = (screen_h - self.h) // 2

        self.text = """Ninmu Nanmu
A Game About Love and Freedom

=== Controls ===
D-Pad: Arrow Keys
Buttons: Z, X, C, V
Triggers: A, S

Press ENTER to open/close this screen.
Close the window to exit the game."""

        self.text_surface = self.font.render_block(self.text, 310)

    def update(self):
        pass
        
    def draw(self):
        self.screen.fill((32, 32, 32), (self.x, self.y, self.w, self.h))

        self.screen.blit(self.text_surface, (self.x+5, self.y+2))

    
class GameMenu:
    def __init__(self, game):
        self.game = game
        self.core = self.game.core
        self.screen = self.game.screen

    def update(self):
        pass

    def draw(self):
        self.screen.fill((32, 128, 32), (32, 32, 128, 256))


class Zone:
    """This class is a disposable container representing a portion of the
    complete game world."""
    def __init__(self, game, zone):
        self.game = game
        self.zone = zone

        self.screen = self.game.screen

        self.battles = [x for x in game.battles if x.zone == self.zone]
        self.targets = [x for x in game.targets if x.zone == self.zone]
        self.terrain = [x for x in game.terrain if x.zone == self.zone]

        # Determine the size required for the map surface
        map_size_rect = Rect()
        for ter in self.terrain:
            map_size_rect.union(ter.rect)

        self.map_surface = pygame.Surface(map_size_rect.size)

        # Draw all static terrain and targets to the map surface
        for ter in self.terrain:
            if ter.static:
                self.map_surface.fill((255, 0, 0), ter)
                ter.draw(self.map_surface)

        for tar in self.targets:
            if tar.static:
                tar.draw(self.map_surface)

    def draw(self):
        self.screen.blit(self.map_surface, (0, 0))

    def update(self):
        pass


class Game:
    """This class represents the highest level of the game logic, managing the
    other more specific components of the game."""
    def __init__(self, core):
        self.core = core
        self.running = True

        self.screen = pygame.display.get_surface()

        self.controller = Controller()
        
        self.main_menu = MainMenu(self)
        self.game_menu = GameMenu(self)

        self.show_main_menu = True
        self.show_game_menu = False

        self.battles = []
        self.targets = []
        self.terrain = []

        ########
        from world_model import Terrain
        terrain_image = self.core.get_image("canister_apartment.png")
        test_terrain = Terrain()
        test_terrain.add_image(terrain_image)
        test_terrain.zone = "apartment"
        self.terrain.append(test_terrain)
        ########

        self.zone = Zone(self, "apartment")
        self.dialogue = None

    def fast_step(self):
        self.update()

    def step(self):
        self.update()
        self.draw()
        
    def update(self):
        for event in pygame.event.get(pygame.QUIT):
            if event.type == pygame.QUIT:
                self.running = False

        self.controller.update()

        if self.controller.just_pressed("START"):
            self.show_main_menu = not self.show_main_menu

        if self.show_main_menu:
            self.main_menu.update()
            return

        if self.show_game_menu:
            self.game_menu.update()
            if self.controller.just_pressed("Y"):
                self.show_game_menu = False
            return

        if self.dialogue is not None:
            self.dialogue.update()
        elif self.zone is not None:
            self.zone.update()

        if self.controller.just_pressed("Y"):
            self.show_game_menu = True

    def draw(self):
        self.screen.fill((0, 0, 0))

        if self.zone is not None:
            self.zone.draw()

        if self.dialogue is not None:
            self.zone.draw()
        
        if self.show_game_menu:
            self.game_menu.draw()

        if self.show_main_menu:
            self.main_menu.draw()
