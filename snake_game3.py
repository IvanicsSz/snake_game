import curses
import time
from curses import KEY_UP,KEY_DOWN,KEY_LEFT,KEY_RIGHT
from curses import wrapper
import random

def food(gety,getx):
    foody=random.randrange(2,gety-2,1)
    foodx=random.randrange(2,getx-2,1)
    return foody,foodx



def main(stdscr):
    # init screen
    curses.noecho()             # Disable default printing of inputs
    curses.curs_set(0)          # Hiding cursor visibility (https://docs.python.org/2/library/curses.html#curses.curs_set)
    screen=curses.newwin(0,0,0,0)   #create a new window with terminal size
    screen.keypad(1)               # enable processing of functional keys by curses (ex. arrow keys)
    screen.border(1)              # set a border for the window
    screen.nodelay(1)       #continous getch command
    dim=screen.getmaxyx()   #max y,x of the screen
    curses.start_color()
    curses.init_pair(1,curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_GREEN)
    color=1
    #screen.mvwin(dim[0]-2,dim[1]-2)
    #variables
    speed=0.1
    score=0
    foods=[2,2]
    food_ok=True
    move=[0,1]              #move the snake y,x
    snake=[10,10]
    monster=[20,20]
    snake_body=[snake[:]]*3
    last=snake_body[-1][:]
    slen=len(snake)       #snake initial position
    key=-1                  # define key unknown key
    #if screen.inch(20,20)==ord(" "):
        #screen.addstr(20,20,ord("d"))
    #game loop
    while key!=27:
        time.sleep(speed)
        if last not in snake_body:
            screen.addstr(last[0],last[1]," ")
        screen.addstr(snake[0],snake[1],"X",curses.color_pair(color))
        screen.addstr(1,1,'SCORE:'+str(score))
        if food_ok:

            foods=food(dim[0],dim[1])
            if (foods)!=ord("X"):
                screen.addstr(foods[0],foods[1],"F",curses.color_pair(2))
            food_ok=False

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
        #if key==ord("w"):
            #screen.addstr(20,20,ord("e"))
        snake[0]+=move[0]
        snake[1]+=move[1]

        if (foods[0]==snake[0] and foods[1]==snake[1]):
             score+=1
             speed-=0.01
             screen.addstr(foods[0],foods[1]," ")
             snake_body.append(snake_body[-1])
             food_ok=True

        last=snake_body[-1]

        for y in range(len(snake_body)-1,0,-1):
            #color=2
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
#   3. speed change
#   3. power ups
#   4. game Over (wall,self)
#
#
