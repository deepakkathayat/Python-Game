"""
asteroid.py - class to implement asteroids.

There are two variations of asteroids, small and large. As well as the obvious
size difference, large ones take more hits and and are worth more points.
Other than that they are identical.
"""

import curses
import random
from gameobject import Gameobject

class Asteroid(Gameobject):
    """
    Base class for asteroids. Derived classes will need to provide:
       - _damage_left
       - _SCORE_VALUE
       - _shape
    """
    _show_hit_until_tick = 0    # when (only) damaged show highl'd until this
    _show_explosion_until = 0
    _SHOW_HIT_TIME = 150        # how many milliseconds highlighted when hit
    #_SCORE_VALUE = 0            # will be overridden by derived class
    _damage_left = 2            # will be overridden by derived class

    def __init__(self, gameobject):
        """Set the initial position of the asteroid."""
        super(Asteroid, self).__init__(gameobject)
        self._x = random.randrange(gameobject.screen_width - 20) + 10
        self._y = 0             # starts at the top

    def _drawing_attribs(self):
        """Curses attributes used by base class drawing method."""
        attribs = curses.color_pair(1)
        if self._gameobject.tickcount() < self._show_hit_until_tick:
            attribs += curses.A_BOLD
        return attribs

    def tick(self, tickcount):
        """Used to update the object because of passing time."""
        # check if we're exploding
        if self._state == 'exploding':
            # fine, but maybe it is time we disappeared
            if self._show_explosion_until <= tickcount:
                self._to_be_deleted = True
                self._state = 'gone'

            # if exploding we don't want to do anything else here
            return

        if tickcount % self._move_rate == 0:
            self._y += 1

        # check if we've moved off screen. if so mark ourselves for deletion
        if self._y >= self._gameobject.screen_height:
            self._to_be_deleted = True
            self._state = 'gone'
        else:
            # Now check if we've hit anything!
            if self._gameobject.check_for_hit(self, self._x, self._y, 3):
                # Asteroid hit something so it is destroyed too
                self._to_be_deleted = True
                self._state = 'gone'
                #self._gameobject.add_score(self._SCORE_VALUE)

    def is_alive(self):
        """Used to test if the object should be kept or should be deleted."""
        if self._state == 'normal':
            assert(self._to_be_deleted == False)
        return not self._to_be_deleted

    def handle_possible_hit(self, x, y, damage):
        """Check if we've been hit by an object (e.g. bullet)"""
        if self._state != 'normal':
            return False
            
        if (x >= self._x-2 and x <= self._x+1) and \
            (y >= self._y-1 and y <= self._y+1):
            # Asteroid has been hit: check if destroyed
            self._damage_left -= damage
            if self._damage_left <= 0:
                # destroyed! show explosion for a little while
                self._state = 'exploding'
                self._explosion_start = self._gameobject.tickcount()
                self._show_explosion_until = \
                    self.explosion_duration() + self._gameobject.tickcount()
                #self._gameobject.add_score(self._SCORE_VALUE)
            else:
                # only damaged, show highlighted for a while
                self._show_hit_until_tick = \
                    self._gameobject.tickcount() + self._SHOW_HIT_TIME
            return True
        else:
            return False

class SmallAsteroid(Asteroid):
    """
    Small version of asteroid.
    """
    _damage_left = 2
    #_SCORE_VALUE = 50
    _normal_shape = {-1:".##.", 0:"####", 1:".##."}
    _explosion_frames = [
        (200, {-1:" ** ", 0:"****", 1:" ** "}),
        (600, {-1:" '' ", 0:"-  -", 1:" .. "}),
        ]

    def __init__(self, asteroid):
        """Set the initial position of the asteroid."""
        super(SmallAsteroid, self).__init__(asteroid)
        self._shape = self._normal_shape


class LargeAsteroid(Asteroid):
    """
    Large version of asteroid.
    """
    _damage_left = 4
    _SCORE_VALUE = 100
    _normal_shape = {
              -2:" .###. ",
              -1:"/#####\\",
               0:"#######",
               1:"\\#####/",
               2:" '###' "}
    _explosion_frames = [
        (200, {-2:" .***. ",
               -1:" ***** ",
                0:".*****.",
                1:" ***** ",
                2:" '***' "}),
        (500, {-2:" .   . ",
               -1:"  '..  ",
                0:". ***' ",
                1:" .'.'  ",
                2:" '   ' "}),
        (800, {-2:" .   . ",
               -1:"       ",
                0:".  *  .",
                1:"       ",
                2:" '   ' "}),
        ]

    def __init__(self, asteroid):
        """Set the initial position of the asteroid."""
        super(LargeAsteroid, self).__init__(asteroid)
        self._shape = self._normal_shape

