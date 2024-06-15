import time
import numpy as np
from agent.agent import *
#Kaan Yücel - 150210318

class BFSAgent(Agent):
    def __init__(self, matrix):
        """
            Initializes the BFS agent class.

            Args:
                matrix (list): Initial game matrix
        """
        # Initializing the parent class
        super().__init__(matrix)

    def tree_solve(self):
        """
            Solves the game using tree-based BFS algorithm.

            Returns:
                list: A list of tuples containing moves and state matrices in the solution.
        """
        self.frontier = [Node(None, self.initial_matrix, None)]  # initalizing the frontier
        self.generated_node += 1
        self.explored = []

        while self.frontier:

            self.maximum_node_in_memory = max(self.maximum_node_in_memory, len(self.frontier))
            node = self.frontier.pop(-1)
            self.explored_node += 1
            if self.check_value(node.matrix, self.desired_value):  # checking for the answer
                moves, path = self.get_moves(node)
                return moves, path

            # expand with actions
            for action in self.actions:  # reverse action not allowed
                if node.move_before is not None and action == [node.move_before[0] * -1, node.move_before[1] * -1]:
                    continue
                new_matrix = self.copy_matrix(node.matrix)
                p1pos, p2pos = self.find_players_positions(new_matrix)
                new_p1pos = [p1pos[0] + action[1], p1pos[1] + action[0]]
                new_p2pos = [p2pos[0] - action[1], p2pos[1] - action[0]]
                # move player 1
                # if out of bounds or wall do not change the position
                if (0 <= new_p1pos[0] < len(new_matrix) and
                        0 <= new_p1pos[1] < len(new_matrix[0]) and
                        new_matrix[new_p1pos[0]][new_p1pos[1]] != 4):
                    if new_p1pos == p2pos:  # updated red and not updated blue found case (next to each other)
                        new_matrix[p1pos[0]][p1pos[1]] = 0
                        new_matrix[p2pos[0]][p2pos[1]] = 3
                        self.frontier.insert(0, Node(node, new_matrix, action))
                        self.generated_node += 1
                        break
                else:
                    new_p1pos = p1pos  # do not update

                # move player 2
                # if out of bounds or wall do not change the position
                if not (0 <= new_p2pos[0] < len(new_matrix) and
                        0 <= new_p2pos[1] < len(new_matrix[0]) and
                        new_matrix[new_p2pos[0]][new_p2pos[1]] != 4):
                    new_p2pos = p2pos
                if new_p1pos == new_p2pos:  # updated red and  updated blue found case (2 grid away)
                    new_matrix[p1pos[0]][p1pos[1]] = 0
                    new_matrix[p2pos[0]][p2pos[1]] = 0
                    new_matrix[new_p1pos[0]][new_p1pos[1]] = 3
                    self.frontier.insert(0, Node(node, new_matrix, action))
                    self.generated_node += 1
                    break
                if p1pos == new_p1pos and p2pos == new_p2pos:  # if both are not updated
                    continue
                # not found case

                new_matrix[p1pos[0]][p1pos[1]] = 0
                new_matrix[p2pos[0]][p2pos[1]] = 0
                new_matrix[new_p1pos[0]][new_p1pos[1]] = 1
                new_matrix[new_p2pos[0]][new_p2pos[1]] = 2
                self.frontier.insert(0, Node(node, new_matrix, action))
                self.generated_node += 1

    def graph_solve(self):
        """
            Solves the game using graph-based BFS algorithm.

            Returns:
                list: A list of tuples containing moves and state matrices in the solution.
        """
        self.frontier = [Node(None, self.initial_matrix, None)]  # initalizing the frontier
        self.generated_node += 1
        self.explored = []
        while self.frontier:
            self.maximum_node_in_memory = max(self.maximum_node_in_memory, len(self.frontier))
            node = self.frontier.pop(-1)
            self.explored.append(node.matrix)
            self.explored_node += 1
            if self.check_value(node.matrix, self.desired_value):  # checking for the answer
                moves, path = self.get_moves(node)
                return moves, path
            # expand with actions
            for action in self.actions:
                # reverse action not allowed
                if node.move_before and action == [node.move_before[0] * -1, node.move_before[1] * -1]:
                    continue
                new_matrix = self.copy_matrix(node.matrix)
                p1pos, p2pos = self.find_players_positions(new_matrix)
                new_p1pos = [p1pos[0] + action[1], p1pos[1] + action[0]]
                new_p2pos = [p2pos[0] - action[1], p2pos[1] - action[0]]
                # move player 1
                # if out of bounds or wall do not change the position
                if (0 <= new_p1pos[0] < len(new_matrix) and
                        0 <= new_p1pos[1] < len(new_matrix[0]) and
                        new_matrix[new_p1pos[0]][new_p1pos[1]] != 4):
                    if new_p1pos == p2pos:  # updated red and not updated blue found case (next to each other)
                        new_matrix[p1pos[0]][p1pos[1]] = 0
                        new_matrix[p2pos[0]][p2pos[1]] = 3
                        if new_matrix not in self.explored:
                            self.frontier.insert(0, Node(node, new_matrix, action))
                            self.generated_node += 1
                        break
                else:
                    new_p1pos = p1pos
                if p1pos == new_p1pos and p2pos == new_p2pos:  # if both are not updated
                    continue
                # move player 2
                if not (0 <= new_p2pos[0] < len(new_matrix) and
                        0 <= new_p2pos[1] < len(new_matrix[0]) and
                        new_matrix[new_p2pos[0]][new_p2pos[1]] != 4):
                    new_p2pos = p2pos
                if new_p1pos == new_p2pos:  # updated red and  updated blue found case (2 grid away)
                    new_matrix[p1pos[0]][p1pos[1]] = 0
                    new_matrix[p2pos[0]][p2pos[1]] = 0
                    new_matrix[new_p1pos[0]][new_p1pos[1]] = 3
                    if new_matrix not in self.explored:
                        self.frontier.insert(0, Node(node, new_matrix, action))
                        self.generated_node += 1
                    break

                # not found case
                new_matrix[p1pos[0]][p1pos[1]] = 0
                new_matrix[p2pos[0]][p2pos[1]] = 0
                new_matrix[new_p1pos[0]][new_p1pos[1]] = 1
                new_matrix[new_p2pos[0]][new_p2pos[1]] = 2
                if new_matrix not in self.explored:
                    self.frontier.insert(0, Node(node, new_matrix, action))
                    self.generated_node += 1


