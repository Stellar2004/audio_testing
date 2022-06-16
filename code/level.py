import pygame
from tiles import Tile
from settings import tile_size, screen_width
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

    def camera_movement(self):
        player = self.player.sprite
        player_x_pos = player.rect.centerx
        direction_x = player.direction.x

        if player_x_pos < (screen_width / 4) and direction_x < 0:
            self.camera_shifting = 6
            player.speed = 0

        elif player_x_pos > (screen_width - (screen_width / 4)) and direction_x > 0:
            self.camera_shifting = -6
            player.speed = 0

        else:
            self.camera_shifting = 0
            player.speed = 6

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right

                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def run(self):
        self.tiles.update(self.camera_shifting)
        self.tiles.draw(self.display_surface)
        self.camera_movement()

        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)