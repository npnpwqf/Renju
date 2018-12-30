import pygame
import sys
from pygame.locals import *
import socket
import tkinter
from tkinter import ttk
import datetime
import time
from game import *
from policy_value_net_tensorflow import PolicyValueNet
from mcts_alphaZero import MCTSPlayer

width=15
height=15
n=5
start_player=0
model_file = 'current_policy.model'
best_policy = PolicyValueNet(width, height, model_file=model_file)
mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)

music = "bgm\BGM.mp3"
luozi = "bgm\Luozi.mp3"
winn = "bgm\Victory.mp3"
losee = "bgm\Lose.mp3"
# music flags
flag2 = 0
i_icon = "images\icon.png"
button = "images\\Mbutton1.png"
mode = "images\selectmode.png"
def judge(X,Y,moves):
    temp = 0
    if (X + 40, Y) in moves and (X + 80, Y) in moves and (X + 120, Y) in moves and (
            X + 160, Y) in moves:
        temp = 1
    elif (X - 40, Y) in moves and (X - 80, Y) in moves and (X - 120, Y) in moves and (
            X - 160, Y) in moves:
        temp = 1
    # VERTICAL
    elif (X, Y + 40) in moves and (X, Y + 80) in moves and (X, Y + 120) in moves and (
            X, Y + 160) in moves:
        temp = 1
    elif (X, Y - 40) in moves and (X, Y - 80) in moves and (X, Y - 120) in moves and (
            X, Y - 160) in moves:
        temp = 1
    # SOUTHEAST
    elif (X + 40, Y + 40) in moves and (X + 80, Y + 80) in moves and (
            X + 120, Y + 120) in moves and (X + 160, Y + 160) in moves:
        temp = 1
    elif (X - 40, Y - 40) in moves and (X - 80, Y - 80) in moves and (
            X - 120, Y - 120) in moves and (X - 160, Y - 160) in moves:
        temp = 1
    # SOUTHWEST
    elif (X - 40, Y + 40) in moves and (X - 80, Y + 80) in moves and (
            X - 120, Y + 120) in moves and (X - 160, Y + 160) in moves:
        temp = 1
    elif (X + 40, Y - 40) in moves and (X + 80, Y - 80) in moves and (
            X + 120, Y - 120) in moves and (X + 160, Y - 160) in moves:
        temp = 1
    # HORIZONTAL
    elif (X - 40, Y) in moves and (X + 40, Y) in moves and (X + 80, Y) in moves and (
            X + 120, Y) in moves:
        temp = 1
    elif (X - 80, Y) in moves and (X - 40, Y) in moves and (X + 40, Y) in moves and (
            X + 80, Y) in moves:
        temp = 1
    elif (X - 120, Y) in moves and (X - 80, Y) in moves and (X - 40, Y) in moves and (
            X + 40, Y) in moves:
        temp = 1
    # SOUTHEAST
    elif (X - 40, Y - 40) in moves and (X + 40, Y + 40) in moves and (X + 80, Y + 80) in moves and (
            X + 120, Y + 120) in moves:
        temp = 1
    elif (X - 80, Y - 80) in moves and (X - 40, Y - 40) in moves and (X + 40, Y + 40) in moves and (
            X + 80, Y + 80) in moves:
        temp = 1
    elif (X - 120, Y - 120) in moves and (X - 80, Y - 80) in moves and (
            X - 40, Y - 40) in moves and (X + 40, Y + 40) in moves:
        temp = 1
    # SOUTHWEST
    elif (X - 40, Y + 40) in moves and (X + 40, Y - 40) in moves and (X + 80, Y - 80) in moves and (
            X + 120, Y - 120) in moves:
        temp = 1
    elif (X - 80, Y + 80) in moves and (X - 40, Y + 40) in moves and (X + 40, Y - 40) in moves and (
            X + 80, Y - 80) in moves:
        temp = 1
    elif (X - 120, Y + 120) in moves and (X - 80, Y + 80) in moves and (
            X - 40, Y + 40) in moves and (X + 40, Y - 40) in moves:
        temp = 1
    # VERTICAL
    elif (X, Y - 40) in moves and (X, Y + 40) in moves and (X, Y + 80) in moves and (
            X, Y + 120) in moves:
        temp = 1
    elif (X, Y - 80) in moves and (X, Y - 40) in moves and (X, Y + 40) in moves and (
            X, Y + 80) in moves:
        temp = 1
    elif (X, Y - 120) in moves and (X, Y - 80) in moves and (X, Y - 40) in moves and (
            X, Y + 40) in moves:
        temp = 1

    return temp

