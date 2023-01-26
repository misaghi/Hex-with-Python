from sys import maxsize
from random import shuffle, choice

from table import Table
from constants import *


class Main:

    def __init__(self, size) -> None:
        self.__table = Table(size)
        self.__values = [maxsize for i in range(size ** 2 + 1)] # Hold the heuristic values for each node
        self.__player_last_move = -1

    def ai_commit_move(self, opponent_color, agent_color):
        """
        AI commits move here. It finds the best cells of the opponent and chooses one that has the best value and 
        closes to the last player's move. If there are better moves which aren't local, they will be chosen.
        """
        self.__get_heuristics(opponent_color) # Find opponent's values
        if self.__player_last_move == -1: # AI started the game
            index = choice(range(1, len(self.__values)))
        else:
            candidate_moves = self.__table.find_candidate_moves(self.__player_last_move, opponent_color)
            candidate = maxsize
            shuffle(candidate_moves)
            # Choose nodes that are good for player (they have lower value)
            for i in range(len(candidate_moves)):
                if self.__values[candidate_moves[i]] < candidate:
                    candidate = self.__values[candidate_moves[i]]
                    index = candidate_moves[i]
            if candidate > min(self.__values[1:]): # Is the local choice the best or the global one?
                index = self.__values.index(min(self.__values[1:]))
        if self.__table.commit_move(index, agent_color):
            return True, index
        return False, -1
    
    def __get_heuristics(self, color):
        """
        Find heuristic values for nodes which aren't colored
        """
        v = dict() # For test purpose and does nothing
        for node in self.__table.nodes[1:]:
            if node.color != WHITE_INDICATOR: # Heuristic won't be calculated for colored nodes
                self.__values[node.number] = maxsize
                v[node.number] = maxsize
            else:
                value = self.__negamax(node, 6, -maxsize, maxsize, 1, color) # White nodes will get heuristic values
                self.__values[node.number] = value
                v[node.number] = value
        # print(v) # For test purpose and does nothing

    def check_game_finished(self):
        """
        Game is finished or not
        """
        for node in self.__table.nodes[1:]:
            if node.color != WHITE_INDICATOR:
                value = self.__table.get_heuristic_value(node.number, node.color)
                # print(node.number, value) # For debug purpose. Does nothing in the code
                if value == 1: # Game is finished if a colored node has a value of one which means we have a connection
                    return True # between two same colored sides of the table
        return False

    def player_commit_move(self, number, player_color):
        """
        Nothing special about this. If move can be commited, returns True; otherwise False.
        """
        if self.__table.commit_move(number, player_color):
            self.__player_last_move = number
            return True
        return False

    def __negamax(self, node, depth, alpha, beta, color, player_color):
        """
        Negamax uses alpha and beta to prune too good or too bad values in its search
        """
        if player_color == 'b':
            if depth == 0 or (node in self.__table.blue_nodes_terminals): # Red agents against blue player
                return color * self.__table.get_heuristic_value(node.number, player_color)
        else:
            if depth == 0 or (node in self.__table.red_nodes_terminals):
                return color * self.__table.get_heuristic_value(node.number, player_color) # Blue agent against red player
       
        neighbors = node.neighbors
        value = -maxsize
        for neighbor in neighbors:
            value = max(value, -self.__negamax(neighbor, depth - 1, -beta, -alpha, -color, player_color))
            alpha = max(alpha, value)
            if alpha >= beta:
                break # Pruning
        return value