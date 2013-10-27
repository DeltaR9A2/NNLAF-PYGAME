import math


class Rect(object):
    """This class represents a rectangular area defined by the x,y coordinate
    of its top-left corner plus its width and height.

    Various accessors and methods are available to manipulate the ``Rect``;
    it's important to note that most of these will *move* the ``Rect`` rather
    than resizing it. Only a few will change the size:

    *   .w
    *   .h
    *   .size
    *   .grow
    *   .union
    *   .match_to"""
    def __init__(self, x=0, y=0, w=1, h=1):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __len__(self):
        return 4

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.w
        elif key == 3:
            return self.h
        else:
            raise KeyError

    def __setitem__(self, key, val):
        if key == 0:
            self.x = val
        elif key == 1:
            self.y = val
        elif key == 2:
            self.w = val
        elif key == 3:
            self.h = val
        else:
            raise KeyError

    def __delitem__(self, key):
        raise Exception("Cannot delete the measurements of an ScRect")

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.w
        yield self.h

    @property
    def l_edge(self):
        """The x position of the left edge, equal to ``self.x``."""
        return self.x

    @l_edge.setter
    def l_edge(self, n):
        self.x = n

    @property
    def r_edge(self):
        """The x position of the right edge, equal to ``self.x + self.w``."""
        return self.x + self.w

    @r_edge.setter
    def r_edge(self, n):
        self.x = n - self.w

    @property
    def t_edge(self):
        """The y position of the top edge, equal to ``self.y``."""
        return self.y

    @t_edge.setter
    def t_edge(self, n):
        self.y = n

    @property
    def b_edge(self):
        """The y position of the bottom edge, equal to ``self.y + self.h``."""
        return self.y + self.h

    @b_edge.setter
    def b_edge(self, n):
        self.y = n - self.h

    @property
    def mid_x(self):
        """The x position of the rect's center, equal to ``self.x + (self.w / 2.0)``."""
        return self.x + (self.w / 2.0)

    @mid_x.setter
    def mid_x(self, n):
        self.x = n - (self.w / 2.0)

    @property
    def mid_y(self):
        """The y position of the rect's center, equal to ``self.y + (self.h / 2.0)``."""
        return self.y + (self.h / 2.0)

    @mid_y.setter
    def mid_y(self, n):
        self.y = n - (self.h / 2.0)

    @property
    def center(self):
        """A tuple containing the x,y position of the rect's center."""
        return self.mid_x, self.mid_y

    @center.setter
    def center(self, pair):
        self.mid_x, self.mid_y = pair

    @property
    def size(self):
        """A tuple containing the width and height of the rect."""
        return self.w, self.h

    @size.setter
    def size(self, pair):
        self.w, self.h = pair

    def grow(self, dw, dh):
        """Increases ``self.w`` by ``dw`` and ``self.h`` by ``dh`` without changing ``self.center``.
        Negative numbers work too if you need to shrink the rect."""
        c = self.center
        self.w += dw
        self.h += dh
        self.center = c

    def move_to(self, other):
        """Moves ``self.center`` to ``other.center``."""
        self.center = other.center

    def range_to(self, other):
        """Calculates the distance between ``self.center`` and ``other.center``."""
        return math.sqrt(pow(other.mid_x - self.mid_x, 2) + pow(other.mid_y - self.mid_y, 2))

    def match_to(self, other):
        """Sets the dimensions of ``self`` exactly equal to ``other``."""
        self.x = other.x
        self.y = other.y
        self.w = other.w
        self.h = other.h

    def angle_to(self, other):
        """Returns the angle from ``self.center`` to ``other.center``, as calculated
        by ``math.atan2`` from the standard library. This angle is in radians."""
        dx = other.mid_x - self.mid_x
        dy = other.mid_y - self.mid_y
        return math.atan2(dy, dx)

    def move_at_angle(self, angle, dist):
        """Moves ``self.center`` at ``angle``; ``dist`` is how far to move. ``angle``
        should be specified in radians, like the angles returned by ``self.angle_to``."""
        self.mid_x += dist * math.cos(angle)
        self.mid_y += dist * math.sin(angle)

    def move_toward(self, other, dist):
        """Moves the center of ``self`` toward the center of ``other`` to a maximum
        distance of ``dist``. If the center of ``other`` is closer than ``dist``,
        matches the centers exactly."""
        if self.range_to(other) > dist:
            self.move_at_angle(self.angle_to(other), dist)
        else:
            self.move_to(other)

    def overlap(self, other):
        """Returns ``True`` if any part of ``self`` overlaps with ``other``."""
        if(
                self.r_edge <= other.l_edge or self.l_edge >= other.r_edge or
                self.b_edge <= other.t_edge or self.t_edge >= other.b_edge
        ):
            return False
        else:
            return True

    def union(self, other):
        """Expands ``self`` exactly enough to cover the entire area of ``other``."""
        new_l = min(self.l_edge, other.l_edge)
        new_t = min(self.t_edge, other.t_edge)
        new_r = max(self.r_edge, other.r_edge)
        new_b = max(self.b_edge, other.b_edge)
        self.x = new_l
        self.y = new_t
        self.w = new_r - new_l
        self.h = new_b - new_t

    def copy(self):
        """Returns a new ``Rect`` with the same size and position as ``self``."""
        return Rect(*self)

    def internal_coords(self, step=1):
        """Returns a list of coordinate pairs (tuples) inside this rectangle;
        starts at ``(self.x, self.y)`` and proceeds left-to-right/top-to-bottom,
        incrementing both x and y by ``step``.

        This is useful for iterating over every pixel or tile coordinate in
        a rectangular region.

        Future versions may return an iterator instead of a list."""
        coord_list = []

        cx = self.x
        cy = self.y

        while cy < self.y + self.h:
            while cx < self.x + self.w:
                coord_list.append((cx, cy))
                cx += step
            cx = self.x
            cy += step

        return coord_list
