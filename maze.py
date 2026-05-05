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

if name == "main":
    main()