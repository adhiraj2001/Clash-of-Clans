from os import system
from time import time, sleep
from colorama import init, Fore, Back, Style
init()

#! This is a wrong fucking method idiot
# dx = [0, 1, 1, 1, 0, -1, -1, -1]
# dy = [1, 1, 0, -1, -1, -1, 0, 1]
class King:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.speed = 1
        self.dmg = 20
        self.range = 3

        self.full_health = 250
        self.health = self.full_health

        self.color = Fore.BLACK + Back.YELLOW + Style.BRIGHT
        self.text = 'K'


    def build(self, board):
        if min(self.x, self.y) > 0 and  self.x < len(board) - 1 and self.y < len(board[0]) - 1 and board[self.x][self.y] == ' ':
            board[self.x][self.y] = self.color + self.text + Style.RESET_ALL
        else:
            board[self.x][self.y] = Back.RED + 'WRONG' + Style.RESET_ALL


    def damage(self, board, dmg):
        if self.health <= 0:
            return

        self.health -= dmg
        
        if self.health >= self.full_health * 0.5:
            self.color = Fore.BLACK + Back.YELLOW + Style.BRIGHT
        elif self.health > 0:
            self.color = Fore.LIGHTWHITE_EX + Back.LIGHTYELLOW_EX + Style.DIM
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


    def move(self, board, text):
        if self.health <= 0:
            return

        x1 = self.x
        y1 = self.y


        if text == 'w':
            x1 -= self.speed
        elif text == 's':
            x1 += self.speed
        elif text == 'a':
            y1 -= self.speed
        elif text == 'd':
            y1 += self.speed


        if min(x1, y1) > 0 and x1 < len(board) - 1 and y1 < len(board[0]) - 1 and (board[x1][y1] == ' ' or (board[x1][y1][-5] in ['B', 'A', 'O', 'K', 'Q'])):
            board[self.x][self.y] = ' '
            self.x = x1
            self.y = y1
            board[self.x][self.y] = self.color + self.text + Style.RESET_ALL



    def hit(self, board, walls, town_hall, huts, cannons):
        if self.health <= 0:
            return

        min_dist = self.range + 1
        min_wt = 4
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

                if len(board[x1][y1]) >= 5 and board[x1][y1][-5] == 'C' and (min_dist > temp_dist or (min_dist == temp_dist and min_wt > 0)):
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

                elif len(board[x1][y1]) >= 5 and board[x1][y1][-5] == 'W' and (min_dist > temp_dist or (min_dist == temp_dist and min_wt > 3)):
                    min_obj = walls[x1][y1]
                    min_dist = temp_dist
                    min_wt = 3

        if min_dist <= self.range:
            self.attack(board, min_obj)
            return True

        return False

class Archer_Queen(King):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.dmg = 15
        self.range = 5
        self.loc = 8
        
        self.full_health = 150
        self.health = self.full_health

        self.text = 'Q'
        self.color = Fore.BLACK + Back.MAGENTA + Style.BRIGHT
        self.dir = 0

    def move(self, board, text):
        if self.health <= 0:
            return

        x1 = self.x
        y1 = self.y


        if text == 'w':
            x1 -= self.speed
            self.dir = 0
        elif text == 's':
            x1 += self.speed
            self.dir = 1
        elif text == 'a':
            y1 -= self.speed
            self.dir = 2
        elif text == 'd':
            y1 += self.speed
            self.dir = 3

        if min(x1, y1) > 0 and x1 < len(board) - 1 and y1 < len(board[0]) - 1 and (board[x1][y1] == ' ' or (board[x1][y1][-5] in ['B', 'A', 'O', 'K', 'Q'])):
            board[self.x][self.y] = ' '

            self.x = x1
            self.y = y1

            board[self.x][self.y] = self.color + self.text + Style.RESET_ALL

    def hit(self, board, walls, town_hall, huts, cannons):
        if self.health <= 0:
            return

        temp_x = self.x
        temp_y = self.y

        if self.dir == 0:
            temp_x -= self.loc
            temp_x = max(temp_x, 0)
        elif self.dir == 1:
            temp_x += self.loc
            temp_x = min(temp_x, len(board) - 2)
        elif self.dir == 2:
            temp_y -= self.loc
            temp_y = max(temp_y, 0)
        elif self.dir == 3:
            temp_y += self.loc
            temp_y = min(temp_y, len(board[0]) - 2)
        
        # Dictionary of objects
        obj_dict = {}

        temp_x -= self.range
        temp_y -= self.range
        for i in range(self.range * 2 + 1):
            for j in range(self.range * 2 + 1):
                x1 = temp_x + i
                y1 = temp_y + j

                if min(x1, y1) <= 0 or x1 >= len(board) - 1 or y1 >= len(board[0]) - 1:
                    continue

                if len(board[x1][y1]) >= 5 and (board[x1][y1][-5] == 'C' or board[x1][y1][-5] == 'Γ'):
                    obj_dict[id(cannons[x1][y1])] = cannons[x1][y1]

                elif len(board[x1][y1]) >= 5 and board[x1][y1][-5] == 'H':
                    obj_dict[id(town_hall)] = town_hall

                elif len(board[x1][y1]) >= 5 and board[x1][y1][-5] == 'Δ':
                    obj_dict[id(huts[x1][y1])] = huts[x1][y1]

                elif len(board[x1][y1]) >= 5 and board[x1][y1][-5] == 'W':
                    obj_dict[id(walls[x1][y1])] = walls[x1][y1]
        

        flag_attack = False
        for key in obj_dict:
            self.attack(board, obj_dict[key])
            flag_attack = True

        return flag_attack