import pygame


class Controller:
    """This class encapsulates the state of a virtual controller, providing
    consistent naming and events to the rest of the game. The state of the
    controller is based on keyboard and/or joystick input, but hides these
    details so that game logic does not need to understand different devices
    or mappings."""
    def __init__(self):
        """Creates a new Controller instance with default bindings. Only one
        instance should be active at a time. Future versions will allow for
        re-mapping controls and may also allow multiple controller instances."""
        if pygame.joystick.get_count() > 0:
            pygame.joystick.Joystick(0).init()

        self.state = {
            "A": False,
            "B": False,
            "X": False,
            "Y": False,

            "U": False,
            "D": False,
            "L": False,
            "R": False,

            "LB": False,
            "RB": False,

            "BACK": False,
            "START": False,
        }

        self.prev = self.state.copy()

        self.bindings = [
            {
                pygame.K_z: "A",
                pygame.K_x: "B",
                pygame.K_c: "X",
                pygame.K_v: "Y",

                pygame.K_UP: "U",
                pygame.K_DOWN: "D",
                pygame.K_LEFT: "L",
                pygame.K_RIGHT: "R",

                pygame.K_a: "LB",
                pygame.K_s: "RB",

                pygame.K_ESCAPE: "BACK",
                pygame.K_RETURN: "START",
            }, {
                ("JB", 1): "A",
                ("JB", 2): "B",
                ("JB", 0): "X",
                ("JB", 3): "Y",

                ("JHY",  1): "U",
                ("JHY", -1): "D",
                ("JHX", -1): "L",
                ("JHX",  1): "R",

                ("JB", 4): "LB",
                ("JB", 5): "RB",

                ("JB", 8): "BACK",
                ("JB", 9): "START",
            },
        ]

    def update(self):
        """Call this once per frame; it reads input from pygame's event system
        and translates that data into virtual controller state."""
        self.prev.update(self.state)

        for event in pygame.event.get():
            for bind_set in self.bindings:
                if event.type == pygame.KEYDOWN:
                    button = bind_set.get(event.key)
                    if button is not None:
                        self.state[button] = True
                elif event.type == pygame.KEYUP:
                    button = bind_set.get(event.key)
                    if button is not None:
                        self.state[button] = False
                elif event.type == pygame.JOYBUTTONDOWN:
                    key = ("JB", event.button)
                    button = bind_set.get(key)
                    if button is not None:
                        self.state[button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    key = ("JB", event.button)
                    button = bind_set.get(key)
                    if button is not None:
                        self.state[button] = False
                elif event.type == pygame.JOYHATMOTION:
                    jhx, jhy = event.value
                    for axis, val in (("JHX", jhx), ("JHY", jhy)):
                        for n in (-1, 1):
                            button = bind_set.get((axis, n))
                            if button is not None:
                                if n == val:
                                    self.state[button] = True
                                else:
                                    self.state[button] = False

    def pressed(self, button):
        """Returns ``True`` if ``button`` is currently pressed."""
        return self.state[button]

    def just_pressed(self, button):
        """Returns ``True`` if ``button`` is currently pressed, but was not pressed last frame."""
        return self.state[button] and not self.prev[button]

    def released(self, button):
        """Returns ``True`` if ``button`` is currently released (not being pressed)."""
        return not self.state[button]

    def just_released(self, button):
        """Returns ``True`` if ``button`` is currently released, but was not released last frame."""
        return self.prev[button] and not self.state[button]
