import pygame
from game_data import levels
from support import import_folder
from decoration import Sky

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed, path):
        super().__init__()

        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        if status == 'available':
            self.status = status
        else:
            self.status = status

        self.rect = self.image.get_rect(center = pos)
        self.collision_zone = pygame.Rect(self.rect.centerx - (icon_speed / 2), self.rect.centery - (icon_speed / 2), icon_speed, icon_speed)

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        if self.status == 'available':
            self.animate()
        else:
            tinted_surf = self.image.copy()
            tinted_surf.fill('black', None, pygame.BLEND_RGB_MULT)
            self.image.blit(tinted_surf, (0, 0))

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.pos = pos
        self.image = pygame.image.load('graphics/overworld/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.rect.center = self.pos

class Overworld:
    def __init__(self, start_level, max_level, surface, create_level):
        
        self.display_surface = surface
        self.current_level = start_level
        self.max_level = max_level
        self.create_level = create_level

        self.moving = False
        self.movement_direction = pygame.math.Vector2(0, 0)
        self.speed = 12

        self.setup_nodes()
        self.setup_icon()
        self.sky = Sky(8, 'overworld')

        self.start_time = pygame.time.get_ticks()
        self.accept_input = False
        self.timer_len = 300

        self.font = pygame.font.Font('graphics/ui/ARCADEPI.TTF', 25)

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available', self.speed, node_data['node_graphics'])

            else:
                node_sprite = Node(node_data['node_pos'], 'locked', self.speed, node_data['node_graphics'])

            self.nodes.add(node_sprite)
            
    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def draw_paths(self):
        if self.max_level > 0:
            points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.max_level]
            pygame.draw.lines(self.display_surface, '#a04f45', False, points, 6)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving and self.accept_input:
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.current_level < self.max_level:
                self.movement_direction = self.movement_data(1)
                self.current_level += 1
                self.moving = True

            elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.current_level > 0:
                self.movement_direction = self.movement_data(-1)
                self.current_level -= 1
                self.moving = True

            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def movement_data(self, change):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + change].rect.center)

        return (end - start).normalize()

    def update_icon(self):
        if self.moving and self.movement_data:
            self.icon.sprite.pos += self.movement_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.collision_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.movement_direction = pygame.math.Vector2(0, 0)

    def input_timer(self):
        if not self.accept_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_len:
                self.accept_input = True

    def display_instructions(self):
        space_surf = self.font.render('Press space to start a level', False, '#33323d')
        space_rect = space_surf.get_rect(center = (567, 505))
        self.display_surface.blit(space_surf, space_rect)

        arrow_surf = self.font.render('Press right and left arrow key', False, '#33323d')
        arrow_rect = space_surf.get_rect(center = (550, 537))
        self.display_surface.blit(arrow_surf, arrow_rect)

        arrow_surf_1 = self.font.render('to move between the levels', False, '#33323d')
        arrow_rect_1 = space_surf.get_rect(center = (580, 569))
        self.display_surface.blit(arrow_surf_1, arrow_rect_1)

    def run(self):
        self.input_timer()
        self.input()
        self.update_icon()
        self.sky.draw(self.display_surface)
        self.draw_paths()
        self.display_instructions()

        self.nodes.draw(self.display_surface)
        self.nodes.update()

        self.icon.draw(self.display_surface)
        self.icon.update()