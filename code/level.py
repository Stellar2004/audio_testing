#Importing the necessary modules
import pygame
from settings import tile_size, screen_width
from tiles import Tile
from player import Player
from particles import ParticleEffects

class Level():
    def __init__(self, surface, level_data):
        self.display_surface = surface
        self.level_setup(level_data)    #Setting up the level the moment the class is initialised
        self.camera_shifting = 0        #No need to be moving the camera at initialisation
        self.instant_x_pos = 0          #Setting the intantaneous x position to 0

        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False


    def level_setup(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        #Getting the row and column indecies as well as their item so as to set the level accordingly
        for row_index, row in enumerate(layout):
            for col_index, item in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                #Adding the Tile or Player sprite according to the placement in level data
                if item == 'X':
                    tile_instance = Tile((x, y), tile_size)
                    self.tiles.add(tile_instance)
                
                if item == 'P':
                    player_instance = Player((x, y), self.display_surface, self.create_jump_effects)    
                    self.player.add(player_instance)


    def camera_movement(self):
        player_sprite = self.player.sprite  #Getting the player sprite object from the group single player class
        player_x_pos = player_sprite.rect.centerx
        direction_x = player_sprite.direction.x

        #Checking if the player is either on the left or right side of the screen then setting the
        #speed 'constant' to 0 and changing the camera shifting variable accordingly
        if player_x_pos < (screen_width / 4) and direction_x < 0:
            self.camera_shifting = 6
            player_sprite.speed = 0

        elif player_x_pos > (screen_width - (screen_width / 4)) and direction_x > 0:
            self.camera_shifting = -6
            player_sprite.speed = 0

        else:   #Resetting the camera shifting to 0 and speed to 6
            self.camera_shifting = 0
            player_sprite.speed = 6

    
    def create_jump_effects(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        
        else:
            pos -= pygame.math.Vector2(-10, 5)

        jump_particle_sprite = ParticleEffects(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)


    def is_player_on_ground(self):
        if self.player.sprite.touching_ground:
            self.player_on_ground = True
        
        else:
            self.player_on_ground = False

    
    def create_land_particles(self):
        if not self.player_on_ground and self.player.sprite.touching_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            
            else:
                offset = pygame.math.Vector2(-10, 15)

            land_particle_sprite = ParticleEffects(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(land_particle_sprite)


    #To have proper collisions we resort to having the player sprite movement addition done here
    def horizontal_movement_collision(self):
        player_sprite = self.player.sprite
        player_sprite.rect.x += player_sprite.direction.x * player_sprite.speed

        for sprite_tile in self.tiles.sprites():
            if sprite_tile.rect.colliderect(player_sprite.rect):

                #We check if the collision was on the left or the right and re-place the
                #player sprite accordingly
                if player_sprite.direction.x < 0:
                    player_sprite.rect.left = sprite_tile.rect.right
                    player_sprite.touching_left = True
                    self.instant_x_pos = player_sprite.rect.left

                elif player_sprite.direction.x > 0:
                    player_sprite.rect.right = sprite_tile.rect.left
                    player_sprite.touching_right = True
                    self.instant_x_pos = player_sprite.rect.right
        
        #We set the touching right wall or left wall to True above as per the collision then
        #set the touching wall status to False by taking an instantaneous x pos at the time of
        #wall collision and then check if the player has moved plus/minus to that instant x pos
        if player_sprite.touching_left and (player_sprite.rect.left < self.instant_x_pos or player_sprite.direction.x >= 0):
            player_sprite.touching_left = False

        if player_sprite.touching_right and (player_sprite.rect.right > self.instant_x_pos or player_sprite.direction.x <= 0):
            player_sprite.touching_right = False


    def vertical_movement_collision(self):
        player_sprite = self.player.sprite
        player_sprite.apply_gravity()

        for sprite_tile in self.tiles.sprites():
            if sprite_tile.rect.colliderect(player_sprite.rect):

                #We check if the collision was on the top or the bottom and re-place the
                #player sprite accordingly and set the direction vector y to 0 so as to
                #not have any residual jump velocity or so as to not have infinite exponential
                #gravity acting on the player
                if player_sprite.direction.y > 0:
                    player_sprite.rect.bottom = sprite_tile.rect.top
                    player_sprite.direction.y = 0
                    player_sprite.touching_ground = True

                if player_sprite.direction.y < 0:
                    player_sprite.rect.top = sprite_tile.rect.bottom
                    player_sprite.direction.y = 0
                    player_sprite.touching_ceiling = True
        
        #We set the touching ground or ceiling to True above as per the collision then set
        #the touching ground status to False here if the direction vector y is -ve (jump) or
        #is greater than 1 (gravity is acting properly and is not a one off acting of gravity)
        if player_sprite.touching_ground and player_sprite.direction.y < 0 or player_sprite.direction.y > 1:
            player_sprite.touching_ground = False

        #We set the touching ceiling status to False here if the direction vector y is +ve (gravity)
        if player_sprite.touching_ceiling and player_sprite.direction.y > 0.1:
            player_sprite.touching_ceiling = False


    def run(self):

        self.dust_sprite.update(self.camera_shifting)
        self.dust_sprite.draw(self.display_surface)

        
        #Updating and drawing the tiles in the tile group created at initialisation
        
        #Passing the camera shifting variable which will cause the camera to move only if the
        #camera movement variable detects the need to do so
        self.tiles.update(self.camera_shifting)
        self.tiles.draw(self.display_surface)
        self.camera_movement()  #Checking if the camera is needed to be moved


        #Updating the player in the player group single and drawing after checking for collisions
        self.player.update()
        self.horizontal_movement_collision()
        self.is_player_on_ground()
        self.vertical_movement_collision()
        self.create_land_particles()
        self.player.draw(self.display_surface)