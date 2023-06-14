from colorama import init, Fore, Back, Style
init()

class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.full_health = 30
        self.health = self.full_health


    def build(self, board):
        if min(self.x, self.y) > 0 and  self.x < len(board)-1 and self.y < len(board[0]) - 1 and board[self.x][self.y] == ' ':
            board[self.x][self.y] = Fore.BLACK + Back.WHITE + 'W' + Style.RESET_ALL
            

    def damage(self, board, attack):
        if self.health <= 0:
            return 
            
        self.health -= attack

        if self.health >= self.full_health * 0.5:
            self.color = Fore.WHITE + Back.MAGENTA + Style.BRIGHT
        elif self.health > 0:
            self.color = Fore.LIGHTWHITE_EX + Back.LIGHTMAGENTA_EX + Style.DIM
        else:
            board[self.x][self.y] = ' '
            