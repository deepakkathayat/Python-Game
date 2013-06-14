#!/usr/bin/env python
import curses
from random import randint,seed
from time import sleep,time
from os import environ
from game import Game
import sys

SPEED = 0.1
game = True

def do_pause(screen):
	"""Implements pause mode - we just block until a key is pressed"""
        screen.nodelay(0)       # turn on blocking input
        game_is_paused = True
	global gameset
	pause_string = "P A U S E D"
	screen.addstr(gameset[levelcount].screen_height / 2 - 2,
		(gameset[levelcount].screen_width - len(pause_string)) / 2,
		pause_string,
		curses.A_BOLD)

	while (game_is_paused):
		screen.getch()
		game_is_paused = False
	screen.addstr(gameset[levelcount].screen_height / 2 - 2,
		(gameset[levelcount].screen_width - len(pause_string)) / 2,
		'           ',
		curses.A_BOLD)
	screen.nodelay(1)       # turn off blocking input

def show_explosion():
	
        global gameset,levelcount
	gameset[levelcount]._bomb._state = 'exploding'
	
	for item in gameset[levelcount].mines:
		item._state='exploding'
	        item._show_explosion_until = gameset[levelcount]._bomb.explosion_duration() + gameset[levelcount]._tickcount
	        item._explosion_start = gameset[levelcount]._tickcount
	
	gameset[levelcount]._explosion_start = gameset[levelcount]._tickcount
	gameset[levelcount]._bomb._show_explosion_until = gameset[levelcount]._bomb.explosion_duration() + gameset[levelcount]._tickcount
	
def level_specific_property():
	global gameset,levelcount,game,lastdraw,success

	if gameset[levelcount]._levelnum>=3.1:
	  for mine in gameset[levelcount].mines:
	    xy=mine.pos
            if (gameset[levelcount]._robot._y <=xy[0] <= gameset[levelcount]._robot._y+2 and gameset[levelcount]._robot._x-3 <= xy[1]<= gameset[levelcount]._robot._x+3):
		show_explosion()
		game=False
		success=False
		lastdraw=True
		curses.flash()
		curses.beep()

def set_level(char):
	global gameset
	if char==ord('l'):
	         	gameset[0]._levelnum=3
			gameset[0]._score=0
			gameset[0].CODES=6
			gameset[0].MINES=0
			gameset[0].timelimit=10000
			gameset[1]._levelnum=3.1
			gameset[1]._score=0
			gameset[1].CODES=8
			gameset[1].MINES=10
			gameset[1].timelimit=12000
			gameset[2]._levelnum=3.14
			gameset[2]._score=0
			gameset[2].CODES=10
			gameset[2].MINES=10
			gameset[2].timelimit=15000
			gameset[3]._levelnum=3.141
			gameset[3]._score=0
			gameset[3].CODES=10
			gameset[3].MINES=10
			gameset[3].timelimit=20000
	elif char==ord('a'):
	         	gameset[0]._levelnum=3
			gameset[0]._score=0
			gameset[0].CODES=5
			gameset[0].MINES=0
			gameset[0].timelimit=11000
			gameset[1]._levelnum=3.1
			gameset[1]._score=0
			gameset[1].CODES=6
			gameset[1].MINES=6
			gameset[1].timelimit=14000
			gameset[2]._levelnum=3.14
			gameset[2]._score=0
			gameset[2].CODES=8
			gameset[2].MINES=6
			gameset[2].timelimit=18000
			gameset[3]._levelnum=3.141
			gameset[3]._score=0
			gameset[3].CODES=8
			gameset[3].MINES=8
			gameset[3].timelimit=25000
	
