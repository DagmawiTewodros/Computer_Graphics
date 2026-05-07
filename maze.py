import pygame
import sys
import random
import time

ROWS        = 15
COLS        = 20
CELL        = 40
MARGIN      = 40
WALL_W      = 3
FPS         = 60

EXTRA_WALLS = True

BG          = (15,  15,  20)
WALL_COL    = (220, 220, 230)
GRID_COL    = (40,  40,  50)
PATH_COL    = (220,  60,  60)
DEAD_COL    = (60,  100, 200)
START_COL   = (80,  220, 120)
END_COL     = (255, 190,  50)
TEXT_COL    = (200, 200, 210)
DOT_R       = CELL // 5

WIDTH  = COLS * CELL + 2 * MARGIN
HEIGHT = ROWS * CELL + 2 * MARGIN + 60

northWall = [[1] * (COLS + 1) for _ in range(ROWS + 1)]
eastWall  = [[1] * (COLS + 1) for _ in range(ROWS + 1)]

visited   = [[False] * (COLS + 1) for _ in range(ROWS + 1)]

def cell_rect(r, c):
    x = MARGIN + (c - 1) * CELL
    y = MARGIN + (ROWS - r) * CELL
    return x, y, CELL, CELL

def cell_center(r, c):
    x, y, w, h = cell_rect(r, c)
    return x + w // 2, y + h // 2

def draw_walls(surf):
    bx, by = MARGIN, MARGIN
    bw, bh = COLS * CELL, ROWS * CELL
    pygame.draw.rect(surf, WALL_COL, (bx, by, bw, bh), WALL_W)

    for r in range(1, ROWS + 1):
        for c in range(1, COLS + 1):
            x, y, w, h = cell_rect(r, c)
            if r < ROWS and northWall[r][c]:
                pygame.draw.line(surf, WALL_COL, (x, y), (x + w, y), WALL_W)
            if c < COLS and eastWall[r][c]:
                pygame.draw.line(surf, WALL_COL, (x + w, y), (x + w, y + h), WALL_W)

    for r in range(1, ROWS + 1):
        x, y, w, h = cell_rect(r, 1)
        if eastWall[r][0] == 0:
            pygame.draw.line(surf, BG, (x, y + 2), (x, y + h - 2), WALL_W + 1)

    for c in range(1, COLS + 1):
        x, y, w, h = cell_rect(1, c)
        if northWall[0][c] == 0:
            pygame.draw.line(surf, BG, (x + 2, y + h), (x + w - 2, y + h), WALL_W + 1)

def draw_dot(surf, r, c, colour, radius=DOT_R):
    cx, cy = cell_center(r, c)
    pygame.draw.circle(surf, colour, (cx, cy), radius)

def draw_status(surf, text):
    font = pygame.font.SysFont("monospace", 18)
    label = font.render(text, True, TEXT_COL)
    surf.blit(label, (MARGIN, HEIGHT - 50))

def neighbours(r, c):
    nb = []
    if r + 1 <= ROWS: nb.append((r + 1, c, 'N'))
    if r - 1 >= 1:    nb.append((r - 1, c, 'S'))
    if c + 1 <= COLS: nb.append((r, c + 1, 'E'))
    if c - 1 >= 1:    nb.append((r, c - 1, 'W'))
    return nb

def all_walls_intact(r, c):
    n_ok = northWall[r][c]
    s_ok = northWall[r-1][c] if r > 1 else 1
    e_ok = eastWall[r][c]
    w_ok = eastWall[r][c-1] if c > 1 else eastWall[r][0]
    return n_ok and s_ok and e_ok and w_ok

def eat_wall(r1, c1, r2, c2):
    dr, dc = r2 - r1, c2 - c1
    if dr == 1:   northWall[r1][c1] = 0
    elif dr == -1: northWall[r2][c2] = 0
    elif dc == 1:  eastWall[r1][c1] = 0
    elif dc == -1: eastWall[r1][c2] = 0

