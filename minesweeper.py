import pygame
import os
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pygame.init()  # Initialize pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.timer_font = pygame.font.SysFont("Consolas", 24)
        self.start_time = pygame.time.get_ticks()

    def new(self):
        self.board = Board()
        self.board.display_board()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
        else:
            self.end_screen()

    def draw(self):
        self.screen.fill(BGCOLOUR)

        # Calculate elapsed time
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        timer_space = 30
        timer_surface = self.timer_font.render(f"Time: {elapsed_time}", True, WHITE)
        self.screen.blit(timer_surface, (10, 10))
        self.board.draw(self.screen, timer_space)

        pygame.display.flip()

    def check_win(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type != "X" and not tile.revealed:
                    return False
        return True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx //= TILESIZE
                my //= TILESIZE

                # Adjust for extra_space
                my -= 1

                if event.button == 1:
                    if not self.board.board_list[mx][my].flagged:
                        # dig and check if exploded
                        if not self.board.dig(mx, my):
                            # explode
                            for row in self.board.board_list:
                                for tile in row:
                                    if tile.flagged and tile.type != "X":
                                        tile.flagged = False
                                        tile.revealed = True
                                        tile.image = tile_not_mine
                                    elif tile.type == "X":
                                        tile.revealed = True
                            self.playing = False

                if event.button == 3:
                    if not self.board.board_list[mx][my].revealed:
                        self.board.board_list[mx][my].flagged = not self.board.board_list[mx][my].flagged

                if self.check_win():
                    self.win = True
                    self.playing = False
                    for row in self.board.board_list:
                        for tile in row:
                            if not tile.revealed:
                                tile.flagged = True


    def end_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Reset the timer when the game ends
                    self.start_time = pygame.time.get_ticks()
                    return
game = Game()
while True:
    game.new()
    game.run()