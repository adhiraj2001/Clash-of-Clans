from colorama import init, Fore, Back, Style
init()

class Building:
    def __init__(self, x, y, rows, cols, text, health):
        self.x = x
        self.y = y
        self.rows = rows
        self.cols = cols
        self.text = text

        self.full_health = health
        self.health = self.full_health
        self.color = 'GREEN'


    def build(self, board):
        flag_can_build = True

        for i in range(self.rows):
            for j in range(self.cols):
                flag_can_build &= (min(self.x + i, self.y + j) > 0 and self.x + i < len(board) - 1 and self.y + j < len(board[0]) - 1 and board[self.x+i][self.y+j] == ' ')

        if flag_can_build:
            for i in range(self.rows):
                for j in range(self.cols):
                    board[self.x+i][self.y+j] = getattr(Back, self.color) + self.text + Style.RESET_ALL
        else:
            board[self.x][self.y] = Back.RED + 'WRONG' + Style.RESET_ALL


    def damage(self, board, attack):
        if self.health <= 0:
            return 
            
        self.health -= attack

        if self.health >= self.full_health * 0.5:
            self.color = 'GREEN'
        elif self.health >= self.full_health * 0.20:
            self.color = 'YELLOW'
        elif self.health > 0:
            self.color = 'RED'

        board[self.x][self.y] = getattr(Back, self.color) + self.text + Style.RESET_ALL

        if self.health <= 0:
            for i in range(self.rows):
                for j in range(self.cols):
                    board[self.x+i][self.y+j] = ' '
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    board[self.x+i][self.y+j] = getattr(Back, self.color) + self.text + Style.RESET_ALL


class TownHall(Building):
    def __init__(self, x, y):
        super().__init__(x, y, 4, 3, Fore.BLACK + 'H', 150)
        self.is_ok = True


class Hut(Building):
    def __init__(self, x, y):
        super().__init__(x, y, 2, 2, Fore.BLACK + 'Δ', 200)
     