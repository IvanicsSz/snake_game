import curses
import time
from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_ENTER
from curses import wrapper
import random


def monster(mon, msg):
    global screen
    # monster_scr = curses.newwin(10, 10, 20, 20)
    # Return a new window, whose left-upper corner is at (begin_y, begin_x), and whose height/width is nlines/ncols.
    # monster_scr.border(1)
    # monster_scr.addstr(21, 21, msg)
    q, vertical, horizontal = -1, 1, 1
    dims = screen.getmaxyx()
    y = mon[0]
    x = mon[1]
    if y == dims[0]-2:
        y = 3
        horizontal = horizontal*-1
    elif y == 2:
        vertical = 1
    if x == dims[1]-len(msg)-2:
        vertical = vertical*-1
        x = 3
    elif x == 2:
        horizontal = 1
    y += vertical
    x += horizontal
    return y, x
# paint the wall


def wall(space=2, longs=1, y=0, x=0, snake_body=[10, 10]):
    global screen
    dims = screen.getmaxyx()
    rng = 5
    random_x = random.randint(space + rng, (dims[1]-space - rng))
    random_y = random.randint(space + rng, (dims[0]-space - rng))
    curses.start_color()
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_RED)
    if not y and not x:
        for i in range(space, dims[0]-space, 1):
            screen.addstr(i, space, "B", curses.color_pair(3))
            screen.addstr(i, dims[1]-space, "B", curses.color_pair(3))
        for i in range(space, dims[1]-space, 1):
            screen.addstr(space, i, "B", curses.color_pair(3))
            screen.addstr(dims[0]-space, i, "B", curses.color_pair(3))
    if y:
        for i in range(space, (dims[0]-space)//longs, 1):
            screen.addstr(i, random_x, "B", curses.color_pair(3))
        return (dims[0]-space)//longs, random_x
    if x:
        for i in range(space, (dims[1]-space)//longs, 1):
            screen.addstr(random_y, i, "B", curses.color_pair(3))
        return random_y, (dims[1]-space)//longs
# keyboard events


def speed_normalize(move, speed):
    change = 3
    if move[0]:
        time.sleep(speed / change)


def keyboard(key, move):

    if key == KEY_DOWN and move[0] != -1:
        move[0], move[1] = 1, 0
        return move
    if key == KEY_UP and move[0] != 1:
        move[0], move[1] = -1, 0
        return move
    if key == KEY_LEFT and move[1] != 1:
        move[0], move[1] = 0, -1
        return move
    if key == KEY_RIGHT and move[1] != -1:
        move[0], move[1] = 0, 1
        return move



def manufactory(snake_body, snake, wall, color):
    global screen
    dims = screen.getmaxyx()
    place = [random.randrange(2, dims[0]-2, 1), random.randrange(2, dims[1]-2, 1)]
    if place not in (snake_body+[snake]+[wall]):
        screen.addstr(place[0], place[1], "F", curses.color_pair(color))
        return place
# random place for the objects


# handel the game over event

    # print (inv)
def print_highscore():
    # global screen
    # dims = screen.getmaxyx()
    score_list = []
    print_list = []
    # line = 0
    for k, i in enumerate(open("highscore.csv", "r"), start=1):
        i = i.replace("\n", "")
        score_list.append(i.split(","))
    print_list = score_list
    score_list = dict(score_list)
    print_list = sorted(score_list, key=score_list.get, reverse=True)
    key_max = len(max(score_list, key=len))
    print("{0:^{1}}".format("High Score:", key_max+5))
    for i in print_list:
        # screen.addstr(int(dims[0]/2)-line, int((dims[1]-key_max)/2), "{0:>{2}}{1:>5}".format(i, score_list[i], key_max))
        # line += 2
        print("{0:>{2}}{1:>5}".format(i, score_list[i], key_max))
    return


def highscore(name, score):
    with open("highscore.csv", "a") as a:
        if score:
            a.write("{0},{1}\n".format(name, str(score)))


def main_menu():
    colour_list = []
    main_win = curses.initscr()
    main_win.nodelay(1)
    main_win.keypad(1)
    curses.use_default_colors()
    dims = main_win.getmaxyx()
    msg1 = "Play Game"
    msg2 = "High Scores"
    msg3 = "Quit"
    count = 1
    color = 0
    key = -1
    while key != 27:
        graphics = [0] * 3
        graphics[color] = curses.A_REVERSE
        key = main_win.getch()
        if key == KEY_DOWN:
            color = (color + 1) % 3
        if key == KEY_UP:
            color = (color - 1) % 3
        if key == ord("\n") and color == 0:
            break
        if key == ord("\n") and color == 1:
            print_highscore()
        if key == ord("\n") and color == 2:
            exit()
        main_win.addstr(int(dims[0]/2), int((dims[1]-len(msg3))/2), msg3, graphics[2])
        main_win.addstr(int(dims[0]/2)-2, int((dims[1]-len(msg2))/2), msg2, graphics[1])
        main_win.addstr(int(dims[0]/2)-4, int((dims[1]-len(msg1))/2), msg1, graphics[0])
        main_win.refresh()


def game_over(sn, sb, sy, sx, dimy, dimx, score):
    global screen
    if sn in sb or sy == 1 or sy == dimy-1 or sx == 1 or sx == dimx-1:
        highscore(name, score)
        screen.clear()
        msg1 = "GAME OVER"
        msg2 = "Your score: "
        screen.addstr(int(dimy/2), int((dimx-len(msg1))/2), msg1)
        screen.addstr(int(dimy/2)-2, int((dimx-len(msg2))/2), msg2+str(score))
        screen.refresh()
        time.sleep(2)
        return 2
    if screen.getch() == 27:
        return 2
# initialize curses screen, colors


def init():
    global screen
    curses.noecho()             # Disable default printing of inputs
    curses.curs_set(0)          # Hiding cursor visibility
    screen = curses.newwin(0, 0, 0, 0)   # create a new window with terminal
    screen.keypad(1)               # enable processing of functional keys
    screen.nodelay(1)       # continous getch command
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)


def main(stdscr):

    main_menu()
    init()
    # main variables
    global screen
    dim = screen.getmaxyx()
    color, speed, speed_change, score, space = 1, 0.1, 0.01, 0, 1
    food_ok = True
    power_ok = True
    _objs = {
        "snake": [10, 10],
        "move": [0, 1],
        "foods": [2, 2],
        "powers": [2, 2],
        "monsterxy": [20, 20],
        "wall": [0, 0]
    }
    # mypad = curses.newpad(10, 10)
    # mypad_pos = 5
    # mypad.border(0)
    start_monster = 25
    snake_body = [_objs["snake"][:]]*4
    last = snake_body[-1][:]
    key = -1
    a = 1
    wall(space)
    wall(2, 2, 0, 1, snake_body)
    # wall(2, 2, 1, 0)
    # main loop for the game actions
    while a != 2:
        time.sleep(speed)
        speed_normalize(_objs["move"], speed)

        if last not in snake_body:
            screen.addstr(last[0], last[1], " ")
        screen.addstr(_objs["snake"][0], _objs["snake"][1], "X", curses.color_pair(color))
        screen.addstr(0, 0, 'SCORE:'+str(score))

        key = screen.getch()
        keyboard(key, _objs["move"])
        temp = []
        _objs["snake"][0] += _objs["move"][0]
        _objs["snake"][1] += _objs["move"][1]
        screen.addstr(_objs["snake"][0], _objs["snake"][1], "X", curses.color_pair(5) | curses.A_BOLD)
        screen.addstr(_objs["monsterxy"][0], _objs["monsterxy"][1], "   ") # _objs["monsterxy"][0], _objs["monsterxy"][1]
        _objs["monsterxy"] = monster(_objs["monsterxy"], "MON")  # _objs["monsterxy"] =
        screen.addstr(_objs["monsterxy"][0], _objs["monsterxy"][1], "MON")
        # objects
        if power_ok:
            _objs["powers"] = manufactory(snake_body, _objs.get("snake"), _objs["wall"], 4)
            power_ok = False
        if (_objs.get("powers") == _objs.get("snake")):
            score += 5
            speed += speed_change*2
            screen.addstr(_objs["powers"][0], _objs["powers"][1], " ")

        if score % 4 == 0 and score != 0 and food_ok:
            power_ok = True



        if food_ok:
            _objs["foods"] = manufactory(snake_body, _objs.get("snake"), _objs["wall"], 2)
            food_ok = False

        if (_objs.get("foods") == _objs.get("snake")):
            score += 1
            speed -= speed_change
            screen.addstr(_objs["foods"][0], _objs["foods"][1], " ")
            snake_body.append(snake_body[-1])
            food_ok = True
        # if (monsterxy[0] == foods[0] and foods[1] in range(monsterxy[1], monsterxy[1] + len("MONSTER"))):
        #     food_ok = True
        # if (monsterxy[0] == powers[0] and powers[1] in range(monsterxy[1], monsterxy[1] + len("MONSTER"))):
        #     powers_ok=True
        # if (monsterxy[0]==snake[0] and snake[1] in range(monsterxy[1],monsterxy[1]+len("MONSTER"))):
        #     score-=1
        #    if (powers[1] in range(monsterxy[1],len("MONSTER"))):
        #        powers_ok=True
        a = game_over(_objs.get("snake"), snake_body, _objs["snake"][0], _objs["snake"][1], dim[0], dim[1], score)
        # move snakes body (like peristaltic movement)
        last = snake_body[-1]
        for y in range(len(snake_body)-1, 0, -1):
            snake_body[y] = snake_body[y-1][:]
        snake_body[0] = _objs["snake"][:]
        # mypad.scrollok(1)
        # mypad.idlok(1)
        # mypad.scroll(-1)
        # mypad.refresh(mypad_pos, 0, 10, 10, 35, 15)

        # mypad.refresh()
        screen.refresh()
# start the project
name = input("Please type your name: ")
wrapper(main)
# end the project
curses.endwin()
print_highscore()