def main(screen):
    """Initialise and then run the main game loop."""
    speed_up = 1
    screen_y, screen_x = screen.getmaxyx()
    if screen_y < Game.SCREEN_MINHEIGHT or screen_x < Game.SCREEN_MINWIDTH:
	# Not big enough, throw a suitable exception
	errorstring = "Incorrect terminal size," \
		       "minimum size is %d x %d, actual size is %d x %d" % \
		       (Game.SCREEN_MINWIDTH, Game.SCREEN_MINHEIGHT, screen_x, screen_y)
        raise ValueError, errorstring
    
    global gameset,levelcount,game,success,lastdraw
    global chars_colors,objectlist
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.curs_set(0)      # turns off the visible cursor
    i=0
    char=True
    while(True):
    	screen.addstr(screen_y/2-2,screen_x/2-9,"ROBOT BOMB DEFUSER",curses.A_BOLD+curses.color_pair(i%5));
    	screen.addstr(screen_y/2+2,screen_x/2-14,"DEVELOPED BY DEEPAK KATHAYAT",curses.A_BOLD+curses.color_pair(i%5));
    	i=i+1
    	screen.addstr(screen_y/2+12,screen_x/2+20,"press spacebar to continue",curses.A_BLINK+curses.A_BOLD+curses.color_pair(0));
    	screen.nodelay(1)
	curses.beep()
	curses.flash()
	sleep(0.05)
	char = screen.getch()
	if char == ord(' '):
		break;
    screen.clear()

    while(True):
    	screen.addstr(screen_y/2-2,screen_x/2-25,"THERE ARE FOUR LEVELS.",curses.A_BOLD+curses.color_pair(1));
    
    	screen.addstr(screen_y/2+2,screen_x/2-25,"LEVELS ARE NAMED IN THE ORDER IN WHICH EACH digit OCCURS IN THE INFAMOUS NUMBER PI",curses.A_BOLD+curses.color_pair(1));
    	screen.addstr(screen_y/2+3,screen_x/2-25,"AT ANY STAGE,YOU CAN SKIP LEVELS.JUST PRESS 'l'.",curses.A_BOLD+curses.color_pair(1));
    	screen.addstr(screen_y/2+7,screen_x/2-25,"ARROW KEYS are used for movement.",curses.A_BOLD+curses.color_pair(1));
    	screen.addstr(screen_y/2+8,screen_x/2-25,"P/p for pause.Q/q for quit.",curses.A_BOLD+curses.color_pair(1));
    	screen.addstr(screen_y/2+9,screen_x/2-25,"z for shooting bullets.USE THEM.",curses.A_BOLD+curses.color_pair(1));
    	screen.addstr(screen_y/2+10,screen_x/2-25,"HEALTH and TIME are IMPORTANT.DO NOT FORGET.",curses.A_BOLD+curses.color_pair(1));
    	screen.addstr(screen_y/2+12,screen_x/2+20,"press spacebar to continue",curses.A_BLINK+curses.A_BOLD+curses.color_pair(0));
    	screen.nodelay(1)
	curses.beep()
	curses.flash()
	sleep(0.05)
	char = screen.getch()
	if char == ord(' '):
		break
    screen.clear()
    while(True):	
    	screen.addstr(screen_y/2-5,screen_x/2-10,"CHOOSE THE PLAY MODE",curses.color_pair(i%5)+curses.A_BOLD)
    	screen.addstr(screen_y/2-3,screen_x/2-9,"* AMATEUR : press 'a'",curses.A_BOLD);
    	screen.addstr(screen_y/2-2,screen_x/2-10,"* LEGENDARY : press 'l'",curses.A_BOLD);
    	i=i+1
	screen.nodelay(1)
	curses.beep()
	curses.flash()
	sleep(0.05)
    	char = screen.getch()
	if char == ord('a') or char == ord('l'):
		break
    sleep(1)
    screen.timeout(0)
    screen.nodelay(1)
    curses.nl()
    curses.curs_set(0)      # turns off the visible cursor
    gameset=[]
    levelcount=0
    num_of_levels=4
    for i in range(num_of_levels):
    	gameset.insert(i,Game(screen))
    
    set_level(char)
    gameset[levelcount]._makeCD()
    gameset[levelcount].draw()
    initial_time = time()  # time seconds as a real number
    tick_count = 0
    tick_interval = 50      # game runs in 50ms steps (20Hz)

    timed_game_end = False  # time-limited game ended
	
    curses.beep()
    curses.flash()
    charBomb = 'B'
    screen.nodelay(1)
    oldchar = curses.KEY_RIGHT
    stopgame=False
    lastdraw=False
