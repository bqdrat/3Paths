import pygame
import heapq
import math
import random

# Define constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
CELL_SIZE = 20
MAP_WIDTH = WINDOW_WIDTH // CELL_SIZE
MAP_HEIGHT = WINDOW_HEIGHT // CELL_SIZE
BACKGROUND_COLOR = (255, 255, 255) # white
OBSTACLE_COLOR = (0, 0, 0) # black
START_COLOR = (0, 255, 0) # green
GOAL_COLOR = (255, 0, 0) # red
PATH_COLOR = (255,165,0)
FPS = 60

# Initialize Pygame
pygame.init()
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("RRT")
clock = pygame.time.Clock()


# Create a 2D array to represent the map
map_array = []
for row in range(MAP_HEIGHT):
    map_row = []
    for column in range(MAP_WIDTH):
        x = column * CELL_SIZE
        y = row * CELL_SIZE
        is_obstacle = False
        is_start = False
        is_goal = False
        # set start and goal cells
        if (row == 0 and column == 0):
            is_start = True
        elif (row == MAP_HEIGHT-1 and column == MAP_WIDTH-1):
            is_goal = True
        # randomly generate obstacles
        elif random.random() < 0.1 and not is_start and not is_goal:
            is_obstacle = True
        map_row.append((x, y, is_obstacle, is_start, is_goal))
    map_array.append(map_row)

print(map_array)


def distance(cell1, cell2):
    return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])


def evkl_distance(cell1, cell2):
    return ((cell1[0] - cell2[0])**2 + (cell1[1] - cell2[1])**2)**0.5


# Draw the map on the screen
def draw_map():
    for row in map_array:
        for cell in row:
            x, y, is_obstacle, is_start, is_goal = cell
            if is_obstacle:
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(WINDOW, OBSTACLE_COLOR, rect)
            elif is_start:
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(WINDOW, START_COLOR, rect)
            elif is_goal:
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(WINDOW, GOAL_COLOR, rect)
            else:
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(WINDOW, BACKGROUND_COLOR, rect, 1)

    # Draw vertical lines
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(WINDOW, OBSTACLE_COLOR, (x, 0), (x, WINDOW_HEIGHT))

    # Draw horizontal lines
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(WINDOW, OBSTACLE_COLOR, (0, y), (WINDOW_WIDTH, y))

    # Draw vertical lines
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(WINDOW, OBSTACLE_COLOR, (x, 0), (x, WINDOW_HEIGHT))

    # Draw horizontal lines
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(WINDOW, OBSTACLE_COLOR, (0, y), (WINDOW_WIDTH, y))


def is_collision_free(start_cell, end_cell):
    x0, y0 = start_cell
    x1, y1 = end_cell
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    err = dx - dy
    while x0 != x1 or y0 != y1:
        if map_array[y0][x0][2]:
            return False
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return True


def RRT(map_array, start_cell, goal_cell):
    max_iterations = 5000
    step_size = 1
    goal_radius = 1
    nodes = [start_cell]
    edges = []
    current_node = start_cell
    iterations = 0
    while current_node != goal_cell and iterations < max_iterations:
        random_point = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))
        nearest_node = nodes[0]
        for node in nodes:
            if evkl_distance(node, random_point) < evkl_distance(nearest_node, random_point):
                nearest_node = node
        dx = random_point[0] - nearest_node[0]
        dy = random_point[1] - nearest_node[1]

        if abs(dx) > abs(dy):
            dx = step_size * math.copysign(1, dx)
            dy = 0
        else:
            dx = 0
            dy = step_size * math.copysign(1, dy)
        new_node = (int(nearest_node[0] + dx), int(nearest_node[1] + dy))
        if new_node[0] < 0 or new_node[0] >= MAP_WIDTH or new_node[1] < 0 or new_node[1] >= MAP_HEIGHT:
            continue
        if is_collision_free(nearest_node, new_node):
            nodes.append(new_node)
            edges.append((nearest_node, new_node))
            current_node = new_node
            if evkl_distance(current_node, goal_cell) < goal_radius:
                nodes.append(goal_cell)
                edges.append((current_node, goal_cell))
                path = [goal_cell]
                while path[-1] != start_cell:
                    for edge in edges:
                        if edge[1] == path[-1]:
                            path.append(edge[0])
                            break
                path.reverse()
                print("edges",edges)
                print("Path", path)
                return path
        iterations += 1
    return None




# Game loop
running = True
start_cell = (0, 0)
goal_cell = (MAP_WIDTH-1, MAP_HEIGHT-1)

rrt_path = RRT(map_array, start_cell, goal_cell)
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False






    # Update game state

    # Draw the map
    WINDOW.fill(BACKGROUND_COLOR)
    draw_map()

    # Update the display
    pygame.display.update()
    clock.tick(FPS)

    for i in range(len(rrt_path) - 1):
        pygame.draw.line(WINDOW, PATH_COLOR, (
        rrt_path[i][0] * CELL_SIZE + CELL_SIZE // 2, rrt_path[i][1] * CELL_SIZE + CELL_SIZE // 2), (
                         rrt_path[i + 1][0] * CELL_SIZE + CELL_SIZE // 2,
                         rrt_path[i + 1][1] * CELL_SIZE + CELL_SIZE // 2), 5)

    # Update the screen
    pygame.display.update()
    clock.tick(FPS)



# Quit Pygame
pygame.quit()
#print(map_array)






