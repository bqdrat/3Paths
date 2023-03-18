import pygame
import heapq
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
pygame.display.set_caption("Dijkstra and A*")
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


def dijkstra(map_array, start_cell, goal_cell):
    # Create a dictionary to store the distance to each cell
    distance_dict = {}
    for row in range(MAP_HEIGHT):
        for column in range(MAP_WIDTH):
            distance_dict[(column, row)] = float('inf')
    distance_dict[start_cell] = 0

    # Create a dictionary to store the previous cell in the shortest path to each cell
    previous_dict = {}

    # Create a priority queue to store the cells to be visited
    queue = [(0, start_cell)]

    while queue:
        # Get the cell with the smallest distance from the start cell
        current_distance, current_cell = heapq.heappop(queue)

        # Stop if we have reached the goal cell
        if current_cell == goal_cell:
            break

        # Check the neighbors of the current cell
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor_cell = (current_cell[0] + dx, current_cell[1] + dy)

            # Check if the neighbor is a valid cell
            if neighbor_cell[0] < 0 or neighbor_cell[0] >= MAP_WIDTH or neighbor_cell[1] < 0 or neighbor_cell[1] >= MAP_HEIGHT:
                continue

            # Check if the neighbor is an obstacle
            if map_array[neighbor_cell[1]][neighbor_cell[0]][2]:
                continue

            # Calculate the distance to the neighbor
            neighbor_distance = current_distance + distance(current_cell, neighbor_cell)
            # Update the distance and previous cell for the neighbor if necessary
            if neighbor_distance < distance_dict[neighbor_cell]:
                distance_dict[neighbor_cell] = neighbor_distance
                previous_dict[neighbor_cell] = current_cell
                heapq.heappush(queue, (neighbor_distance, neighbor_cell))

    # Construct the shortest path from the start cell to the goal cell
    path = []
    current_cell = goal_cell
    while current_cell in previous_dict:
        path.append(current_cell)
        current_cell = previous_dict[current_cell]
    path.append(start_cell)
    path.reverse()
    print("dijkstra", "length", len(path), path)
    return path


def astar(map_array, start_cell, goal_cell):
    # Create a dictionary to store the distance to each cell
    distance_dict = {}
    for row in range(MAP_HEIGHT):
        for column in range(MAP_WIDTH):
            distance_dict[(column, row)] = float('inf')
    distance_dict[start_cell] = 0

    # Create a dictionary to store the previous cell in the shortest path to each cell
    previous_dict = {}

    # Create a priority queue to store the cells to be visited
    queue = [(0, start_cell)]

    while queue:
        # Get the cell with the smallest distance from the start cell
        current_distance, current_cell = heapq.heappop(queue)

        # Stop if we have reached the goal cell
        if current_cell == goal_cell:
            break

        # Check the neighbors of the current cell
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor_cell = (current_cell[0] + dx, current_cell[1] + dy)

            # Check if the neighbor is a valid cell
            if neighbor_cell[0] < 0 or neighbor_cell[0] >= MAP_WIDTH or neighbor_cell[1] < 0 or neighbor_cell[
                1] >= MAP_HEIGHT:
                continue

            # Check if the neighbor is an obstacle
            if map_array[neighbor_cell[1]][neighbor_cell[0]][2]:
                continue

            # Calculate the distance to the neighbor
            neighbor_distance = current_distance + distance(current_cell, neighbor_cell)

            # Calculate the heuristic estimate of the cost from the neighbor to the goal cell
            if goal_cell != None:
                heuristic_distance = evkl_distance(neighbor_cell, goal_cell)
            else:
                continue

            # Update the distance and previous cell for the neighbor if necessary
            if neighbor_distance + heuristic_distance < distance_dict[neighbor_cell]:
                distance_dict[neighbor_cell] = neighbor_distance + heuristic_distance
                previous_dict[neighbor_cell] = current_cell
                heapq.heappush(queue, (distance_dict[neighbor_cell], neighbor_cell))

    # Construct the shortest path from the start cell to the goal cell
    #global path
    path = []
    current_cell = goal_cell
    while current_cell in previous_dict:
        path.append(current_cell)
        current_cell = previous_dict[current_cell]
    path.append(start_cell)
    path.reverse()
    print("astar", "lengh", len(path), path)
    return path


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






# Game loop
running = True
start_cell = (0, 0)
goal_cell = (MAP_WIDTH-1, MAP_HEIGHT-1)
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Get the cell that was clicked
            x, y = event.pos
            cell_x = x // CELL_SIZE
            cell_y = y // CELL_SIZE
            #map_array[cell_y][cell_x] = (start_cell[0] * CELL_SIZE, start_cell[1] * CELL_SIZE, False, True, False)
            #print(cell_x, cell_y)
            #if start_cell == (cell_x, cell_y):
                # If the clicked cell is the current start cell, unmark it
               # map_array[cell_y][cell_x] = (cell_x * CELL_SIZE, cell_y * CELL_SIZE, False, False, False)
               # start_cell = None
            if goal_cell == (cell_x, cell_y):
                # If the clicked cell is the current goal cell, unmark it
                map_array[cell_y][cell_x] = (cell_x * CELL_SIZE, cell_y * CELL_SIZE, False, False, False)
                goal_cell = None
            elif not map_array[cell_y][cell_x][2]:
                # If the clicked cell is not an obstacle, mark it as either the start or goal cell
                if start_cell is None:
                    map_array[cell_y][cell_x] = (cell_x * CELL_SIZE, cell_y * CELL_SIZE, False, True, False)
                    start_cell = (cell_x, cell_y)
                elif goal_cell is None:
                    map_array[cell_y][cell_x] = (cell_x * CELL_SIZE, cell_y * CELL_SIZE, False, False, True)
                    goal_cell = (cell_x, cell_y)






    # Update game state

    # Draw the map
    WINDOW.fill(BACKGROUND_COLOR)
    draw_map()

    # Update the display
    pygame.display.update()
    clock.tick(FPS)

    #dijkstra_path = []
    #astar_path = []
# Calculate the Dijkstra path
# Calculate the A* path
    dijkstra_path = dijkstra(map_array, start_cell, goal_cell)
    astar_path = astar(map_array, start_cell, goal_cell)
# Draw the paths
    for i in range(len(dijkstra_path)-1):
        pygame.draw.line(WINDOW, PATH_COLOR, (dijkstra_path[i][0]*CELL_SIZE+CELL_SIZE//2, dijkstra_path[i][1]*CELL_SIZE+CELL_SIZE//2), (dijkstra_path[i+1][0]*CELL_SIZE+CELL_SIZE//2, dijkstra_path[i+1][1]*CELL_SIZE+CELL_SIZE//2), 5)
    for i in range(len(astar_path)-1):
        pygame.draw.line(WINDOW, GOAL_COLOR, (astar_path[i][0]*CELL_SIZE+CELL_SIZE//2, astar_path[i][1]*CELL_SIZE+CELL_SIZE//2), (astar_path[i+1][0]*CELL_SIZE+CELL_SIZE//2, astar_path[i+1][1]*CELL_SIZE+CELL_SIZE//2), 5)


    # Update the screen
    pygame.display.update()
    clock.tick(FPS)



# Quit Pygame
pygame.quit()
#print(map_array)






