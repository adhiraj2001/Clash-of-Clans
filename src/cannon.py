from os import system
from time import time, sleep
from colorama import init, Fore, Back, Style
init()


class Cannon:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.full_health = 50
        self.health = self.full_health

        self.dmg = 6
        self.range = 5
        
        self.color = Fore.WHITE + Back.BLUE + Style.BRIGHT
        self.text = 'C'


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
            self.color = Fore.WHITE + Back.BLUE + Style.BRIGHT
        elif self.health > 0:
            self.color = Fore.LIGHTWHITE_EX + Back.LIGHTBLUE_EX + Style.DIM

        if self.health > 0:
            board[self.x][self.y] = self.color + self.text + Style.RESET_ALL
        else:
            board[self.x][self.y] = ' '


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

        dist = max(abs(self.x - object.x), abs(self.y - object.y), 1)

        # object.damage(board, self.dmg // dist)
        object.damage(board, self.dmg)

        board[self.x][self.y] = temp
         

    def update(self, board, king, barbarians_list):
        if self.health <= 0:
            return

        min_bar = None
        min_dist = self.range + 1

        if king.health > 0 and self.range >= max(abs(self.x - king.x), abs(self.y - king.y)) and min_dist > max(abs(self.x - king.x), abs(self.y - king.y)):
            min_dist = max(abs(self.x - king.x), abs(self.y - king.y))
            min_bar = king


        for B in barbarians_list:
            if B.health > 0 and (B.text != 'O') and self.range >= max(abs(self.x - B.x), abs(self.y - B.y)) and min_dist > max(abs(self.x - B.x), abs(self.y - B.y)):
                min_dist = max(abs(self.x - B.x), abs(self.y - B.y))
                min_bar = B

        if min_dist <= self.range:
            self.attack(board, min_bar)


class Wizard_Tower(Cannon):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.full_health = 70
        self.health = self.full_health

        self.color = Fore.WHITE + Back.CYAN + Style.BRIGHT
        self.text = 'Γ'

        self.rows = 2
        self.cols = 1

        self.range2 = 3

    def build(self, board):
        flag_can_build = True

        for i in range(self.rows):
            for j in range(self.cols):
                flag_can_build &= (min(self.x + i, self.y + j) > 0 and self.x + i < len(board) - 1 and self.y + j < len(board[0]) - 1 and board[self.x+i][self.y+j] == ' ')

        if flag_can_build:
            for i in range(self.rows):
                for j in range(self.cols):
                    board[self.x+i][self.y+j] = self.color + self.text + Style.RESET_ALL
        else:
            board[self.x][self.y] = Back.RED + 'WRONG' + Style.RESET_ALL

    def damage(self, board, dmg):
        if self.health <= 0:
            return

        self.health -= dmg
        
        if self.health >= self.full_health * 0.5:
            self.color = Fore.WHITE + Back.CYAN + Style.BRIGHT
        elif self.health > 0:
            self.color = Fore.LIGHTWHITE_EX + Back.LIGHTBLUE_EX + Style.DIM

        if self.health <= 0:
            for i in range(self.rows):
                for j in range(self.cols):
                    board[self.x+i][self.y+j] = ' '
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    board[self.x+i][self.y+j] = self.color + self.text + Style.RESET_ALL

    def attack(self, board, object):
        if self.health <= 0:
            return
    
        temp = board[self.x][self.y]
        
        for i in range(self.rows):
                for j in range(self.cols):
                    board[self.x+i][self.y+j] = Fore.BLACK + Back.WHITE + Style.BRIGHT + self.text + Style.RESET_ALL

        system('clear')

        for i in range(len(board)):
            for j in range(len(board[0])):
                print(board[i][j], end='')
            print()

        # To show the change
        sleep(0.01)

        dist = max(abs(self.x - object.x), abs(self.y - object.y), 1)

        # object.damage(board, self.dmg // dist)
        object.damage(board, self.dmg)

        for i in range(self.rows):
                for j in range(self.cols):
                    board[self.x+i][self.y+j] = temp

    def update(self, board, king, barbarians_list):
        if self.health <= 0:
            return

        min_bar = None
        min_dist = self.range + 1

        if king.health > 0 and self.range >= max(abs(self.x - king.x), abs(self.y - king.y)) and min_dist > max(abs(self.x - king.x), abs(self.y - king.y)):
            min_dist = max(abs(self.x - king.x), abs(self.y - king.y))
            min_bar = king


        for B in barbarians_list:
            if B.health > 0 and self.range >= max(abs(self.x - B.x), abs(self.y - B.y)) and min_dist > max(abs(self.x - B.x), abs(self.y - B.y)):
                min_dist = max(abs(self.x - B.x), abs(self.y - B.y))
                min_bar = B

        if min_dist > self.range:
            return

        if king.health > 0 and self.range2 >= max(abs(min_bar.x - king.x), abs(min_bar.y - king.y)):
            self.attack(board, king)


        for B in barbarians_list:
            if B.health > 0 and self.range2 >= max(abs(min_bar.x - B.x), abs(min_bar.y - B.y)):
                self.attack(board, B)