import sys
import imageio.v2 as imageio
import tempfile
import os
from PIL import Image, ImageDraw

class Node():
    def __init__(self, state, parent, action, h_dist, t_dist):
        self.state = state
        self.parent = parent
        self.action = action
        self.h_dist = h_dist
        self.t_dist = t_dist

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class GreedyFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            self.frontier = list(sorted(self.frontier, key=lambda x: x.h_dist))
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class AStarFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            self.frontier = list(sorted(self.frontier, key=lambda x: x.h_dist + x.t_dist))
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():
    def __init__(self, filename):
        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None
        self.frames = []  # To store images for GIF

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                elif solution is not None and len(sys.argv) >= 4 and (i, j) in self.explored:
                    print("%", end="")                
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None,
                     h_dist=abs(self.goal[0] - self.start[0]) + abs(self.goal[1] - self.start[1]),
                     t_dist=0)
        if sys.argv[2] in ['Stack', 'stack', 'DFS', 'dfs']: 
            frontier = StackFrontier()
        elif sys.argv[2] in ['Queue', 'queue', 'BFS', 'bfs']:
            frontier = QueueFrontier()
        elif sys.argv[2] in ['Greedy', 'greedy', 'GBFS', 'gbfs']:
            frontier = GreedyFrontier()
        elif sys.argv[2] in ['A*', 'a*', 'AStar', 'astar', 'a_star']:
            frontier = AStarFrontier()
        else:
            raise Exception("incorrect type, use DFS or BFS")
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()
        FPS = int(sys.argv[5]) if len(sys.argv) == 6 else 5
        frame_counter = 0
        self.save_frame(show_explored=True if len(sys.argv) >= 4 else False)

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                if len(sys.argv) >= 5:
                    self.save_frame(show_explored=True if len(sys.argv) >= 4 else False)
                    self.create_gif()  # Create GIF after finding solution
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action, h_dist=0, t_dist=node.t_dist + 1)
                    child.h_dist = abs(self.goal[0] - child.state[0]) + abs(self.goal[1] - child.state[1])
                    frontier.add(child)

            # Save the current state of the maze
            if len(sys.argv) >= 5 and frame_counter == FPS:
                FPS == int(sys.argv[5]) if len(sys.argv) == 6 else 5
                self.save_frame(show_explored=True if len(sys.argv) >= 4 else False)
                frame_counter = 0
            frame_counter+=1

    def output_image(self, filename, show_solution=True, show_explored=False):
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)

    def save_frame(self, show_solution=True, show_explored=False):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            self.output_image(tmpfile.name, show_solution, show_explored)
            self.frames.append(tmpfile.name)

    def create_gif(self):
        images = []
        for filename in self.frames:
            images.append(imageio.imread(filename))
        imageio.mimsave('maze.gif', images, duration=0.5)
        for filename in self.frames:  # Cleanup temporary files
            os.remove(filename)

if len(sys.argv) < 3:
    sys.exit("Usage: python3 maze.py 'maze.txt' 'algorith type' 'show_progress' 'show_progress_gif' 'gif_FPS'")
m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored = True if len(sys.argv) >= 4 else False)
