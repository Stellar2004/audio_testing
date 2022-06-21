#Importing the necessary modules
import pygame
from os import walk

def import_assets(path):
    image_list = []

    #walk method of os returns the dir location, folders in that dir and a list of
    #the names of the files within that dir
    for junk_var_1, junk_var_2, images in walk(path):
        for image in images:
            full_image_path = path + '/' + image

            #loading the images via pygame, adding them to a image list which is returned
            #to player.py in which the blank list of the dict gets overwritten by the
            #returned image list
            image_surface = pygame.image.load(full_image_path).convert_alpha()
            image_list.append(image_surface)

    return image_list