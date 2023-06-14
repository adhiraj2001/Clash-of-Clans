from sys import exit
from os import system
from time import time, sleep

from art import text2art
from colorama import init, Fore, Back, Style
init()

from src.input import input_to
from src.village import Village


def menu():
    # Initialize the board
    system('clear')

    print(Fore.YELLOW + Back.BLACK + text2art("Clash of Clans") + Fore.RESET + Back.RESET)
    print(text2art("Rules:", font="cybermedium"))
    print()

    run = True
    start = True

    while run:
        print('Rules: ')
        print('1. Press P / p to start the game.')
        print('2. Press Q / q to exit the game.')
        print('3. Press W,A,S,D to control King / Queen.')
        print('4. Press ' ' to use attack with King / Queen.')
        print('5. Press Z,X,C to spawn Barbarians at different locations.')
        print('6. Press J,K,L to spawn Barbarians at different locations.')
        print('7. Press I,O,P to spawn Barbarians at different locations.')
        print('8. Press N to use Rage Spell and M to use Heal Spell.')
        print()

        text = input("Press 'p' to start or 'q' to quit: ")
        print()
        
        if text == "p" or text == "P":
            start = True
            run = False
        elif text == "q" or text == "Q":
            start = False
            run = False
        else:
            print('Invalid input. Please try again.')
            print()

            # time.sleep(1)

    system('clear')
    
    ch = 0
    run = True
    while run:
        print('Press 1 to play King')
        print('Press 2 to play Queen')
        print('Press 3 to quit')
        print()

        no = input("Enter: ")
        
        if no == '1':
            ch = 1
            run = False
        elif no == '2':
            ch = 2
            run = False
        elif no == '3':
            start = False
            run = False
        else:
            print('Invalid input. Please try again.')
            print()

            # time.sleep(1)

    return [start, ch]


def play(_ROWS, _COLS, _ch, _level):

    # Creating game object
    village = Village(_ROWS, _COLS, _ch, _level)

    start_time = time()

    while village.raid:
        
        # print("*" * 81)
        # print()

        #* The time difference between two frames / iterations of the game is due to INPUT_TO() timeout value.
        #* We are using 1s as the time interval between two frames.

        #! use this text everywhere in other parts of the code rather than calling it separately
        text = input_to()

        if(text == "q" or text == "Q"):
            break

        village.update(text)
        village.display(text)


    system('clear')

    if village.raid == 1:
        print(Fore.RED + Back.BLACK + text2art("Game Exited at Level: " + str(_level)) + Style.RESET_ALL)
        return False

        # print(list(village.board[village.cannons_list[1].x][village.cannons_list[1].y]))
        # print(getattr(Fore, "RED") + "Testing getattr" + Style.RESET_ALL)
    else:
        if village.building_count == 0:
            print(Fore.LIGHTYELLOW_EX + Back.BLACK + text2art("Victory at Level: " + str(_level)) + Style.RESET_ALL)
        else:
            print(Fore.RED + Back.BLACK + text2art("Defeated at Level: " + str(_level)) + Style.RESET_ALL)

        print("Time taken (seconds): ", str(time() - start_time))

        print("King's Health: ", max(village.king.health, 0))

        print("Barbarians remain: " + str(village.barbarian_alive))
        print("Archers remain: " + str(village.archer_alive))
        print("Balloons remain: " + str(village.balloon_alive))

        print("Buildings remaining: " + str(village.building_count))

        print("Rage Spells used: ", 2 - village.rage_count)
        print("Heal Spells used: ", 2 - village.heal_count)
        
        return (village.building_count == 0)

    return False


#* The time difference between two frames / iterations of the game is due to INPUT_TO() timeout value.

if __name__ == '__main__' :

    ROWS = 30
    COLS = 80

    # Initialize the board
    system('clear')

    [start, ch] = menu()

    if start == False:
        system('clear')

        print(Fore.RED + Back.BLACK + text2art("Game Exited") + Style.RESET_ALL)
        exit(1)

    for level in range(3):
        result = play(ROWS, COLS, ch, (level + 1))
        if result:
            sleep(3)
        else:
            break