"""
objects.py
"""

import random
import curses
from gameobject import Gameobject
from random import randint,seed
from time import sleep
COLOR= True
curses.initscr()
curses.start_color()

class Mine(Gameobject):
    _shape = {0:"X"}
    
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

    _show_hit_until_tick = 0    # when (only) damaged show highl'd until this
    _show_explosion_until = 0
    _SHOW_HIT_TIME = 150        # how many milliseconds highlighted when hit
    _SCORE_VALUE = 0            # will be overridden by derived class
    _damage_left = 0            # will be overridden by derived class
    _explosion_start = -1
    def __init__(self,blacklist,gameobject):
                super(Mine, self).__init__(gameobject)
		self.blacklist = blacklist
#		self.screen = screen
		self.play_area_size=(85,30)
		self.screen_height=self.play_area_size[1]
		self.screen_width=self.play_area_size[0]
		self.icolor=-1;
                self._state = "normal"

		while True:
			self.pos = tuple([randint(5,self.screen_height-2), \
					randint(5,self.screen_width-2)])
			if self.pos not in self.blacklist: break
		self._x = self.pos[1]
		self._y = self.pos[0]

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

    def _drawing_attribs(self):
		"""Curses attributes to be used when drawing.Many derived objects will override this; the default is white.
	"""     
		self.icolor=self.icolor+1
		return curses.color_pair(self.icolor%5)+curses.A_BOLD


class Bomb(object):
    _shape = {0:" _ ",1:"//B\\\\",2:"\\\_//"}
    #_damage_left = 4
    #    _SCORE_VALUE = 100
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

    _show_hit_until_tick = 0    # when (only) damaged show highl'd until this
    _show_explosion_until = 0
    _SHOW_HIT_TIME = 150        # how many milliseconds highlighted when hit
    _SCORE_VALUE = 0            # will be overridden by derived class
    _damage_left = 0            # will be overridden by derived class
    _explosion_start = -1
    
    #super(Bomb, self).__init__(Gameobject)
        #self._shape = self._normal_shape
    def __init__(self,screen,blacklist):
		self.blacklist = blacklist
		self.screen = screen
		self.play_area_size=(85,24)
		self.screen_height=self.play_area_size[1]
		self.screen_width=self.play_area_size[0]
		self.icolor=-1;
		self._state = "normal"

		while True:
			self.pos = tuple([randint(5,self.screen_height-4), \
					randint(5,self.screen_width-4)])
			if self.pos not in self.blacklist: break
	
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

    def _drawing_attribs(self):
		"""Curses attributes to be used when drawing.Many derived objects will override this; the default is white.
	"""     
		self.icolor=self.icolor+1
		return curses.color_pair(self.icolor%5)+curses.A_BOLD


    def draw(self, stdscr,tickcount):
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
            self._draw_exploding_object(stdscr,tickcount)
        else:
            assert(0)

    def _draw_normal_object(self,screen):
	   """Implements drawing for an object in its normal state."""
	   attribs = self._drawing_attribs()
	   for key in self._shape:
		   self._draw_object_line(attribs, key, self._shape[key],self.pos[0],self.pos[1])


    def _draw_exploding_object(self, stdscr,tickcount):
        """Implements drawing for an object in an exploding state."""
        assert(len(self._explosion_frames) > 0)

        attribs = self._drawing_attribs()        
        # loop through each explosion frame looking for the correct one by time
        for frame in self._explosion_frames:
            explosion_ends = frame[0] + self._explosion_start
            #if tickcount < explosion_ends:
            for key in frame[1]:
               	self._draw_object_exp_line(stdscr, attribs, key, frame[1][key])
	    break       # don't look at the next one!
	

    def _draw_object_line(self, attribs, key, line,pos_y,pos_x):
        	"""Draws one line within an object."""
	        ypos = pos_y + key
		if ypos >= 0 and ypos < self.screen_height:
		            xpos = pos_x - len(line)/2
		            self.screen.addstr(ypos, xpos, line, attribs)

    def _draw_object_exp_line(self, stdscr, attribs, key, line):
        """Draws one line within an object."""
        ypos = self.pos[0] + key
	#if ypos >= 0 and ypos < self.screen_height:
	xpos = self.pos[1] - len(line)/2
    	stdscr.addstr(ypos, xpos, line, attribs)

class Code(Gameobject):
	#global chars_colors
	_shape = {0:" _ " , 1:"|C|"}

	def __init__(self, screen, blacklist):
		self.codes=[]
		self.screen = screen
		self.play_area_size=(85,30)
		self.screen_height=self.play_area_size[1]
		self.screen_width=self.play_area_size[0]
	
		while True:
			self.pos = tuple([randint(2,self.screen_height-3), \
					randint(2,self.screen_width-3)])
			if self.pos not in blacklist: break
                

	def draw(self,screen,codelist):
		for item in codelist:
		        self._draw_normal_object(item.pos[0], item.pos[1])
		
	def _draw_normal_object(self,pos_y,pos_x):
		   """Implements drawing for an object in its normal state."""
		   attribs = self._drawing_attribs()
		   for key in self._shape:
			   self._draw_object_line(attribs, key, self._shape[key],pos_y,pos_x)


        def _drawing_attribs(self):
		"""Curses attributes to be used when drawing.Many derived objects will override this; the default is white.
	"""
		return curses.color_pair(2)+curses.A_BOLD

	def _draw_object_line(self, attribs, key, line,pos_y,pos_x):
        	"""Draws one line within an object."""
	        ypos = pos_y + key
		if ypos >= 0 and ypos < self.screen_height:
		            xpos = pos_x - len(line)/2
		            self.screen.addstr(ypos, xpos, line, attribs)





