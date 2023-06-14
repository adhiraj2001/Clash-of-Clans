from os import system
from time import time, sleep
from colorama import init, Fore, Back, Style
init()

#! This is a wrong fucking method idiot
# dx = [0, 1, 1, 1, 0, -1, -1, -1]
# dy = [1, 1, 0, -1, -1, -1, 0, 1]

b_speed = 1
b_dmg = 5
b_range = 1

b_full_health = 60
b_color = Fore.WHITE + Back.MAGENTA + Style.BRIGHT
b_text = 'B'

class Troops:
    def __init__(self, _x, _y, _speed, _dmg, _range, _full_health, _color, _text):
        self.x = _x
        self.y = _y

        self.speed = _speed
        self.dmg = _dmg
        self.range = _range

        self.full_health = _full_health
        self.health = self.full_health

        self.color = _color
        self.text = _text

        # self.color = Fore.WHITE + Back.MAGENTA + Style.BRIGHT


    def build(self, board):
        if min(self.x, self.y) > 0 and  self.x < len(board) - 1 and self.y < len(board[0]) - 1 and (board[self.x][self.y] == ' ' or (board[self.x][self.y][-5] in ['W', 'Q', 'K'])):
            board[self.x][self.y] = self.color + self.text + Style.RESET_ALL
        else:
            board[self.x][self.y] = Back.RED + 'WRONG' + Style.RESET_ALL


    def damage(self, board, dmg):
        if self.health <= 0:
            return

        self.health -= dmg

        if self.health >= self.full_health * 0.5:
            self.color = Fore.WHITE + Back.MAGENTA + Style.BRIGHT
        elif self.health > 0:
            self.color = Fore.LIGHTWHITE_EX + Back.LIGHTMAGENTA_EX + Style.DIM
        else:
            self.color = Fore.LIGHTWHITE_EX + Back.LIGHTRED_EX + Style.DIM

        board[self.x][self.y] = self.color + self.text + Style.RESET_ALL


    def attack(self, board, object):
        if self.health <= 0:
            return

        temp = board[self.x][self.y]
        board[self.x][self.y] = Fore.BLACK + Back.WHITE + Style.BRIGHT + self.text + Style.RESET_ALL

        system('clear')

        for i in range(len(board)):
            for j in range(len(board[0])):
                print(board[i][j], end='')
            print()
        
        # To show the change
        sleep(0.01)
        
        object.damage(board, self.dmg)

        board[self.x][self.y] = temp
        
    def check_range(self, board, walls, town_hall, huts, huts_list, cannons, cannons_list):
        # for k in range(self.range):
        #     min_dist = 3
        #     min_obj = None

        #     for i in dx:
        #         for j in dy:
        #             x1 = self.x + i * (k + 1)
        #             y1 = self.y + j * (k + 1)

        #             if min(x1, y1) <= 0 or x1 >= len(board) - 1 or y1 >= len(board[0]) - 1:
        #                 continue

        #             if len(board[x1][y1]) >= 5 and (board[x1][y1][-5] == 'C' or board[x1][y1][-5] == 'Γ') and min_dist > 0:
        #                 min_obj = cannons[x1][y1]
        #                 min_dist = 0
        #             elif len(board[x1][y1]) >= 5 and board[x1][y1][-5] == 'H' and min_dist > 1:
        #                 min_obj = town_hall
        #                 min_dist = 1
        #             elif len(board[x1][y1]) >= 5 and board[x1][y1][-5] == 'Δ' and min_dist > 2:
        #                 min_obj = huts[x1][y1]
        #                 min_dist = 2

        #     if min_dist < 3:
        #         self.attack(board, min_obj)
        #         return True

        # return False

        min_dist = self.range + 1
        min_wt = 3
        min_obj = None

        temp_x = self.x - self.range
        temp_y = self.y - self.range
        for i in range(self.range * 2 + 1):
            for j in range(self.range * 2 + 1):
                x1 = temp_x + i
                y1 = temp_y + j
                temp_dist = max(abs(self.x - x1), abs(self.y - y1))

                if min(x1, y1) <= 0 or x1 >= len(board) - 1 or y1 >= len(board[0]) - 1:
                    continue

                if len(board[x1][y1]) >= 5 and (board[x1][y1][-5] == 'C' or board[x1][y1][-5] == 'Γ') and (min_dist > temp_dist or (min_dist == temp_dist and min_wt > 0)):
                    min_obj = cannons[x1][y1]
                    min_dist = temp_dist
                    min_wt = 0

                elif len(board[x1][y1]) >= 5 and board[x1][y1][-5] == 'H' and (min_dist > temp_dist or (min_dist == temp_dist and min_wt > 1)):
                    min_obj = town_hall
                    min_dist = temp_dist
                    min_wt = 1

                elif len(board[x1][y1]) >= 5 and board[x1][y1][-5] == 'Δ' and (min_dist > temp_dist or (min_dist == temp_dist and min_wt > 2)):
                    min_obj = huts[x1][y1]
                    min_dist = temp_dist
                    min_wt = 2

        if min_dist <= self.range:
            self.attack(board, min_obj)
            return True

        return False
        
        # min_dist = self.range + 1
        # min_obj = None
        
        # for C in cannons_list:
        #     if C.health > 0:
        #         if min_dist > max(abs(self.x - C.x), abs(self.y - C.y)):
        #             min_dist = max(abs(self.x - C.x), abs(self.y - C.y))
        #             min_obj = C

        # if town_hall.health > 0:
        #     if min_dist > max(abs(self.x - town_hall.x), abs(self.y - town_hall.y)):
        #         min_dist = max(abs(self.x - town_hall.x), abs(self.y - town_hall.y))
        #         min_obj = town_hall

        # for H in huts_list:
        #     if H.health > 0:
        #         if min_dist > max(abs(self.x - H.x), abs(self.y - H.y)):
        #             min_dist = max(abs(self.x - H.x), abs(self.y - H.y))
        #             min_obj = H

        # if min_dist <= self.range:
        #     self.attack(board, min_obj)
        #     return True

        # return False

    def move(self, board, walls, town_hall, huts, huts_list, cannons, cannons_list):
        min_x = len(board)
        min_y = len(board[0])
        min_dist = len(board) + len(board[0])

        flag_cannon = False
        for C in cannons_list:
            if C.health > 0:
                # Only target cannons when in their range
                if min_dist >= max(abs(self.x - C.x), abs(self.y - C.y)) and max(abs(self.x - C.x), abs(self.y - C.y)) <= C.range:
                    min_dist = max(abs(self.x - C.x), abs(self.y - C.y))
                    min_x = C.x
                    min_y = C.y
                    flag_cannon = True


        if flag_cannon == False:
            if town_hall.health > 0 and min_dist >= abs(town_hall.x - self.x) + abs(town_hall.y - self.y):
                min_dist = abs(town_hall.x - self.x) + abs(town_hall.y - self.y)
                min_x = town_hall.x
                min_y = town_hall.y
                
            for i in range(len(huts_list)):
                if huts_list[i].health > 0 and min_dist >= abs(huts_list[i].x - self.x) + abs(huts_list[i].y - self.y):
                    min_dist = abs(huts_list[i].x - self.x) + abs(huts_list[i].y - self.y)
                    min_x = huts_list[i].x
                    min_y = huts_list[i].y


        temp_speed = min(self.speed, min_dist - 1)
        board[self.x][self.y] = ' '

        # Moving in the direction of the nearest object
        if abs(min_x - self.x) > abs(min_y - self.y):
            if min_x > self.x:
                flag = False
                for i in range(1, temp_speed):
                    if len(board[self.x + i][self.y]) >= 5 and board[self.x + i][self.y][-5] == 'W':
                        flag = True
                        temp_speed = i - 1
                        break

                if flag:
                    self.attack(board, walls[self.x + (temp_speed + 1)][self.y])

                self.x += temp_speed
            else:
                flag = False
                for i in range(1, temp_speed):
                    if len(board[self.x - i][self.y]) >= 5 and board[self.x - i][self.y][-5] == 'W':
                        flag = True
                        temp_speed = i - 1
                        break
                
                if flag:
                    self.attack(board, walls[self.x - (temp_speed + 1)][self.y])

                self.x -= temp_speed
        else:
            if min_y > self.y:
                flag = False
                for i in range(1, temp_speed):
                    if len(board[self.x][self.y + i]) >= 5 and board[self.x][self.y + i][-5] == 'W':
                        flag = True
                        temp_speed = i - 1
                        break

                if flag:
                    self.attack(board, walls[self.x][self.y + (temp_speed + 1)])

                self.y += temp_speed
            else:
                flag = False
                for i in range(1, temp_speed):
                    if len(board[self.x][self.y - i]) >= 5 and board[self.x][self.y - i][-5] == 'W':
                        flag = True
                        temp_speed = i - 1
                        break

                if flag:
                    self.attack(board, walls[self.x][self.y - (temp_speed + 1)])
                
                self.y -= temp_speed

        board[self.x][self.y] = self.color + self.text + Style.RESET_ALL

    def update(self, board, walls, town_hall, huts, huts_list, cannons, cannons_list):
        if self.health <= 0:
            return

        # check range function here
        flag_move = not self.check_range(board, walls, town_hall, huts, huts_list, cannons, cannons_list)

        if flag_move:
            self.move(board, walls, town_hall, huts, huts_list, cannons, cannons_list)


