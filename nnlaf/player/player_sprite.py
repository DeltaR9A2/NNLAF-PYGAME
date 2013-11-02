import pygame
from rect import Rect


class Animation:
    def __init__(self, frames, rate=6.0):
        self.frames = frames
        self.rate = rate

    def frame_at_ticks(self, ticks):
        return self.frames[int(((ticks // self.rate) % len(self.frames)))]


class Sprite(Rect):
    def __init__(self, frames):
        super(Sprite, self).__init__()

        self.frames = frames

        self.size = self.frames[0].get_size()

        self.ticks = 0
        self.animations = {}
        self.active_animation = None
        self.active_frame = None

        self.flashing = 0

        self.add_animation("default", 0)
        self.select_animation("default")

    def add_animation(self, name, start, length=1, rate=6):
        self.animations[name] = Animation(self.frames[start:start + length], rate)

    def select_animation(self, name):
        if self.active_animation is not self.animations[name]:
            self.ticks = 0
            self.active_animation = self.animations[name]
            self.active_frame = self.active_animation.frame_at_ticks(self.ticks)

    def update(self, ticks):
        self.ticks += 1
        self.active_frame = self.active_animation.frame_at_ticks(self.ticks)
        if self.flashing > 0:
            self.flashing -= 1

    def draw_self(self, camera):
        if self.flashing == 0 or (self.flashing % 2) == 0:
            camera.surface.blit(self.active_frame, (
                self.x + ((self.w - self.active_frame.get_width()) // 2) - camera.sx,
                self.y + ((self.h - self.active_frame.get_height()) // 2) - camera.sy,
            ))


class PlayerSprite(Sprite):
    def __init__(self, player):
        self.player = player

        frames = list(self.player.game.core.get_tiles("player_anarchy_female.png", 8, 4))
        for frame in frames[:]:
            flip = pygame.transform.flip(frame, True, False)
            frames.append(flip)

        Sprite.__init__(self, frames)

        self.size = self.player.size

        self.add_animation("stand_r",  0, 1)
        self.add_animation("run_r",    1, 6)
        self.add_animation("skid_r",   7, 1)
        self.add_animation("dash_r",   8, 1)
        self.add_animation("rise_r",  16, 1)
        self.add_animation("float_r", 17, 1)
        self.add_animation("fall_r",  18, 1)
        self.add_animation("stand_l", 32, 1)
        self.add_animation("run_l",   33, 6)
        self.add_animation("skid_l",  39, 1)
        self.add_animation("dash_l",  40, 1)
        self.add_animation("rise_l",  48, 1)
        self.add_animation("float_l", 49, 1)
        self.add_animation("fall_l",  50, 1)

        self.update_animation()

    def update(self, ticks):
        Sprite.update(self, ticks)
        self.move_to(self.player.body)
        self.update_animation()

    def update_animation(self):
        if self.player.body.dash_timer > 0:
            if self.player.body.facing == "right":
                self.select_animation("dash_r")
            else:
                self.select_animation("dash_l")
        elif self.player.body.b_blocked:
            if self.player.body.x_vel > 0.5:
                if self.player.body.x_dir > 0:
                    self.select_animation("run_r")
                else:
                    self.select_animation("skid_r")
            elif self.player.body.x_vel < -0.5:
                if self.player.body.x_dir < 0:
                    self.select_animation("run_l")
                else:
                    self.select_animation("skid_l")
            else:
                if self.player.body.facing == "right":
                    self.select_animation("stand_r")
                else:
                    self.select_animation("stand_l")
        else:
            if self.player.body.facing == "right":
                if self.player.body.y_vel < -2.0:
                    self.select_animation("rise_r")
                elif self.player.body.y_vel > 2.0:
                    self.select_animation("fall_r")
                else:
                    self.select_animation("float_r")
            else:
                if self.player.body.y_vel < -2.0:
                    self.select_animation("rise_l")
                elif self.player.body.y_vel > 2.0:
                    self.select_animation("fall_l")
                else:
                    self.select_animation("float_l")
