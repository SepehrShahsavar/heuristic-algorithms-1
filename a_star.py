import pygame
from pygame.locals import KEYDOWN, K_q
import sys
import math
import time
import random


def draw_lines():
    for i in range(ROW - 1):
        pygame.draw.line(screen, BLACK, (0, (i + 1) * (HEIGHT // ROW)),
                         (WIDTH - 1, (i + 1) * (HEIGHT // ROW)))
    for j in range(COL - 1):
        pygame.draw.line(screen, BLACK, ((j + 1) * (WIDTH // COL),
                                         0), ((j + 1) * (WIDTH // COL), HEIGHT - 1))


def update_screen(grid):
    size_w = WIDTH // COL
    size_h = HEIGHT // ROW
    for i in range(ROW):
        for j in range(COL):
            if grid[i][j] == "blocked":
                screen.fill(GREY, (j * size_w, i * size_h,
                                   (j + 1) * size_w, (i + 1) * size_h))
            elif grid[i][j] == "current":
                screen.fill(RED, (j * size_w, i * size_h,
                                  (j + 1) * size_w, (i + 1) * size_h))
            elif grid[i][j] == "possible":
                screen.fill(BLUE, (j * size_w, i * size_h,
                                   (j + 1) * size_w, (i + 1) * size_h))
            elif grid[i][j] == "visited":
                screen.fill(MAROON, (j * size_w, i * size_h,
                                   (j + 1) * size_w, (i + 1) * size_h))
            elif grid[i][j] == "path":
                screen.fill(YELLOW, (j * size_w, i * size_h,
                                   (j + 1) * size_w, (i + 1) * size_h))
            else:
                screen.fill(WHITE, (j * size_w, i * size_h,
                                    (j + 1) * size_w, (i + 1) * size_h))


def find_edges(grid):
    edges = []
    for i in range(ROW):
        for j in range(COL):
            if grid[i][j] != "blocked":
                start_node = str(i * ROW + j)
                if i != ROW - 1 and grid[i+1][j] != "blocked":
                    edges.append((start_node, str((i + 1) * ROW + j)))
                if j != COL - 1 and grid[i][j + 1] != "blocked":
                    edges.append((start_node, str(i * ROW + j + 1)))
                if j != 0 and grid[i][j - 1] != "blocked":
                    edges.append((start_node, str(i * ROW + j - 1)))
                if i != ROW - 1 and j != 0 and grid[i + 1][j - 1] != "blocked":
                    edges.append((start_node, str((i + 1) * ROW + j - 1)))
                if i != ROW - 1 and j != COL - 1 and grid[i + 1][j + 1] != "blocked":
                    edges.append((start_node, str((i + 1) * ROW + j + 1)))
                    
                if i != 0 and grid[i - 1][j] != "blocked":
                    edges.append((start_node, str((i - 1) * ROW + j)))
                if i != 0 and j != 0 and grid[i - 1][j - 1] != "blocked":
                    edges.append((start_node, str((i - 1) * ROW + j - 1)))
                if i != 0 and j != COL - 1 and grid[i - 1][j + 1] != "blocked":
                    edges.append((start_node, str((i - 1) * ROW + j + 1)))
    return edges


def find_nodes(edges):
    nodes = []
    for edge in edges:
        if edge[0] not in nodes:
            nodes.append(edge[0])
        if edge[1] not in nodes:
            nodes.append(edge[1])
    return nodes


def get_heu_distances(nodes):
    heu_distances = {}
    for node in nodes:
        node_i, node_j = int(node) // ROW, int(node) % ROW
        goal_i, goal_j = ROW - 1, COL - 1
        heu_distances[node] = math.sqrt(
            ((goal_i - node_i) ** 2) + ((goal_j - node_j) ** 2))
    return heu_distances


def get_childs(node):
    childs = []
    for edge in edges:
        if node == edge[0]:
            childs.append(edge[1])
    return childs


### Constants ###
WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (105, 105, 105)
RED = (255, 0, 0)
BLUE = (30, 144, 255)
MAROON = (128,0,0)
YELLOW = (255,255,0)
ROW = 50
COL = 50
MAXINT = 10000


### Pygame Initialization ###
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Finding")
screen.fill(WHITE)
pygame.display.update()


### The Grid  ###
grid = []
for i in range(ROW):
    row = []
    for j in range(COL):
        row.append("not visited")
    grid.append(row)

### The Obstacles ###
# num_objects = int(input("How many objects do you want? "))
# for i in range(num_objects):
#     start_row = random.randint(0, ROW - 1)
#     end_row = random.randint(start_row + 1, ROW - 1)
#     start_col = random.randint(0, COL - 1)
#     end_col = random.randint(start_col + 1, COL - 1)
#     for j in range(start_row, end_row + 1, 1):
#         for k in range(start_col, end_col + 1, 1):
#             grid[j][k] = "blocked"
            
### OR ####
for i in range(1, 20, 1):
    for j in range(1, 20, 1):
        grid[i][j] = "blocked"

for i in range(25, 40, 1):
    for j in range(1, 30, 1):
        grid[i][j] = "blocked"
        
for i in range(6, 26, 1):
    for j in range(30, 40, 1):
        grid[i][j] = "blocked"

for i in range(30, 45, 1):
    for j in range(45, COL, 1):
        grid[i][j] = "blocked"


### Graph ###
edges = find_edges(grid)
nodes = find_nodes(edges)
start, goal = str(0), str((ROW - 1) * ROW + COL - 1)
heu_distances = get_heu_distances(nodes)


### A* Algorithm ###
current = start

grid[int(current) // ROW][int(current) % ROW] = "current"

shortest_distance_from_start = {}
shortest_distance_from_start[current] = 0

total_distances = {}
total_distances[current] = shortest_distance_from_start[current] + \
    heu_distances[current]

previous_node = {}

possible_next_nodes = []


while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()
    # update_screen(grid)
    # draw_lines()
    # pygame.display.update()

    if current != goal:
        childs = get_childs(current)

        for child in childs:
            if child not in possible_next_nodes:
                if grid[int(child) // ROW][int(child) % ROW] != "visited":
                    possible_next_nodes.append(child)
                    grid[int(child) // ROW][int(child) % ROW] = "possible"
                    previous_node[child] = current
                    shortest_distance_from_start[child] = shortest_distance_from_start[current] + 1
                    total_distances[child] = shortest_distance_from_start[child] + \
                        heu_distances[child]
            elif child in possible_next_nodes:
                temp = shortest_distance_from_start[current] + 1 + heu_distances[child]
                if total_distances[child] > temp:
                    shortest_distance_from_start[child] = shortest_distance_from_start[current] + 1
                    total_distances[child] = temp
                    previous_node[child] = current
        
        min_node = None
        min_distance = MAXINT
        for node in possible_next_nodes:
            if total_distances[node] < min_distance:
                min_distance = total_distances[node]
                min_node = node

        update_screen(grid)
        draw_lines()
        pygame.display.update()
        
        possible_next_nodes.remove(min_node)
        grid[int(current) // ROW][int(current) % ROW] = "visited"
        current = min_node
        grid[int(current) // ROW][int(current) % ROW] = "current"
    
    else:
        node = current
        while node != start:
            pre_node = previous_node[node]
            grid[int(node) // ROW][int(node) % ROW] = 'path'
            node = pre_node
        grid[int(start) // ROW][int(start) % ROW] = 'path'
        update_screen(grid)
        draw_lines()
        pygame.display.update()
        
    # time.sleep(.1)
        
