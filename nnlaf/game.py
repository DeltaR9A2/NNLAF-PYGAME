import pygame

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

        self.strings = (
            "Ninmu Nanmu",
            "A Game About Love and Freedom",
            "",
            "=== Controls ===",
            "D-Pad: Arrow Keys",
            "Buttons: Z, X, C, V",
            "Triggers: A, S",
            "",
            "Press ENTER to open/close this screen.",
            "Close the window to exit the game.",
        )
       
    def update(self):
        pass
        
    def draw(self):
        self.screen.fill((32, 32, 32), (self.x, self.y, self.w, self.h))

        x = self.x+5
        y = self.y+2
        for string in self.strings:
            self.font.render(string, self.screen, (x, y))
            y += self.font.height

    
class GameMenu:
    def __init__(self, game):
        self.game = game
        self.core = self.game.core
        self.screen = self.core.screen

    def update(self):
        pass

    def draw(self):
        self.screen.fill((32, 128, 32), (32, 32, 128, 256))


class State:
    """This class is a disposable container representing a portion of the
    complete game world."""
    def __init__(self, game, zone):
        self.game = game
        self.zone = zone

        self.battles = [x for x in game.battles if x.zone == self.zone]
        self.targets = [x for x in game.targets if x.zone == self.zone]
        self.terrain = [x for x in game.terrain if x.zone == self.zone]


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

        self.state = None
        self.dialogue = None

        self.show_main_menu = True
        self.show_game_menu = False

        self.dialogue_queue = []

        self.message_timer = 0
        self.message_queue = []

        self.battles = []
        self.targets = []
        self.terrain = []

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
        elif self.state is not None:
            self.state.update()

        if self.controller.just_pressed("Y"):
            self.show_game_menu = True

    def draw(self):
        self.screen.fill((0, 0, 0))

        if self.state is not None:
            self.state.draw()

        if self.dialogue is not None:
            self.state.draw()
        
        if self.show_game_menu:
            self.game_menu.draw()

        if self.show_main_menu:
            self.main_menu.draw()
