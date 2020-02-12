import time

import pygame
import sys
import random
import math
from level_generation import Generator

SIZE = (800, 600)  # size of the screen
CENTER = (SIZE[0]/2, SIZE[1]/2)
FPS = 30


class StartingScreen(pygame.sprite.Sprite):
    def __init__(self, source, coords):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(source).convert_alpha()
        self.rect = self.image.get_rect(center=coords)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('imgs/player_standing_down.png').convert_alpha()
        self.rect = self.image.get_rect(center=CENTER)
        self.cycle = 0
        self.angle = 0
        self.speedx = 0
        self.speedy = 0
        self.health_points = 100

    def update(self):
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        player_x, player_y = self.rect.center[0], self.rect.center[1]
        if mouse_y - self.rect.center[1] != 0:
            self.angle = math.atan2((mouse_y - player_y), (mouse_x - player_x)) * 180 / math.pi
        else:
            self.angle = math.atan2((mouse_y - player_y + 1), (mouse_x - player_x)) * 180 / math.pi
        if self.cycle == 10:
            self.cycle = 0

        standing_up = pygame.image.load('imgs/player_standing_up.png')
        standing_down = pygame.image.load('imgs/player_standing_down.png')
        standing_left = pygame.image.load('imgs/player_standing_left.png')
        standing_right = pygame.image.load('imgs/player_standing_right.png')
        going_up = [pygame.image.load('imgs/player_up_1.png'), pygame.image.load('imgs/player_up_2.png')]
        going_right = [pygame.image.load('imgs/player_right_1.png'), pygame.image.load('imgs/player_right_2.png')]
        going_down = [pygame.image.load('imgs/player_down_1.png'), pygame.image.load('imgs/player_down_2.png')]
        going_left = [pygame.image.load('imgs/player_left_1.png'), pygame.image.load('imgs/player_left_2.png')]

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


class DungeonTile(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, is_floor):
        pygame.sprite.Sprite.__init__(self)
        if not is_floor:
            self.image = pygame.image.load('imgs/wall_tile_1.png')
        else:
            self.image = pygame.image.load('imgs/floor_tile_' + str(random.randint(1, 4)) + '.png')
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
        if abs(self.speedy) <= 5:
            if vector == 'up':
                self.speedy += 1
            if vector == 'down':
                self.speedy -= 1
        if abs(self.speedx) <= 5:
            if vector == 'left':
                self.speedx += 1
            if vector == 'right':
                self.speedx -= 1

    def update(self):
        if abs(self.speedx) > 5:
            self.give_force('0x')
        if abs(self.speedy) > 5:
            self.give_force('0y')
        self.rect.x += self.speedx
        self.rect.y += self.speedy


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, behavior=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('imgs/enemy0.png')
        self.rect = self.image.get_rect(center=(x * 100 - dx, y * 100 - dy))
        self.speedx = 0
        self.speedy = 0
        self.health_points = 100
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
        if abs(self.speedy) <= 5:
            if vector == 'up':
                self.speedy += 2
            if vector == 'down':
                self.speedy -= 2
        if abs(self.speedx) <= 5:
            if vector == 'left':
                self.speedx += 2
            if vector == 'right':
                self.speedx -= 2

    def update(self):
        if abs(self.speedx) > 5:
            self.give_force('0x')
        if abs(self.speedy) > 5:
            self.give_force('0y')
        self.rect.x += self.speedx
        self.rect.y += self.speedy


def update_surroundings_with_motion(motion):
    global floors
    global walls
    global npcs
    for wall in walls:
        wall.give_force(motion)
    for floor in floors:
        floor.give_force(motion)


def distance_between_two_dots(x1, y1, x2, y2):
    dstx = x2 - x1
    dsty = y2 - y1
    dstx **= 2
    dsty **= 2
    dst = dstx + dsty
    dst = math.sqrt(dst)
    return dst


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

walls = []
floors = []
npcs = []

motion_up = False
motion_right = False
motion_down = False
motion_left = False
# spawning walls and floor and npcs
for i in range(64):
    for j in range(64):
        if dungeon.tiles_level[i][j] == "#":
            walls.append(DungeonTile(i, j, spawn_point_x, spawn_point_y, False))
        if dungeon.tiles_level[i][j] == ".":
            floors.append(DungeonTile(i, j, spawn_point_x, spawn_point_y, True))
            if random.randint(1, 50) == 42:
                npcs.append(Entity(i, j, spawn_point_x, spawn_point_y))

with open('numberofenemies.txt', 'a') as npclog:
    npclog.write(str(len(npcs)) + '\n')


