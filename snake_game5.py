import curses
import time
from curses import KEY_UP,KEY_DOWN,KEY_LEFT,KEY_RIGHT
from curses import wrapper
import random


#paint the wall
def wall(space,direction):
    global screen
    dims=screen.getmaxyx()
    curses.start_color()
    curses.init_pair(3,curses.COLOR_RED,curses.COLOR_RED)
    if direction=="round":
        for i in range(space,dims[1]-space,1):
            screen.addstr(space,i,"B",curses.color_pair(3))
        for i in range(space,dims[0]-space,1):
            screen.addstr(i,space,"B",curses.color_pair(3))
        for i in range(space,dims[1]-space,1):
            screen.addstr(dims[0]-space,i,"B",curses.color_pair(3))
        for i in range(space,dims[0]-space,1):
            screen.addstr(i,dims[1]-space,"B",curses.color_pair(3))

    if direction=="half":
        for i in range(dims[1]-space,space,-1):
            screen.addstr(20,i,"B")
        for i in range(dims[0]-space,space,-1):
            screen.addstr(i,20,"B")
#keyboard events
def keyboard(key,move):
    if key==27:
        return 2
    if key==KEY_DOWN and move[0]!=-1:
        move[0],move[1]=1,0
        return move
    if key==KEY_UP and move[0]!=1:
        move[0],move[1]=-1,0
        return move
    if key==KEY_LEFT and move[1]!=1:
        move[0],move[1]=0,-1
        return move
    if key==KEY_RIGHT and move[1]!=-1:
        move[0],move[1]=0,1
        return move
# random place for the objects
def food(gety,getx):
    foody=random.randrange(2,gety-2,1)
    foodx=random.randrange(2,getx-2,1)
    return foody,foodx
# handel the game over event
def game_over(sn,sb,sy,sx,dimy,dimx,score):
    global screen
    if sn in sb or sy==1 or sy==dimy or sx==1 or sx==dimx:
        screen.clear()
        msg1="GAME OVER"
        msg2="Your score: "
        screen.addstr(int(dimy/2),int((dimx-len(msg1))/2),msg1)
        screen.addstr(int(dimy/2)-2,int((dimx-len(msg2))/2),msg2+str(score))
        screen.refresh()
        time.sleep(2)
        return  2
# initialize curses screen, colors
def init():
    global screen
    curses.noecho()             # Disable default printing of inputs
    curses.curs_set(0)          # Hiding cursor visibility (https://docs.python.org/2/library/curses.html#curses.curs_set)
    screen=curses.newwin(0,0,0,0)   #create a new window with terminal size
    screen.keypad(1)               # enable processing of functional keys by curses (ex. arrow keys)
    screen.nodelay(1)       #continous getch command
    curses.start_color()
    curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_GREEN)
    curses.init_pair(3,curses.COLOR_RED,curses.COLOR_RED)
    curses.init_pair(4,curses.COLOR_YELLOW,curses.COLOR_YELLOW)
    curses.init_pair(5,curses.COLOR_WHITE,curses.COLOR_BLACK)


def main(stdscr):
    init()
    #main variables
    global screen
    dim=screen.getmaxyx()
    color,speed,speed_change,score,space=1,0.1,0.01,0,1
    foods=[2,2]
    food_ok=True
    powers=[2,2]
    power_ok=True
    move=[0,1]
    snake=[10,10]
    monster=[20,20]
    snake_body=[snake[:]]*10
    last=snake_body[-1][:]
    slen=len(snake)
    key=-1
    a=1
    wall(space,"round")

    #main loop for the game actions
    while a!=2:
        time.sleep(speed)
        if last not in snake_body:
            screen.addstr(last[0],last[1]," ")
        screen.addstr(snake[0],snake[1],"X",curses.color_pair(color))
        screen.addstr(0,0,'SCORE:'+str(score))

        key=screen.getch()
        keyboard(key,move)
        #let's move the snake
        snake[0]+=move[0]
        snake[1]+=move[1]
        screen.addstr(snake[0],snake[1],"X",curses.color_pair(5)|curses.A_BOLD)
        #objects
        if power_ok:
            powers=food(dim[0],dim[1])
            if powers not in snake_body:
                screen.addstr(powers[0],powers[1],"P",curses.color_pair(4))
            power_ok=False
        if (powers[0]==snake[0] and powers[1]==snake[1]):
             score+=5
             speed+=speed_change*2
             screen.addstr(powers[0],powers[1]," ")

        if score%4==0 and score!=0 and food_ok:
            power_ok=True
            
        if food_ok:
            foods=food(dim[0],dim[1])
            if (foods) not in snake_body:
                screen.addstr(foods[0],foods[1],"F",curses.color_pair(2))
            food_ok=False
        if (foods[0]==snake[0] and foods[1]==snake[1]):
             score+=1
             speed-=speed_change
             screen.addstr(foods[0],foods[1]," ")
             snake_body.append(snake_body[-1])
             food_ok=True

        a=game_over(snake,snake_body,snake[0],snake[1],dim[0],dim[1],score)
        # move snakes body (like peristaltic movement)
        last=snake_body[-1]
        for y in range(len(snake_body)-1,0,-1):
            snake_body[y]=snake_body[y-1][:]
        snake_body[0]=snake[:]
        screen.refresh()
#start the project
wrapper(main)
#end the project
curses.endwin()
