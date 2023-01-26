from main import Main
from constants import *

from os import system
from colorama import Fore

class ui:
    def __init__(self) -> None:
        # Returns the color of the current player
        self.__player = lambda x: Fore.RED + RED + Fore.RESET if x == RED_INDICATOR else Fore.BLUE + BLUE + Fore.RESET
        
    def start(self):
        """
        Starts the game
        """
        self.__menu()

    def __menu(self):
        while True:
            """
            Display's game menu
            """
            system('clear')
            print('_________________HEX!_________________\n\n')
            print('              1.Start!')
            print('             2.Credits!')
            print('               3.Exit\n\n')
            while True:
                print('Option:', end=' ')
                option = input()
                if option == '1':
                    self.__prepare_game()
                    break
                elif option == '2':
                    self.__credits()
                    break
                elif option == '3':
                    self.__exit()
                    break
                else:
                    print('Invalid option!')

    def __initialize_game(self):
        # Some default values
        self.__game_mode = VSAI # Game mode defaults to play versus AI
        self.__player_color = RED_INDICATOR # Default player's color and AI's color
        self.__opponent_color = BLUE_INDICATOR
        self.__table_size = 7 # Default table size
        self.__nodes = ['#'] # To start nodes from 1. Table's cells. Filled with color or number
        self.__player_turn = True # Who will start the game?
        self.__winner = '' # The winner
    
    def __prepare_game(self):
        self.__initialize_game()
        system('clear')
        print('___________Prepare for Game!___________\n\n')
        while True: # Get the game mode
            print('Select mode:\n1.You Vs AI\n2.You Vs. Someone else\n\n')
            print('Option:', end=' ')
            option = input()
            if option == '1':
                self.__game_mode = VSAI
                break
            elif option == '2':
                self.__game_mode = VSHUMAN
                break
            else:
                print('Invalid option!\n')

        print('\n')
        while True: # Get colors
            print(f'Select your color:\n1.{Fore.RED}Red{Fore.RESET}\n2.{Fore.BLUE}Blue{Fore.RESET}\n\n')
            print('Option:', end=' ')
            option = input()
            if option == '1':
                self.__player_color = RED_INDICATOR
                self.__opponent_color = BLUE_INDICATOR
                break
            elif option == '2':
                self.__player_color = BLUE_INDICATOR
                self.__opponent_color = RED_INDICATOR
                break
            else:
                print('Invalid option!\n')

        print('\n')
        while True: # Who will start the game?
            print(f'Who will start first?\n1.You\n2.Your opponent\n\n')
            print('Option:', end=' ')
            option = input()
            if option == '1':
                self.__player_turn = True
                break
            elif option == '2':
                self.__player_turn = False
                break
            else:
                print('Invalid option!\n')

        print('\n')
        while True: # Get table size
            print('Enter game size (bigger than 1):', end=' ')
            try:
                size = int(input())
            except ValueError:
                print('Invalid size')
            else:
                if size > 1:
                    self.__table_size = size
                    break
                else:
                    print('Table size must be bigger than 1.\n')
        
        self.__main = Main(self.__table_size)
        self.__initial_nodes()
        if self.__game_mode == VSAI:
            self.__play_game_human_vs_ai()
            self.__finish_game()
        else:
            self.__play_game_human_vs_human()
            self.__finish_game()

    def __play_game_human_vs_ai(self):
        """
        Human vs AI
        """
        system('clear')
        print("______________Let's Play!______________\n\n")
        self.__draw_game()
        while True:
            while self.__player_turn: # Player's turn
                print(f'Pleaes enter your move {self.__player(self.__player_color)} player:', end=' ')
                try:
                    move = int(input())
                except ValueError:
                    print('Please enter a number!')
                else:
                    if move >= 1 and move <= self.__table_size ** 2:
                        if self.__main.player_commit_move(move, self.__player_color): # Move can be commited
                            self.__winner = self.__player_color
                            self.__nodes[move] = self.__color(self.__player_color)
                            self.__player_turn = False
                            system('clear')
                            print("______________Let's Play!______________\n\n")
                            self.__draw_game()
                        else:
                            print('Choice is already colored! Please choose another cell.')
                    else:
                        print('Please enter a valid number')
            if self.__main.check_game_finished(): # Check if the player is the winner
                break
            
            # AI's turn
            result, move = self.__main.ai_commit_move(self.__player_color, self.__opponent_color)
            if result:
                self.__winner = self.__opponent_color
                self.__nodes[move] = self.__color(self.__opponent_color)
                self.__player_turn = True
                system('clear')
                print("______________Let's Play!______________\n\n")
                self.__draw_game()
                print('AI move: ', move)
            if self.__main.check_game_finished():
                break
                

    def __play_game_human_vs_human(self):
        """
        Human vs Human
        """
        system('clear')
        print("______________Let's Play!______________\n\n")
        self.__draw_game()
        while True:
            while self.__player_turn: # Player's turn
                print(f'Pleaes enter your move {self.__player(self.__player_color)} player :', end=' ')
                try:
                    move = int(input())
                except ValueError:
                    print('Please enter a number!')
                else:
                    if move >= 1 and move <= self.__table_size ** 2:
                        if self.__main.player_commit_move(move, self.__player_color): # Move can be commited
                            self.__winner = self.__player_color
                            self.__nodes[move] = self.__color(self.__player_color)
                            self.__player_turn = False
                            system('clear')
                            print("______________Let's Play!______________\n\n")
                            self.__draw_game()
                        else:
                            print('Choice is already colored! Please choose another cell.')
                    else:
                        print('Please enter a valid number')
            if self.__main.check_game_finished():
                break
            
            # Other player's turn
            while not self.__player_turn: # Player's turn
                print(f'Pleaes enter your move {self.__player(self.__opponent_color)} player:', end=' ')
                try:
                    move = int(input())
                except ValueError:
                    print('Please enter a number!')
                else:
                    if move >= 1 and move <= self.__table_size ** 2:
                        if self.__main.player_commit_move(move, self.__opponent_color):
                            self.__winner = self.__opponent_color
                            self.__nodes[move] = self.__color(self.__opponent_color)
                            self.__player_turn = True
                            system('clear')
                            print("______________Let's Play!______________\n\n")
                            self.__draw_game()
                        else:
                            print('Choice is already colored! Please choose another cell.')
                    else:
                        print('Please enter a valid number')
            if self.__main.check_game_finished():
                break

    def __finish_game(self):
        """
        States winner and the final table; Also asks the player what to happen next
        """
        system('clear')
        print('___________Game is Finished!___________\n\n')
        self.__draw_game()
        if self.__winner == RED_INDICATOR: # Print the winner
            print(Fore.RED + RED.title() + Fore.RESET + ' is the winner!.\n')
        else:
            print(Fore.BLUE + BLUE.title() + Fore.RESET + ' is the winner!.\n')

        print('1.Play again\n or \n2.Return to the menu?\n\n')
        print('Option:', end=' ')
        while True:
            option = input()
            if option == '1':
                self.__prepare_game()
                break
            elif option == '2':
                break
            else:
                print('Invalid option!')


    def __initial_nodes(self):
        """
        Here we create nodes which will be shown to the user in the draw table.
        """
        base = 10
        power = 1
        while True: # Here a same length for all numbers will be found
            if self.__table_size ** 2 < base:
                break
            power += 1
            base = 10 ** power
        maxlen = len(str(base)) - 1 # All nodes' lenght
        if maxlen < 2: maxlen = 2 # Set the smallest cell's length to 2
        
        # A function to get the the filling table color easily
        self.__color = lambda x: Fore.RED + RED_INDICATOR * maxlen + Fore.RESET if x == RED_INDICATOR else Fore.BLUE + BLUE_INDICATOR * maxlen + Fore.RESET
        self.__cell_length = maxlen # Lenght of each cell

        for i in range(1, self.__table_size ** 2 + 1):
            self.__nodes.append('0' * (maxlen - len(str(i))))
            self.__nodes[i] += f'{i}'
    
    def __draw_game(self):
        """
        Draw game's board according to moves
        """
        base = 1
        print((self.__table_size * self.__cell_length + 5) * ' ' + Fore.BLUE + ' B' + Fore.RED + 'R' + Fore.RESET)
        for depth in range(1, self.__table_size * 2):
            if depth > self.__table_size: # drawing rows bigger than self.__table_size
                number_of_nodes_in_the_row = self.__table_size * 2 - depth # How many cells are in this row?
                alphabet = Fore.RED + 'R  ' + Fore.RESET # Extra spaces to justify the table
                case = 'R'
            else: # Drawing rows smaller than self.__table_size
                # Every row has cells equal to its depth in depths which are smaller than table_size
                number_of_nodes_in_the_row = depth 
                if depth == self.__table_size: # adding BR for the depth == table_size
                    alphabet = Fore.BLUE + 'B' + Fore.RED + 'R ' + Fore.RESET # Extra spaces to justify the table
                    case = 'BR'
                else:
                    alphabet = Fore.BLUE + 'B  ' + Fore.RESET # Extra spaces to justify the table
                    case = 'B'
            spaces = abs(self.__table_size - depth) * self.__cell_length # Spaces which must be added before each row to justify the table
            row = (spaces + 5) * ' ' + alphabet # The +5 is for adjusting table to right a bit
            for j in range(number_of_nodes_in_the_row):
                row += f'{self.__nodes[base]}' + self.__cell_length * ' ' # Adding cells plus extra spaces
                base += 1
            row = row.rstrip()
            if case == 'BR': # Adding the other end's color indicator
                row += Fore.BLUE + ' B' + Fore.RED + 'R' + Fore.RESET
            elif case == 'B':
                row += Fore.RED + '  R' + Fore.RESET
            else:
                row += Fore.BLUE + '  B' + Fore.RESET
            print(row)
        print((self.__table_size * self.__cell_length + 5) * ' ' + Fore.RED + ' R' + Fore.BLUE + 'B' + Fore.RESET + '\n\n')
    
    def __credits(self):
        """
        Nothing special
        """
        system('clear')
        print('________________Credits________________\n\n')
        print('Hex By Seyyed Amirhosein Misaghi')
        print('This game was a project for AI course, University of Guilan.')
        print('Fall 1401\n\n')
        print('Please enter 1 to go back to the Menu:', end=' ')
        while True:
            option = input()
            if option == '1':
                break
            else:
                print('Invalid option!')

    def __exit(self):
        exit()


if __name__ == '__main__':
    game = ui()
    game.start()