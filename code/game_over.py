import pygame
from decoration import Sky

class GameOver:
    def __init__(self, surface, coin_data, reset_overworld):
        self.display_surface = surface
        self.coin_data = coin_data
        self.reset_overworld = reset_overworld

        self.sky = Sky(8, 'overworld')

        self.font = pygame.font.Font('graphics/ui/ARCADEPI.TTF', 25)
        self.font_game_over = pygame.font.Font('graphics/ui/ARCADEPI.TTF', 50)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.reset_overworld()

    def display_game_over(self):
        game_over_text = self.font_game_over.render('GAME OVER', False, '#33323d')
        game_over_rect = game_over_text.get_rect(center = (600, 400))
        self.display_surface.blit(game_over_text, game_over_rect)

        coins_text = self.font.render('Coins: {}'.format(self.coin_data), False, '#33323d')
        coins_rect = coins_text.get_rect(center = (600, 450))
        self.display_surface.blit(coins_text, coins_rect)

    def run(self):
        self.sky.draw(self.display_surface)
        self.display_game_over()
        self.input()