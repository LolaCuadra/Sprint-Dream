import random
import pygame
import os
from settings import *

# types list
# "." -> unknown
# "X" -> mine
# "C" -> clue
# "/" -> empty
class Tile:
    def __init__(self, x, y, image, type, revealed=False, flagged=False):
        self.x, self.y = x * TILESIZE, y * TILESIZE
        self.image = image
        self.type = type
        self.revealed = revealed
        self.flagged = flagged

    def draw(self, screen, extra_space=0):
        adjusted_y = self.y + extra_space
        if not self.flagged and self.revealed:
            screen.blit(self.image, (self.x, adjusted_y))
        elif self.flagged and not self.revealed:
            screen.blit(tile_flag, (self.x, adjusted_y))
        elif not self.revealed:
            screen.blit(tile_unknown, (self.x, adjusted_y))

    def __repr__(self):
        return self.type

class Board:
    def __init__(self):
        self.board_list = [[Tile(col, row, tile_empty, ".") for row in range(ROWS)] for col in range(COLS)]
        self.place_mines()
        self.place_clues()
        self.dug = []

    def place_mines(self):
        # define the RGB value for white,
        #  green, blue colour
        white = (255, 255, 255)
        black = (0, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 128)

        # assigning values to X and Y variable
        X = 400
        Y = 400

        # create the display surface object
        # of specific dimension..e(X, Y).
        display_surface = pygame.display.set_mode((X, Y))

        # set the pygame window name
        pygame.display.set_caption('Difficulty Select')

        # create a font object.
        # 1st parameter is the font file
        # which is present in pygame.
        # 2nd parameter is size of the font
        font = pygame.font.Font('Merriweather-Black.ttf', 32)

        # create a text surface object,
        # on which text is drawn on it.
        text = font.render('Easy Difficulty', True, black, white)
        text2 = font.render('Hard Difficulty', True, black, white)

        # create a rectangular object for the
        # text surface object
        textRect = text.get_rect()
        textRect2 = text2.get_rect()

        # set the center of the rectangular object.
        textRect.center = (X // 2, Y // 2)
        textRect2.center = (X // 2, Y // 3)

        x = True

        while x == True:
            # completely fill the surface object
            # with white color
            display_surface.fill(white)

            # copying the text surface object
            # to the display surface object
            # at the center coordinate.
            display_surface.blit(text, textRect)
            display_surface.blit(text2, textRect2)

            # iterate over the list of Event objects
            # that was returned by pygame.event.get() method.
            for event in pygame.event.get():

                # Get mouse position
                mpos = pygame.mouse.get_pos()
                # Check if position is in the rect
                if event.type == pygame.MOUSEBUTTONUP and textRect2.collidepoint(mpos):
                    AMOUNT_MINES = 40
                    x = False
                elif event.type == pygame.MOUSEBUTTONUP and textRect.collidepoint(mpos):
                    AMOUNT_MINES = 20
                    x = False

                # Draws the surface object to the screen.
                pygame.display.update()
        for _ in range(AMOUNT_MINES):
            while True:
                x = random.randint(0, ROWS-1)
                y = random.randint(0, COLS-1)

                if self.board_list[x][y].type == ".":
                    self.board_list[x][y].image = tile_mine
                    self.board_list[x][y].type = "X"
                    break

    def place_clues(self):
        for x in range(ROWS):
            for y in range(COLS):
                if self.board_list[x][y].type != "X":
                    total_mines = self.check_neighbours(x, y)
                    if total_mines > 0:
                        self.board_list[x][y].image = tile_numbers[total_mines-1]
                        self.board_list[x][y].type = "C"


    @staticmethod
    def is_inside(x, y):
        return 0 <= x < ROWS and 0 <= y < COLS

    def check_neighbours(self, x, y):
        total_mines = 0
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                neighbour_x = x + x_offset
                neighbour_y = y + y_offset
                if self.is_inside(neighbour_x, neighbour_y) and self.board_list[neighbour_x][neighbour_y].type == "X":
                    total_mines += 1

        return total_mines


    def draw(self, screen, extra_space=0):
        for row in self.board_list:
            for tile in row:
                tile.draw(screen, extra_space)

    def dig(self, x, y):
        self.dug.append((x, y))
        if self.board_list[x][y].type == "X":
            self.board_list[x][y].revealed = True
            self.board_list[x][y].image = tile_exploded

            return False
        elif self.board_list[x][y].type == "C":
            self.board_list[x][y].revealed = True
            return True

        self.board_list[x][y].revealed = True

        for row in range(max(0, x-1), min(ROWS-1, x+1) + 1):
            for col in range(max(0, y-1), min(COLS-1, y+1) + 1):
                if (row, col) not in self.dug:
                    self.dig(row, col)
        return True

    def display_board(self):
        for row in self.board_list:
            print(row)