def generate_maze(surf, clock):
    start_r = random.randint(1, ROWS)
    start_c = random.randint(1, COLS)
    visited[start_r][start_c] = True

    stack = [(start_r, start_c)]

    while stack:
        r, c = stack[-1]
        candidates = [(nr, nc) for nr, nc, _ in neighbours(r, c)
                      if all_walls_intact(nr, nc)]
        if candidates:
            nr, nc = random.choice(candidates)
            eat_wall(r, c, nr, nc)

            if EXTRA_WALLS and random.random() < 0.05:
                extra = [(er, ec) for er, ec, _ in neighbours(nr, nc)
                         if (er, ec) != (r, c)]
                if extra:
                    er, ec = random.choice(extra)
                    eat_wall(nr, nc, er, ec)

            visited[nr][nc] = True
            stack.append((nr, nc))
        else:
            stack.pop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        surf.fill(BG)
        draw_walls(surf)
        draw_dot(surf, r, c, (180, 220, 180), DOT_R - 1)
        draw_status(surf, "Generating maze…  (mouse eating walls)")
        pygame.display.flip()
        clock.tick(FPS)

def make_entrance_exit():
    sr = random.randint(1, ROWS)
    er = random.randint(1, ROWS)
    eastWall[sr][0]    = 0
    eastWall[er][COLS] = 0
    return (sr, 1), (er, COLS)

def can_move(r, c, direction):
    if direction == 'N':
        return r < ROWS and northWall[r][c] == 0
    if direction == 'S':
        return r > 1 and northWall[r-1][c] == 0
    if direction == 'E':
        if c == COLS: return eastWall[r][COLS] == 0
        return eastWall[r][c] == 0
    if direction == 'W':
        if c == 1:  return eastWall[r][0] == 0
        return eastWall[r][c-1] == 0
    return False

def solve_maze(surf, clock, start, end):
    sr, sc = start
    er, ec = end

    path      = [(sr, sc)]
    seen      = {(sr, sc)}
    dead_ends = set()

    found = False
    while path:
        r, c = path[-1]

        if (r, c) == (er, ec):
            found = True
            break

        dirs = ['N', 'S', 'E', 'W']
        random.shuffle(dirs)
        moved = False
        for d in dirs:
            if not can_move(r, c, d):
                continue
            dr = {'N': 1, 'S': -1, 'E': 0, 'W': 0}[d]
            dc = {'N': 0, 'S':  0, 'E': 1, 'W': -1}[d]
            nr, nc = r + dr, c + dc
            if (nr, nc) in seen:
                continue
            seen.add((nr, nc))
            path.append((nr, nc))
            moved = True
            break

        if not moved:
            dead_ends.add(path.pop())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        surf.fill(BG)
        draw_walls(surf)

        draw_dot(surf, sr, sc, START_COL, DOT_R + 2)
        draw_dot(surf, er, ec, END_COL,   DOT_R + 2)

        for pr, pc in dead_ends:
            draw_dot(surf, pr, pc, DEAD_COL)
        for pr, pc in path:
            draw_dot(surf, pr, pc, PATH_COL)

        draw_status(surf, "Solving maze…  red=path  blue=dead ends")
        pygame.display.flip()
        clock.tick(FPS)

    return found, path

def main():
    pygame.init()
    surf  = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze – Building & Running")
    clock = pygame.time.Clock()
    font  = pygame.font.SysFont("monospace", 20, bold=True)

    generate_maze(surf, clock)

    start, end = make_entrance_exit()

    found, solution = solve_maze(surf, clock, start, end)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                main()

        surf.fill(BG)
        draw_walls(surf)

        draw_dot(surf, start[0], start[1], START_COL, DOT_R + 2)
        draw_dot(surf, end[0],   end[1],   END_COL,   DOT_R + 2)

        for r, c in solution:
            draw_dot(surf, r, c, PATH_COL)

        msg = "Path found! Press R to regenerate." if found else "No path! Press R to retry."
        label = font.render(msg, True, TEXT_COL)
        surf.blit(label, (MARGIN, HEIGHT - 50))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
