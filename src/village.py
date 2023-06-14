from os import system
from time import time, sleep

import numpy as np

from colorama import init, Fore, Back, Style
init()

##! DONT USE init(reset=True) IN YOUR CODE => Slows down printing by a lot

from src.building import TownHall, Hut
from src.wall import Wall
from src.cannon import Cannon, Wizard_Tower
from src.troops import Barbarian, Archer, Balloon
from src.king import King, Archer_Queen


class Village:
    def __init__(self, rows, cols, ch, level):
        
        self.raid = True
        
        self.rows = rows
        self.cols = cols

        self.board = np.full((self.rows + 2, self.cols + 2), ' ', dtype='<U20')

        # Initialize Board
        self.board[0, :] = Back.BLACK + '+' + Style.RESET_ALL
        self.board[self.rows+1, :] = Back.BLACK + '+' + Style.RESET_ALL

        self.board[:, 0] = Back.BLACK + '+' + Style.RESET_ALL
        self.board[:, self.cols+1] = Back.BLACK + '+' + Style.RESET_ALL

        self.walls = [[None for i in range(self.cols + 2)] for j in range(self.rows + 2)]
        
        for i in range(1, self.rows+1):
            self.walls[i][self.cols // 4] = Wall(i, self.cols // 4)
            self.walls[i][self.cols // 4].build(self.board)

            self.walls[i][self.cols * 3 // 4] = Wall(i, self.cols * 3 // 4)
            self.walls[i][self.cols * 3 // 4].build(self.board)

        for j in range(1, self.cols + 1):
            self.walls[self.rows // 4][j] = Wall(self.rows // 4, j)
            self.walls[self.rows // 4][j].build(self.board)

            self.walls[self.rows * 3 // 4][j] = Wall(self.rows * 3 // 4, j)
            self.walls[self.rows * 3 // 4][j].build(self.board)

        
        
        self.building_count = 6
        
        # Town Hall

        self.town_hall = TownHall(self.rows // 2 - 1, self.cols // 2 - 1)
        self.town_hall.build(self.board)


        # Huts 

        self.huts = [[None for i in range(self.cols + 2)] for j in range(self.rows + 2)]
        self.huts_list = []

        x = self.rows // 8
        y = self.cols // 2

        temp = Hut(x, y)
        temp.build(self.board)
        self.huts_list.append(temp)
        
        for i in range(2):
            for j in range(2):
                self.huts[x+i][y+j] = temp

        x = self.rows // 2
        y = self.cols // 8

        temp = Hut(x, y)
        temp.build(self.board)
        self.huts_list.append(temp)
        
        for i in range(2):
            for j in range(2):
                self.huts[x+i][y+j] = temp

        x = self.rows // 2
        y = self.cols * 7 // 8

        temp = Hut(x, y)
        temp.build(self.board)
        self.huts_list.append(temp)
        
        for i in range(2):
            for j in range(2):
                self.huts[x+i][y+j] = temp

        x = self.rows * 7 // 8
        y = self.cols // 8

        temp = Hut(x, y)
        temp.build(self.board)
        self.huts_list.append(temp)
        
        for i in range(2):
            for j in range(2):
                self.huts[x+i][y+j] = temp

        x = self.rows * 7 // 8
        y = self.cols * 7 // 8

        temp = Hut(x, y)
        temp.build(self.board)
        self.huts_list.append(temp)
        
        for i in range(2):
            for j in range(2):
                self.huts[x+i][y+j] = temp


        # Cannons 

        self.cannon_count = 3
        self.cannons = [[None for i in range(self.cols + 2)] for j in range(self.rows + 2)]
        self.cannons_list = []

        if level >= 1:
            temp1 = Cannon(self.rows // 16, self.cols // 2)
            temp1.build(self.board)

            self.cannons[self.rows // 16][self.cols // 2] = temp1 
            self.cannons_list.append(temp1)


            temp1 = Cannon(self.rows * 3 // 8, self.cols // 2)
            temp1.build(self.board)

            self.cannons[self.rows * 3 // 8][self.cols // 2] = temp1 
            self.cannons_list.append(temp1)

        if level >= 1:
            x1 = self.rows // 2
            y1 = self.cols // 16

            temp1 = Wizard_Tower(x1, y1)
            temp1.build(self.board)
            self.cannons_list.append(temp1)

            for i in range(temp1.rows):
                for j in range(temp1.cols):
                    self.cannons[x1 + i][y1 + j] = temp1 


            x2 = self.rows * 5 // 8
            y2 = self.cols * 3 // 8

            temp2 = Wizard_Tower(x2, y2)
            temp2.build(self.board)
            self.cannons_list.append(temp2)

            for i in range(temp2.rows):
                for j in range(temp2.cols):
                    self.cannons[x2 + i][y2 + j] = temp2

        if level >= 2:
            x1 = self.rows * 5 // 8
            y1 = self.cols * 5 // 8

            temp1 = Wizard_Tower(x1, y1)
            temp1.build(self.board)
            self.cannons_list.append(temp1)

            for i in range(temp1.rows):
                for j in range(temp1.cols):
                    self.cannons[x1 + i][y1 + j] = temp1 

        if level >= 3:
            x1 = self.rows // 2
            y1 = self.cols * 15 // 16

            temp1 = Wizard_Tower(x1, y1)
            temp1.build(self.board)
            self.cannons_list.append(temp1)

            for i in range(temp1.rows):
                for j in range(temp1.cols):
                    self.cannons[x1 + i][y1 + j] = temp1 

        if level >= 2:
            temp1 = Cannon(self.rows * 7 // 8, self.cols // 16)
            temp1.build(self.board)

            self.cannons[self.rows * 7 // 8][self.cols // 16] = temp1 
            self.cannons_list.append(temp1)

        if level >= 3:
            temp1 = Cannon(self.rows * 7 // 8, self.cols * 15 // 16)
            temp1.build(self.board)

            self.cannons[self.rows * 7 // 8][self.cols * 15 // 16] = temp1 
            self.cannons_list.append(temp1)


        # Barbarians
        
        self.barbarian_alive = 6
        self.barbarian_deploy = 6

        self.archer_alive = 6
        self.archer_deploy = 6

        self.balloon_alive = 3
        self.balloon_deploy = 3

        self.barbarians_list = []

        self.king_alive = True

        if ch == 1:
            self.king = King(self.rows * 7 // 8, self.cols // 2)
        elif ch == 2:
            self.king = Archer_Queen(self.rows * 7 // 8, self.cols // 2)

        self.king.build(self.board)

        self.rage_count = 2
        self.heal_count = 2


    def rage_spell(self):
        if self.king.health > 0:
            self.king.dmg *= 2

        for B in self.barbarians_list:
            if B.health > 0:
                B.dmg *= 2
                B.speed *= 2

    def heal_spell(self):
        if self.king.health > 0:
            self.king.health = min(self.king.health * 1.5, self.king.full_health)
        
        for B in self.barbarians_list:
            if B.health > 0:
                B.health = min(B.health * 1.5, B.full_health)


    def update(self, text):
            
        if self.barbarian_deploy > 0:
            if text == 'z':
                temp = Barbarian(self.rows // 8, self.cols // 8)
                temp.build(self.board)

                self.barbarians_list.append(temp)
                self.barbarian_deploy -= 1
            
            if text == 'x':
                temp = Barbarian(self.rows // 8, self.cols * 7 // 8)
                temp.build(self.board)

                self.barbarians_list.append(temp)
                self.barbarian_deploy -= 1

            if text == 'c':
                temp = Barbarian(self.rows * 7 // 8, self.cols // 2)
                temp.build(self.board)

                self.barbarians_list.append(temp)
                self.barbarian_deploy -= 1

        if self.archer_deploy > 0:
            if text == 'j':
                temp = Archer(self.rows // 8, self.cols // 8)
                temp.build(self.board)

                self.barbarians_list.append(temp)
                self.archer_deploy -= 1
            
            if text == 'k':
                temp = Archer(self.rows // 8, self.cols * 7 // 8)
                temp.build(self.board)

                self.barbarians_list.append(temp)
                self.archer_deploy -= 1

            if text == 'l':
                temp = Archer(self.rows * 7 // 8, self.cols // 2)
                temp.build(self.board)

                self.barbarians_list.append(temp)
                self.archer_deploy -= 1

        if self.balloon_deploy > 0:
            if text == 'i':
                temp = Balloon(self.rows // 8, self.cols // 8)
                temp.build(self.board)

                self.barbarians_list.append(temp)
                self.balloon_deploy -= 1
            
            if text == 'o':
                temp = Balloon(self.rows // 8, self.cols * 7 // 8)
                temp.build(self.board)

                self.barbarians_list.append(temp)
                self.balloon_deploy -= 1

            if text == 'p':
                temp = Balloon(self.rows * 7 // 8, self.cols // 2)
                temp.build(self.board)

                self.barbarians_list.append(temp)
                self.balloon_deploy -= 1

        if text == 'n' and self.rage_count > 0:
            self.rage_spell()
            self.rage_count -= 1

        if text == 'm' and self.heal_count > 0:
            self.heal_spell()
            self.heal_count -= 1

        if text == ' ':
            self.king.hit(self.board, self.walls, self.town_hall, self.huts, self.cannons)


        if self.king.health > 0:
            self.king.move(self.board, text)
        elif self.king_alive:
            self.king_alive = False

        for B in self.barbarians_list:
            if B.health > 0:
                B.update(self.board, self.walls, self.town_hall, self.huts, self.huts_list, self.cannons, self.cannons_list)
            else:
                if B.text == 'B':
                    self.barbarian_alive -= 1
                elif B.text == 'A':
                    self.archer_alive -= 1
                elif B.text == 'O':
                    self.balloon_alive -= 1

                self.barbarians_list.remove(B)

        for C in self.cannons_list:
            if C.health > 0:
                C.update(self.board, self.king, self.barbarians_list)
            else:
                self.cannon_count -= 1
                self.cannons_list.remove(C)


        if self.town_hall.is_ok and self.town_hall.health <= 0:
            self.town_hall.is_ok = False
            self.building_count -= 1

        for H in self.huts_list:
            if H.health <= 0:
                self.building_count -= 1
                self.huts_list.remove(H)

        if self.king_alive and self.king.health <= 0:
            self.king_alive = False


        if self.building_count == 0:
            self.raid = False

        if self.barbarian_alive + self.archer_alive + self.balloon_alive == 0 and self.king_alive == False:
            self.raid = False


    def display(self, text=""):

        system('clear')

        for i in range(self.rows+2):
            for j in range(self.cols+2):
                print(self.board[i][j], end='')
            print()

        print('King Health Left: ', max(self.king.health, 0), end=' | ')

        print('Barbarians Deployed:', self.barbarian_deploy, end=' | ')
        print('Archers Deployed:', self.archer_deploy, end=' | ')
        print('Balloons Deployed:', self.balloon_deploy)
        
        print('Rage Spells Left:', self.rage_count, end=' | ')
        print('Heal Spells Left:', self.heal_count)

        # for i in range(self.rows+2):
        #     print(*self.board[i], sep='')