main_menu = True
game = True
stsc = StartingScreen('imgs/screen_menu.png', CENTER)
new_game_button = StartingScreen('imgs/new_game.png', (400, 150))
credits_button = StartingScreen('imgs/credits.png', (400, 300))
exit_game_button = StartingScreen('imgs/exit_game.png', (400, 450))


while main_menu:
    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True

    mouse_x, mouse_y = pygame.mouse.get_pos()
    stsc.update()
    sc.blit(stsc.image, stsc.rect)
    if 230 < mouse_x < 570:
        if 105 < mouse_y < 200:
            new_game_button.update()
            sc.blit(new_game_button.image, new_game_button.rect)
            if click:
                main_menu = False
        if 253 < mouse_y < 348:
            credits_button.update()
            sc.blit(credits_button.image, credits_button.rect)
            if click:
                stsc = StartingScreen('imgs/screen_credits.png', CENTER)
                credits_starting_time = time.process_time()
                print(credits_starting_time)
                while credits_starting_time + 0.2 > time.process_time():
                    print(credits_starting_time + 0.2, time.process_time())
                    sc.blit(stsc.image, stsc.rect)
                    clock.tick(FPS)
                    pygame.display.update()
                stsc = StartingScreen('imgs/screen_menu.png', CENTER)
        if 400 < mouse_y < 495:
            exit_game_button.update()
            sc.blit(exit_game_button.image, exit_game_button.rect)
            if click:
                pygame.quit()
                sys.exit()


    clock.tick(FPS)
    pygame.display.update()


while game:
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

    sc.fill((20, 20, 3))
    for wall in walls:
        if pygame.sprite.spritecollide(player, [wall], False):
            this_wall_coords = wall.rect.center
            if this_wall_coords[0] > 450:
                update_surroundings_with_motion('left')
                update_surroundings_with_motion('left')
            if this_wall_coords[0] < 350:
                update_surroundings_with_motion('right')
                update_surroundings_with_motion('right')
            if this_wall_coords[1] > 350:
                update_surroundings_with_motion('up')
                update_surroundings_with_motion('up')
            if this_wall_coords[1] < 250:
                update_surroundings_with_motion('down')
                update_surroundings_with_motion('down')

    if motion_up:
        update_surroundings_with_motion('up')
    if motion_down:
        update_surroundings_with_motion('down')
    if motion_left:
        update_surroundings_with_motion('left')
    if motion_right:
        update_surroundings_with_motion('right')
    if not (motion_up or motion_down):
        update_surroundings_with_motion('0y')
    if not (motion_left or motion_right):
        update_surroundings_with_motion('0x')
    if not (motion_up or motion_down or motion_left or motion_right):
        update_surroundings_with_motion('0')
    player.speedx = walls[0].speedx
    player.speedy = walls[0].speedy

    for npc in npcs:
        npc.speedx = walls[0].speedx
        npc.speedy = walls[0].speedy
        for wall in walls:
            if pygame.sprite.spritecollide(npc, [wall], False):
                if wall.rect.center[0] > npc.rect.center[0]:
                    npc.give_force('right')
                    npc.give_force('right')
                if wall.rect.center[0] < npc.rect.center[0]:
                    npc.give_force('left')
                    npc.give_force('left')
                if wall.rect.center[1] > npc.rect.center[1]:
                    npc.give_force('down')
                    npc.give_force('down')
                if wall.rect.center[1] < npc.rect.center[1]:
                    npc.give_force('up')
                    npc.give_force('up')
        from_this_npc_to_player = distance_between_two_dots(npc.rect.x, npc.rect.y, player.rect.x, player.rect.y)
        if 50 < from_this_npc_to_player < 300:
            if npc.rect.y > player.rect.y + 10:
                npc.give_force('down')
                npc.give_force('down')
            if npc.rect.y < player.rect.y - 10:
                npc.give_force('up')
                npc.give_force('up')
            if npc.rect.x > player.rect.x + 10:
                npc.give_force('right')
                npc.give_force('right')
            if npc.rect.x < player.rect.x - 10:
                npc.give_force('left')
                npc.give_force('left')

    # updating walls
    for wall in walls:
        sc.blit(wall.image, wall.rect)
        wall.update()

    # updating floor
    for floor in floors:
        sc.blit(floor.image, floor.rect)
        floor.update()

    # updating npcs
    for npc in npcs:
        sc.blit(npc.image, npc.rect)
        npc.update()
    sc.blit(player.image, player.rect)
    player.update()

    clock.tick(FPS)
    pygame.display.update()