# Restricted Move Detect
def RMD(X,Y,moves):
    temp_x = X+40
    temp_y = Y
    horizontal = 0
    while((temp_x,temp_y) in moves):
        horizontal+=1
        temp_x = temp_x+40

    temp_x = X-40
    temp_y = Y
    while((temp_x,temp_y) in moves):
        horizontal += 1
        temp_x = temp_x - 40

    if horizontal>=5:
        return True

    temp_x = X
    temp_y = Y+40
    vertical = 0
    while ((temp_x, temp_y) in moves):
        vertical += 1
        temp_y = temp_y + 40

    temp_x = X
    temp_y = Y-40
    while ((temp_x, temp_y) in moves):
        vertical += 1
        temp_y = temp_y - 40

    if vertical >= 5:
        return True

    temp_x = X +40
    temp_y = Y + 40
    '''
    LURD stands for Left Up Corner to Right Down corner
    '''
    LURD = 0
    while ((temp_x, temp_y) in moves):
        LURD += 1
        temp_y = temp_y + 40
        temp_x = temp_x + 40

    temp_x = X - 40
    temp_y = Y - 40
    while ((temp_x, temp_y) in moves):
        LURD += 1
        temp_y = temp_y - 40
        temp_x = temp_x - 40

    if LURD >= 5:
        return True

    temp_x = X - 40
    temp_y = Y + 40
    '''
    LDRU stands for Left Down Corner to Right Up corner
    '''
    LDRU = 0
    while ((temp_x, temp_y) in moves):
        LDRU += 1
        temp_y = temp_y + 40
        temp_x = temp_x - 40

    temp_x = X + 40
    temp_y = Y - 40
    while ((temp_x, temp_y) in moves):
        LDRU += 1
        temp_y = temp_y - 40
        temp_x = temp_x + 40

    if LDRU >= 5:
        return True

    num=0
    temp_moves = moves[:]
    for (x,y) in temp_moves:
        if (x+40,y) in temp_moves and (x+80,y) in temp_moves:
            temp_moves.remove((x,y))
            temp_moves.remove((x+40, y))
            temp_moves.remove((x+80, y))
            num+=1
        elif (x-40,y) in temp_moves and (x+40,y) in temp_moves:
            temp_moves.remove((x,y))
            temp_moves.remove((x+40, y))
            temp_moves.remove((x-40, y))
            num += 1
        elif (x-40,y) in temp_moves and (x-80,y) in temp_moves:
            temp_moves.remove((x,y))
            temp_moves.remove((x-80, y))
            temp_moves.remove((x-40, y))
            num += 1
        elif (x,y+40) in temp_moves and (x,y+80) in temp_moves:
            temp_moves.remove((x,y))
            temp_moves.remove((x, y+40))
            temp_moves.remove((x, y+80))
            num += 1
        elif (x,y-40) in temp_moves and (x,y+40) in temp_moves:
            temp_moves.remove((x,y))
            temp_moves.remove((x, y-40))
            temp_moves.remove((x, y+40))
            num += 1
        elif (x,y-40) in temp_moves and (x,y-80) in temp_moves:
            temp_moves.remove((x,y))
            temp_moves.remove((x, y-40))
            temp_moves.remove((x, y-80))
            num += 1
        elif (x+40,y+40) in temp_moves and (x+80,y+80) in temp_moves:
            temp_moves.remove((x,y))
            temp_moves.remove((x+80, y+80))
            temp_moves.remove((x+40, y+40))
            num += 1
        elif (x-40,y-40) in temp_moves and (x+40,y+40) in temp_moves:
            temp_moves.remove((x,y))
            temp_moves.remove((x-40,y-40))
            temp_moves.remove((x+40,y+40))
            num += 1
        elif (x-40,y-40) in temp_moves and (x-80,y-80) in temp_moves:
            temp_moves.remove((x,y))
            temp_moves.remove((x-40, y-40))
            temp_moves.remove((x-80, y-80))
            num += 1
        elif (x+40,y-40) in temp_moves and (x+80,y-80) in temp_moves:
            temp_moves.remove((x,y))
            temp_moves.remove((x+40, y-40))
            temp_moves.remove((x+80, y-80))
            num += 1
        elif (x-40,y+40) in temp_moves and (x+40,y-40) in temp_moves:
            temp_moves.remove((x,y))
            temp_moves.remove((x-40,y+40))
            temp_moves.remove((x+40,y-40))
            num += 1
        elif (x-40,y+40) in temp_moves and (x-80,y+80) in temp_moves:
            temp_moves.remove((x,y))
            temp_moves.remove((x-40, y-40))
            temp_moves.remove((x-80, y-80))
            num += 1
    if num>=2:
        return True

    return False
def record(list1,list2):
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    with open('saved.txt', 'a') as file:
        file.write('{}  '.format(nowTime))

    len1 = len(list1)
    len2 = len(list2)

    total=0
    if len1>len2:
        total=len2
    else:
        total=len1
    for i in range(total):
        with open('saved.txt', 'a') as file:
            file.write('1_{}_{} '.format(list1[i][0],list1[i][1]))
            file.write('0_{}_{} '.format(list2[i][0], list2[i][1]))

    if len1>len2:
        with open('saved.txt', 'a') as file:
            file.write('1_{}_{} '.format(list1[len1-1][0],list1[len1-1][1]))
    else:
        with open('saved.txt', 'a') as file:
            file.write('0_{}_{} '.format(list2[len2-1][0],list2[len2-1][1]))

    with open('saved.txt', 'a') as file:
        file.write('\n')

