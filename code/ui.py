import pygame

class UI:
    def __init__(self, surface):
        
        self.display_surface = surface

        self.hp_bar = pygame.image.load('graphics/ui/health_bar.png').convert_alpha()
        self.hp_bar_topleft = (54, 39)
        self.bar_max_width = 152
        self.bar_height = 4

        self.coin = pygame.image.load('graphics/ui/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (50, 61))

        self.font = pygame.font.Font('graphics/ui/ARCADEPI.TTF', 30)

    def display_hp(self, current_hp, full_hp):
        self.display_surface.blit(self.hp_bar, (20, 10))
        health_ratio = current_hp / full_hp
        bar_width = self.bar_max_width * health_ratio
        hp_bar_rect = pygame.Rect(self.hp_bar_topleft, (bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface, '#dc4949', hp_bar_rect)

    def display_coins(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        amount_surf = self.font.render(str(amount), False, '#33323d')
        amount_rect = amount_surf.get_rect(midleft = (self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(amount_surf, amount_rect)
