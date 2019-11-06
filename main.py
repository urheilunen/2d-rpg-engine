import pygame
import sys
import random
import math
from level_generation import Generator
SIZE = (800, 600)
CENTER = (SIZE[0]/2, SIZE[1]/2)
FPS = 120


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('player_standing_down.png').convert_alpha()
        self.rect = self.image.get_rect(center=CENTER)
        self.cycle = 0
        self.angle = 0
        self.speedx = 0
        self.speedy = 0

    def update(self):
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        player_x, player_y = self.rect.center[0], self.rect.center[1]
        if mouse_y - self.rect.center[1] != 0:
            self.angle = math.atan2((mouse_y - player_y), (mouse_x - player_x)) * 180 / math.pi
        else:
            self.angle = math.atan2((mouse_y - player_y + 1), (mouse_x - player_x)) * 180 / math.pi
        if self.cycle == 10:
            self.cycle = 0

        standing_up = pygame.image.load('player_standing_up.png')
        standing_down = pygame.image.load('player_standing_down.png')
        standing_left = pygame.image.load('player_standing_left.png')
        standing_right = pygame.image.load('player_standing_right.png')
        going_up = [pygame.image.load('player_up_1.png'), pygame.image.load('player_up_2.png')]
        going_right = [pygame.image.load('player_right_1.png'), pygame.image.load('player_right_2.png')]
        going_down = [pygame.image.load('player_down_1.png'), pygame.image.load('player_down_2.png')]
        going_left = [pygame.image.load('player_left_1.png'), pygame.image.load('player_left_2.png')]

        if -135 < self.angle < -45:
            if self.speedx == 0 and self.speedy == 0:
                self.image = standing_up
            else:
                self.image = going_up[self.cycle // 5]
        if -45 < self.angle < 45:
            if self.speedx == 0 and self.speedy == 0:
                self.image = standing_right
            else:
                self.image = going_right[self.cycle // 5]
        if 45 < self.angle < 135:
            if self.speedx == 0 and self.speedy == 0:
                self.image = standing_down
            else:
                self.image = going_down[self.cycle // 5]
        if self.angle > 135 or self.angle < -135:
            if self.speedx == 0 and self.speedy == 0:
                self.image = standing_left
            else:
                self.image = going_left[self.cycle // 5]

        self.cycle += 1


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('wall_tile_1.png')
        self.rect = self.image.get_rect(center=(x*100 - dx, y*100 - dy))
        self.speedx = 0
        self.speedy = 0
        self.reverse = 1

    def give_force(self, vector):
        if vector == '0':
            if self.speedx > 0:
                self.speedx -= 1
            if self.speedx < 0:
                self.speedx += 1
            if self.speedy > 0:
                self.speedy -= 1
            if self.speedy < 0:
                self.speedy += 1
        if vector == '0x':
            if self.speedx > 0:
                self.speedx -= 1
            if self.speedx < 0:
                self.speedx += 1
        if vector == '0y':
            if self.speedy > 0:
                self.speedy -= 1
            if self.speedy < 0:
                self.speedy += 1
        if vector == 'up':
            self.speedy += 1
        if vector == 'down':
            self.speedy -= 1
        if vector == 'left':
            self.speedx += 1
        if vector == 'right':
            self.speedx -= 1

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if abs(self.speedx) > 5:
            self.give_force('0x')
        if abs(self.speedy) > 5:
            self.give_force('0y')


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('floor_tile_1.png')
        self.rect = self.image.get_rect(center=(x*100 - dx, y*100 - dy))
        self.speedx = 0
        self.speedy = 0

    def give_force(self, vector):
        if vector == '0':
            if self.speedx > 0:
                self.speedx -= 1
            if self.speedx < 0:
                self.speedx += 1
            if self.speedy > 0:
                self.speedy -= 1
            if self.speedy < 0:
                self.speedy += 1
        if vector == '0x':
            if self.speedx > 0:
                self.speedx -= 1
            if self.speedx < 0:
                self.speedx += 1
        if vector == '0y':
            if self.speedy > 0:
                self.speedy -= 1
            if self.speedy < 0:
                self.speedy += 1
        if vector == 'up':
            self.speedy += 1
        if vector == 'down':
            self.speedy -= 1
        if vector == 'left':
            self.speedx += 1
        if vector == 'right':
            self.speedx -= 1

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if abs(self.speedx) > 5:
            self.give_force('0x')
        if abs(self.speedy) > 5:
            self.give_force('0y')


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, behavior=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('enemy0.png')
        self.rect = self.image.get_rect(center=(x * 100 - dx, y * 100 - dy))
        self.speedx = 0
        self.speedy = 0
        self.behavior = behavior

    def give_force(self, vector):
        if vector == '0':
            if self.speedx > 0:
                self.speedx -= 1
            if self.speedx < 0:
                self.speedx += 1
            if self.speedy > 0:
                self.speedy -= 1
            if self.speedy < 0:
                self.speedy += 1
        if vector == '0x':
            if self.speedx > 0:
                self.speedx -= 1
            if self.speedx < 0:
                self.speedx += 1
        if vector == '0y':
            if self.speedy > 0:
                self.speedy -= 1
            if self.speedy < 0:
                self.speedy += 1
        if vector == 'up':
            self.speedy += 1
        if vector == 'down':
            self.speedy -= 1
        if vector == 'left':
            self.speedx += 1
        if vector == 'right':
            self.speedx -= 1

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if abs(self.speedx) > 5:
            self.give_force('0x')
        if abs(self.speedy) > 5:
            self.give_force('0y')


pygame.init()
sc = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
player = Player()
dungeon = Generator()
dungeon.gen_level()
dungeon.gen_tiles_level()
is_stone = True
while is_stone:
    spawn_room = dungeon.room_list[random.randint(0, len(dungeon.room_list) - 1)]
    spawn_cell_x = abs(spawn_room[2] - spawn_room[0])
    spawn_cell_y = abs(spawn_room[3] - spawn_room[1])
    spawn_point_x = spawn_cell_x * 100 - SIZE[0] / 2
    spawn_point_y = spawn_cell_y * 100 - SIZE[1] / 2
    if dungeon.tiles_level[spawn_cell_x][spawn_cell_y] == '.':
        is_stone = False
# print(spawn_room, ';', spawn_point_x, ';', spawn_point_y)
walls = []
floors = []
for i in range(64):
    for j in range(64):
        if dungeon.tiles_level[i][j] == ".":
            if random.randint(0, 50) == 42:
                enemy0 = Entity(i, j, spawn_point_x, spawn_point_y)
enemy1 = Entity(0, 0, 0, 0)

tmp = 1
motion_up = False
motion_right = False
motion_down = False
motion_left = False
motion_inverter = False
for i in range(64):
    for j in range(64):
        if dungeon.tiles_level[i][j] == "#":
            walls.append(Wall(i, j, spawn_point_x, spawn_point_y))
            # walls.append(Wall(i, j, 0, 0))
        if dungeon.tiles_level[i][j] == ".":
            floors.append(Floor(i, j, spawn_point_x, spawn_point_y))
            # floors.append(Floor(i, j, 0, 0))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                motion_right = True
            if event.key == pygame.K_a:
                motion_left = True
            if event.key == pygame.K_w:
                motion_up = True
            if event.key == pygame.K_s:
                motion_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                motion_right = False
            if event.key == pygame.K_a:
                motion_left = False
            if event.key == pygame.K_w:
                motion_up = False
            if event.key == pygame.K_s:
                motion_down = False
    sc.fill((0, 0, 0))
    hits = pygame.sprite.spritecollide(player, walls, False)
    if hits:
        for wall in walls:
            wall.speedx *= -2
            wall.speedy *= -2
        for floor in floors:
            floor.speedx *= -2
            floor.speedy *= -2

    if motion_up:
        for wall in walls:
            wall.give_force('up')
            sc.blit(wall.image, wall.rect)
            wall.update()
        for floor in floors:
            floor.give_force('up')
            sc.blit(floor.image, floor.rect)
            floor.update()
    if motion_down:
        for wall in walls:
            wall.give_force('down')
            sc.blit(wall.image, wall.rect)
            wall.update()
        for floor in floors:
            floor.give_force('down')
            sc.blit(floor.image, floor.rect)
            floor.update()
    if motion_left:
        for wall in walls:
            wall.give_force('left')
            sc.blit(wall.image, wall.rect)
            wall.update()
        for floor in floors:
            floor.give_force('left')
            sc.blit(floor.image, floor.rect)
            floor.update()
    if motion_right:
        for wall in walls:
            wall.give_force('right')
            sc.blit(wall.image, wall.rect)
            wall.update()
        for floor in floors:
            floor.give_force('right')
            sc.blit(floor.image, floor.rect)
            floor.update()
    if not (motion_up or motion_down):
        for wall in walls:
            wall.give_force('0y')
            sc.blit(wall.image, wall.rect)
            wall.update()
        for floor in floors:
            floor.give_force('0y')
            sc.blit(floor.image, floor.rect)
            floor.update()
    if not (motion_left or motion_right):
        for wall in walls:
            wall.give_force('0x')
            sc.blit(wall.image, wall.rect)
            wall.update()
        for floor in floors:
            floor.give_force('0x')
            sc.blit(floor.image, floor.rect)
            floor.update()
    if not (motion_up or motion_down or motion_left or motion_right):
        for wall in walls:
            wall.give_force('0')
            sc.blit(wall.image, wall.rect)
            wall.update()
        for floor in floors:
            floor.give_force('0')
            sc.blit(floor.image, floor.rect)
            floor.update()

    player.speedx = walls[0].speedx
    player.speedy = walls[0].speedy

    for wall in walls:
        wall.update()
    for floor in floors:
        floor.update()
    sc.blit(player.image, player.rect)
    sc.blit(enemy0.image, enemy0.rect)
    player.update()
    enemy0.update()

    clock.tick(FPS)
    pygame.display.update()

