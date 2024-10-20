# Credit for this: Nicholas Swift
# as found at https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
from warnings import warn

import argparse # allows for arguments from the command line to be parsed
import heapq

class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
      return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
      return self.f < other.f

    # defining greater than for purposes of heap queue
    def __gt__(self, other):
      return self.f > other.f


# ================================BEGIN=================================
# TODO: Create new function to extract the maze from the given text file
# ======================================================================
def extract_grid(file_path):
    """
    :param file path with grid (i.e., the maze to explore).
    :return Returns the grid as a 2D list, the size of the grid as tuple (rows, columns), start, and end positions
    """

    # Open and read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Initialize an empty list to store the grid
    grid = []

    # Process the file line by line to extract the grid
    for line in lines:
        stripped_line = line.strip() # remove whitespace which includes \n

        # this will be true if the line is non-empty
        if stripped_line:

            # the map() function applies the int() function to every element in the list provided
            row = list(map(int, stripped_line.split())) #
            grid.append(row)

    # Determine maze dimensions
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    size = (rows, cols)

    # Determine start and end positions based on the size of the maze
    start = (0, 0)  # Top-left corner
    end = (rows - 1, cols - 1)  # Bottom-right corner

    return grid, size, start, end
# =================================END==================================




# ================================BEGIN=================================
# TODO: Create new function to compute h(n)
# ======================================================================
def heuristic(pos, goal, heuristic_type=None):
    if heuristic_type == 'manhattan':
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
    elif heuristic_type == 'euclidean':
        return ((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2) ** 0.5
    elif heuristic_type == 'zero':
        return 0  # effectively uses no heuristic.
    else:
        raise ValueError(f"Unknown heuristic type: {heuristic_type}")
# =================================END==================================



# ================================BEGIN=================================
# TODO: Implement Dijkstra's Algorithm
# status: complete
# ======================================================================
# Dijkstra's algorithm (Heuristic h(n) = 0 for all nodes)
def dijkstra(grid, start, goal):
    return astar(grid, start, goal, 'zero') # Pass zero heuristic
# =================================END==================================


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def astar(maze, start, end, heuristic_type, allow_diagonal_movement = True):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze: the array representing the grid
    :param start: the start position
    :param end: the goal position
    :param heuristic_type: can be dijkstra, euclidean, manhattan, or None
    :return path: a list of tuples representing the optimal path from start to end
    :return cost: the total cost to the end node
    :return nodes_expanded: the number of nodes expanded
    """

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = 1000 #(len(maze[0]) * len(maze) // 2)

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
          # if we hit this point return the path such as it is
          # it will not contain the destination
          warn("giving up on pathfinding too many iterations")
          return return_path(current_node)

        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # ===========================BEGIN=============================
        # TODO: modify to return the total cost and num expanded nodes
        # =============================================================
        '''
        # Found the goal
        if current_node == end_node:
            return return_path(current_node)
        '''
        if current_node == end_node:
            optimal_path = return_path(current_node)
            cost = current_node.g
            expanded_nodes = len(closed_list)
            return optimal_path, cost, expanded_nodes
        # ============================END==============================


        # Generate children
        children = []

        for new_position in adjacent_squares: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # ===========================BEGIN=============================
            # TODO: modify the check for walkable terrain
            # =============================================================
            # Make sure walkable terrain
            '''
            # this is the old code
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            '''
            # zeros mean unpassable terrain. so they are not valid children
            if maze[node_position[0]][node_position[1]] == 0:
                continue
            # ============================END==============================


            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # ===========================BEGIN=============================
            # TODO: Heuristic Function
            # =============================================================
            # Use the defined function for the heuristic to compute h(n)
            # replace h computation (below) with defined function

            # Create the f, g, and h values
            # child.g = current_node.g + 1

            child.g = current_node.g + maze[child.position[0]][child.position[1]]

            #child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.h = heuristic(child.position, end_node.position, heuristic_type)

            child.f = child.g + child.h
            # ============================END==============================


            '''
            print(f'current node: {current_node}')
            print(f'child nodes: {children}')
            print(f'processing child: {child}')
            print(f'closed_list: {closed_list}')
            print(f'open_list: {open_list}')
            print('\n')
            '''

            # Child is already in the open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)

    warn("Couldn't get a path to destination")
    return None



# ===================================BEGIN===================================
# TODO: create function to print the grid properly
# ===========================================================================
def print_2d_array(grid, path=None):
    '''
    :param grid is a list but 2D:
    :param if path is provided, grid will print with solution
    :return Nothing; just prints either the :
    '''

    # case when path is not provided
    if path is None:
        for row in grid:
            print(" ".join(map(str, row)))

    else:
        for (row, col) in path:
            grid[row][col] = '.'

        # Replace 0's with special block characters in the grid
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 0:
                    grid[i][j] = '\u2588'  # Replace 0 with a block character

        # print the modified grid
        for row in grid:
            print(" ".join(map(str, row)))
# ================================END========================================



def example(print_maze = True):

    '''
    maze = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,] * 2,
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,] * 2,
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,] * 2,
            [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,] * 2,
            [0,0,0,1,1,0,0,1,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,] * 2,
            [0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,] * 2,
            [0,0,0,1,0,1,1,1,1,0,1,1,0,0,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,0,] * 2,
            [0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,0,1,1,1,0,] * 2,
            [0,0,0,1,0,1,1,0,1,1,0,1,1,1,0,0,0,0,0,1,0,0,1,1,1,1,1,0,0,0,] * 2,
            [0,0,0,1,0,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,0,1,0,1,1,] * 2,
            [0,0,0,1,0,1,0,1,1,0,1,1,1,1,0,0,1,1,1,1,1,1,1,0,1,0,1,0,0,0,] * 2,
            [0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,1,0,] * 2,
            [0,0,0,1,0,1,1,1,1,0,1,0,0,1,1,1,0,1,1,1,1,0,1,1,1,0,1,0,0,0,] * 2,
            [0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1,] * 2,
            [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,] * 2,
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,] * 2,]
    '''

    maze = [[1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,] ,
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,] ,
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,] ,
            [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,] ,
            [0,0,0,1,1,0,0,1,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,] ,
            [0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,] ,
            [0,0,0,1,0,1,1,1,1,0,1,1,0,0,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,0,] ,
            [0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,0,1,1,1,0,] ,
            [0,0,0,1,0,1,1,0,1,1,0,1,1,1,0,0,0,0,0,1,0,0,1,1,1,1,1,0,0,0,] ,
            [0,0,0,1,0,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,0,1,0,1,1,] ,
            [0,0,0,1,0,1,0,1,1,0,1,1,1,1,0,0,1,1,1,1,1,1,1,0,1,0,1,0,0,0,] ,
            [0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,1,0,] ,
            [0,0,0,1,0,1,1,1,1,0,1,0,0,1,1,1,0,1,1,1,1,0,1,1,1,0,1,0,0,0,] ,
            [0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1,] ,
            [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,] ,
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,] ,]

    start = (0, 0)
    end = (len(maze)-1, len(maze[0])-1)

    path = astar(maze, start, end, 'euclidean')

    if print_maze:
      for step in path:
        maze[step[0]][step[1]] = 2

      for row in maze:
        line = []
        for col in row:
          if col == 1:
            line.append("\u2588")
          elif col == 0:
            line.append(" ")
          elif col == 2:
            line.append(".")
        print("".join(line))

    print(path)


# ===================================BEGIN===================================
# TODO: The main function. Needs to use the command line to take in arguments
# ===========================================================================
# example: python a_star.py input_grid.txt manhattan
# ===========================================================================
def main():
    '''
    :param: None
    :return: Nothing. Just prints out the path as well as a simple diagram.
    '''

    # create a parser object
    parser = argparse.ArgumentParser('A-Star', description='A* search algorithm')

    # add the arguments
    parser.add_argument('filepath', type=str, help='file containing the grid')
    parser.add_argument('heuristic', type=str, nargs='?', default='zero',
                        choices=['manhattan', 'euclidean', 'dijkstra', 'zero'],
                        help='Heuristic to use (default: zero)')

    # parse the arguments
    args = parser.parse_args()

    # ======================================BEGIN===================================
    # TODO: determine which heuristic to use: Manhattan/Euclidean or None (Dijkstra)
    # ==============================================================================
    heuristic_type = args.heuristic
    # =======================================END====================================


    # ======================================BEGIN===================================
    # TODO: extract the grid from the provided file path and print contents
    # ==============================================================================
    grid, size, start, end = extract_grid(args.filepath)
    print('The original grid is:')
    print_2d_array(grid)
    print('\n')
    print(f'Size: {size[0]} x {size[1]}')
    print(f'Start: {start}')
    print(f'End: {end}')
    # =======================================END====================================


    # ======================================BEGIN===================================
    # TODO: run A-star with the extracted data from the grid file
    # ==============================================================================
    if (heuristic_type == 'dijkstra'):
        path, cost, num_expanded = dijkstra(grid, start, end)
    else:
        path, cost, num_expanded = astar(grid, start, end, heuristic_type)


    print(f'Cost: {cost}')
    print(f'Nodes Expanded: {num_expanded}')

    print_2d_array(grid, path)
    print(path)
    # =======================================END====================================

# ====================================END====================================


if __name__ == '__main__':
    # execute only if run as a script
    main()