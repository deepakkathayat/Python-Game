"""
robot.py - Classes and other code to implement the player robot for Robot Bomb Defuser.
"""

import curses
import random
from gameobject import Gameobject

class Bullet(Gameobject):
    """Represents a bullet from the player's robot."""
    _shape = {0:"!"}
   
    def __init__(self, x, y, gameobject):
        """Set the initial position of the bullet."""
        super(Bullet, self).__init__(gameobject)
        self._x = x
        self._y = y
        self._move_rate = 50 # move 20 times per second

    def _drawing_attribs(self):
        return curses.color_pair(1) + curses.A_BOLD

    def tick(self, tickcount):
        """ Tells the bullet that the game has moved on in time. """
        if tickcount % self._move_rate == 0:
            # It's time for the bullet to move upward
            self._y -= 1
        # Check if the bullet has moved off the playfield
        if self._y < 0:
            self._to_be_deleted = True
        else:
            # Now check if we've hit anything!
            if self._gameobject.check_for_hit(self, self._x, self._y, 1):
                # Bullet hit something so it is destroyed too
                self._to_be_deleted = True

    def is_alive(self):
        return not self._to_be_deleted


class Robot(Gameobject):
    """
    Represents the player's robot.

    Handled in many ways like any other game object in that it has a
    draw method, knows its co-ordinates etc. However it is different
    in that it takes keyboard input (done by Game knowing about this
    object directly, as well as through its game object list) rather
    than being driven by tick().
    Also generates bullets
    """
    _shape = {}
    _shape1 = {0:" ~|~ ", 1:"/|=|/", 2:"() ()"}
    _shape2 = {0:" ~|~ ", 1:"\|=|\\", 2:"() ()"}
    def __init__(self, gameobject):
        """Set the initial position of the robot."""
        super(Robot, self).__init__(gameobject)
        self._shield_strength = 10
    	self.walk=0    
        self.play_area_size = (90, 30) 
        self.info_area_size = (25, 30) 
        self.info_area_topleft = (90, 0)
	self.screen_width = self.play_area_size[0]
	self.screen_height = self.play_area_size[1]
	self._x = 3
        self._y = 3   # robot starts from the top-left screen position
	self.prev = curses.KEY_RIGHT

    def _drawing_attribs(self):
        return curses.color_pair(3) + curses.A_BOLD

    def handle_key(self, key_char=None):
        """Takes a key press and if it means a player robot control
        from the user then it updates the robot appropriately."""
           
	if key_char == curses.KEY_LEFT:
            self._x -= 1
            self.prev = key_char
	elif key_char == curses.KEY_RIGHT:
            self._x += 1
            self.prev = key_char
	elif key_char == curses.KEY_UP:
	    self._y -= 1
            self.prev = key_char
	elif key_char == curses.KEY_DOWN:
	    self._y += 1
            self.prev = key_char
	elif key_char ==ord('z'):
            self._do_shoot()
	else:
	    if self.prev == curses.KEY_LEFT:
            	self._x -= 1
            	#prev = key_char
	    elif self.prev == curses.KEY_RIGHT:
            	self._x += 1
            	#prev = key_char
	    elif self.prev == curses.KEY_UP:
	    	self._y -= 1
            	#prev = key_char
	    elif self.prev == curses.KEY_DOWN:
	    	self._y += 1
            	#prev = key_char
	    
		
    def _do_shoot(self):
        """
        User is trying to fire.

        Currently this just causes a new bullet to be created but
        in the future it will consider the robot's current equipment,
        gun status etc.
        """
        new_bullet = Bullet(self._x, self._y, self._gameobject)
        self._gameobject.add_object(new_bullet)

    def handle_possible_hit(self, x, y, damage):
        """Check if we've been hit by an object (e.g. alien)"""
        if (x >= self._x-1 and x <= self._x+1) and \
            (y >= self._y and y <= self._y+2):
            # we've been hit!
            # reduce shields, check if destroyed
            self._shield_strength -= damage
            if self._shield_strength <= 0:
                self._to_be_deleted = True
                self._shield_strength = 0   # in case we went -ve
            else:
                # not destroyed but damaged so make it obvious
                curses.flash()
            return True
        else:
            return False

    def is_alive(self):
        """Has the robot been destroyed?"""
        return not self._to_be_deleted

    def shield(self):
        return self._shield_strength


class Autopilot(Robot,Gameobject):
    """
    Robot controlled by the computer.

    Provides a means of doing an automated system test, although in the
    future this could also be used to provide a demo mode.
    Derived from Robot object but controls the robot from the tick() method
    rather than keys.
    """
    _shape1 = {0:"*^*", 1:"/|=|\\", 2:"/|I|\\"}
    _shape2 = {0:"*^*", 1:"\|=|/", 2:"/|I|\\"}

    _lastmove = None        # remembers last left/right/neither decision
    def __init__(self,gameobject):
        super(Autopilot, self).__init__(gameobject)
        self.play_area_size = (90, 30) 
        self.info_area_size = (25, 30) 
        self.info_area_topleft = (90, 0)
	self.screen_width = self.play_area_size[0]
	self.screen_height = self.play_area_size[1]+5
	self._x = 45
        self._y = 27 # robot starts from the top-left screen position
    	self._state="normal"
    
    def handle_key(self, key_char):
        """Overide this to do nothing as the computer is in control :-)"""
        pass

    def tick(self, tickcount):
        # decide whether to move left, right, or neither.
        self._decide_leftright()

        # decide whether to fire or not
        if self._lastmove == None:
            if random.randrange(10) == 0:
                self._do_shoot()

    def _decide_leftright(self):
        if self._lastmove == None:
            if random.randrange(6) > 0:
                self._lastmove = None   # 5/6 times stay still
            else:
                moveval = random.randrange(self.play_width())
                if moveval < self._x:
                    self._moveleft()
                else:
                    self._moveright()
        elif self._lastmove == 'l':
            if random.randrange(4) < 3:
                self._moveleft()
            else:
                self._lastmove = None
        else: # self._lastmove == 'r'
            if random.randrange(4) < 3:
                self._moveright()
            else:
                self._lastmove = None

    def _moveleft(self):
        if self._x - 2 > 0:
            self._x -= 1
            self._lastmove = 'l'

    def _moveright(self):
        if self._x + 2 < self.play_width() - 1:
            self._x += 1
            self._lastmove = 'r'
