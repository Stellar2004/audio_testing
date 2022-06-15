import pygame
from tiles import Tile
from settings import tile_size
from player import Player

class Level():
    def __init__(self, surface, level_data):
        self.display_surface = surface
        self.level_setup(level_data)
        self.camera_shifting = 0

    def level_setup(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if col == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                
                if col == 'P':
                    player = Player((x, y))
                    self.player.add(player)

    def run(self):
        self.tiles.update(self.camera_shifting)
        self.tiles.draw(self.display_surface)

        self.player.update()
        self.player.draw(self.display_surface)