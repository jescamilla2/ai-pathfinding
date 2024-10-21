# Pathfinding Using A* Algorithm with Cycle Detection

Usage is fairly straightforward as the program can be run from the command line.
The input is as follows:

`$ python a_star.py file_name.txt heuristic_name`

If no heuristic is provided, then it defaults to zero.
Options for the heuristic include: `euclidean`, `manhattan`, `dijkstra`
If no heuristic is supplied, then a default heuristic is used: `h(n) = 0`

Here is an example:

`$ python a_star.py input_grid.txt manhattan`

Make sure to include the full path of the input file as it may be in a different directory than the `a_star.py` file.
