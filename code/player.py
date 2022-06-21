#Importing the necessary modules
import pygame
from setup import import_assets

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        #Importing the player graphics and setting the default image to idle
        self.import_graphics()
        self.frame_index = 0
        self.animation_speed = 0.14
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        #Creating the direction vector which will be changed to +-1 for movement
        self.direction = pygame.math.Vector2(0, 0)

        #The speed is a 'constant' that will be set to 0 whenever we don't eant the player to move
        #regardless of input dictant that player should be moving
        self.speed = 6

        #Rest of the player constants
        self.gravity = 0.8
        self.jump_velocity = -16

        #Player statuses
        self.status = 'idle'
        self.facing_right = True
        self.touching_ground = False
        self.touching_ceiling = False
        self.touching_right = False
        self.touching_left = False


    #A simple method to set the direction vector to +-1 or call the jump method depending on input key
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True

        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False

        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.touching_ground:
            self.jump()


    #We add the gravity constant to the direction vector and then add the direction vector y
    #to the rectangle position of y, essentially making this a 2 step process
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y


    #We do a similar thing for jump method but instead we set the direction vector y to the
    #jump veolcity constant
    def jump(self):
        self.direction.y = self.jump_velocity


    #Importing all of the player graphics and placing them in a animations dictionary
    def import_graphics(self):
        animation_path = 'graphics/player/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation_set in self.animations.keys():
            full_path = animation_path + animation_set
            self.animations[animation_set] = import_assets(full_path)


    #Animating the player by increasing the frame index by animation speed
    def animate(self):
        animation_set = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation_set):
            self.frame_index = 0

        image = animation_set[int(self.frame_index)]
        if self.facing_right:
            self.image = image

        else:

            #The flip method in transform flips the image according to the boolean values given
            #The first boolean is for x axis and the second is for y axis
            self.image = pygame.transform.flip(image, True, False)

        
        #Setting the new rectangle according if the player is touching the ground or ceiling with
        #combinations of touching the right or left wall
        if self.touching_ground and self.touching_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        
        elif self.touching_ground and self.touching_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)

        elif self.touching_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

        elif self.touching_ceiling and self.touching_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)

        elif self.touching_ceiling and self.touching_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)

        elif self.touching_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

        else:
            self.rect = self.image.get_rect(center = self.rect.center)


    #This method will return the current run, jump, fall, idle status as a string which will
    #be used in animate method
    def movement_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def update(self):
        self.input()
        self.movement_status()
        self.animate()