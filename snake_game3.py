import curses
import time
from curses import KEY_UP,KEY_DOWN,KEY_LEFT,KEY_RIGHT
from curses import wrapper



def main(stdscr):
    #screen=curses.initscr()
    curses.noecho()             # Disable default printing of inputs
    curses.curs_set(0)          # Hiding cursor visibility (https://docs.python.org/2/library/curses.html#curses.curs_set)
    screen=curses.newwin(0,0,0,0)   #create a new window with terminal size
    screen.keypad(1)               # enable processing of functional keys by curses (ex. arrow keys)
    screen.border(0)               # set a border for the window
    screen.nodelay(1)       #continous getch command
    dim=screen.getmaxyx()   #max y,x of the screen

    move=[0,1]              #move the snake y,x
    snake=[10,10]
    snake_body=[snake[:]]*5
    last=snake_body[-1][:]
    slen=len(snake)       #snake initial position
    key=-1                  # define key unknown key

    while key!=27:
        time.sleep(0.1)
        if last not in snake_body:
            screen.addstr(last[0],last[1]," ")
        screen.addstr(snake[0],snake[1],"X")
        key=screen.getch()
        if key==KEY_DOWN and move[0]!=-1:
            move[0]=1
            move[1]=0

        if key==KEY_UP  and move[0]!=1:
            move[0]=-1
            move[1]=0

        if key==KEY_LEFT  and move[1]!=1:
            move[0]=0
            move[1]=-1

        if key==KEY_RIGHT  and move[1]!=-1:
            move[0]=0
            move[1]=1
        #if screen.inch(snake[0],snake[1])!=ord(' '):
        #    break
        snake[0]+=move[0]
        snake[1]+=move[1]
        last=snake_body[-1]

        for y in range(len(snake_body)-1,0,-1):
            snake_body[y]=snake_body[y-1][:]

        snake_body[0]=snake[:]


        screen.refresh()
        #snake[0,0]+=move[0]

wrapper(main)
curses.endwin()
#snake game
#features:
#   1. score
#   2. snake grows
#   3. power ups
#   4. game Over (wall,self)
#   5. speed change
#
