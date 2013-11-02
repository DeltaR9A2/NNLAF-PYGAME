from rect import Rect


class Body(Rect):
    def __init__(self):
        super(Body, self).__init__()

        self.x_vel = 0.0
        self.y_vel = 0.0

        self.l_blocked = False
        self.r_blocked = False
        self.t_blocked = False
        self.b_blocked = False

        self.fall_through = False


class PlayerBody(Body):
    def __init__(self, player):
        self.player = player

        super(PlayerBody, self).__init__()

        self.size = self.player.size

        self.x_dir = 0
        self.y_dir = 0
        self.facing = "left"

        self.accel = 0.5
        self.decel = 0.3
        self.run_vel = 5
        self.dash_vel = 8
        self.dash_timer = 0
        self.air_dash = False

        self.gravity = 0.6
        self.termvel = 14.0

        self.jump_start = -13.2
        self.jump_cut = -5

        self.dash_sound = self.player.game.core.get_sound("player_dash.ogg")
        self.jump_sound = self.player.game.core.get_sound("player_jump.ogg")

    def update_self(self, ticks):
        super(PlayerBody, self).update_self(ticks)

        if self.b_blocked:
            self.air_dash = 0

        if self.player.game.controller.just_pressed("jump"):
            if self.b_blocked or (self.dash_timer > 0 and not self.air_dash):
                self.dash_timer = 0
                self.y_vel = self.jump_start
                self.jump_sound.play()
        elif self.player.game.controller.just_released("jump"):
            if self.y_vel < self.jump_cut:
                self.y_vel = self.jump_cut

        if self.player.game.controller.pressed("fall"):
            self.fall_through = True
        else:
            self.fall_through = False

        if self.player.game.controller.just_pressed("dash") and self.dash_timer <= 0:
            if self.b_blocked:
                self.dash_timer = 30
                self.dash_sound.play()
            elif self.air_dash < 1:
                self.dash_timer = 30
                self.air_dash += 1
                self.dash_sound.play()

        if self.dash_timer <= 0:
            if self.player.game.controller.pressed("run_left") and ScG.controller.released("run_right"):
                self.x_dir = -1
                self.facing = "left"
            elif self.player.game.controller.pressed("run_right") and ScG.controller.released("run_left"):
                self.x_dir = 1
                self.facing = "right"
            else:
                self.x_dir = 0

            if self.x_vel == 0 and self.x_dir == 0:
                pass
            elif self.x_dir > 0:
                self.x_vel = min(self.x_vel + self.accel, +self.run_vel)
            elif self.x_dir < 0:
                self.x_vel = max(self.x_vel - self.accel, -self.run_vel)
            elif self.x_vel > 0:
                self.x_vel = max(self.x_vel - self.decel, 0)
            elif self.x_vel < 0:
                self.x_vel = min(self.x_vel + self.decel, 0)

            self.y_vel = min(self.y_vel + self.gravity, self.termvel)
        else:
            self.dash_timer -= 1
            self.y_vel = 0
            if self.facing == "right":
                if self.r_blocked:
                    self.x_vel = 0
                    self.dash_timer = 0
                elif self.player.game.controller.pressed("run_left"):
                    self.x_vel = min(self.x_vel, +self.run_vel)
                    self.dash_timer = 0
                else:
                    self.x_vel = self.dash_vel
            elif self.facing == "left":
                if self.l_blocked:
                    self.x_vel = 0
                    self.dash_timer = 0
                elif self.player.game.controller.pressed("run_right"):
                    self.x_vel = max(self.x_vel, -self.run_vel)
                    self.dash_timer = 0
                else:
                    self.x_vel = -self.dash_vel