class DFSAgent(Agent):
    def __init__(self, matrix):
        """
            Initializes the DFS agent class.

            Args:
                matrix (list): Initial game matrix
        """
        # Initializing the parent class
        super().__init__(matrix)

    def tree_solve(self):
        """
            Solves the game using tree-based DFS algorithm.

            Returns:
                list: A list of tuples containing moves and state matrices in the solution.
        """
        self.frontier = [Node(None, self.initial_matrix, None)]  # initalizing the frontier
        self.generated_node += 1
        self.explored = []
        while self.frontier:
            self.maximum_node_in_memory = max(self.maximum_node_in_memory, len(self.frontier))
            node = self.frontier.pop(0)
            self.explored_node += 1
            if self.check_value(node.matrix, self.desired_value):  # checking for the answer
                moves, path = self.get_moves(node)
                return moves, path
            # expand with actions
            for action in self.actions:
                # reverse action not allowed
                if node.move_before and action == [node.move_before[0] * -1, node.move_before[1] * -1]:
                    continue
                new_matrix = self.copy_matrix(node.matrix)
                p1pos, p2pos = self.find_players_positions(new_matrix)
                new_p1pos = [p1pos[0] + action[1], p1pos[1] + action[0]]
                new_p2pos = [p2pos[0] - action[1], p2pos[1] - action[0]]
                # move player 1
                # if out of bounds or wall do not change the position
                if (0 <= new_p1pos[0] < len(new_matrix) and
                        0 <= new_p1pos[1] < len(new_matrix[0]) and
                        new_matrix[new_p1pos[0]][new_p1pos[1]] != 4):
                    if new_p1pos == p2pos:  # updated red and not updated blue found case (next to each other)
                        new_matrix[p1pos[0]][p1pos[1]] = 0
                        new_matrix[p2pos[0]][p2pos[1]] = 3
                        self.frontier.insert(0, Node(node, new_matrix, action))
                        self.generated_node += 1
                        break
                else:
                    new_p1pos = p1pos

                # move player 2
                if not (0 <= new_p2pos[0] < len(new_matrix) and
                        0 <= new_p2pos[1] < len(new_matrix[0]) and
                        new_matrix[new_p2pos[0]][new_p2pos[1]] != 4):
                    new_p2pos = p2pos
                if new_p1pos == new_p2pos:  # updated red and  updated blue found case (2 grid away)
                    new_matrix[p1pos[0]][p1pos[1]] = 0
                    new_matrix[p2pos[0]][p2pos[1]] = 0
                    new_matrix[new_p1pos[0]][new_p1pos[1]] = 3
                    self.frontier.insert(0, Node(node, new_matrix, action))
                    self.generated_node += 1
                    break
                if p1pos == new_p1pos and p2pos == new_p2pos:  # if both are not updated
                    continue
                # not found case
                new_matrix[p1pos[0]][p1pos[1]] = 0
                new_matrix[p2pos[0]][p2pos[1]] = 0
                new_matrix[new_p1pos[0]][new_p1pos[1]] = 1
                new_matrix[new_p2pos[0]][new_p2pos[1]] = 2
                self.frontier.insert(0, Node(node, new_matrix, action))
                self.generated_node += 1

    def graph_solve(self):
        """
            Solves the game using graph-based DFS algorithm.

            Returns:
                list: A list of tuples containing moves and state matrices in the solution.
        """
        self.frontier = [Node(None, self.initial_matrix, None)]  # initalizing the frontier
        self.generated_node += 1
        self.explored = []
        while self.frontier:
            self.maximum_node_in_memory = max(self.maximum_node_in_memory, len(self.frontier))
            node = self.frontier.pop(0)
            self.explored.append(node.matrix)
            self.explored_node += 1
            if self.check_value(node.matrix, self.desired_value):  # checking for the answer
                moves, path = self.get_moves(node)
                return moves, path
            # expand with actions
            for action in self.actions:
                if node.move_before and action == [node.move_before[0] * -1, node.move_before[1] * -1]:
                    continue
                # reverse action not allowed
                new_matrix = self.copy_matrix(node.matrix)
                p1pos, p2pos = self.find_players_positions(new_matrix)
                new_p1pos = [p1pos[0] + action[1], p1pos[1] + action[0]]
                new_p2pos = [p2pos[0] - action[1], p2pos[1] - action[0]]
                # move player 1
                # if out of bounds or wall do not change the position
                if (0 <= new_p1pos[0] < len(new_matrix) and
                        0 <= new_p1pos[1] < len(new_matrix[0]) and
                        new_matrix[new_p1pos[0]][new_p1pos[1]] != 4):
                    if new_p1pos == p2pos:  # updated red and not updated blue found case (next to each other)
                        new_matrix[p1pos[0]][p1pos[1]] = 0
                        new_matrix[p2pos[0]][p2pos[1]] = 3
                        if new_matrix not in self.explored:
                            self.frontier.insert(0, Node(node, new_matrix, action))
                            self.generated_node += 1
                        break
                else:
                    new_p1pos = p1pos

                # move player 2
                if not (0 <= new_p2pos[0] < len(new_matrix) and
                        0 <= new_p2pos[1] < len(new_matrix[0]) and
                        new_matrix[new_p2pos[0]][new_p2pos[1]] != 4):
                    new_p2pos = p2pos
                if new_p1pos == new_p2pos:  # updated red and  updated blue found case (2 grid away)
                    new_matrix[p1pos[0]][p1pos[1]] = 0
                    new_matrix[p2pos[0]][p2pos[1]] = 0
                    new_matrix[new_p1pos[0]][new_p1pos[1]] = 3
                    if new_matrix not in self.explored:
                        self.frontier.insert(0, Node(node, new_matrix, action))
                        self.generated_node += 1
                    break
                # not found case
                new_matrix[p1pos[0]][p1pos[1]] = 0
                new_matrix[p2pos[0]][p2pos[1]] = 0
                new_matrix[new_p1pos[0]][new_p1pos[1]] = 1
                new_matrix[new_p2pos[0]][new_p2pos[1]] = 2
                if new_matrix not in self.explored:
                    self.frontier.insert(0, Node(node, new_matrix, action))
                    self.generated_node += 1