class Barbarian(Troops):
    def __init__(self, _x, _y):
        super().__init__(_x, _y, b_speed, b_dmg, b_range, b_full_health, b_color, b_text)


class Archer(Troops):
    def __init__(self, _x, _y):
        super().__init__(_x, _y, b_speed * 2, b_dmg / 2, b_range * 3, b_full_health / 2, b_color, 'A')
    

class Balloon(Troops):
    def __init__(self, _x, _y):
        super().__init__(_x, _y, 2 * b_speed, 2 * b_dmg,  b_range, b_full_health, b_color, 'O')
        self.curr_pos = ' '

    def check_range(self, board, walls, town_hall, huts, huts_list, cannons, cannons_list):
        min_dist = self.range + 1
        min_obj = None
        
        cannon_flag = False

        for C in cannons_list:
            if C.health > 0:
                cannon_flag = True
                if min_dist > max(abs(self.x - C.x), abs(self.y - C.y)):
                    min_dist = max(abs(self.x - C.x), abs(self.y - C.y))
                    min_obj = C

        if cannon_flag == False:
            if town_hall.health > 0:
                if min_dist > max(abs(self.x - town_hall.x), abs(self.y - town_hall.y)):
                    min_dist = max(abs(self.x - town_hall.x), abs(self.y - town_hall.y))
                    min_obj = town_hall

            for H in huts_list:
                if H.health > 0:
                    if min_dist > max(abs(self.x - H.x), abs(self.y - H.y)):
                        min_dist = max(abs(self.x - H.x), abs(self.y - H.y))
                        min_obj = H

        if min_dist <= self.range:
            self.attack(board, min_obj)
            return True

        return False

    def attack(self, board, object):
        if self.health <= 0:
            return

        temp = board[self.x][self.y]
        board[self.x][self.y] = Fore.BLACK + Back.WHITE + Style.BRIGHT + self.text + Style.RESET_ALL

        system('clear')

        for i in range(len(board)):
            for j in range(len(board[0])):
                print(board[i][j], end='')
            print()
        
        # To show the change
        sleep(0.01)
        
        object.damage(board, self.dmg)

        ## We want to replace with empty space when the bulding is dead my nibba
        if object.health <= 0 and len(self.curr_pos) >= 5 and self.curr_pos[-5] in ['H', 'Δ']:
            self.curr_pos = ' '

        board[self.x][self.y] = temp

    def move(self, board, walls, town_hall, huts, huts_list, cannons, cannons_list):
        min_x = len(board)
        min_y = len(board[0])
        min_dist = len(board) + len(board[0])

        flag_cannon = False
        for C in cannons_list:
            if C.health > 0:
                # Give priority to cannons
                if min_dist >= max(abs(self.x - C.x), abs(self.y - C.y)):
                    min_dist = max(abs(self.x - C.x), abs(self.y - C.y))
                    min_x = C.x
                    min_y = C.y
                    flag_cannon = True


        if flag_cannon == False:
            if town_hall.health > 0 and min_dist >= abs(town_hall.x - self.x) + abs(town_hall.y - self.y):
                min_dist = abs(town_hall.x - self.x) + abs(town_hall.y - self.y)
                min_x = town_hall.x
                min_y = town_hall.y
                
            for i in range(len(huts_list)):
                if huts_list[i].health > 0 and min_dist >= abs(huts_list[i].x - self.x) + abs(huts_list[i].y - self.y):
                    min_dist = abs(huts_list[i].x - self.x) + abs(huts_list[i].y - self.y)
                    min_x = huts_list[i].x
                    min_y = huts_list[i].y            


        temp_speed = min(self.speed, min_dist - 1)

        # board[self.x][self.y] = ' '

        board[self.x][self.y] = self.curr_pos

        # Moving in the direction of the nearest object
        if abs(min_x - self.x) > abs(min_y - self.y):
            if min_x > self.x:
                self.x += temp_speed
            else:
                self.x -= temp_speed
        else:
            if min_y > self.y:
                self.y += temp_speed
            else:
                self.y -= temp_speed

        if not (len(board[self.x][self.y]) >= 5 and board[self.x][self.y][-5] == 'O'):
            self.curr_pos = board[self.x][self.y]
        else:
            self.curr_pos = ' '

        board[self.x][self.y] = self.color + self.text + Style.RESET_ALL

 