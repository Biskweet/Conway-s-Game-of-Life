import pygame as pg
from pygame.locals import K_ESCAPE, QUIT
# import time


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 500
running = True
play = False
clock = pg.time.Clock()

BLACK = (15, 15, 15)
WHITE = (240, 240, 240)
colors = {WHITE: BLACK, BLACK: WHITE}


class Cell():
    def __init__(self, x, y, width, height, color):
        self.obj = pg.Rect(x, y, width, height)
        self.color = color
        self.isalive = False
    
    def isinteracted(self):
        return self.obj.collidepoint(pg.mouse.get_pos())
    
    def draw(self, color=None):
        if color is None:
            pg.draw.rect(screen, self.color, self.obj)
        else:
            pg.draw.rect(screen, color, self.obj)
    
    def change(self):
        self.isalive = not self.isalive
        self.color = colors[self.color]


button = {"main": Cell(40, 40, 50, 50, (100, 100, 100)),
          "pause_left": Cell(50, 50, 10, 30, (175, 175, 175)),
          "pause_right": Cell(70, 50, 10, 30, (175, 175, 175))}
        

def print_pause(color, secondary_color):
    button["main"].draw(color=color)
    if not play:
        button["pause_left"].draw(color=secondary_color)
        button["pause_right"].draw(color=secondary_color)
    else:
        pg.draw.polygon(screen, secondary_color, [(50, 50), (50, 80), (80, 65)])


grid = [[Cell(x+1, y+1, 8, 8, BLACK) for x in range(0, WINDOW_WIDTH, 10)] for y in range(0, WINDOW_HEIGHT, 10)]

GRID_HEIGHT = len(grid)
GRID_WIDTH = len(grid[0])

screen = pg.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

while running:  
    for event in pg.event.get():
        if event.type == QUIT or event.type == K_ESCAPE:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if not button["main"].isinteracted():
                for line in grid:
                    for cell in line:
                        if cell.isinteracted():
                            cell.change()

        if event.type == pg.MOUSEBUTTONUP:
            if button["main"].isinteracted():
                play = not play

    screen.fill(BLACK)
    
    new_grid = [line.copy() for line in grid]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if play:
                alive_count = 0
                if x > 0:
                    alive_count += grid[y][x-1].isalive
                    if y > 0:
                        alive_count += grid[y-1][x-1].isalive
                    if y < (GRID_HEIGHT - 1):
                        alive_count += grid[y+1][x-1].isalive
                if x < (GRID_WIDTH - 1):
                    alive_count += grid[y][x+1].isalive
                    if y > 0:
                        alive_count += grid[y-1][x+1].isalive
                    if y < (GRID_HEIGHT - 1):
                        alive_count += grid[y+1][x+1].isalive
                if y > 0:
                    alive_count += grid[y-1][x].isalive
                if y < (GRID_HEIGHT - 1):
                    alive_count += grid[y+1][x].isalive

                if (grid[y][x].isalive and (alive_count != 2 and alive_count != 3)) or (not grid[y][x].isalive and (alive_count == 3)):
                    new_grid[y][x].change()

            
    for line in new_grid:
        for cell in line:
            cell.draw()

    grid = new_grid


    if button["main"].isinteracted():
        print_pause((125, 125, 125), (195, 195, 195))  # Hover, lighter
    else:
        print_pause((100, 100, 100), (175, 175, 175))  # No hover, dark
        
    pg.display.flip()
    clock.tick(FPS)

pg.quit()
