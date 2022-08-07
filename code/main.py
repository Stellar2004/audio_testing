import pygame, sys
from settings import * 
from level import Level
from overworld import Overworld
from ui import UI
from game_over import GameOver

class Game:
    def __init__(self, screen):
        self.max_level = 0
        self.screen = screen
        self.max_hp = 100
        self.current_hp = 100
        self.coins = 0

        self.overworld = Overworld(0, self.max_level, self.screen, self.create_level)
        self.status = 'overworld'

        self.ui = UI(self.screen)

    def create_level(self, current_level):
        self.level = Level(current_level, self.screen, self.create_overworld, self.update_coins, self.update_health)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, self.screen, self.create_level)
        self.status = 'overworld'

    def update_coins(self, amount):
        self.coins += amount

    def update_health(self, amount):
        self.current_hp += amount

    def game_over_check(self):
        if self.current_hp <= 0:
            self.over_screen = GameOver(self.screen, self.coins, self.restart_overworld)
            self.status = 'game over'

    def restart_overworld(self):
        self.overworld = Overworld(0, 0, self.screen, self.create_level)
        self.current_hp = 100
        self.coins = 0
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()

        elif self.status == 'game over':
            self.over_screen.run()

        else:
            self.level.run()
            self.ui.display_hp(self.current_hp, self.max_hp)
            self.ui.display_coins(self.coins)
            self.game_over_check()

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game(screen)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	screen.fill('grey')
	game.run()

	pygame.display.update()
	clock.tick(60)