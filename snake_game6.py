import curses
import time
from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_ENTER
from curses import wrapper
import random

# move the monster
def monster(mon, move, msg, wall_check):
    global screen

    dims = screen.getmaxyx()
    y = mon[0]
    x = mon[1]
    if y == dims[0]-2:
        move[0] = -1
    if y == 2:
        move[0] = 1
    if x == dims[1]-len(msg)-2:
        move[1] = -1
    if x == 2:
        move[1] = 1
    return move[0], move[1]


# paint the wall and build new walls
def wall(space=2, longs=1, y=0, x=0, snake_body=[10, 10]):
    global screen
    dims = screen.getmaxyx()
    list_x = []
    list_y = []
    rng = 5
    random_x = random.randint(space + rng, (dims[1]-space - rng))
    random_y = random.randint(space + rng+5, (dims[0]-space - rng))
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
            list_y.append([i, random_x])

    if x:
        for i in range(space, (dims[1]-space)//longs, 1):
            screen.addstr(random_y, i, "B", curses.color_pair(3))
            list_x.append([random_y, i])
    return list_y, list_x


# normalize the speed in vertical
def speed_normalize(move, speed):
    change = 3
    if move[0]:
        time.sleep(speed / change)

# keyboard events
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


# build food and power ups in random places
def manufactory(snake_body, snake, wall, color):
    global screen
    inwall = 0
    dims = screen.getmaxyx()
    place = [random.randrange(2, dims[0]-2, 1), random.randrange(2, dims[1]-2, 1)]
    if wall:
        for i in range(len(wall[0])):
            if place in wall[0][i]:
                inwall = 1
    if place not in (snake_body+[snake]) and not inwall:
        screen.addstr(place[0], place[1], "F", curses.color_pair(color))
        return place


# print sorted highscore
def print_highscore():
    curses.noecho()
    curses.curs_set(0)
    high_win = curses.newwin(curses.LINES, curses.COLS, 0, 0)
    dim = high_win.getmaxyx()
    high_win.clear()
    score_list = []
    print_list = []
    x = 2
    for k, i in enumerate(open("highscore.csv", "r"), start=1):
        i = i.replace("\n", "")
        score_list.append(i.split(","))
    for j in range(len(score_list)):
        score_list[j][1] = int(score_list[j][1])
    print_list = score_list
    score_list = dict(score_list)
    print_list = sorted(score_list, key=score_list.get, reverse=True)
    key_max = len(max(score_list, key=len))
    high_win.addstr(5-2, int((dim[1]-key_max))//2, "{0:^{1}}".format("High Score:", key_max+5))
    for i in print_list:
        high_win.addstr(int(5+x), int((dim[1]-key_max))//2, "{0:>{2}}{1:>5}".format(i, score_list[i], key_max))
        x += 1
    high_win.refresh()
    time.sleep(3)
    return main_menu()


# write file
def highscore(name, score):
    with open("highscore.csv", "a") as a:
        if score:
            a.write("{0},{1}\n".format(name, str(score)))


# main menu at the beggining of the game
def main_menu():
    colour_list = []
    curses.noecho()             # Disable default printing of inputs
    curses.curs_set(0)
    main_win = curses.newwin(curses.LINES, curses.COLS, 0, 0)
    main_win.clear()
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


# game over screen
def over_screen(score):
    global screen
    dim = screen.getmaxyx()
    highscore(name, score)
    screen.clear()
    msg1 = "GAME OVER"
    msg2 = "Your score: "
    screen.addstr(int(dim[0]/2), int((dim[1]-len(msg1))/2), msg1)
    screen.addstr(int(dim[0]/2)-2, int((dim[1]-len(msg2))/2), msg2+str(score))
    screen.refresh()
    time.sleep(2)


# handle the game over event
def game_over(sn, sb, monster, sy, sx, wall_check, score):
    global screen
    monster = [monster]
    for i in range(1, 3, 1):
        monster.append([monster[0][0], monster[0][1] + i])
    dim = screen.getmaxyx()
    if sn in sb or sy == 1 or sy == dim[0]-1 or sx == 1 or sx == dim[1]-1:
        over_screen(score)
        print_highscore()
        return 2
    if sn in monster:
        over_screen(score)
        print_highscore()
        return 2
    for i in range(len(monster)):
        if monster[i] in sb:
            over_screen(score)
            print_highscore()
            return 2
    if wall_check:
        for i in range(len(wall_check[0])):
            if sn in wall_check[0][i]:
                over_screen(score)
                print_highscore()
                return 2


# initialize curses screen, colors
def init():
    global screen
    curses.noecho()             # Disable default printing of inputs
    curses.curs_set(0)          # Hiding cursor visibility
    screen = curses.newwin(curses.LINES, curses.COLS, 0, 0)   # create a new window with terminal
    screen.keypad(1)               # enable processing of functional keys
    screen.nodelay(1)       # continous getch command
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)

# main loop function, with variables
def main(stdscr):
    main_menu()
    init()
    global screen
    dim = screen.getmaxyx()
    color, speed, speed_change, score, space = 1, 0.1, 0.01, 0, 1
    wall_check = []
    food_ok = True
    power_ok = True
    wall_ok = True
    _objs = {
        "snake": [10, 10],
        "move": [0, 1],
        "foods": [2, 2],
        "powers": [2, 2],
        "monsterxy": [20, 20],
        "wall": [0, 0],
        "mm": [1, 1]
    }
    start_monster = 25
    snake_body = [_objs["snake"][:]]*4
    last = snake_body[-1][:]
    key = -1
    a = 1
    wall(space)
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
        screen.addstr(_objs["monsterxy"][0], _objs["monsterxy"][1], "   ") # _objs["monsterxy"][0], _objs["monsterxy"][1]
        _objs["monsterxy"][0] += monster(_objs["monsterxy"], _objs["mm"], "MON", wall_check)[0]
        _objs["monsterxy"][1] += monster(_objs["monsterxy"], _objs["mm"], "MON", wall_check)[1]
        screen.addstr(_objs["snake"][0], _objs["snake"][1], "X", curses.color_pair(5) | curses.A_BOLD)
        screen.addstr(_objs["monsterxy"][0], _objs["monsterxy"][1], "MON")
        if power_ok:
            _objs["powers"] = manufactory(snake_body, _objs.get("snake"), wall_check, 4)
            power_ok = False
        if (_objs.get("powers") == _objs.get("snake")):
            score += 5
            speed += speed_change*2
            screen.addstr(_objs["powers"][0], _objs["powers"][1], " ")
        if food_ok:
            _objs["foods"] = manufactory(snake_body, _objs.get("snake"), wall_check, 2)
            food_ok = False
        if (_objs.get("foods") == _objs.get("snake")):
            score += 1
            speed -= speed_change
            screen.addstr(_objs["foods"][0], _objs["foods"][1], " ")
            snake_body.append(snake_body[-1])
            food_ok = True
        if score % 4 == 0 and score != 0 and food_ok:
            power_ok = True
        if score % 10 == 0 and score != 0 and wall_ok:
            wall_check.append(wall(2, 3, 1, 1, snake_body))
            wall_ok = False
        if score % 10 != 0 and score != 0 and wall_ok == False:
            wall_ok = True

        if _objs["monsterxy"][0] == _objs["foods"][0]:
            if _objs["foods"][1] in list(range(_objs["monsterxy"][1], _objs["monsterxy"][1] + len("MON"))):
                food_ok = True
        if _objs["monsterxy"][0] == _objs["powers"][0]:
            if _objs["powers"][1] in list(range(_objs["monsterxy"][1], _objs["monsterxy"][1] + len("MON"))):
                powers_ok = True
        a = game_over(_objs.get("snake"), snake_body, _objs["monsterxy"], _objs["snake"][0], _objs["snake"][1], wall_check, score)
        last = snake_body[-1]
        for y in range(len(snake_body)-1, 0, -1):
            snake_body[y] = snake_body[y-1][:]
        snake_body[0] = _objs["snake"][:]
        screen.refresh()
# start the project
name = input("Please type your name: ")
wrapper(main)
# end the project
curses.endwin()
