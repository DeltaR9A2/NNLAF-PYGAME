
class PlayerStatus:
    def __init__(self, player):
        self.player = player

        self.health_bars_image = self.player.game.core.get_image("ui_health_bars.png")

        self.blank_bar = self.health_bars_image.subsurface((0, 0, 256, 16))
        self.full_bar = self.health_bars_image.subsurface((0, 16, 256, 16))
        self.stun_bar = self.health_bars_image.subsurface((0, 32, 256, 16))

        self.stun_fraction = 0.0
        self.full_fraction = 0.0

    def update_self(self, ticks):
        self.stun_fraction = float(self.player.health - self.player.damage) / float(self.player.health)
        self.full_fraction = float(self.player.health - (self.player.stun + self.player.damage)) / float(self.player.health)

    def draw_self(self, camera):
        x = 8
        y = camera.surface.get_height() - (16+8)
        camera.surface.blit(self.blank_bar, (x, y))
        camera.surface.blit(self.stun_bar, (x, y), (0, 0, int(256*self.stun_fraction), 16))
        camera.surface.blit(self.full_bar, (x, y), (0, 0, int(256*self.full_fraction), 16))
