import pygame

CHAR_ORDER = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""


class Font:
    """This class encapsulates a variable-width bitmap font.

    The font is loaded from a ``pygame.Surface``; characters are delimited
    by specially colored pixels in the top row. The delimiter color is taken
    from the top-left pixel in the surface; Each pixel in the top row matching
    that color indicates the break between two characters."""
    def __init__(self, surface):
        """Creates a new ``Font`` from ``surface``."""
        self._height = surface.get_height()

        mark_color = surface.get_at((0, 0))

        marks = []
        for x in xrange(surface.get_width()):
            color = surface.get_at((x, 0))
            if color == mark_color:
                marks.append(x)
        marks.append(surface.get_width())

        char_surfaces = []
        for i in xrange(len(marks) - 1):
            rect = (
                marks[i] + 1,
                0,
                (marks[i + 1] - marks[i]) - 1,
                self._height
            )

            char_surfaces.append(surface.subsurface(rect))

        self.char_dict = {}
        for c, surf in zip(CHAR_ORDER, char_surfaces):
            self.char_dict[c] = surf

    @property
    def height(self):
        """The height of the font and, therefore, the height of any single line of text
        rendered in this font."""
        return self._height

    def line_width(self, text):
        """Returns the width in pixels that would be occupied by ``text`` if rendered as a single line."""
        total = 0
        for c in text:
            surf = self.char_dict.get(c)
            if surf is not None:
                total += surf.get_width()

        return total

    def render(self, text, surface, pos):
        """This method renders ``text`` onto ``surface`` with the top-left corner of the first
        character at ``pos``. This method is best used for text that changes often; direct rendering
        avoids the overhead of creating/destroying a surface every time the text changes."""
        cur_x, cur_y = pos
        for c in text:
            surf = self.char_dict.get(c)
            if surf is not None:
                surface.blit(surf, (cur_x, cur_y))
                cur_x += surf.get_width()

    def render_line(self, text):
        """Returns a ``pygame.Surface`` with ``text`` rendered to it as a single line. This surface
        is exactly large enough to contain the rendered text. This method is best used for text that
        will be saved and rendered many times; creating the surface allows the text to be re-used
        many times without re-calculating and blitting each character."""
        width = self.line_width(text)
        surface = pygame.Surface((width, self._height), flags=pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        self.render(text, surface, (0, 0))

        return surface

    def render_block(self, text, width):
        """Returns a ``pygame.Surface`` with ``text`` rendered to it, broken into multiple lines
         so that the rendered text is not wider than ``width``. The surface will be ``width`` pixels
         wide, and its height will be a multiple of ``self.height``."""
        lines = []
        line_start = 0
        line_stop = 0
        while line_start < len(text):
            line_width = 0

            while line_width < width:
                line_stop += 1
                line_width = self.line_width(text[line_start:line_stop])

                if line_stop > len(text):
                    break

            line_stop -= 1
            original_stop = line_stop

            while text[line_stop - 1] != " " and line_stop != len(text):
                line_stop -= 1
                if line_stop <= line_start:
                    line_stop = original_stop
                    break

            lines.append(text[line_start:line_stop])
            line_start = line_stop

        surface = pygame.Surface((width, self._height * len(lines)), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        for i, line in enumerate(lines):
            self.render(line, surface, (0, self._height * i))

        return surface