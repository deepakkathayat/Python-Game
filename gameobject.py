"""
gameobject.py - implements Gameobject class.
"""
import curses

#from logger import Logger
#log = Logger()
#log.on()

class Gameobject(object):
    """
    Base class for most of the game elements in the game and incudes methods for being updated and drawn.
    """
    # The following attributes are ones all objects need to have
    #_x = 0                  # the current x co-ord of the object
    #_y = 0                  # the current y co-ord of the object
    _move_rate = 150        # the interval (in ms) that the item should move
    _shape = {}             # display data for the object (think "pixels"!)
    _explosion_frames = []  # set of 'frames' used to animate an explosion
    _explosion_start = -1   # time at which explosion starts
    def __init__(self, gameobject):
        """Set the initial state of the object, e.g. position."""
        self._gameobject = gameobject
        self._to_be_deleted = False
        self._state = "normal"  # can be 'normal', 'exploding', 'gone'
    
    def draw(self, stdscr):
        """
        Draws the object at its current location.

        The colour and other attributes an object is drawn in is determined
        by the value returned by _drawing_attributes(); derived classes
        can overide this.
        The routine is also careful to make sure nothing is drawn off screen.
        """
        if self._state == "normal":
            self._draw_normal_object(stdscr)
        elif self._state == "exploding":
            self._draw_exploding_object(stdscr)
        else:
            assert(0)

    def _draw_normal_object(self, stdscr):
        """Implements drawing for an object in its normal state."""
        attribs = self._drawing_attribs()
	for key in self._shape:
        	self._draw_object_line(stdscr, attribs, key, self._shape[key])
    
    def _draw_exploding_object(self, stdscr):
        """Implements drawing for an object in an exploding state."""
        assert(len(self._explosion_frames) > 0)

        attribs = self._drawing_attribs()        
        # loop through each explosion frame looking for the correct one by time
        for frame in self._explosion_frames:
            explosion_ends = frame[0] + self._explosion_start
            if self._gameobject.tickcount() < explosion_ends:
                for key in frame[1]:
                    self._draw_object_line(stdscr, attribs, key, frame[1][key])
                break       # don't look at the next one!

    def _draw_object_line(self, stdscr, attribs, key, line):
        """Draws one line within an object."""
        ypos = self._y + key
	if ypos >= 0 and ypos < self._gameobject.screen_height:
		xpos = self._x - len(line)/2
		if xpos>=0:
    			stdscr.addstr(ypos, xpos, line, attribs)
		
    def _drawing_attribs(self):
        """
        Curses attributes to be used when drawing.

        Many derived objects will override this; the default is white.
        """
        return curses.color_pair(1)

    def tick(self, _tickcount):
        """Used to update the object because of passing time."""
        pass

    def is_alive(self):
        """Used to test if the object should be kept or should be deleted."""
        return True

    def handle_possible_hit(self, _xpos, _ypos, _damage):
        """
        Checks if the object has been hit.

        Derived objects should (as appropriate) check if they include
        the specified x, y coordinates and are therefore hit. If they
        are they should update themselves according to the damage value.
        The result of the update could be damaged or destroyed.
        """
        return False    # derived class may need to implement this

    def play_width(self):
        """Convenience/abstraction method to return the width of the
        play area."""
        return self._gameobject.screen_width

    def explosion_duration(self):
        """
        Returns the gametime (in milliseconds) at which the explosion
        animation for the object ends.
        """
        if len(self._explosion_frames) == 0:
            return 0
        else:
            lastframe = self._explosion_frames[len(self._explosion_frames) - 1]
            return lastframe[0]


