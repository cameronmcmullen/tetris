# This is our main file for the application
# The following game is made using pygame

import copy
import numpy as np
import pygame
import random
# launch the application

pygame.init()

# Set all the global variables
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 650
GAME_HEIGHT = 600
GAME_WIDTH = 300
BLOCK_SIZE = 20
ROWS = 20 # 10 blocks wide but we will start counting at 0
COLUMNS = 10 # 20 blocks long but we will start counting at 0

clock = pygame.time.Clock()

# Create all the pieces and possible rotations

I = [
    [1, 1, 1, 1],
    [0, 0, 0, 0]
]

J = [
    [1, 1, 1, 0],
    [0, 0, 1 ,0]
]

L = [
    [1, 1, 1, 0],
    [1, 0, 0 ,0]
]

O = [
    [0, 1, 1, 0],
    [0, 1, 1 ,0]
]


T = [
    [1, 1, 1, 0],
    [0, 1, 0 ,0]
]

S = [
    [0, 1, 1, 0],
    [1, 1, 0 ,0]
]


Z = [
    [1, 1, 0, 0],
    [0, 1, 1 ,0]
]

grid = [[0 for i in range(COLUMNS)] for j in range(ROWS)]
score = 0


# Store all the shapes in one array

SHAPES = [I, J, L, O, S, T, Z]
# Create a specific color for each shape
SHAPES_COLOR = [(0, 255, 255), (0, 0, 255), (255, 97, 3), (255, 255, 0), (153, 50, 204), (255, 48, 48), (0, 255, 0)]
PivRPivC = [(0, 5), (0, 4), (0, 4), (0, 4), (1, 4), (0, 4), (1, 4)]

# Create the block class

class Block(object):
    def __init__(self):
        self.movable = True
        self.index = random.randint(0, len(SHAPES) - 1)
        self.cubes = self.generateBlock()

    def generateBlock(self):
        block = SHAPES[self.index]
        pivot_row, pivot_col = PivRPivC[self.index]
        blockCubes = []
        for i in range(len(block)):
            for j in range(len(block[0])):
                if block[i][j]:
                    blockCubes.append(Cube(i, j + 3, pivot_row, pivot_col, SHAPES_COLOR[self.index]))
        return blockCubes


    def move(self, blocks):
        if self.movable:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if len(blocks) == 0:
                    if all(cube.col > 0 for cube in self.cubes):
                        for cube in self.cubes:
                            cube.col -= 1
                            cube.pivot_col -= 1
                else:
                    if all(cube.col > 0 for cube in self.cubes):
                        if not(self.blockLeft(blocks)):
                            for cube in self.cubes:
                                cube.col -= 1
                                cube.pivot_col -= 1

            if keys[pygame.K_RIGHT]:
                if len(blocks) == 0:
                    if all(cube.col < COLUMNS -1 for cube in self.cubes):
                        for cube in self.cubes:
                            cube.col += 1
                            cube.pivot_col += 1
                else:
                    if all(cube.col < COLUMNS - 1 for cube in self.cubes):
                        if not (self.blockRight(blocks)):
                            for cube in self.cubes:
                                cube.col += 1
                                cube.pivot_col += 1

            if keys[pygame.K_DOWN]:
                clock.tick(100)
            else:
                clock.tick(8)

            if keys[pygame.K_UP]:
                if self.index != 3:
                    cubes = copy.deepcopy(self.cubes)
                    # print(self.cubes[0].row)
                    for cube in cubes:
                        cube.rotate()
                    # print(self.cubes[0].row)
                    colLeft = min([cube.col for cube in cubes])
                    colRight = max([cube.col for cube in cubes])
                    rowBottom = max([cube.row for cube in cubes])

                    if colLeft < 0:
                        pivColDif = 0 - colLeft
                        for cube in cubes:
                            cube.col += pivColDif
                            cube.pivot_col += pivColDif

                    if colRight >= COLUMNS:
                        pivColDif = colRight - (COLUMNS - 1)
                        for cube in cubes:
                            cube.col -= pivColDif
                            cube.pivot_col -= pivColDif

                    if rowBottom >= ROWS:
                        pivRowDif = rowBottom - (ROWS - 1)
                        for cube in cubes:
                            cube.row -= pivRowDif
                            cube.pivot_row -= pivRowDif

                    if not(overlap(cubes, blocks)):
                        for i in range(len(cubes)):
                            self.cubes[i] = cubes[i]

                    if rowBottom >= ROWS:
                        self.movable = False

    def blockBelow(self, blocks):
        if len(blocks) != 0:
            for block in blocks:
                for x in block.cubes:
                    for y in self.cubes:
                        if (x.row, x.col) == (y.row + 1, y.col):
                            return True
            return False
        else:
            return False

    def draw(self, surface):
        for cube in self.cubes:
            cube.draw(surface)

    def shiftCubesRD(self):
        for cube in self.cubes:
            cube.row += 2
            cube.col += 8

    def shiftCubesLU(self):
        for cube in self.cubes:
            cube.row -= 2
            cube.col -= 8

    def blockLeft(self, blocks):
        for block in blocks:
            for x in block.cubes:
              for y in self.cubes:
                if (x.row, x.col) == (y.row, y.col - 1):
                  return True
        return False

    def blockRight(self, blocks):
        for block in blocks:
            for x in block.cubes:
              for y in self.cubes:
                if (x.row, x.col) == (y.row, y.col + 1):
                  return True
        return False

    def maxRow(self):
        return max([cube.row for cube in self.cubes])

