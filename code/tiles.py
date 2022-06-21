#Importing pygame
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()

        #Creating and placing the tiles according to the given position and size
        self.image = pygame.Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)

    #A simple update function for moving the tiles when the camera needs to be moved
    def update(self, dx):
        self.rect.x += dx