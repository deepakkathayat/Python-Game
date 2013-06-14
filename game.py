"""
game.py - encapsulates the game state.
"""

import random
import curses
from gameobject import Gameobject
from robot import Robot,Autopilot
from objects import Code,Bomb,Mine
from asteroid import SmallAsteroid, LargeAsteroid
from time import time,sleep

GAME_OVER_MESSAGE = "Game over. You have Lost. Press 'q' to quit."
GAME_SUCCESS_MESSAGE = "Game over. You have Won. Press 'q' to quit."

class Game:
    """
    Wraps up all the game state information for the active game.

    Currently main function is to have the list of all objects and
    to manage them all.
    """
    play_area_size = (90, 30)
    info_area_size = (25, 30)
    info_area_topleft = (90, 0)
    SCREEN_MINWIDTH = play_area_size[0] + info_area_size[0]
    SCREEN_MINHEIGHT = play_area_size[1]
    def __init__(self, stdscr):
        """Initialise state and store curses window object."""
        # first some properties intended to be public
        self.screen_width = self.play_area_size[0]
        self.screen_height = self.play_area_size[1]
        self.stdscr = stdscr
	# now the private properties
        self._tickcount = 0
        self._time_in_seconds = 0
        self._levelnum = 1
	self._score = 0
	self.icolor=-1
        self._code = Code(self.stdscr,[])
       # self._mine = Mine(self.stdscr,[])
        self._robot = Robot(self)
        # prepare list of game objects
        self._gameobjects = []
        self.add_object(self._robot)


    def _makeCD(self):
        self.codes=[]
	for i in range(self.CODES):
	    self.codes.append(Code(self.stdscr,[self._robot._y+key for key in self._robot._shape] + [code.pos for code in self.codes]))
        self._bomb=Bomb(self.stdscr,[self._robot._y+key for key in self._robot._shape] + [code.pos for code in self.codes])
	self.mines=[]
	for i in range(self.MINES):
	    self.mines.append(Mine([self._robot._y+key for key in self._robot._shape] + [code.pos for code in self.codes]+[self._bomb.pos],self))
	self.add_object(self.mines)
    	if self._levelnum>=3.14:
    		self._level = Level(self, 1)     
        if self._levelnum==3.141:
            self._enemy = Autopilot(self)
            self.add_object(self._enemy)
	self.stdscr.clear()	
	self.print_level_info()
    
    def print_level_info(self):
    	y,x=self.stdscr.getmaxyx()
	y=y/2
	x=x/2
	while(True):
			if self._levelnum==3:
				self.stdscr.addstr(y-14, x-3, "LEVEL " + str(self._levelnum),curses.A_BOLD+curses.color_pair(2))
				self.stdscr.addstr(y-8, x-15, "COLLECT THE CODES.DEFUSE THE BOMB.IN TIME.",curses.A_BOLD+curses.color_pair(1))
				self.stdscr.addstr(y-6, x-15, "FAIR AND EASY.",curses.A_BOLD+curses.color_pair(1))

                        elif self._levelnum==3.1:
				self.stdscr.addstr(y-14, x-3, "LEVEL " + str(self._levelnum),curses.A_BOLD+curses.color_pair(2))
				self.stdscr.addstr(y-8, x-15, "SAME AS BEFORE.ONLY THIS TIME,LOOK OUT FOR THE MINES.",curses.A_BOLD+curses.color_pair(1))
				self.stdscr.addstr(y-6, x-15, "THEY EXPLODE.AND THEY EXPLODE HARD.",curses.A_BOLD+curses.color_pair(1))

			elif self._levelnum==3.14:
				self.stdscr.addstr(y-14, x-3, "LEVEL " + str(self._levelnum),curses.A_BOLD+curses.color_pair(2))
				self.stdscr.addstr(y-8, x-15, "COLLECT THE CODES,DEFUSE THE BOMB,THE SAME OLD BUSINESS.",curses.A_BOLD+curses.color_pair(1))
				self.stdscr.addstr(y-6, x-15, "WHAT'S DIFFERENT?",curses.A_BOLD+curses.color_pair(1))
				self.stdscr.addstr(y-2, x-15, "GO FIGURE.",curses.A_BOLD+curses.color_pair(1)) 

			elif self._levelnum==3.141:
				self.stdscr.addstr(y-14, x-3, "LEVEL " + str(self._levelnum),curses.A_BOLD+curses.color_pair(2))
				self.stdscr.addstr(y-8, x-15, "MIGHTY OF YOU TO HAVE COME THIS FAR.",curses.A_BOLD+curses.color_pair(1))
				self.stdscr.addstr(y-6, x-15, "SOMETIMES, YOU FEEL YOU HAVE HAD ENOUGH TO KEEP A MAN LIKE YOU INTERESTED.",curses.A_BOLD+curses.color_pair(1))
				self.stdscr.addstr(y-4, x-15, "SOMETIMES, YOU ARE WRONG.",curses.A_BOLD+curses.color_pair(1)) 
				self.stdscr.addstr(y-1, x-15, "FEELING BAD? OH WELL,YOU'VE GOT COMPANY.",curses.A_BOLD+curses.color_pair(1)) 
				self.stdscr.addstr(y+2, x-15, "GO FISH.",curses.A_BOLD+curses.color_pair(1)) 
			
    			self.stdscr.addstr(y+12,x+20,"press spacebar to continue",curses.A_BLINK+curses.A_BOLD+curses.color_pair(0));
			c=self.stdscr.getch()
			if c==ord(' '):
				break
	
    def tick(self, tickcount):
        """Tell all game objects to update themselves."""
        self._tickcount = tickcount

        for gameobject in self._gameobjects:
            if gameobject!=self.mines:
	    	assert(isinstance(gameobject, Gameobject))
            	gameobject.tick(tickcount)

        # check if any game objects are marked for deletion
        self.remove_dead_objects()

        # debug: check for any remaining dead objects
        for gameobject in self._gameobjects:
	    if(gameobject!=self.mines):
            	assert(gameobject.is_alive())

        # Ask the level if it needs to create any new game objects
        if self._levelnum>=3.14:
		self._level.tick(tickcount)
        self._time_in_seconds = tickcount / 1000.0

    def draw(self):
        """Tell all game objects to draw themselves."""
        self.stdscr.erase()
	# draw time and score in panel then refresh
        self._draw_panel()
        self._draw_info()
        self._draw_time()
        self._draw_score()
        self._draw_shield(self._robot.shield())
        if self._robot.walk % 5==0:
		self._robot._shape=self._robot._shape1
		if self._levelnum==3.141:
			self._enemy._shape=self._enemy._shape1
		self._robot.walk+=1
	else:
		self._robot._shape=self._robot._shape2
		if self._levelnum==3.141:
			self._enemy._shape=self._enemy._shape2
		self._robot.walk+=1
	for gameobject in self._gameobjects:
	    if(gameobject==self.mines):
	    	for item in self.mines:
			item.draw(self.stdscr)
            else: gameobject.draw(self.stdscr)
        self._code.draw(self.stdscr,self.codes) 
	self._bomb.draw(self.stdscr,self._tickcount)
        #self._mine.draw(self.stdscr,self._tickcount,self.mines)
	
        self.stdscr.refresh()

    def handle_key(self, keychar):
        """Give user's key press to appropriate game object: the robot!"""
        self._robot.handle_key(keychar)

    def add_object(self, new_object):
        """Adds a game object to the 'alive' list."""
        self._gameobjects.append(new_object)

    def check_for_hit(self, source, x, y, damage):
        """See if an object which can do damage has hit another object."""
 	has_hit = False
        for gameobject in self._gameobjects:
              if gameobject!=self.mines:
	      	  if id(source) != id(gameobject):
                  	if gameobject.handle_possible_hit(x, y, damage):
                      		has_hit = True
        return has_hit

    def remove_dead_objects(self):
        """Removes objects that are no longer alive."""
        # pythonic way is to scan a temp list removing from real list
        temp_objects = self._gameobjects[:]
        for gameobject in temp_objects:
            if gameobject!=self.mines:
	    	if not gameobject.is_alive():
                	self._gameobjects.remove(gameobject)

    #def add_score(self, score):
     #   self._score += score

    def tickcount(self):
        return self._tickcount

    def over(self):
        # Check if robot destroyed: if so game over!
        return not self._robot.is_alive()

    def _draw_panel(self):
        """Display the static parts of the info panel."""
        self.stdscr.vline(
            self.info_area_topleft[1], self.info_area_topleft[0],
            "|", self.play_area_size[1])
        
	for i in range(2):
		self.stdscr.hline(self.play_area_size[1]-1,0,"-",150)

    def _draw_time(self):
        """Display time to nearest 10th second."""
        display_time = str(int(self.timelimit)/1000 - int(10 * self._time_in_seconds) / 10.0)
        xpos = self.info_area_topleft[0] + 2
        self.stdscr.addstr(13, xpos+11, "TIME LEFT",curses.A_BOLD+curses.color_pair(1))
        self.stdscr.addstr(14,xpos+14, display_time,curses.A_BOLD)

    def _draw_score(self):
        xpos = self.info_area_topleft[0] + 2
        self.stdscr.addstr(5, xpos+9, "CODES COLLECTED",curses.A_BOLD+curses.color_pair(1))
        self.stdscr.addstr(6, xpos+15, str(self._score),curses.A_BOLD)
        pass

    def _draw_info(self):
        self.icolor=self.icolor+1
        xpos = self.info_area_topleft[0] + 2
        self.stdscr.addstr(0, xpos+5, "***ROBOT-BOMB-DEFUSER***",curses.A_BOLD+curses.color_pair(self.icolor%6))
        self.stdscr.addstr(1, xpos+6, "**BY DEEPAK KATHAYAT**",curses.color_pair(self.icolor%6))
        self.stdscr.addstr(3, xpos+10, "** LEVEL "+ str(self._levelnum)+" **",curses.color_pair(self.icolor%6))
        pass
 
    def _draw_shield(self, strength):
        """Display the robot's strength in the panel."""
        assert(strength <= 10 and strength >= 0)
        xpos = self.info_area_topleft[0] + 2
        self.stdscr.addstr(9, xpos+13, "HEALTH",curses.A_BOLD+curses.color_pair(1))
        self.stdscr.addstr(10, xpos+11, "##########"[0:strength],curses.A_BOLD)

    def center(self,screen, raw_text):
        (screen_height, screen_width) = screen.getmaxyx()
	texts = raw_text.split('\n')
	y_padding = ( (screen_height-len(texts)) / 2 )
	for i in range(0, len(texts)):
		x_padding = ( (screen_width-len(texts[i])) / 2 )
		try: screen.addstr(y_padding+i, x_padding, str(texts[i]),curses.A_BOLD+curses.color_pair(1))
	     	except curses.error: pass
     	screen.move(0, 0)  # Keep the cursor out of the way

    def game_over(self,flag):

	self.stdscr.clear()
        if flag==0:
	     self.center(self.stdscr, GAME_OVER_MESSAGE+'\n'+'Score: '+str(self._score))
	else:
	     self.center(self.stdscr, GAME_SUCCESS_MESSAGE+'\n'+'Score: '+str(self._score))
	return
class Level(object):
    def __init__(self, game, levelnumber):
        self._levelnumber = levelnumber
        self._game = game

    def tick(self, tickcount):
        ASTEROIDS_BEGIN = 200
        if tickcount >= ASTEROIDS_BEGIN and \
            (tickcount % 700 == 0 or tickcount % 2000 == 0):
            # generate an asteroid
            # start with small asteroids but gradually introduce large ones
            # until it is 50:50 chance of either
            blah = min(10000, tickcount - ASTEROIDS_BEGIN)
            if random.randrange(15000) < blah:
                new_asteroid = LargeAsteroid(self._game)
            else:
                new_asteroid = SmallAsteroid(self._game)
            self._game.add_object(new_asteroid)

