#!/usr/bin/env python2

"""This 'module' is the main entry point for the game. If this file is loaded
directly by the python interpreter, it will call the ``main()`` function."""

import os
import sys
import pygame

game_path = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
data_path = os.path.join(game_path, 'data')
save_path = os.path.join(game_path, 'save')


def run(that, fps=60.0, check=lambda x: x.running):
    """Run ``that`` in a timed loop, calling ``that.step()`` and/or
    ``that.fast_step()`` at ``fps`` times per second until ``check(that)``
    returns ``False``.
    
    The default check function simply returns the value of ``that.running``
    so ``that`` can terminate itself internally by setting ``self.running``
    to ``False``.
    
    If the loop is running on time, ``that.step()`` is called. If the loop is
    running slowly, ``that.fast_step()`` is called instead; ``fast_step()`` is
    assumed to take less time than ``step()`` so that the loop can catch up.
    
    Returns ``that`` for slick one-liners."""

    interval = 1000.0 / fps

    curr_tick = pygame.time.get_ticks()
    tick_accum = 0

    while check(that):
        prev_tick = curr_tick
        curr_tick = pygame.time.get_ticks()
        tick_delta = curr_tick - prev_tick
        tick_accum += tick_delta

        if tick_accum > interval:
            tick_accum -= interval

            if tick_accum < interval:
                that.step()
            else:
                that.fast_step()

        pygame.display.flip()
        pygame.time.wait(1)

        sys.stdout.flush()

    return that


def main():
    """Main entry point for the game; initializes pygame, creates the
    :class:`Core <core.Core>`, and then starts the :class:`Game <game.Game>`\ ."""
    
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.init()
    pygame.display.set_mode((640, 480))

    from core import Core
    core = run(Core(data_path, save_path))

    if not core.ready:
        sys.exit("Core failed to load; launch aborted.")

    from game import Game
    game = run(Game(core))

    print game.running

if __name__ == "__main__":
    main()
