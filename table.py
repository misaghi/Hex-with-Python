"""
    BR
   B  R
  B    R
BR      BR
  R    B
   R  B
    BR

"""


from sys import maxsize
from copy import deepcopy

from node import Node
from constants import *

class Table:

    def __init__(self, size) -> None:
        self.__table_size = size
        self.__nodes = ['#']
        self.__costs_reds = [[maxsize, True]] # Initializes like __nodes, so real cells start from 1
        self.__costs_blues = [[maxsize, True]]
        self.__edge_nodes_red_start = [] # Red terminals
        self.__edge_nodes_red_goal = []
        self.__edge_nodes_blue_start = [] # Blue terminals
        self.__edge_nodes_blue_goal = []

        for i in range(1, self.__table_size ** 2 + 1):
            n = Node(i)
                                # It's default cost, visited or not during Dijkstra search
            self.__costs_blues.append([n.cost_blue, False]) # A list of all nodes with their costs
            self.__costs_reds.append([n.cost_red, False]) # A list of all nodes with their costs
            self.__nodes.append(n)

        self.__set_neighbors()

    @property
    def blue_nodes_terminals(self):
        return self.__edge_nodes_blue_goal + self.__edge_nodes_blue_start

    @property
    def red_nodes_terminals(self):
        return self.__edge_nodes_red_goal + self.__edge_nodes_red_start

    @property
    def nodes(self):
        return self.__nodes

    def __set_neighbors(self):
        """
        Find all neighbors for current nodes
        """
        current_range_upper = 1
        current_range_lower = 0
        current_depth = 1
        for number in range(1, self.__table_size ** 2 + 1):
            if number > current_range_upper:
                current_range_lower = current_range_upper
                current_depth += 1
                if current_depth > self.__table_size:
                    current_range_upper += 2 * self.__table_size - current_depth # Nodes are decreasing before depth n
                else:
                    current_range_upper += current_depth # Nodes are increasing before depth n
            neighbors = []
            if number == 1:
                neighbors.extend([self.__nodes[number + 1], self.__nodes[number + 2]])
                self.__edge_nodes_blue_start.append(self.__nodes[number])
                self.__edge_nodes_red_start.append(self.__nodes[number])
            elif number == self.__table_size ** 2:
                neighbors.extend([self.__nodes[number - 1], self.__nodes[number - 2]])
                self.__edge_nodes_blue_goal.append(self.__nodes[number])
                self.__edge_nodes_red_goal.append(self.__nodes[number])
            elif number <= current_range_upper:
                # Neighbors
                if current_depth < self.__table_size:
                    # Every node before depth n will have two next level neighbors
                    neighbors.append(self.__nodes[number + current_depth])
                    neighbors.append(self.__nodes[number + current_depth + 1])
                    if number == current_range_upper:
                        # Node at the right edge of the table
                        neighbors.append(self.__nodes[number - current_depth])
                        neighbors.append(self.__nodes[number - 1])
                        self.__edge_nodes_red_start.append(self.__nodes[number])
                    elif number == current_range_lower + 1:
                        # Node at the left edge of the table
                        neighbors.append(self.__nodes[number - current_depth + 1])
                        neighbors.append(self.__nodes[number + 1])
                        self.__edge_nodes_blue_start.append(self.__nodes[number])
                    else:
                        # Node in the middle of the table
                        neighbors.append(self.__nodes[number - current_depth + 1])
                        neighbors.append(self.__nodes[number - current_depth])
                        neighbors.append(self.__nodes[number + 1])
                        neighbors.append(self.__nodes[number - 1])
                elif current_depth == self.__table_size:
                    # Node at depth n of the table
                    if number == current_range_upper:
                        # Node at the right corner of the table
                        neighbors.append(self.__nodes[number + current_depth - 1])
                        neighbors.append(self.__nodes[number - 1])
                        neighbors.append(self.__nodes[number - current_depth])
                        self.__edge_nodes_blue_goal.append(self.__nodes[number])
                        self.__edge_nodes_red_start.append(self.__nodes[number])
                    elif number == current_range_lower + 1:
                        # Node at the left corner of the table
                        neighbors.append(self.__nodes[number + current_depth])
                        neighbors.append(self.__nodes[number + 1])
                        neighbors.append(self.__nodes[number - (current_depth - 1)])
                        self.__edge_nodes_blue_start.append(self.__nodes[number])
                        self.__edge_nodes_red_goal.append(self.__nodes[number])
                    else:
                        # Node in the middle of the depth n
                        neighbors.append(self.__nodes[number + current_depth])
                        neighbors.append(self.__nodes[number + current_depth - 1])
                        neighbors.append(self.__nodes[number + 1])
                        neighbors.append(self.__nodes[number - 1])
                        neighbors.append(self.__nodes[number - current_depth])
                        neighbors.append(self.__nodes[number - (current_depth - 1)])
                else:
                    # Every node after depth n will have two lower level neighbors
                    neighbors.append(self.__nodes[number - (2 * self.__table_size - current_depth)])
                    neighbors.append(self.__nodes[number - (2 * self.__table_size - current_depth + 1)])
                    if number == current_range_upper:
                        # Node at the right edge of the table
                        neighbors.append(self.__nodes[number + 2 * self.__table_size - 1 - current_depth])
                        neighbors.append(self.__nodes[number - 1])
                        self.__edge_nodes_blue_goal.append(self.__nodes[number])
                    elif number == current_range_lower + 1:
                        # Node at the left edge of the table
                        neighbors.append(self.__nodes[number + 2 * self.__table_size - current_depth])
                        neighbors.append(self.__nodes[number + 1])
                        self.__edge_nodes_red_goal.append(self.__nodes[number])
                    else:
                        # Node in the middle of the table
                        neighbors.append(self.__nodes[number + 2 * self.__table_size - 1 - current_depth])
                        neighbors.append(self.__nodes[number + 2 * self.__table_size - current_depth])
                        neighbors.append(self.__nodes[number + 1])
                        neighbors.append(self.__nodes[number - 1])
            
            self.__nodes[number].neighbors = neighbors

    def find_candidate_moves(self, number, color): 
        """
        Agent's possible moves will be found here according to the player's move
        """
        current_range_upper = 1
        current_range_lower = 0
        current_depth = 1
        candidate_moves = set() # Eliminates repetitive numbers automatically

        # Find depth of the current node
        while True:
            if number > current_range_upper:
                current_range_lower = current_range_upper
                current_depth += 1
                if current_depth > self.__table_size:
                    current_range_upper += 2 * self.__table_size - current_depth # Nodes are decreasing before depth n
                else:
                    current_range_upper += current_depth # Nodes are increasing before depth n
            else:
                break

        for node in self.__nodes[number].neighbors: # Adding its own neighbors
            candidate_moves.add(node.number)
        
        if color == RED_INDICATOR:
            if current_depth < self.__table_size:
                # Next level neighbor's neighbors
                current_neighbor = self.__nodes[number + current_depth]
                for node in current_neighbor.neighbors:
                    candidate_moves.add(node.number)
                if number == current_range_upper:
                    # Node at the right edge of the table which has no desired previous neighbors
                    pass
                elif number == current_range_lower + 1:
                    # Node at the left edge of the table which has desired previous neighbors
                    current_neighbor = self.__nodes[number - current_depth + 1]
                    for node in current_neighbor.neighbors:
                        candidate_moves.add(node.number)
                else:
                    # Node in the middle of the table which has desired previous neighbors too
                    current_neighbor = self.__nodes[number - current_depth + 1]
                    for node in current_neighbor.neighbors:
                        candidate_moves.add(node.number)
            elif current_depth == self.__table_size:
                # Node at depth n of the table
                if number == current_range_upper:
                    # Node at the right corner of the table which has desired next neighbors
                    current_neighbor = self.__nodes[number + current_depth - 1]
                    for node in current_neighbor.neighbors:
                        candidate_moves.add(node.number)
                elif number == current_range_lower + 1:
                    # Node at the left corner of the table with desired previous neighbors
                    current_neighbor = self.__nodes[number - (current_depth - 1)]
                    for node in current_neighbor.neighbors:
                        candidate_moves.add(node.number)
                else:
                    # Node in the middle of the depth n. We assign both next and previous neighbors
                    current_neighbor = self.__nodes[number + current_depth - 1]
                    for node in current_neighbor.neighbors:
                        candidate_moves.add(node.number)
                    current_neighbor = self.__nodes[number - (current_depth - 1)]
                    for node in current_neighbor.neighbors:
                        candidate_moves.add(node.number)
            else:
                # These nodes all have previous neighbor which is needed
                current_neighbor = self.__nodes[number - (2 * self.__table_size - current_depth)]
                for node in current_neighbor.neighbors:
                    candidate_moves.add(node.number)
                if number == current_range_upper:
                    # Node at the right edge of the table and its needed next neighbor
                    current_neighbor = self.__nodes[number + 2 * self.__table_size - 1 - current_depth]
                    for node in current_neighbor.neighbors:
                        candidate_moves.add(node.number)
                elif number == current_range_lower + 1:
                    # Node at the left edge of the table, and no next neighbors
                    pass
                else:
                    # Node in the middle of the table. We add its next neighbors
                    current_neighbor = self.__nodes[number + 2 * self.__table_size - 1 - current_depth]
                    for node in current_neighbor.neighbors:
                        candidate_moves.add(node.number)
        else:
            if current_depth < self.__table_size:
                # Next level neighbor's neighbors
                current_neighbor = self.__nodes[number + current_depth + 1]
                for node in current_neighbor.neighbors:
                    candidate_moves.add(node.number)
                if number == current_range_upper:
                    # Node at the right edge of the table which has desired previous neighbors
                    current_neighbor = self.__nodes[number - current_depth]
                    for node in current_neighbor.neighbors:
                        candidate_moves.add(node.number)
                elif number == current_range_lower + 1:
                    # Node at the left edge of the table which has no desired previous neighbors
                    pass
                else:
                    # Node in the middle of the table which has desired previous neighbors too
                    current_neighbor = self.__nodes[number - current_depth]
                    for node in current_neighbor.neighbors:
                        candidate_moves.add(node.number)
            elif current_depth == self.__table_size:
                # Node at depth n of the table
                if number == current_range_upper:
                    # Node at the right corner of the table which has desired next neighbors
                    current_neighbor = self.__nodes[number - current_depth]
                    for node in current_neighbor.neighbors:
                        candidate_moves.add(node.number)
                elif number == current_range_lower + 1:
                    # Node at the left corner of the table with desired previous neighbors
                    current_neighbor = self.__nodes[number + current_depth]
                    for node in current_neighbor.neighbors:
                        candidate_moves.add(node.number)
                else:
                    # Node in the middle of the depth n. We assign both next and previous neighbors
                    current_neighbor = self.__nodes[number + current_depth]
                    for node in current_neighbor.neighbors:
                        candidate_moves.add(node.number)
                    current_neighbor = self.__nodes[number - current_depth]
                    for node in current_neighbor.neighbors:
                        candidate_moves.add(node.number)
            else:
                # These nodes all have previous neighbor which is needed
                current_neighbor = self.__nodes[number - (2 * self.__table_size - current_depth + 1)]
                for node in current_neighbor.neighbors:
                    candidate_moves.add(node.number)
                if number == current_range_upper:
                    # Node at the right edge of the table, and no next neighbors
                    pass
                elif number == current_range_lower + 1:
                    # Node at the left edge of the table and its needed next neighbor
                    current_neighbor = self.__nodes[number + 2 * self.__table_size - current_depth]
                    for node in current_neighbor.neighbors:
                        candidate_moves.add(node.number)
                else:
                    # Node in the middle of the table. We add its next neighbors
                    current_neighbor = self.__nodes[number + 2 * self.__table_size - current_depth]
                    for node in current_neighbor.neighbors:
                        candidate_moves.add(node.number)
        try:
            candidate_moves.remove(number) # Remove the player's current move which will be added to the set
        except KeyError:
            pass
        return list(candidate_moves)

    def commit_move(self, number, color):
        """
        Commit move if the node is white also make it unusable for opposite color
        """
        if self.__nodes[number].color == WHITE_INDICATOR:
            self.__nodes[number].color = color
            if color == BLUE_INDICATOR:
                self.__costs_reds[number] = [maxsize, True] # Sets 
            else:
                self.__costs_blues[number] = [maxsize, True] # This node will be ignored calculating blue nodes
            return True
        return False

    def __if_all_nodes_visited(self, l):
        """
        Check if all of the nodes are visited or not
        """
        for node in l[1:]:
            if not node[1]:
                return False
        return True

    # def get_heuristic_value(self, number, agent_color):
    #     """
    #     Using Dijkstra shortest path from the current node (source which is the defined by number),
    #     find the shortest path to all other nodes and then find the minimum cost.
    #     """
    #     temp = [node[0] for node in self.__costs_blues]
    #     blues_heuristic = deepcopy(self.__costs_blues)
    #     temp[number] = 1
    #     blues_heuristic[number][0] = 1
    #     while not self.__if_all_nodes_visited(blues_heuristic):
    #         index = temp.index(min(temp)) # Find lowest cost node
    #         current_node = self.__nodes[index] # Find lowest cost node
    #         for neighbor in current_node.neighbors: # For all neighbors check if this path has the lowest cost or not
    #             if neighbor.color == 'w': # If that neighbor is white
    #                 if blues_heuristic[neighbor.number][0] > blues_heuristic[current_node.number][0] + 1:
    #                     blues_heuristic[neighbor.number][0] = blues_heuristic[current_node.number][0] + 1 # Update the costs list
    #             elif neighbor.color == 'b': # No cost if the neighbor has the same color
    #                 if blues_heuristic[neighbor.number][0] > blues_heuristic[current_node.number][0]:
    #                     blues_heuristic[neighbor.number][0] = blues_heuristic[current_node.number][0] # Update the costs list
    #             if not blues_heuristic[neighbor.number][1]:
    #                 temp[neighbor.number] = blues_heuristic[neighbor.number][0]

    #         blues_heuristic[index][1] = True # Node is visited
    #         temp[index] = maxsize # Node won't be chosen again
            
    #     temp = [node[0] for node in self.__costs_reds]
    #     reds_heuristic = deepcopy(self.__costs_reds)
    #     temp[number] = 1
    #     reds_heuristic[number][0] = 1
    #     while not self.__if_all_nodes_visited(reds_heuristic):
    #         index = temp.index(min(temp)) # Find lowest cost node
    #         current_node = self.__nodes[index] # Find lowest cost node
    #         for neighbor in current_node.neighbors: # For all neighbors check if this path has the lowest cost or not
    #             if neighbor.color == 'w': # If that neighbor is white
    #                 if reds_heuristic[neighbor.number][0] > reds_heuristic[current_node.number][0] + 1:
    #                     reds_heuristic[neighbor.number][0] = reds_heuristic[current_node.number][0] + 1 # Update the costs list
    #             elif neighbor.color == 'r': # No cost if the neighbor has the same color
    #                 if reds_heuristic[neighbor.number][0] > reds_heuristic[current_node.number][0]:
    #                     reds_heuristic[neighbor.number][0] = reds_heuristic[current_node.number][0] # Update the costs list
    #             if not reds_heuristic[neighbor.number][1]:
    #                 temp[neighbor.number] = reds_heuristic[neighbor.number][0]

    #         reds_heuristic[index][1] = True # Node is visited
    #         temp[index] = maxsize # Node won't be chosen again

    #     # Find the minimum path cost between blue sides of the table
    #     min_blue_start_value = maxsize
    #     for node in self.__edge_nodes_blue_start:
    #         min_blue_start_value = min(min_blue_start_value, blues_heuristic[node.number][0])

    #     min_blue_goal_value = maxsize
    #     for node in self.__edge_nodes_blue_goal:
    #         min_blue_goal_value = min(min_blue_goal_value, blues_heuristic[node.number][0])

    #     # Find the minimum path cost between blue sides of the table
    #     min_red_start_value = maxsize
    #     for node in self.__edge_nodes_red_start:
    #         min_red_start_value = min(min_red_start_value, reds_heuristic[node.number][0])

    #     min_red_goal_value = maxsize
    #     for node in self.__edge_nodes_red_goal:
    #         min_red_goal_value = min(min_red_goal_value, reds_heuristic[node.number][0])

    #     blue_heuristic = min_blue_goal_value + min_blue_start_value - 1
    #     red_heuristic = min_red_goal_value + min_red_start_value - 1
    #     if agent_color == 'b':
    #         # return red_heuristic - blue_heuristic
    #         return red_heuristic
    #     else:
    #         # return blue_heuristic - red_heuristic
    #         return blue_heuristic

    def get_heuristic_value(self, number, color):
        """
        Using Dijkstra shortest path from the current node (source which is the defined by number),
        find the shortest path to all other nodes and then find the minimum cost.
        """
        if color == BLUE_INDICATOR:
            temp = [node[0] for node in self.__costs_blues]
            heuristics = deepcopy(self.__costs_blues)
            heuristics[number][0] = 1
        else:
            temp = [node[0] for node in self.__costs_reds]
            heuristics = deepcopy(self.__costs_reds)
            heuristics[number][0] = 1

        temp[number] = 1 # Coloring current cell has value of 1
        while not self.__if_all_nodes_visited(heuristics):
            index = temp.index(min(temp)) # Find lowest cost node index
            current_node = self.__nodes[index] # Find lowest cost node
            for neighbor in current_node.neighbors: # For all neighbors check if this path has the lowest cost or not
                if neighbor.color == WHITE_INDICATOR: # If that neighbor is white
                    if heuristics[neighbor.number][0] > heuristics[current_node.number][0] + 1:
                        heuristics[neighbor.number][0] = heuristics[current_node.number][0] + 1 # Update the costs list
                elif neighbor.color == color: # No cost if the neighbor has the same color
                    if heuristics[neighbor.number][0] > heuristics[current_node.number][0]:
                        heuristics[neighbor.number][0] = heuristics[current_node.number][0] # Update the costs list
                if not heuristics[neighbor.number][1]: # If that node is not visited, assign the new value
                    temp[neighbor.number] = heuristics[neighbor.number][0]

            heuristics[index][1] = True # Node is visited
            temp[index] = maxsize # Node won't be chosen again
            
        # Find the minimum path cost between two sides of the table
        min_start_value = maxsize
        min_goal_value = maxsize
        if color == BLUE_INDICATOR:
            for node in self.__edge_nodes_blue_start:
                min_start_value = min(min_start_value, heuristics[node.number][0])

            for node in self.__edge_nodes_blue_goal:
                min_goal_value = min(min_goal_value, heuristics[node.number][0])
        else:
            for node in self.__edge_nodes_red_start:
                min_start_value = min(min_start_value, heuristics[node.number][0])

            for node in self.__edge_nodes_red_goal:
                min_goal_value = min(min_goal_value, heuristics[node.number][0])

        heuristic = min_goal_value + min_start_value - 1
        return heuristic