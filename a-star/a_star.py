import pygame
import argparse
import math
from queue import PriorityQueue

from node import Node


WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

def h(p1, p2):
    """
    The Heuristic function is Manhattan distance.
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def a_star_algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = h(start.get_position(), end.get_position())

    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_position(), end.get_position())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()

        if current != start:
            current.make_closed()
    
    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows, pygame)
            grid[i].append(node)

    return grid


def draw_grid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GRAY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(window, GRAY, (j * gap, 0), (j * gap, width))


def draw(window, grid, rows, width):
    window.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid(window, rows, width)
    pygame.display.update()


def get_clicked_position(position, rows, width):
    gap = width // rows
    y, x = position
    row = y // gap
    col = x // gap
    return row, col


def main(width, rows):
    window = pygame.display.set_mode((width, width))
    
    grid = make_grid(rows, width)
    start = None
    end = None
    run = True

    while run:
        pygame.display.set_caption('A* Path Finding Algorithm')
        draw(window, grid, rows, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Left button was pressed
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, col = get_clicked_position(position, rows, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    node.make_end()
                elif node != start and node != end:
                    node.make_barrier()

            # Right button was pressed
            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, col = get_clicked_position(position, rows, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    a_star_algorithm(lambda: draw(window, grid, rows, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, width)

    pygame.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A* Path Finding Algorithm')
    parser.add_argument('-w', '--width', help='Width of screen', type=int, default=800)
    parser.add_argument('-r', '--rows', help='Number of rows', type=int, default=50)
    args = parser.parse_args()
    width = args.width
    rows = args.rows
    main(width, rows)
