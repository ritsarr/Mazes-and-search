# Maze-and-search

## Maze launch:
- First argument: the path to the maze.txt file or a similar one, maze_generator creates this type of file.
- Second argument: type of the algorithm (DFS, BFS, GBFS, AStar).
- Third argument: showing the explored nodes (show).
- The graphical representation of the algorithm's operation uses the pillow module (pip install pillow).


## Maze_generatoe launch:
- First and second arguments: width and height.
- Third argument: percentage of passages in the walls.
- Alternatively, you can omit specifying the size of the maze; in that case, the first argument will indicate the percentage of passages.

**Maze generation:** A depth-first search generation algorithm is used: we navigate the maze until we hit a wall or an already existing passage, then we try to turn in other available directions. If none are available, we return to the previous vertex and repeat the described actions for it. Thus, we traverse all possible paths, bounded by walls one unit thick. We always move in steps of two to leave walls between the paths. If you do not specify the percentage of passages, there will be only one way from the start to the finish. This is a beneficial feature for mazes but is not typically encountered in the real world. Therefore, if you are testing different search algorithms, it would be better to have multiple ways from the start to the finish.

**DFS:** A depth-first search (DFS) uses a stack in the frontier, allowing us to explore each path to its end before backtracking to the last turn.

**BFS:** In the second case, the frontier is a queue, and we explore each path uniformly, taking all turns sequentially (BFS).

**GBFS:** In this algorithm, we have created a heuristic that chooses the closest way to the finish using the *Manhattan distance*. A node will be explored only if it's not further to the finish than the other one.

**AStar:** Here we also count how many steps it took to get to this node from the start. We will explore that node which has the smallest sum of its Manhattan and travel distances.

###### Additional information: 
1. BFS and AStar will guaranteed find the optimal way, while DFS and GBFS will not.
1. Sometimes DFS and GBFS can find the way faster due to their aggressive strategy.
1. If you don't create passages in the walls, there will be only one way from the start to the finish. In such cases, using the specific "DFS" maze generation algorithm can be optimal and often more effective.