def overlap(b, blocks):
    for block in blocks:
        for cube1 in block.cubes:
            for cube2 in b:
                if (cube1.row, cube1.col) == (cube2.row, cube2.col):
                  return True
    return False


class Cube(object):
    # cubes are going to be the squares that make up the blocks
    def __init__(self, row, col, pivot_row, pivot_col, color):
        self.row = row
        self.col = col
        self.width = GAME_WIDTH / COLUMNS
        self.height = GAME_HEIGHT / ROWS
        self.pivot_col = pivot_col # the x coordinate of the pivot cube in the block
        self.pivot_row = pivot_row # the y coordinate of the pivot cube in the block
        self.color = color

    def rotate(self):
        relative_col = self.col - self.pivot_col
        relative_row = self.row - self.pivot_row

        vector = [relative_col, relative_row]
        rotation_matrix = [[0, 1], [-1, 0]]

        rotated_rel_col, rotated_rel_row = np.matmul(rotation_matrix, vector).tolist()

        self.row = rotated_rel_row + self.pivot_row
        self.col = rotated_rel_col + self.pivot_col

    def printRowCol(self):
        print(self.row, self.col)

    def draw(self, surface):
        gap = self.width
        pygame.draw.rect(surface, self.color, (self.col * gap, self.row * gap, self.width, self.height))

def clear_rows(grid, blocks):
    # need to see if row is clear the shift every other row above down one

    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if 0 not in row:
            inc += 1
            # add positions to remove from locked
            ind = i

    if inc > 0:
        for i in (range(ind, ind + inc)):
            grid[i] = [0] * COLUMNS

        for i in range(ind - 1, -1, -1):
            for j in range(len(grid[i])):
                grid[i + inc][j] = grid[i][j]
                grid[i][j] = 0

        for block in blocks:
            length = len(block.cubes) - 1
            for j, cube in enumerate(reversed(block.cubes)):
                if cube.row >= ind and cube.row < ind + inc:
                    block.cubes.pop(length - j)
                elif cube.row < ind:
                    cube.row += inc

def drawGrid(surface, width, height, rows, cols):
    sizeBtwn = width // cols

    x = 0
    y = 0

    for c in range(cols):
        x = x + sizeBtwn
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, height))

    for w in range(rows):
        y = y + sizeBtwn
        pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))


def redrawWindow(surface, blocks, speed, blockNext):
    surface.fill((0, 0, 0))
    drawGrid(surface, GAME_WIDTH, GAME_HEIGHT, ROWS, COLUMNS)
    font = pygame.font.SysFont('comicsans', 28, True)
    text1 = font.render('Next Block', 1, (255, 255, 255))
    text2 = font.render('Score: ' + str(score), 1, (255, 255, 255))
    text3 = font.render('Level: ' + str(5 - speed), 1, (255, 255, 255))
    surface.blit(text1, (GAME_WIDTH + 30, (30 - text1.get_height() / 2)))
    surface.blit(text2, (GAME_WIDTH + 30, (220 + text2.get_height())))
    surface.blit(text3, (GAME_WIDTH + 30, (320 - text3.get_height())))
    for block in blocks:
        block.draw(surface)
    for cube in blockNext.cubes:
        cube.draw(surface)
    pygame.display.update()
4
pygame.key.set_repeat(410,10)

def main():
    global grid, score
    speed = 4
    win = pygame.display.set_mode((SCREEN_WIDTH, GAME_HEIGHT)) # create the window object
    run = True
    blocksDone = []
    blockNew = Block()
    blockNext = Block()
    blockNext.shiftCubesRD()
    allBlocks = blocksDone + [blockNew]

    i = 1
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for block in allBlocks:
            block.move(blocksDone)
        redrawWindow(win, allBlocks, speed, blockNext)

        if  i % speed == 0:
          if any(cube.row == ROWS - 1 for cube in blockNew.cubes) or blockNew.blockBelow(blocksDone):
              blockNew.movable = False

          else:
              for cube in blockNew.cubes:
                  cube.row += 1
                  cube.pivot_row += 1
        i += 1

        if not blockNew.movable:
            for cube in blockNew.cubes:
                grid[cube.row][cube.col] = cube

            blocksDone.append(blockNew)
            clear_rows(grid, blocksDone)

            blockNext.shiftCubesLU()
            blockNew = blockNext
            blockNext = Block()
            blockNext.shiftCubesRD()
            allBlocks = blocksDone + [blockNew]

            score += 1
            if score % 20 == 0 and score < 60:
                speed -= 1

        if overlap(blockNew.cubes, blocksDone):
            while run:
              for event in pygame.event.get():
                if event.type == pygame.QUIT:
                  run = False
    pygame.quit()

main()