# start the game loop here
    
    while (True and not timed_game_end):
	char = screen.getch()
        if char == ord('q') or char==ord('Q'): break  # quit
	elif char == ord('l'):
		levelcount=levelcount+1
		if levelcount<num_of_levels:
			tick_count = 0
			curses.flash()
			curses.beep()
			gameset[levelcount]._makeCD()
		else:   
			break
	elif char == 27 : 
		gameset[levelcount].game_over(0)
		game=False
		stopgame=True
	elif char == ord('p') or char==ord('P'): #pause:
		do_pause(screen) 
		curses.flushinp()
		oldchar = char
	elif game == True:
            if char != oldchar:
		if char == curses.KEY_RIGHT: gameset[levelcount].handle_key(char)
                elif char == curses.KEY_LEFT: gameset[levelcount].handle_key(char)
                elif char == curses.KEY_UP: gameset[levelcount].handle_key(char)
                elif char == curses.KEY_DOWN: gameset[levelcount].handle_key(char) 
                elif char == ord('z'):gameset[levelcount].handle_key(char) 
                else:
		     gameset[levelcount].handle_key(None)
            else:
                gameset[levelcount].handle_key(None)
                curses.flushinp()
            oldchar = char
       	if game==False:
		curses.flash()
		curses.beep()
		continue
	if (gameset[levelcount]._robot._y<=-1 or gameset[levelcount]._robot._y+3 >= gameset[levelcount].screen_height or gameset[levelcount]._robot._x-2 <=0 or gameset[levelcount]._robot._x+1>=gameset[levelcount].screen_width):
		game=False
		success=False
		lastdraw=True
		curses.flash()
		curses.beep()
        elif (gameset[levelcount].codes!=[] and gameset[levelcount]._robot._y-2 <=gameset[levelcount]._bomb.pos[0] <= gameset[levelcount]._robot._y+2 and gameset[levelcount]._robot._x-4 <= gameset[levelcount]._bomb.pos[1] <= gameset[levelcount]._robot._x+4):
		show_explosion()
		game=False
		success=False
		lastdraw=True
		curses.flash()
		curses.beep()
        elif (gameset[levelcount].codes==[] and gameset[levelcount]._robot._y-2 <=gameset[levelcount]._bomb.pos[0] <= gameset[levelcount]._robot._y+2 and gameset[levelcount]._robot._x-4 <= gameset[levelcount]._bomb.pos[1] <= gameset[levelcount]._robot._x+4):
		levelcount += 1		
		tick_count = 0
		if levelcount>=num_of_levels:
			game=False
			success=True
			lastdraw=True
		else:gameset[levelcount]._makeCD()
		curses.flash()
		curses.beep()
	if game==True:
		for code in gameset[levelcount].codes:
	    		xy=code.pos
            		if gameset[levelcount]._robot._x-3 <= xy[1] <= gameset[levelcount]._robot._x+3 and gameset[levelcount]._robot._y-1 <= xy[0] <= gameset[levelcount]._robot._y+2:
                		gameset[levelcount]._score=gameset[levelcount]._score+1
                		gameset[levelcount].codes.pop(gameset[levelcount].codes.index(code))
		level_specific_property()
                gameset[levelcount].tick(tick_count)
	tick_count += tick_interval
        secs_elapsed_total = time() - initial_time
        ms_elapsed_total = int(secs_elapsed_total * 1000)
        target_real_ms = tick_count / speed_up
        ms_to_wait = max(0, target_real_ms - ms_elapsed_total)
        curses.napms(ms_to_wait)
        if game == True:
		if tick_count > gameset[levelcount].timelimit:  # 10 seconds for 1st level
	    		show_explosion() 
	    		success=False
	    		game=False
	    		lastdraw=True
	    		curses.beep()
	    		curses.flash()

	if not stopgame:
		try:gameset[levelcount].draw()
		except:pass
	if lastdraw==True:
		stopgame=True
	
	if(stopgame==True):
		if success==True:	
	    		try:gameset[levelcount].game_over(1)
			except:gameset[levelcount-1].game_over(1)
		elif success==False:	
	   		gameset[levelcount].game_over(0)
	sleep(SPEED)

    quit()

try: _orig_ESCDELAY = environ['ESCDELAY']
except KeyError: pass
environ['ESCDELAY'] = str(0)  # Stop escape key from pausing game
try:
    curses.wrapper(main)
except ValueError, error_string:
    print error_string

environ['ESCDELAY'] = _orig_ESCDELAY  # Revert to original ESCDELAY
