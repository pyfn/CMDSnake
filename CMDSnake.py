from time import sleep as time_sleep
from os import system as os_system
from threading import Thread
from sys import platform as sys_platform, exit as sys_exit
from exceptions import Warning
from random import randint

try:
	from msvcrt import getch  # try to import Windows version
	CLEAR_SCREEN = 'CLS'	
except ImportError:
	def getch():   # define non-Windows version
		import sys, tty, termios
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch
	CLEAR_SCREEN = 'clear'
    
START_MSG = "\rTo play snake you have to use the WASD keys."\
	"(press Enter to start)"
_GAME_OVER  = '\r ___   ___  __    __  ___\n'\
'\r/ __\\ / _ \\ | \\  / | |  _|\n'\
'\r||___ | | | |  \\/  | | [_\n'\
'\r||_|| |   | |      | | [_\n'\
'\r\\___/ |_|_| |_|\\/|_| |___|\n'\
'\r  ___  __ __  ___  ____   \n'\
'\r /   \\ | | | |  _| | _ \\\n'\
'\r | | | | | | | [_  | | /\n'\
'\r | | | \\   / | [_  |   \\\n'\
'\r \\___/  \\_/  |___| |_|\_\\\n'\


MAX_FIELD = 12
_POINTS = 0
_NEXT_MOVE = "d"
_PREV_MOVE = "s"

_FOOD_POS = [(randint(1,MAX_FIELD-2),randint(1,MAX_FIELD-2))]

_SNAKE_POS = [(MAX_FIELD/2,(MAX_FIELD/2)-1),(MAX_FIELD/2,MAX_FIELD/2)]
	
SNAKE_FIELD = []

OPPOSING_MOVE = {"a":"d","s":"w","d":"a","w":"s"}

input_thread = None

for i in range(MAX_FIELD):
	temp = []
	if i == 0 or i == MAX_FIELD - 1:
		for j in range(MAX_FIELD):
			if j == 0 or j == MAX_FIELD - 1:
				temp.append("+")
			else:
				temp.append("-")
		SNAKE_FIELD.append(temp)
	else:
		for j in range(MAX_FIELD):
			if j == 0 or j == MAX_FIELD - 1:
				temp.append("|")
			else:
				temp.append(" ")
		SNAKE_FIELD.append(temp)	
SNAKE_FIELD[MAX_FIELD/2][(MAX_FIELD/2) - 1] = "o"
SNAKE_FIELD[MAX_FIELD/2][MAX_FIELD/2] = "O"

def main():
	while True:
		os_system(CLEAR_SCREEN)
		raw_input(START_MSG)
		try:
			gameloop(7)
		except Warning:
			os_system(CLEAR_SCREEN)
			print "\r" + _GAME_OVER
			print "\rYou lost!(press %s)" % _NEXT_MOVE
			while input_thread.isAlive():
				continue
			a = raw_input("\rWant to play again?(y/n)")
			if a.lower().startswith("y"):
				reset()
				continue
			else:
				sys_exit(0)
				
def gameloop(check):
	global input_thread
	while True:
		os_system(CLEAR_SCREEN)
		printScreen()
		if input_thread == None or not input_thread.isAlive():
			input_thread = Thread(target=getMove)
			input_thread.start()
		time_sleep(0.3)
		if check >= 8:
			createFood()
			check = 0
		nextSnakePos(_NEXT_MOVE,_PREV_MOVE)
		check += 1
		
def reset():
	global _NEXT_MOVE
	global _PREV_MOVE
	global _FOOD_POS
	global _SNAKE_POS
	global SNAKE_FIELD
	global input_thread
	global _POINTS
	_NEXT_MOVE = "d"
	_PREV_MOVE = "s"
	_POINTS = 0		
	_FOOD_POS = [(randint(1,MAX_FIELD),randint(1,MAX_FIELD))]
	_SNAKE_POS = [(MAX_FIELD/2,(MAX_FIELD/2)-1),(MAX_FIELD/2,MAX_FIELD/2)]
	SNAKE_FIELD = []
	input_thread = None
	for i in range(MAX_FIELD):
		temp = []
		if i == 0 or i == MAX_FIELD - 1:
			for j in range(MAX_FIELD):
				if j == 0 or j == MAX_FIELD - 1:
					temp.append("+")
				else:
					temp.append("-")
			SNAKE_FIELD.append(temp)
		else:
			for j in range(MAX_FIELD):
				if j == 0 or j == MAX_FIELD - 1:
					temp.append("|")
				else:
					temp.append(" ")
			SNAKE_FIELD.append(temp)	
	SNAKE_FIELD[MAX_FIELD/2][(MAX_FIELD/2) - 1] = "o"
	SNAKE_FIELD[MAX_FIELD/2][MAX_FIELD/2] = "O"

def isCrash(newSnake):
	if newSnake[-1] in newSnake[:-1]:
		return True
	if (newSnake[-1][0] == (MAX_FIELD - 1) or 
			newSnake[-1][1] == (MAX_FIELD - 1) or
			newSnake[-1][0] == 0 or newSnake[-1][1] ==0):
		return True
	return False
	
def createFood():
	global _FOOD_POS
	while True:	
		temp = (randint(1,MAX_FIELD - 2), randint(1,MAX_FIELD - 2))
		if not temp in _SNAKE_POS:
			break
	_FOOD_POS.append(temp)
		
def nextSnakePos(nmove,pmove):
	global _SNAKE_POS
	global SNAKE_FIELD
	if nmove == "w" and not pmove == "s":
		_SNAKE_POS.append((_SNAKE_POS[-1][0] - 1 ,_SNAKE_POS[-1][1]))
	elif nmove == "s" and not pmove == "w":
		_SNAKE_POS.append((_SNAKE_POS[-1][0] + 1 ,_SNAKE_POS[-1][1]))
	elif nmove == "d" and not pmove == "a":
		_SNAKE_POS.append((_SNAKE_POS[-1][0],_SNAKE_POS[-1][1] + 1))
	elif nmove == "a" and not pmove == "d":
		_SNAKE_POS.append((_SNAKE_POS[-1][0],_SNAKE_POS[-1][1] - 1))
	if not _SNAKE_POS[0] in _FOOD_POS:
		SNAKE_FIELD[_SNAKE_POS[0][0]][_SNAKE_POS[0][1]] = " "
		del _SNAKE_POS[0]
	else:
		global _POINTS
		_FOOD_POS.remove(_SNAKE_POS[0])
		_POINTS += 1
	if isCrash(_SNAKE_POS):
		raise Warning("You lose!")
	for food in _FOOD_POS:
		SNAKE_FIELD[food[0]][food[1]] = "X"		
	for pos in _SNAKE_POS:
		if pos in _FOOD_POS[:-1]:
			SNAKE_FIELD[pos[0]][pos[1]] = "O"
		else:
			SNAKE_FIELD[pos[0]][pos[1]] = "o"
	SNAKE_FIELD[_SNAKE_POS[-1][0]][_SNAKE_POS[-1][1]] = "O"
	
def getMove():
	global _NEXT_MOVE
	global _PREV_MOVE
	while True:	
		temp = getch()
		if (temp.lower() in "wasd" and 
			not temp.lower() == OPPOSING_MOVE[_NEXT_MOVE]):
			break
	_PREV_MOVE = _NEXT_MOVE
	_NEXT_MOVE = temp.lower()

	
def printScreen():
	global _POINTS
	for field_list in SNAKE_FIELD:
		print "\r",
		for field in field_list:
			print field , 
		print ""
	print "\r {}".format(_POINTS)

		
if __name__ == "__main__":
	main()