class AStarAgent(Agent):
    def __init__(self, matrix):
        """
            Initializes the A* agent class.

            Args:
                matrix (list): Initial game matrix
        """
        # Initializing the parent class
        super().__init__(matrix)
        initial_matrix = self.initial_matrix

    # 3 Heuristic functions.To choose one uncomment that function.

    def heuristic(self, xpos, ypos):  # manhattan
        irpos, ibpos = self.find_players_positions(self.initial_matrix)  # initial red pos , initial blue pos
        return (max((abs(xpos - ibpos[0])), (abs(ypos - ibpos[1])))) / 2

    '''
    def heuristic(self, xpos, ypos):  # eucilidian/2
        irpos, ibpos = self.find_players_positions(self.initial_matrix)  # initial red pos , initial blue pos
        return (((ibpos[0] - xpos) ** 2 + (ibpos[1] - ypos) ** 2) ** (1 / 2)) / 2
    '''
    '''
    def heuristic(self, xpos, ypos): # 4th norm of difference vector
        irpos, ibpos = self.find_players_positions(self.initial_matrix)  # initial red pos , initial blue pos
        return (((ibpos[0] - xpos) ** 4 + (ibpos[1] - ypos) ** 4) ** (1 / 4))/2
    '''

    def tree_solve(self):
        """
            Solves the game using tree-based A* algorithm.

            Returns:
                list: A list of tuples containing moves and state matrices in the solution.
        """

        self.frontier = PriorityQueue()  # initializing the frontier as priority queue
        x, y = self.find_players_positions(self.initial_matrix)
        start_node = Node(None, self.initial_matrix, None, 0, self.heuristic(x[0], x[1]))
        self.generated_node += 1
        self.frontier.push(start_node, start_node.f_score)
        self.explored = []
        self.maximum_node_in_memory = self.frontier.size()

        while not self.frontier.is_empty():
            self.maximum_node_in_memory = max(self.maximum_node_in_memory, self.frontier.size())
            node = self.frontier.pop()
            self.explored.append(node.matrix)
            self.explored_node += 1

            if self.check_value(node.matrix, self.desired_value):  # checking for the answer
                moves, path = self.get_moves(node)
                return moves, path
            # expand with actions
            for action in self.actions:  # reverse action not allowed
                if node.move_before and action == [node.move_before[0] * -1, node.move_before[1] * -1]:
                    continue
                new_matrix = self.copy_matrix(node.matrix)
                p1pos, p2pos = self.find_players_positions(new_matrix)
                new_p1pos = [p1pos[0] + action[1], p1pos[1] + action[0]]
                new_p2pos = [p2pos[0] - action[1], p2pos[1] - action[0]]
                # move player 1
                # if out of bounds or wall do not change the position
                if (0 <= new_p1pos[0] < len(new_matrix) and
                        0 <= new_p1pos[1] < len(new_matrix[0]) and
                        new_matrix[new_p1pos[0]][new_p1pos[1]] != 4):
                    if new_p1pos == p2pos:  # updated red and not updated blue found case (next to each other)
                        new_matrix[p1pos[0]][p1pos[1]] = 0
                        new_matrix[p2pos[0]][p2pos[1]] = 3
                        new_node = Node(node, new_matrix, action, node.g_score + 1, 0)
                        self.frontier.push(new_node, new_node.f_score)
                        self.generated_node += 1
                        break
                else:
                    new_p1pos = p1pos

                # move player 2
                if not (0 <= new_p2pos[0] < len(new_matrix) and
                        0 <= new_p2pos[1] < len(new_matrix[0]) and
                        new_matrix[new_p2pos[0]][new_p2pos[1]] != 4):
                    new_p2pos = p2pos
                if new_p1pos == new_p2pos:  # updated red and  updated blue found case (2 grid away)
                    new_matrix[p1pos[0]][p1pos[1]] = 0
                    new_matrix[p2pos[0]][p2pos[1]] = 0
                    new_matrix[new_p1pos[0]][new_p1pos[1]] = 3
                    new_node = Node(node, new_matrix, action, node.g_score + 1, 0)
                    self.frontier.push(new_node, new_node.f_score)
                    self.generated_node += 1
                    break
                if p1pos == new_p1pos and p2pos == new_p2pos:  # if both are not updated
                    continue
                # not found case
                new_matrix[p1pos[0]][p1pos[1]] = 0
                new_matrix[p2pos[0]][p2pos[1]] = 0
                new_matrix[new_p1pos[0]][new_p1pos[1]] = 1
                new_matrix[new_p2pos[0]][new_p2pos[1]] = 2
                new_node = Node(node, new_matrix, action, node.g_score + 1,
                                self.heuristic(new_p1pos[0], new_p1pos[1]))
                self.frontier.push(new_node, new_node.f_score)
                self.generated_node += 1

    def graph_solve(self):
        """
            Solves the game using graph-based A* algorithm.

            Returns:
                list: A list of tuples containing moves and state matrices in the solution.
        """
        self.frontier = PriorityQueue()  # initalizing the frontier as priority queue
        x, y = self.find_players_positions(self.initial_matrix)
        start_node = Node(None, self.initial_matrix, None, 0, self.heuristic(x[0], x[1]))
        self.generated_node += 1
        self.frontier.push(start_node, start_node.f_score)
        self.explored = []
        self.maximum_node_in_memory = self.frontier.size()
        while not self.frontier.is_empty():
            self.maximum_node_in_memory = max(self.maximum_node_in_memory, self.frontier.size())
            node = self.frontier.pop()
            self.explored.append(node.matrix)
            self.explored_node += 1
            if self.check_value(node.matrix, self.desired_value):  # checking for the answer
                moves, path = self.get_moves(node)
                return moves, path
            # expand with actions
            for action in self.actions:  # reverse action not allowed
                if node.move_before and action == [node.move_before[0] * -1, node.move_before[1] * -1]:
                    continue
                new_matrix = self.copy_matrix(node.matrix)
                p1pos, p2pos = self.find_players_positions(new_matrix)
                new_p1pos = [p1pos[0] + action[1], p1pos[1] + action[0]]
                new_p2pos = [p2pos[0] - action[1], p2pos[1] - action[0]]
                # move player 1
                # if out of bounds or wall do not change the position
                if (0 <= new_p1pos[0] < len(new_matrix) and
                        0 <= new_p1pos[1] < len(new_matrix[0]) and
                        new_matrix[new_p1pos[0]][new_p1pos[1]] != 4):
                    if new_p1pos == p2pos:  # updated red and not updated blue found case (next to each other)
                        new_matrix[p1pos[0]][p1pos[1]] = 0
                        new_matrix[p2pos[0]][p2pos[1]] = 3
                        if new_matrix not in self.explored:
                            new_node = Node(node, new_matrix, action, node.g_score + 1, 0)
                            self.frontier.push(new_node, new_node.f_score)
                            self.generated_node += 1
                        break
                else:
                    new_p1pos = p1pos

                # move player 2
                if not (0 <= new_p2pos[0] < len(new_matrix) and
                        0 <= new_p2pos[1] < len(new_matrix[0]) and
                        new_matrix[new_p2pos[0]][new_p2pos[1]] != 4):
                    new_p2pos = p2pos
                if new_p1pos == new_p2pos:  # updated red and  updated blue found case (2 grid away)
                    new_matrix[p1pos[0]][p1pos[1]] = 0
                    new_matrix[p2pos[0]][p2pos[1]] = 0
                    new_matrix[new_p1pos[0]][new_p1pos[1]] = 3
                    if new_matrix not in self.explored:
                        new_node = Node(node, new_matrix, action, node.g_score + 1, 0)
                        self.frontier.push(new_node, new_node.f_score)
                        self.generated_node += 1
                    break
                if p1pos == new_p1pos and p2pos == new_p2pos:  # if both are not updated
                    continue
                # not found case
                new_matrix[p1pos[0]][p1pos[1]] = 0
                new_matrix[p2pos[0]][p2pos[1]] = 0
                new_matrix[new_p1pos[0]][new_p1pos[1]] = 1
                new_matrix[new_p2pos[0]][new_p2pos[1]] = 2
                if new_matrix not in self.explored:
                    new_node = Node(node, new_matrix, action, node.g_score + 1,
                                    self.heuristic(new_p1pos[0], new_p1pos[1]))
                    self.frontier.push(new_node, new_node.f_score)
                    self.generated_node += 1
