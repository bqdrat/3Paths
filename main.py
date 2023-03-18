import pygame
import heapq
import random



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


# Создаем 2-D карту
map_array = []
for row in range(MAP_HEIGHT):
    map_row = []
    for column in range(MAP_WIDTH):
        x = column * CELL_SIZE
        y = row * CELL_SIZE
        is_obstacle = False
        is_start = False
        is_goal = False
        # Создаем старт и гоал точки
        if (row == 0 and column == 0):
            is_start = True
        elif (row == MAP_HEIGHT-1 and column == MAP_WIDTH-1):
            is_goal = True
        # рандомно генерируем препятствия
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
    # Создание словаря для хранения расстояний до каждой клетки
    distance_dict = {}
    for row in range(MAP_HEIGHT):
        for column in range(MAP_WIDTH):
            distance_dict[(column, row)] = float('inf')
    distance_dict[start_cell] = 0

    # Создание словаря для хранения предыдущей клетки в кратчайшем пути до каждой клетки
    previous_dict = {}

    # Создание приоритетной очереди для хранения клеток, необходимых посетить
    queue = [(0, start_cell)]

    while queue:
        # Достаем клетку с кратчайшим расстоянием от старта
        current_distance, current_cell = heapq.heappop(queue)

        # Стоп если достигли цели
        if current_cell == goal_cell:
            break

        # Чек соседей текущей точки
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor_cell = (current_cell[0] + dx, current_cell[1] + dy)

            # Проверка соседей
            if neighbor_cell[0] < 0 or neighbor_cell[0] >= MAP_WIDTH or neighbor_cell[1] < 0 or neighbor_cell[1] >= MAP_HEIGHT:
                continue

            if map_array[neighbor_cell[1]][neighbor_cell[0]][2]:
                continue

            # Считаем расстояние до соседа
            neighbor_distance = current_distance + distance(current_cell, neighbor_cell)

            # Обновляем расстояние и предыдущую клетку при необходимости
            if neighbor_distance < distance_dict[neighbor_cell]:
                distance_dict[neighbor_cell] = neighbor_distance
                previous_dict[neighbor_cell] = current_cell
                heapq.heappush(queue, (neighbor_distance, neighbor_cell))


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
    # Создание словаря для хранения расстояний до каждой клетки
    distance_dict = {}
    for row in range(MAP_HEIGHT):
        for column in range(MAP_WIDTH):
            distance_dict[(column, row)] = float('inf')
    distance_dict[start_cell] = 0

    # Создание словаря для хранения предыдущей клетки в кратчайшем пути до каждой клетки
    previous_dict = {}

    # Создание приоритетной очереди для хранения клеток, необходимых посетить
    queue = [(0, start_cell)]

    while queue:
        # Достаем клетку с кратчайшим расстоянием от старта
        current_distance, current_cell = heapq.heappop(queue)

        # Стоп, если достигли цели
        if current_cell == goal_cell:
            break

        # Чек соседей текущей точки
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor_cell = (current_cell[0] + dx, current_cell[1] + dy)

            # Проверка соседей
            if neighbor_cell[0] < 0 or neighbor_cell[0] >= MAP_WIDTH or neighbor_cell[1] < 0 or neighbor_cell[
                1] >= MAP_HEIGHT:
                continue

            if map_array[neighbor_cell[1]][neighbor_cell[0]][2]:
                continue

            # Считаем расстояние до соседа
            neighbor_distance = current_distance + distance(current_cell, neighbor_cell)

            # Считаем евристическое расстояние от соседа до целевой точки
            if goal_cell != None:
                heuristic_distance = evkl_distance(neighbor_cell, goal_cell)
            else:
                continue

            # Обновляем расстояние и предыдущую клетку при необходимости
            if neighbor_distance + heuristic_distance < distance_dict[neighbor_cell]:
                distance_dict[neighbor_cell] = neighbor_distance + heuristic_distance
                previous_dict[neighbor_cell] = current_cell
                heapq.heappush(queue, (distance_dict[neighbor_cell], neighbor_cell))



    path = []
    current_cell = goal_cell
    while current_cell in previous_dict:
        path.append(current_cell)
        current_cell = previous_dict[current_cell]
    path.append(start_cell)
    path.reverse()
    print("astar", "lengh", len(path), path)
    return path


# Построение карты на экране
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

    # Вертикальные линии
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(WINDOW, OBSTACLE_COLOR, (x, 0), (x, WINDOW_HEIGHT))

    # Горизонтальные линии
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
            # Получаем точку по кликам
            x, y = event.pos
            cell_x = x // CELL_SIZE
            cell_y = y // CELL_SIZE

            if goal_cell == (cell_x, cell_y):
                # Если кликнули на целевую - убираем ее
                map_array[cell_y][cell_x] = (cell_x * CELL_SIZE, cell_y * CELL_SIZE, False, False, False)
                goal_cell = None
            elif not map_array[cell_y][cell_x][2]:
                # Если кликнули не на препятствие, красим как старт или цель
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



    dijkstra_path = dijkstra(map_array, start_cell, goal_cell)
    astar_path = astar(map_array, start_cell, goal_cell)

# Рисуем путь
    for i in range(len(dijkstra_path)-1):
        pygame.draw.line(WINDOW, PATH_COLOR, (dijkstra_path[i][0]*CELL_SIZE+CELL_SIZE//2, dijkstra_path[i][1]*CELL_SIZE+CELL_SIZE//2), (dijkstra_path[i+1][0]*CELL_SIZE+CELL_SIZE//2, dijkstra_path[i+1][1]*CELL_SIZE+CELL_SIZE//2), 5)
    for i in range(len(astar_path)-1):
        pygame.draw.line(WINDOW, GOAL_COLOR, (astar_path[i][0]*CELL_SIZE+CELL_SIZE//2, astar_path[i][1]*CELL_SIZE+CELL_SIZE//2), (astar_path[i+1][0]*CELL_SIZE+CELL_SIZE//2, astar_path[i+1][1]*CELL_SIZE+CELL_SIZE//2), 5)


    # Update the screen
    pygame.display.update()
    clock.tick(FPS)



# Quit Pygame
pygame.quit()






