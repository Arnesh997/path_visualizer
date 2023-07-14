import pygame
import queue

# Set up the dimensions of the grid
WIDTH = 600
HEIGHT = 400
ROWS = 20
COLS = 30
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Create a grid with each cell initially unvisited
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Set the start and end positions
start_pos = (5, 5)
end_pos = (ROWS - 6, COLS - 6)

# Initialize Pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BFS Visualizer")

# Function to draw the grid
def draw_grid():
    for i in range(ROWS):
        for j in range(COLS):
            color = WHITE
            if grid[i][j] == 1:
                color = BLACK
            elif grid[i][j] == 2:
                color = RED
            elif grid[i][j] == 3:
                color = GREEN
            elif grid[i][j] == 4:
                color = BLUE
            elif grid[i][j] == 5:
                color = YELLOW
            elif grid[i][j] == 6:
                color = PURPLE
            pygame.draw.rect(win, color, (j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

# Function to perform breadth-first search
def bfs(start):
    visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
    q = queue.Queue()
    q.put(start)
    visited[start[0]][start[1]] = True
    prev = [[None for _ in range(COLS)] for _ in range(ROWS)]

    while not q.empty():
        current = q.get()
        row, col = current

        if current == end_pos:
            return True, prev

        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for neighbor in neighbors:
            n_row, n_col = neighbor
            if 0 <= n_row < ROWS and 0 <= n_col < COLS and not visited[n_row][n_col] and grid[n_row][n_col] != 1:
                q.put(neighbor)
                visited[n_row][n_col] = True
                prev[n_row][n_col] = (row, col)
                grid[n_row][n_col] = 4  # Mark as visited (blue color)

        draw_grid()
        pygame.display.update()

    return False, prev

# Function to display the path
def display_path(prev):
    curr = end_pos
    while curr != start_pos:
        row, col = curr
        grid[row][col] = 6  # Mark as path (purple color)
        curr = prev[row][col]
        draw_grid()
        pygame.display.update()

# Main game loop
def game_loop():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    row = pos[1] // CELL_HEIGHT
                    col = pos[0] // CELL_WIDTH
                    if (row, col) != start_pos and (row, col) != end_pos:
                        grid[row][col] = 1  # Mark as obstacle (black color)
                elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                    pos = pygame.mouse.get_pos()
                    row = pos[1] // CELL_HEIGHT
                    col = pos[0] // CELL_WIDTH
                    if (row, col) != start_pos and (row, col) != end_pos:
                        grid[row][col] = 0  # Mark as unvisited (white color)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    found, prev = bfs(start_pos)
                    if found:
                        print("Path Found!")
                        display_path(prev)
                    else:
                        print("No Path Found!")

        draw_grid()
        pygame.draw.rect(win, GREEN, (start_pos[1] * CELL_WIDTH, start_pos[0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
        pygame.draw.rect(win, RED, (end_pos[1] * CELL_WIDTH, end_pos[0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
        pygame.display.update()

    pygame.quit()

# Start the game loop
game_loop()