def model():
    fread = open('info\\theme.txt', 'r')  # 读取棋盘主题
    default = "images\\" + fread.readline()
    fread.close()
    bif = default
    USER = "images\\noir.png"
    AI = "images\\blanc.png"
    # loading ingame images
    i_icon = "images\icon.png"
    EXIT = "images\exit.png"
    PANE = "images\pane.jpg"
    ABOUT = "images\\about.png"
    WIN = "images\win.png"
    LOSE = "images\lost.png"
    YOU = "images\you.png"
    ME = "images\me.png"
    UNDO = "images\disabled.png"
    AGAIN = "images\\again.png"
    NOTHING = "images\waste.png"
    # initializing the arrays
    HUMAN = []
    COMPUTER = []
    pygame.init()
    # pygame.mixer.init()
    # drawing the images on display surface
    icon = pygame.image.load(i_icon)
    pygame.display.set_icon(icon)  # 设置窗口图标
    # setting the screen to 960 x 640 resolution
    screen = pygame.display.set_mode((960, 640), 0, 32)  # 返回一个surface对象
    # loading the background and stone images
    background = pygame.image.load(bif).convert()  # 加载位图，bif主题图
    pane = pygame.image.load(PANE).convert()
    about = pygame.image.load(ABOUT).convert_alpha()
    win = pygame.image.load(WIN).convert_alpha()
    lost = pygame.image.load(LOSE).convert_alpha()
    no_undo = pygame.image.load(UNDO).convert_alpha()
    user = pygame.image.load(USER).convert_alpha()
    playAgain = pygame.image.load(AGAIN).convert_alpha()
    ai = pygame.image.load(AI).convert_alpha()
    you = pygame.image.load(YOU).convert_alpha()
    me = pygame.image.load(ME).convert_alpha()
    nothing = pygame.image.load(NOTHING).convert_alpha()
    escape = pygame.image.load(EXIT).convert_alpha()
    pygame.display.set_caption('RENJU')
    board = Board(width=width, height=height, n_in_row=n)
    board.init_board(start_player)
    # loading the initial screen
    screen.blit(background, (0, 0))  # 加载位图与设定起始坐标
    screen.blit(pane, (640, 0))
    count = 0
    pygame.display.update()

    # the game loop
    complete = False
    while True:
        pos = [0, 0]
        for event in pygame.event.get():
            # to quit when the user clicks the close button
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # handling the display when it is minimized
            if event.type == ACTIVEEVENT or event.type == 17:
                i = 0
                while i < len(HUMAN):
                    screen.blit(user, HUMAN[i])
                    pygame.display.update()
                    i = i + 1
                i = 0
                while i < len(COMPUTER):
                    screen.blit(ai, COMPUTER[i])
                    pygame.display.update()
                    i = i + 1
                    # we can detect the position where the player clicks
            if event.type == MOUSEBUTTONDOWN:
                pos = list(event.pos)
                flag = 0
                if pos[0] > 670 and pos[0] < 760 and pos[1] > 500 and pos[1] < 590:
                    del (HUMAN)
                    del (COMPUTER)
                    model()
                # quit to main menu
                if pos[0] > 790 and pos[0] < 940 and pos[1] > 400 and pos[1] < 476:
                    del (HUMAN)
                    del (COMPUTER)
                    pygame.quit()
                    initial()
                # save unfinished game
                if pos[0] > 790 and pos[0] < 940 and pos[1] > 500 and pos[1] < 590:
                    record(HUMAN, COMPUTER)
                    initial()

                if (count % 2 == 0):  # black
                    # #undo move
                    if pos[0] > 640 and pos[0] < 960 and pos[1] > 25 and pos[1] < 90 and not complete and count>2:
                        # if undo move is available and enabled then
                        # When player already win, screw undo.
                        x1,x2 = HUMAN[len(HUMAN) - 1]
                        y1,y2 = COMPUTER[len(COMPUTER) - 1]
                        move1 = board.location_to_move([(x1 - 20) // 40, (x2 - 20) // 40])
                        move2 = board.location_to_move([(y1 - 20) // 40, (y2 - 20) // 40])
                        board.undo_move(move1)
                        board.undo_move(move2)
                        del (HUMAN[len(HUMAN) - 1])
                        del (COMPUTER[len(COMPUTER) - 1])
                        count = count - 2

                        i = 0
                        while i < len(HUMAN):
                            screen.blit(user, HUMAN[i])
                            pygame.display.update()
                            i = i + 1
                        i = 0
                        while i < len(COMPUTER):
                            screen.blit(ai, COMPUTER[i])
                            pygame.display.update()
                            i = i + 1
                    #make move
                    if pos[0] > 20 and pos[0] < 620 and pos[1] > 20 and pos[1] < 620 and not complete:
                        flag = 1
                    # finding the position at which the stones are to be placed
                    if flag == 1:
                        X = pos[0] - pos[0] % 40
                        if pos[0] % 40 > 40 - pos[0] % 40:
                            X = X + 40
                        X = X - 20
                        Y = pos[1] - pos[1] % 40
                        if pos[1] % 40 > 40 - pos[1] % 40:
                            Y = Y + 40
                        Y = Y - 20
                        # checking if the move is valid
                        j = 0
                        while j < len(HUMAN):
                            if X == HUMAN[j][0] and Y == HUMAN[j][1]:
                                flag = 0
                                break
                            j = j + 1
                        j = 0
                        while j < len(COMPUTER):
                            if X == COMPUTER[j][0] and Y == COMPUTER[j][1]:
                                flag = 0
                                break
                            j = j + 1
                    # appending the coin to the human player
                    if flag == 1:
                        screen.blit(me, (650, 400))
                        pygame.mixer.music.load(luozi)
                        pygame.mixer.music.play()
                        HUMAN.append((X, Y))
                        move = board.location_to_move([(X - 20) // 40, (Y - 20) // 40])
                        board.do_move(move)
                        i = 0
                        while i < len(HUMAN):
                            screen.blit(user, HUMAN[i])
                            pygame.display.update()
                            i = i + 1
                        i = 0
                        while i < len(COMPUTER):
                            screen.blit(ai, COMPUTER[i])
                            pygame.display.update()
                            i = i + 1
                        temp = 0
                        temp = judge(X,Y,HUMAN)
                        lose = RMD(X,Y,HUMAN)
                        # declaring the winner
                        if lose:
                            with open('history.txt', 'a') as file:
                                file.write('{} {}\n'.format('AlphaGoZero', len(COMPUTER)))

                            screen.blit(nothing, (650, 400))
                            screen.blit(lost, (640, 87))
                            screen.blit(escape, (790, 500))
                            screen.blit(playAgain, (670, 500))
                            pygame.mixer.music.load(losee)
                            pygame.mixer.music.play()
                            i = 0
                            while i < len(HUMAN):
                                screen.blit(user, HUMAN[i])
                                pygame.display.update()
                                i = i + 1
                            i = 0
                            while i < len(COMPUTER):
                                screen.blit(ai, COMPUTER[i])
                                pygame.display.update()
                                i = i + 1
                            pygame.display.update()
                            complete = True
                        elif temp == 1:
                            window = tkinter.Tk()
                            window.wm_attributes('-topmost', 1)
                            window.title('Enter your name')
                            window.geometry('350x80')
                            e = tkinter.Entry(window)
                            e.pack()

                            name = []

                            def shutdown(name):
                                name.append(e.get())
                                if name[-1] != "":
                                    window.destroy()

                            b = tkinter.Button(window, text='Enter', width=15, height=2, command=lambda: shutdown(name))
                            b.pack()
                            window.mainloop()

                            with open('history.txt', 'a') as file:
                                file.write('{} {}\n'.format(name[-1], len(HUMAN)))

                            screen.blit(nothing, (650, 400))
                            screen.blit(win, (640, 87))
                            screen.blit(escape, (790, 500))
                            screen.blit(playAgain, (670, 500))
                            pygame.mixer.music.load(winn)
                            pygame.mixer.music.play()
                            i = 0
                            while i < len(HUMAN):
                                screen.blit(user, HUMAN[i])
                                pygame.display.update()
                                i = i + 1
                            i = 0
                            while i < len(COMPUTER):
                                screen.blit(ai, COMPUTER[i])
                                pygame.display.update()
                                i = i + 1
                            pygame.display.update()
                            complete = True
                        count = count + 1
                # the computer player

                if (count % 2 == 1) and not complete:
                    # if not complete:
                    #     flag = 1
                    if flag == 1:
                        move = mcts_player.get_action(board)
                        board.do_move(move)
                        react=board.move_to_location(move)
                        react[0] = react[0]*40+20
                        react[1] = react[1] * 40 + 20
                        X,Y=react[0],react[1]
                        # checking if the move is valid
                        j = 0
                        while j < len(HUMAN):
                            if X == HUMAN[j][0] and Y == HUMAN[j][1]:
                                flag = 0
                                break
                            j = j + 1
                        j = 0
                        while j < len(COMPUTER):
                            if X == COMPUTER[j][0] and Y == COMPUTER[j][1]:
                                flag = 0
                                break
                            j = j + 1

                    if flag == 1:
                        COMPUTER.append((X, Y))
                        pygame.mixer.music.load(luozi)
                        pygame.mixer.music.play()
                        screen.blit(you, (650, 400))
                        pygame.display.update()
                        i = 0
                        while i < len(HUMAN):
                            screen.blit(user, HUMAN[i])
                            pygame.display.update()
                            i = i + 1
                        i = 0
                        while i < len(COMPUTER):
                            screen.blit(ai, COMPUTER[i])
                            pygame.display.update()
                            i = i + 1
                        X = COMPUTER[len(COMPUTER) - 1][0]
                        Y = COMPUTER[len(COMPUTER) - 1][1]
                        # checking after each step if any of the player has done five in a line
                        temp = 0
                        # SEARCHING FOR FIVES
                        # HORIZONTAL
                        temp=judge(X,Y,COMPUTER)

                        if temp == 1:
                            with open('history.txt', 'a') as file:
                                file.write('{} {}\n'.format("AlphaGoZero", len(COMPUTER)))

                            screen.blit(nothing, (650, 400))
                            screen.blit(lost, (640, 87))
                            screen.blit(escape, (790, 500))
                            screen.blit(playAgain, (670, 500))
                            # pygame.mixer.music.load(winn)
                            # pygame.mixer.music.play()
                            pygame.mixer.music.load(losee)
                            pygame.mixer.music.play()
                            i = 0
                            while i < len(HUMAN):
                                screen.blit(user, HUMAN[i])
                                pygame.display.update()
                                i = i + 1
                            i = 0
                            while i < len(COMPUTER):
                                screen.blit(ai, COMPUTER[i])
                                pygame.display.update()
                                i = i + 1
                            pygame.display.update()
                            complete = True
                        count = count + 1

                screen.blit(background, (0, 0))


# player to player
def p2p(u):

    enabled = False
    undo = 1
    s = 1
    # reading the board theme
    fread = open('info\\theme.txt', 'r')  # 读取棋盘主题
    default = "images\\" + fread.readline()
    fread.close()
    bif = default
    USER = "images\\noir.png"
    AI = "images\\blanc.png"
    # loading ingame images
    i_icon = "images\icon.png"
    EXIT = "images\exit.png"
    PANE = "images\pane.jpg"
    ABOUT = "images\\about.png"
    WIN = "images\win.png"
    LOSE = "images\lost.png"
    YOU = "images\you.png"
    ME = "images\me.png"
    UNDO = "images\disabled.png"
    AGAIN = "images\\again.png"
    NOTHING = "images\waste.png"
    # initializing the arrays
    HUMAN = []
    COMPUTER = []
    pygame.init()
    #pygame.mixer.init()
    # drawing the images on display surface
    icon = pygame.image.load(i_icon)
    pygame.display.set_icon(icon)  # 设置窗口图标
    # setting the screen to 960 x 640 resolution
    screen = pygame.display.set_mode((960, 640), 0, 32)  # 返回一个surface对象
    # loading the background and stone images
    background = pygame.image.load(bif).convert()  # 加载位图，bif主题图
    pane = pygame.image.load(PANE).convert()
    about = pygame.image.load(ABOUT).convert_alpha()
    win = pygame.image.load(WIN).convert_alpha()
    lost = pygame.image.load(LOSE).convert_alpha()
    no_undo = pygame.image.load(UNDO).convert_alpha()
    user = pygame.image.load(USER).convert_alpha()
    playAgain = pygame.image.load(AGAIN).convert_alpha()
    ai = pygame.image.load(AI).convert_alpha()
    you = pygame.image.load(YOU).convert_alpha()
    me = pygame.image.load(ME).convert_alpha()
    nothing = pygame.image.load(NOTHING).convert_alpha()
    escape = pygame.image.load(EXIT).convert_alpha()
    pygame.display.set_caption('RENJU')
    # loading the initial screen
    screen.blit(background, (0, 0))  # 加载位图与设定起始坐标
    screen.blit(pane, (640, 0))
    # the first move (for new game)
    HUMAN.append((300, 300))
    screen.blit(user, (300, 300))
    screen.blit(me, (650, 400))
    count = 1
    pygame.display.update()

    # the game loop
    complete = False
    while True:
        pos = [0, 0]
        for event in pygame.event.get():
            # to quit when the user clicks the close button
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # handling the display when it is minimized
            if event.type == ACTIVEEVENT or event.type == 17:
                i = 0
                while i < len(HUMAN):
                    screen.blit(user, HUMAN[i])
                    pygame.display.update()
                    i = i + 1
                i = 0
                while i < len(COMPUTER):
                    screen.blit(ai, COMPUTER[i])
                    pygame.display.update()
                    i = i + 1
                    # we can detect the position where the player clicks
            if event.type == MOUSEBUTTONDOWN:
                pos = list(event.pos)
                flag = 0
                # restart game
                if pos[0] > 670 and pos[0] < 760 and pos[1] > 500 and pos[1] < 590:
                    pygame.quit()
                    del (HUMAN)
                    del (COMPUTER)
                    p2p(1)
                # quit to main menu
                if pos[0] > 790 and pos[0] < 940 and pos[1] > 400 and pos[1] < 476:
                    pygame.quit()
                    del (HUMAN)
                    del (COMPUTER)
                    pygame.quit()
                    initial()
                # save unfinished game
                if pos[0] > 790 and pos[0] < 940 and pos[1] > 500 and pos[1] < 590:
                    record(HUMAN, COMPUTER)
                    pygame.quit()
                    initial()
                # The operation can only be processed when AI finished it's move.

                if (count % 2 == 0):  # black
                    # undo move
                    if pos[0] > 640 and pos[0] < 960 and pos[1] > 25 and pos[1] < 90 and count > 2 and not complete:
                        del (COMPUTER[len(COMPUTER) - 1])
                        count = count - 1

                        i = 0
                        while i < len(HUMAN):
                            screen.blit(user, HUMAN[i])
                            pygame.display.update()
                            i = i + 1
                        i = 0
                        while i < len(COMPUTER):
                            screen.blit(ai, COMPUTER[i])
                            pygame.display.update()
                            i = i + 1
                    # make move
                    if pos[0] > 20 and pos[0] < 620 and pos[1] > 20 and pos[1] < 620 and not complete:
                        flag = 1
                    # finding the position at which the stones are to be placed
                    if flag == 1:
                        X = pos[0] - pos[0] % 40
                        if pos[0] % 40 > 40 - pos[0] % 40:
                            X = X + 40
                        X = X - 20
                        Y = pos[1] - pos[1] % 40
                        if pos[1] % 40 > 40 - pos[1] % 40:
                            Y = Y + 40
                        Y = Y - 20
                        # checking if the move is valid
                        j = 0
                        while j < len(HUMAN):
                            if X == HUMAN[j][0] and Y == HUMAN[j][1]:
                                flag = 0
                                break
                            j = j + 1
                        j = 0
                        while j < len(COMPUTER):
                            if X == COMPUTER[j][0] and Y == COMPUTER[j][1]:
                                flag = 0
                                break
                            j = j + 1
                    # appending the coin to the human player
                    if flag == 1:
                        screen.blit(me, (650, 400))
                        pygame.mixer.music.load(luozi)
                        pygame.mixer.music.play()
                        HUMAN.append((X, Y))
                        i = 0
                        while i < len(HUMAN):
                            screen.blit(user, HUMAN[i])
                            pygame.display.update()
                            i = i + 1
                        i = 0
                        while i < len(COMPUTER):
                            screen.blit(ai, COMPUTER[i])
                            pygame.display.update()
                            i = i + 1
                        temp = 0
                        # checking after each step if the player has done five in a line
                        # SEARCHING FOR FIVES
                        # HORIZONTAL
                        # Check the rest chess, see if we got another four chess in a line.
                        temp = judge(X, Y, HUMAN)
                        lose = RMD(X, Y, HUMAN)

                        if lose:
                            window = tkinter.Tk()
                            window.wm_attributes('-topmost', 1)
                            window.title('Enter your name')
                            window.geometry('350x80')
                            e = tkinter.Entry(window)
                            e.pack()

                            name = []

                            def shutdown(name):
                                name.append(e.get())
                                if name[-1] != "":
                                    window.destroy()

                            b = tkinter.Button(window, text='Enter', width=15, height=2, command=lambda: shutdown(name))
                            b.pack()
                            window.mainloop()

                            with open('history.txt', 'a') as file:
                                file.write('{} {}\n'.format(name[-1], len(COMPUTER)))

                            screen.blit(nothing, (650, 400))
                            screen.blit(lost, (640, 87))
                            screen.blit(escape, (790, 500))
                            screen.blit(playAgain, (670, 500))
                            pygame.mixer.music.load(losee)
                            pygame.mixer.music.play()
                            i = 0
                            while i < len(HUMAN):
                                screen.blit(user, HUMAN[i])
                                pygame.display.update()
                                i = i + 1
                            i = 0
                            while i < len(COMPUTER):
                                screen.blit(ai, COMPUTER[i])
                                pygame.display.update()
                                i = i + 1
                            pygame.display.update()
                            complete = True
                        # declaring the winner
                        elif temp == 1:
                            window = tkinter.Tk()
                            window.wm_attributes('-topmost', 1)
                            window.title('Enter your name')
                            window.geometry('350x80')
                            e = tkinter.Entry(window)
                            e.pack()

                            name = []

                            def shutdown(name):
                                name.append(e.get())

                                if name[-1] != "":
                                    window.destroy()

                            b = tkinter.Button(window, text='Enter', width=15, height=2, command=lambda: shutdown(name))
                            b.pack()
                            window.mainloop()

                            with open('history.txt', 'a') as file:
                                file.write('{} {}\n'.format(name[-1], len(HUMAN)))

                            screen.blit(nothing, (650, 400))
                            screen.blit(win, (640, 87))
                            screen.blit(escape, (790, 500))
                            screen.blit(playAgain, (670, 500))
                            pygame.mixer.music.load(winn)
                            pygame.mixer.music.play()
                            i = 0
                            while i < len(HUMAN):
                                screen.blit(user, HUMAN[i])
                                pygame.display.update()
                                i = i + 1
                            i = 0
                            while i < len(COMPUTER):
                                screen.blit(ai, COMPUTER[i])
                                pygame.display.update()
                                i = i + 1
                            pygame.display.update()
                            complete = True
                        count = count + 1
                # the computer player

                else:
                    # undo move
                    if pos[0] > 640 and pos[0] < 960 and pos[1] > 25 and pos[1] < 90 and count > 2 and not complete:
                        del (HUMAN[len(HUMAN) - 1])
                        count = count - 1


                        i = 0
                        while i < len(HUMAN):
                            screen.blit(user, HUMAN[i])
                            pygame.display.update()
                            i = i + 1
                        i = 0
                        while i < len(COMPUTER):
                            screen.blit(ai, COMPUTER[i])
                            pygame.display.update()
                            i = i + 1
                    # the other player
                    if pos[0] > 20 and pos[0] < 620 and pos[1] > 20 and pos[1] < 620 and not complete:
                        flag = 1
                    # finding the position at which the stones are to be placed
                    if flag == 1:

                        X = pos[0] - pos[0] % 40
                        if pos[0] % 40 > 40 - pos[0] % 40:
                            X = X + 40
                        X = X - 20
                        Y = pos[1] - pos[1] % 40
                        if pos[1] % 40 > 40 - pos[1] % 40:
                            Y = Y + 40
                        Y = Y - 20
                        # checking if the move is valid
                        j = 0
                        while j < len(HUMAN):
                            if X == HUMAN[j][0] and Y == HUMAN[j][1]:
                                flag = 0
                                break
                            j = j + 1
                        j = 0
                        while j < len(COMPUTER):
                            if X == COMPUTER[j][0] and Y == COMPUTER[j][1]:
                                flag = 0
                                break
                            j = j + 1

                    if flag == 1:
                        COMPUTER.append((X, Y))
                        pygame.mixer.music.load(luozi)
                        pygame.mixer.music.play()
                        screen.blit(you, (650, 400))
                        pygame.display.update()
                        i = 0
                        while i < len(HUMAN):
                            screen.blit(user, HUMAN[i])
                            pygame.display.update()
                            i = i + 1
                        i = 0
                        while i < len(COMPUTER):
                            screen.blit(ai, COMPUTER[i])
                            pygame.display.update()
                            i = i + 1
                        X = COMPUTER[len(COMPUTER) - 1][0]
                        Y = COMPUTER[len(COMPUTER) - 1][1]
                        # checking after each step if any of the player has done five in a line
                        temp = 0
                        temp = judge(X, Y, COMPUTER)
                        # declaring the winner
                        if temp == 1:
                            window = tkinter.Tk()
                            window.wm_attributes('-topmost', 1)
                            window.title('Enter your name')
                            window.geometry('350x80')
                            e = tkinter.Entry(window)
                            e.pack()

                            name = []

                            def shutdown(name):
                                name.append(e.get())
                                if name[-1] !="":
                                    window.destroy()

                            b = tkinter.Button(window, text='Enter', width=15, height=2, command=lambda: shutdown(name))
                            b.pack()
                            window.mainloop()
                            with open('history.txt', 'a') as file:
                                file.write('{} {}\n'.format(name[-1], len(COMPUTER)))

                            screen.blit(nothing, (650, 400))
                            screen.blit(lost, (640, 87))
                            screen.blit(escape, (790, 500))
                            screen.blit(playAgain, (670, 500))
                            pygame.mixer.music.load(losee)
                            pygame.mixer.music.play()
                            i = 0
                            while i < len(HUMAN):
                                screen.blit(user, HUMAN[i])
                                pygame.display.update()
                                i = i + 1
                            i = 0
                            while i < len(COMPUTER):
                                screen.blit(ai, COMPUTER[i])
                                pygame.display.update()
                                i = i + 1
                            pygame.display.update()
                            complete = True
                        count = count + 1

                screen.blit(background, (0, 0))

# online game
def onlineGame(port=8080):
    host = '58.87.117.109'
    csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    csocket.connect((host, port))
    csocket.sendall(("Request").encode("utf8"))
    rep = csocket.recv(1024)
    user = rep.decode('UTF-8', 'ignore')
    rep = csocket.recv(1024)
    if rep.decode('UTF-8', 'ignore') == "clear":
        model_(user, csocket)

def model_(u, csoc):
    enabled = False
    u = int(u)

    if u == 1:
        u = 0
    elif u == 0:
        u = 1

    s = 1
    # reading the board theme
    fread = open('info\\theme.txt', 'r')
    default = "images\\" + fread.readline()
    fread.close()
    bif = default
    # if u = 0 then white otherwise black
    if u == 1:
        USER = "images\\noir.png"
        AI = "images\\blanc.png"

    elif u == 0:
        USER = "images\\blanc.png"
        AI = "images\\noir.png"
    # loading ingame images
    i_icon = "images\icon.png"
    EXIT = "images\exit.png"
    PANE = "images\pane_on.jpg"
    #ABOUT = "images\\about.png"
    WIN = "images\win.png"
    LOSE = "images\lost.png"
    YOU = "images\you.png"
    ME = "images\me.png"
    UNDO = "images\disabled.png"
    AGAIN = "images\\again.png"
    NOTHING = "images\waste.png"
    # initializing the arrays
    HUMAN = []
    COMPUTER = []
    pygame.init()
    # drawing the images on display surface
    icon = pygame.image.load(i_icon)
    pygame.display.set_icon(icon)
    # setting the screen to 960 x 640 resolution
    screen = pygame.display.set_mode((960, 640), 0, 32)
    # loading the background and stone images
    background = pygame.image.load(bif).convert()
    pane = pygame.image.load(PANE).convert()
    #about = pygame.image.load(ABOUT).convert_alpha()
    win = pygame.image.load(WIN).convert_alpha()
    lost = pygame.image.load(LOSE).convert_alpha()
    no_undo = pygame.image.load(UNDO).convert_alpha()
    user = pygame.image.load(USER).convert_alpha()
    playAgain = pygame.image.load(AGAIN).convert_alpha()
    ai = pygame.image.load(AI).convert_alpha()
    you = pygame.image.load(YOU).convert_alpha()
    me = pygame.image.load(ME).convert_alpha()
    nothing = pygame.image.load(NOTHING).convert_alpha()
    escape = pygame.image.load(EXIT).convert_alpha()
    pygame.display.set_caption('RENJU')
    # loading the initial screen
    screen.blit(background, (0, 0))
    screen.blit(pane, (640, 0))
    screen.blit(no_undo, (640, 25))
    # the first move (for new game)
    if u == 1:
        csoc.sendall(("300,300").encode("utf8"))
        HUMAN.append((300, 300))
        screen.blit(user, (300, 300))
        screen.blit(me, (650, 400))
        count = 1
    elif u == 0:
        count = 1
        p2_tmp = csoc.recv(1024)
        p2_x1, p2_x2 = p2_tmp.decode("UTF-8", 'ignore').split(',')[0], p2_tmp.decode("UTF-8", 'ignore').split(',')[1]
        COMPUTER.append((int(p2_x1), int(p2_x2)))
        screen.blit(ai, (int(p2_x1), int(p2_x2)))
        screen.blit(you, (650, 400))

    pygame.display.update()

    # the game loop
    complete = False
    while True:
        pos = [0, 0]
        for event in pygame.event.get():
            # to quit when the user clicks the close button
            if event.type == QUIT:
                # csoc.sendall(("%d"%u).encode("utf8"))
                pygame.quit()
                sys.exit()
            # handling the display when it is minimized
            if event.type == ACTIVEEVENT or event.type == 17:
                i = 0
                while i < len(HUMAN):
                    screen.blit(user, HUMAN[i])
                    pygame.display.update()
                    i = i + 1
                i = 0
                while i < len(COMPUTER):
                    screen.blit(ai, COMPUTER[i])
                    pygame.display.update()
                    i = i + 1
                    # we can detect the position where the player clicks
            if event.type == MOUSEBUTTONDOWN:
                pos = list(event.pos)
                flag = 0
                # restart game
                if pos[0] > 670 and pos[0] < 760 and pos[1] > 500 and pos[1] < 590:
                    del (HUMAN)
                    del (COMPUTER)
                    onlineGame()
                # quit to main menu
                if pos[0] > 790 and pos[0] < 940 and pos[1] > 400 and pos[1] < 476:
                    del (HUMAN)
                    del (COMPUTER)
                    pygame.quit()
                    select()
                # save unfinished game
                if pos[0] > 790 and pos[0] < 940 and pos[1] > 500 and pos[1] < 590:
                    if u ==1:
                        record(HUMAN, COMPUTER)
                    else:
                        record(COMPUTER, HUMAN)
                    initial()

                # The operation can only be processed when OP finished it's move.
                if (count % 2 == 1 and u == 0) or (count % 2 == 0 and u == 1):

                    # make move
                    if pos[0] > 20 and pos[0] < 620 and pos[1] > 20 and pos[1] < 620 and not complete:
                        flag = 1
                    # finding the position at which the stones are to be placed
                    if flag == 1:

                        X = pos[0] - pos[0] % 40
                        if pos[0] % 40 > 40 - pos[0] % 40:
                            X = X + 40
                        X = X - 20
                        Y = pos[1] - pos[1] % 40
                        if pos[1] % 40 > 40 - pos[1] % 40:
                            Y = Y + 40
                        Y = Y - 20
                        # checking if the move is valid
                        j = 0
                        while j < len(HUMAN):
                            if X == HUMAN[j][0] and Y == HUMAN[j][1]:
                                flag = 0
                                break
                            j = j + 1
                        j = 0
                        while j < len(COMPUTER):
                            if X == COMPUTER[j][0] and Y == COMPUTER[j][1]:
                                flag = 0
                                break
                            j = j + 1
                    # appending the coin to the human player
                    if flag == 1:
                        screen.blit(me, (650, 400))
                        HUMAN.append((X, Y))
                        csoc.sendall(("{},{}".format(X, Y)).encode("utf8"))
                        i = 0
                        while i < len(HUMAN):
                            screen.blit(user, HUMAN[i])
                            pygame.display.update()
                            i = i + 1
                        i = 0
                        while i < len(COMPUTER):
                            screen.blit(ai, COMPUTER[i])
                            pygame.display.update()
                            i = i + 1
                        temp = 0
                        # checking after each step if the player has done five in a line
                        # SEARCHING FOR FIVES
                        # HORIZONTAL
                        # Check the rest chess, see if we got another four chess in a line.
                        temp = judge(X, Y, HUMAN)
                        # declaring the winner
                        if temp == 1:
                            csoc.shutdown(socket.SHUT_RDWR)
                            csoc.close()
                            screen.blit(nothing, (650, 400))
                            screen.blit(win, (640, 87))
                            screen.blit(escape, (790, 500))
                            screen.blit(playAgain, (670, 500))
                            i = 0
                            while i < len(HUMAN):
                                screen.blit(user, HUMAN[i])
                                pygame.display.update()
                                i = i + 1
                            i = 0
                            while i < len(COMPUTER):
                                screen.blit(ai, COMPUTER[i])
                                pygame.display.update()
                                i = i + 1
                            pygame.display.update()
                            complete = True
                        count = count + 1
            # the computer player
            if ((count % 2 == 0 and u == 0) or (count % 2 == 1 and u == 1)) and not complete:
                p2_tmp = csoc.recv(1024)
                p2_x1, p2_x2 = p2_tmp.decode("UTF-8", 'ignore').split(',')[0], \
                               p2_tmp.decode("UTF-8", 'ignore').split(',')[1]
                COMPUTER.append((int(p2_x1), int(p2_x2)))
                screen.blit(you, (650, 400))
                pygame.display.update()
                i = 0
                while i < len(HUMAN):
                    screen.blit(user, HUMAN[i])
                    pygame.display.update()
                    i = i + 1
                i = 0
                while i < len(COMPUTER):
                    screen.blit(ai, COMPUTER[i])
                    pygame.display.update()
                    i = i + 1
                X = COMPUTER[len(COMPUTER) - 1][0]
                Y = COMPUTER[len(COMPUTER) - 1][1]
                # checking after each step if any of the player has done five in a line
                temp = 0
                temp = judge(X, Y, COMPUTER)
                # declaring the winner
                if temp == 1:
                    csoc.sendall(("done").encode("utf8"))
                    csoc.shutdown(socket.SHUT_RDWR)
                    csoc.close()
                    screen.blit(nothing, (650, 400))
                    screen.blit(lost, (640, 87))
                    screen.blit(escape, (790, 500))
                    screen.blit(playAgain, (670, 500))
                    i = 0
                    while i < len(HUMAN):
                        screen.blit(user, HUMAN[i])
                        pygame.display.update()
                        i = i + 1
                    i = 0
                    while i < len(COMPUTER):
                        screen.blit(ai, COMPUTER[i])
                        pygame.display.update()
                        i = i + 1
                    pygame.display.update()
                    complete = True
                count = count + 1
        screen.blit(background, (0, 0))

# select window
def select():
    user = 0
    undo = 0
    pygame.init()
    OPTIONS = "images\Choose.png"
    WINDOW1 = pygame.display.set_mode((660, 390))
    pygame.display.set_caption("RENJU")
    icon = pygame.image.load(i_icon)
    options = pygame.image.load(OPTIONS).convert_alpha()
    WINDOW1.blit(options, (0, 0))
    pygame.display.set_icon(icon)
    while True:
        pos = [0, 0]
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pos = list(event.pos)
                # local game
                if pos[0] < 230 and pos[0] > 70 and pos[1] > 110 and pos[1] < 220:
                    #pygame.quit()
                    p2p(1)
                # online game
                if pos[0] < 640 and pos[0] > 450 and pos[1] > 110 and pos[1] < 220:
                    #pygame.quit()
                    onlineGame()
                # theme
                if pos[0] < 165 and pos[0] > 35 and pos[1] > 295 and pos[1] < 345:
                    fread = open('info\\theme.txt', 'r')
                    prev = fread.readline()
                    fread.close()
                    img = list(prev)
                    img[4] = str((int(img[4]) + 1) % 7)
                    fwrite = open('info\\theme.txt', 'w')
                    i = 0
                    while i < len(img):
                        fwrite.writelines(img[i])
                        i = i + 1
                    fwrite.close()
                if pos[0] < 620 and pos[0] > 500 and pos[1] > 300 and pos[1] < 350:
                    if flag2 == 1:
                        background = pygame.image.load(mode).convert()
                        WINDOW1.blit(background, (0, 0))
                    if flag2 == 2:
                        background = pygame.image.load(mode).convert()
                        WINDOW1.blit(background, (0, 0))
                        musicb = pygame.image.load(button).convert_alpha()
                        WINDOW1.blit(musicb, (98, 150))
                    initial()
        pygame.display.update()

def help():
    pygame.init()
    HELP = "images\Help.png"
    WINDOW1 = pygame.display.set_mode((660, 390))
    pygame.display.set_caption("RENJU")
    icon = pygame.image.load(i_icon)
    help = pygame.image.load(HELP).convert_alpha()
    WINDOW1.blit(help, (0, 0))
    pygame.display.set_icon(icon)
    while True:
        pos = [0, 0]
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pos = list(event.pos)
                # local game
                if pos[0] < 600 and pos[0] > 520 and pos[1] > 345 and pos[1] < 378:
                    initial()
        pygame.display.update()

def initial():
    i_icon = "images\icon.png"
    mode = "images\selectmode.png"
    pygame.init()
    icon = pygame.image.load(i_icon)

    # music flags
    flag1 = 0
    #pygame.init()
    pygame.mixer.init()
    WINDOW1 = pygame.display.set_mode((660, 390))
    pygame.display.set_caption("RENJU")
    pygame.display.set_icon(icon)
    background = pygame.image.load(mode).convert()
    WINDOW1.blit(background, (0, 0))
    musicb = pygame.image.load(button).convert_alpha()
    WINDOW1.blit(musicb, (98, 150))

    while True:
        pos = [0, 0]
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                # coordinate of [x,y]
                pos = list(event.pos)
                # bgm
                if pos[0] > 92 and pos[0] < 132 and pos[1] > 142 and pos[1] < 182:

                    if flag1 == 0:
                        pygame.mixer.music.load(music)
                        pygame.mixer.music.play()
                        flag2 = 1
                        WINDOW1.blit(background, (0, 0))
                        pygame.display.update()
                    if flag1 == 1:
                        pygame.mixer.music.pause()
                        flag2 = 2
                        WINDOW1.blit(musicb, (98, 150))
                    if flag2 == 1:
                        flag1 = 1
                    if flag2 == 2:
                        flag1 = 0
                # player VS player
                if pos[0] > 300 and pos[0] < 584 and pos[1] > 4 and pos[1] < 60:
                    select()
                # player VS computer
                if pos[1] < 146 and pos[1] > 79 and pos[0] < 584 and pos[0] > 300:
                    model()

                # ranking list
                if pos[0] > 300 and pos[0] < 584 and pos[1] > 176 and pos[1] < 232:
                    root = tkinter.Tk()
                    root.wm_attributes('-topmost', 1)
                    tree = ttk.Treeview(root)
                    tree["columns"] = ("Username", "Score")
                    tree.column("Username", width=100)
                    tree.column("Score", width=100)

                    tree.heading("Username", text="Username")
                    tree.heading("Score", text="Score")

                    idx = 1
                    content = []
                    with open('history.txt', 'r') as file:
                        for line in file.readlines():
                            data = line.split()
                            data[1] = int(data[1])
                            content.append(data)
                            # tree.insert("", idx, text="{}".format(idx), values=("{}".format(data[0]), "{}".format(data[1])))
                            idx += 1

                        content.sort(key=lambda x: x[1])
                        for x in range(len(content)):
                            tree.insert("", x + 1, text="{}".format(x),
                                        values=("{}".format(content[x][0]), "{}".format(content[x][1])))

                    tree.pack()
                    root.mainloop()
                # resume last saved game
                if pos[0] > 300 and pos[0] < 584 and pos[1] > 249 and pos[1] < 316:
                    lists = []
                    with open('saved.txt', 'r') as file:
                        for line in file.readlines():
                            lists.append(line.split(' ')[0])

                    chosen = [x for x in range(1)]
                    win = tkinter.Tk()  # 构造窗体
                    win.wm_attributes('-topmost', 1)

                    def go(*args):
                        chosen[0] = comboxlist.get()
                        win.destroy()

                    comvalue = tkinter.StringVar()  # 窗体自带的文本，新建一个值
                    comboxlist = ttk.Combobox(win, textvariable=comvalue)  # 初始化
                    comboxlist["values"] = lists
                    comboxlist.bind("<<ComboboxSelected>>", go)
                    comboxlist.pack()



                    win.mainloop()  # 进入消息循环
                    if chosen[0] != 0:
                        idx = lists.index(chosen[0])
                        with open('saved.txt', 'r') as file:
                            line = file.readlines()
                            line = line[idx]

                        first = []
                        second = []
                        line = line.split(' ')[2:]
                        line[-1] = line[-1].strip('\n')
                        line = line[:-1]
                        for tmp in line:
                            if tmp.split('_')[0] == '1':
                                position = (int(tmp.split('_')[1]), int(tmp.split('_')[2]))
                                first.append(position)

                            else:
                                position = (int(tmp.split('_')[1]), int(tmp.split('_')[2]))
                                second.append(position)
                        fread = open('info\\theme.txt', 'r')  # 读取棋盘主题
                        default = "images\\" + fread.readline()
                        fread.close()
                        bif = default
                        USER = "images\\noir.png"
                        AI = "images\\blanc.png"
                        # loading ingame images
                        i_icon = "images\icon.png"
                        EXIT = "images\exit.png"
                        PANE = "images\pane_replay.jpg"
                        WIN = "images\win.png"
                        LOSE = "images\lost.png"
                        YOU = "images\you.png"
                        ME = "images\me.png"
                        NOTHING = "images\waste.png"
                        # initializing the arrays
                        HUMAN = first
                        COMPUTER = second
                        pygame.init()
                        # drawing the images on display surface
                        icon = pygame.image.load(i_icon)
                        pygame.display.set_icon(icon)  # 设置窗口图标
                        # setting the screen to 960 x 640 resolution
                        screen = pygame.display.set_mode((960, 640), 0, 32)  # 返回一个surface对象
                        # loading the background and stone images
                        background = pygame.image.load(bif).convert()  # 加载位图，bif主题图
                        pane = pygame.image.load(PANE).convert()
                        # about = pygame.image.load(ABOUT).convert_alpha()
                        win = pygame.image.load(WIN).convert_alpha()
                        lost = pygame.image.load(LOSE).convert_alpha()
                        # no_undo = pygame.image.load(UNDO).convert_alpha()
                        user = pygame.image.load(USER).convert_alpha()
                        # playAgain = pygame.image.load(AGAIN).convert_alpha()
                        ai = pygame.image.load(AI).convert_alpha()
                        you = pygame.image.load(YOU).convert_alpha()
                        me = pygame.image.load(ME).convert_alpha()
                        nothing = pygame.image.load(NOTHING).convert_alpha()
                        escape = pygame.image.load(EXIT).convert_alpha()
                        pygame.display.set_caption('RENJU')
                        # loading the initial screen
                        screen.blit(background, (0, 0))  # 加载位图与设定起始坐标
                        screen.blit(pane, (640, 0))

                        i = 0
                        j = 0
                        added=[]
                        '''
                        while i < len(HUMAN) or j < len(COMPUTER):
                            if (i < len(HUMAN)):
                                screen.blit(user, HUMAN[i])
                                pygame.display.update()
                                i = i + 1
                                time.sleep(1)
                            if (j < len(COMPUTER)):
                                screen.blit(ai, COMPUTER[j])
                                pygame.display.update()
                                j = j + 1
                                time.sleep(1)
                        '''
                        while i < len(HUMAN) or j < len(COMPUTER):
                            if (i < len(HUMAN)):
                                added.append(HUMAN[i])
                                i = i + 1
                            if (j < len(COMPUTER)):
                                added.append(COMPUTER[j])
                                j = j + 1

                        for x in range(len(added)):
                            if x %2==0:
                                screen.blit(user, added[x])
                                pygame.display.update()
                                time.sleep(1)
                            else:
                                screen.blit(ai, added[x])
                                pygame.display.update()
                                time.sleep(1)
                        while True:
                            pos = [0, 0]
                            for event in pygame.event.get():
                                if event.type == QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event.type == MOUSEBUTTONDOWN:
                                    pos = list(event.pos)
                                    # quit to main menu
                                    if pos[0] > 790 and pos[0] < 940 and pos[1] > 400 and pos[1] < 476:
                                        pygame.quit()
                                        initial()
                # Help
                if pos[0] > 300 and pos[0] < 584 and pos[1] > 334 and pos[1] < 390:
                    help()
        pygame.display.update()


initial()