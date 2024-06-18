#Search-and-maze
A depth-first search generation algorithm is used: we navigate the maze until we hit a wall or an already existing passage, 
then we try to turn in other available directions. If none are available, we return to the previous vertex and repeat the 
described actions for it. Thus, we traverse all possible paths, bounded by walls one unit thick. The algorithm generates a 
maze with only one path to the endpoint. We always move in steps of two to leave walls between the paths.
Support for launch arguments is added — maze dimensions (width height).

Pathfinding in the maze is implemented using either a depth-first search (DFS) or breadth-first search (BFS) algorithm. In the 
first case, the frontier is a stack, allowing us to explore each path to its end before backtracking to the last turn (DFS). 
In the second case, the frontier is a queue, and we explore each path uniformly, taking all turns sequentially (BFS). 
It is also necessary to specify the path to the maze.txt file or a similar one, maze_generator creates this type of file.
The next argument should specify the algorithm used — DFS or BFS. Adding an additional argument will show all the explored paths.
The graphical representation of the algorithm's operation uses the pillow module (pip install pillow).
