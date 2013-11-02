from player_body import PlayerBody
from player_sprite import PlayerSprite
from player_status import PlayerStatus


class Player:
    def __init__(self, game):
        self.game = game

        self.size = (28, 60)

        self.body = PlayerBody(self)
        self.sprite = PlayerSprite(self)
        self.status = PlayerStatus(self)

        self.health = 1000
        self.damage = 0
        self.stun = 0

        self.keys = ["default"]

        #self.hurt_sound = self.game.core.get_sound("player_hurt.ogg")

    def update(self, ticks):
        self.body.update(ticks)
        self.sprite.update(ticks)
        self.status.update(ticks)

        if self.stun > 0:
            self.stun = max(self.stun - 0.1, 0)

    def collect(self, pickup):
        if pickup.drop_type == "key":
            self.keys.append(pickup.config)

    def take_damage(self, n):
        if self.sprite.flashing == 0:
            self.damage = min(self.damage + n, self.health)
            self.stun = min(self.stun + (n*10), self.health - self.damage)
            self.sprite.flashing = 60
            #self.hurt_sound.play()

    def is_dangerous(self):
        if self.body.dash_timer > 0:
            return True
        else:
            return False
