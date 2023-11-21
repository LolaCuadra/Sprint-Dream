# COLORS (r, g, b)
import pygame
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
DARKGREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BGCOLOUR = DARKGREY

# game settings

TILESIZE = 32
ROWS = 15
COLS = 15
AMOUNT_MINES = 20
WIDTH = TILESIZE * ROWS
HEIGHT = TILESIZE * COLS
FPS = 60
TITLE = "Coolest Minesweeper by Sprint Dream"

tile_numbers = []
for i in range(1, 9):
    tile_numbers.append(pygame.transform.scale(pygame.image.load(os.path.join("images", f"Tile{i}.png")), (TILESIZE, TILESIZE)))

tile_empty = pygame.transform.scale(pygame.image.load(os.path.join("images", "TileEmpty.png")), (TILESIZE, TILESIZE))
tile_exploded = pygame.transform.scale(pygame.image.load(os.path.join("images", "TileExploded.png")), (TILESIZE, TILESIZE))
tile_flag = pygame.transform.scale(pygame.image.load(os.path.join("images", "TileFlag.png")), (TILESIZE, TILESIZE))
tile_mine = pygame.transform.scale(pygame.image.load(os.path.join("images", "TileMine.png")), (TILESIZE, TILESIZE))
tile_unknown = pygame.transform.scale(pygame.image.load(os.path.join("images", "TileUnknown.png")), (TILESIZE, TILESIZE))
tile_not_mine = pygame.transform.scale(pygame.image.load(os.path.join("images", "TileNotMine.png")), (TILESIZE, TILESIZE))

# # Load sounds
# bomb_explosion_sound = pygame.mixer.Sound(os.path.join("sounds", "bomba.wav"))
# flag_placement_sound = pygame.mixer.Sound(os.path.join("sounds", "flag.wav"))
# ships_bells_sound = pygame.mixer.Sound(os.path.join("sounds", "shipsbell.wav"))