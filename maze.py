import pygame
import sys

ROWS   = 15
COLS   = 20
CELL   = 40
MARGIN = 40
WALL_W = 3

WIDTH  = COLS * CELL + 2 * MARGIN
HEIGHT = ROWS * CELL + 2 * MARGIN + 60

BG       = (15, 15, 20)
WALL_COL = (220, 220, 230)

northWall = [[1] * (COLS + 1) for _ in range(ROWS + 1)]
eastWall  = [[1] * (COLS + 1) for _ in range(ROWS + 1)]

def cell_rect(r, c):
    x = MARGIN + (c - 1) * CELL
    y = MARGIN + (ROWS - r) * CELL
    return x, y, CELL, CELL

def draw_grid(surf):
    for r in range(1, ROWS + 1):
        for c in range(1, COLS + 1):
            x, y, w, h = cell_rect(r, c)
            pygame.draw.rect(surf, WALL_COL, (x, y, w, h), WALL_W)

def main():
    pygame.init()
    surf  = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze - Initial Grid")
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        surf.fill(BG)
        draw_grid(surf)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()