import random
import sys

def generate_maze(width, height):
    # Создаем пустую сетку
    maze = [['#' for column in range(width)] for row in range(height)]

    def carve_passages_from(start_x, start_y, grid):
        stack = [(start_x, start_y)]
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while stack:
            cx, cy = stack[-1]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = cx + dx*2, cy + dy*2

                if 1 <= nx < width-1 and 1 <= ny < height-1 and grid[ny][nx] == '#':
                    grid[cy + dy][cx + dx] = ' '
                    grid[ny][nx] = ' '
                    stack.append((nx, ny))
                    break
            else:
                stack.pop()

    # Начинаем с центральной точки
    start_x, start_y = (width // 2) | 1, (height // 2) | 1
    maze[start_y][start_x] = ' '
    carve_passages_from(start_x, start_y, maze)

    # Устанавливаем 'A' и 'B' в нужные места
    maze[height-2][1] = 'A'
    maze[1][width-2] = 'B'

    def replace_hashes_with_spaces(maze):
        passage_chance = sys.argv[3] if len(sys.argv) == 4 else sys.argv[1] if len(sys.argv) == 2 else '0'
        passage_chance = int(passage_chance.replace('%', ''))
        for y in range(1, len(maze)-1):
            for x in range(1, len(maze[y])-1):
                if maze[y][x] == '#':
                    if random.randint(0, 100) <= passage_chance:
                        maze[y][x] = ' '

    # Применяем функцию к лабиринту
    replace_hashes_with_spaces(maze)
    
    return maze

def save_maze_to_file(maze, filename):
    with open(filename, 'w') as file:
        for row in maze:
            file.write(''.join(row) + '\n')

# Задаем размеры лабиринта
if len(sys.argv) < 3:
    maze_width = 17
    maze_height = 17
else:
    maze_width = int(sys.argv[1])
    maze_height = int(sys.argv[2])

# Генерируем лабиринт
maze = generate_maze(maze_width, maze_height)

# Сохраняем лабиринт в текстовый файл
save_maze_to_file(maze, 'maze.txt')
