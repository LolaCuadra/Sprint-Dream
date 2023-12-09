import pygame
import os
from settings import *
from sprites import *

from pymongo import MongoClient
# fetch the high score
client = MongoClient("mongodb+srv://Datramer:Goog4me1@cluster0.dfekkct.mongodb.net?retryWrites=true&w=majority")
db = client.get_database('Minesweep')
record = db["highscore"]
realrecord = record.find()
permtime = 0
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.timer_font = pygame.font.SysFont("Consolas", 24)
        self.start_time = pygame.time.get_ticks()

        # Declare elapsed_time as an instance variable
        self.elapsed_time = 0  
    

    def new(self):
        # Accessing Board from sprites to create the display
        self.board = Board()
        self.board.display_board()

    def run(self):
        #load and play music
        pygame.mixer.init()
        pygame.mixer.music.load('sounds/tetrisC.mp3')
        pygame.mixer.music.play(loops=0)
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
        self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        timer_space = 30
        timer_surface = self.timer_font.render(f"Time: {self.elapsed_time}", True, WHITE)
        self.screen.blit(timer_surface, (10, 10))
        
        # Use self.elapsed_time as "Your Score"
        score_surface = self.timer_font.render(f"Your Score: {self.elapsed_time}", True, WHITE)
        self.screen.blit(score_surface, (10, 40))
        
        timer_surface = self.timer_font.render(f"High Score: {realrecord[0]['HighScore']}", True, WHITE)
        self.screen.blit(timer_surface, (275, 10))
        self.board.draw(self.screen, timer_space)

        pygame.display.flip()

    def check_win(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type != "X" and not tile.revealed:
                    return False

        # Use self.elapsed_time as the score
        record.delete_many({})
        mydict = {"HighScore": self.elapsed_time}
        x = record.insert_one(mydict)
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
                            # stop music and explode
                            pygame.mixer.music.unload()
                            pygame.mixer.music.load('sounds/bomba.wav')
                            pygame.mixer.music.play(loops=0)
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
        game_over_font = pygame.font.SysFont("Consolas", 36)
        score_font = pygame.font.SysFont("Consolas", 24)
        button_font = pygame.font.SysFont("Consolas", 18)

        game_over_text = game_over_font.render("Game Over", True, RED)
        
        # Use self.elapsed_time as the player's score
        score_text = score_font.render(f"Your Score: {self.elapsed_time}", True, WHITE)
        
        high_score_text = score_font.render(f"Highest Score: {realrecord[0]['HighScore']}", True, WHITE)
        new_game_text = button_font.render("New Game", True, WHITE)

        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        new_game_rect = new_game_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))

        self.screen.fill(BGCOLOUR)
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(high_score_text, high_score_rect)
        self.screen.blit(new_game_text, new_game_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if new_game_rect.collidepoint(mx, my):
                        # Reset the timer when the new game button is clicked
                        self.start_time = pygame.time.get_ticks()
                        return
game = Game()
while True:
    game.new()
    game.run()