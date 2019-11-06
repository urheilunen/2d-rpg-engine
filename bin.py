import pygame
from level_generation import Generator

pygame.init()


#
###
class Player:
    def __init__(self):
        self.image = pygame.image.load('player_up.png')
        self.rect = self.image.get_rect()
        self.image.set_colorkey((200, 0, 200))

    def move(self, camera_pos):
        pos_x, pos_y = camera_pos  # Split camara_pos
        #
        key = pygame.key.get_pressed()  # Get Keyboard Input
        if key[pygame.K_w]:  # Check Key
            self.rect.y -= 8  # Move Player Rect Coord
            pos_y += 8  # Move Camara Coord Against Player Rect
        if key[pygame.K_a]:
            self.rect.x -= 8
            pos_x += 8
        if key[pygame.K_s]:
            self.rect.y += 8
            pos_y -= 8
        if key[pygame.K_d]:
            self.rect.x += 8
            pos_x -= 8
        #
        if self.rect.x < 0:  # Simple Sides Collision
            self.rect.x = 0  # Reset Player Rect Coord
            pos_x = camera_pos[0]  # Reset Camera Pos Coord
        elif self.rect.x > SQUARE - 16:
            self.rect.x = SQUARE - 16
            pos_x = camera_pos[0]
        if self.rect.y < 0:
            self.rect.y = 0
            pos_y = camera_pos[1]
        elif self.rect.y > SQUARE - 16:
            self.rect.y = SQUARE - 16
            pos_y = camera_pos[1]
        #
        return (pos_x, pos_y)  # Return New Camera Pos

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))


###
#
#
###
def Main(display, clock):
    world = pygame.Surface((SQUARE, SQUARE))  # Create Map Surface
    world.fill(colors["BLACK"])  # Fill Map Surface Black
    dungeon = Generator()
    dungeon.gen_level()
    dungeon.gen_tiles_level()
    for x in range(10):
        pygame.draw.rect(world, colors["BLUE"], ((x * 100, x * 100), (20, 20)))  # Put Blue Rectangles On Map Surface
    #
    player = Player()  # Initialize Player Class
    camera_pos = (192, 192)  # Create Camera Starting Position
    #
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        #
        camera_pos = player.move(camera_pos)  # Run Player Move Function And Return New Camera Pos
        #
        display.fill(colors["WHITE"])  # Fill The Background White To Avoid Smearing
        world.fill(colors["BLACK"])  # Refresh The World So The Player Doesn't Smear
        for i in range(len(dungeon.tiles_level)):
            for j in range(len(dungeon.tiles_level[i])):
                if dungeon.tiles_level[i][j] == '#':
                    pygame.draw.rect(world, colors["BLUE"], ((j * 30, i * 30), (30, 30)))
        player.render(world)  # Render The Player
        display.blit(world, camera_pos)  # Render Map To The Display
        #
        pygame.display.flip()


###
#


display = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Scrolling Camera")
clock = pygame.time.Clock()
#
global colors  # Difign Colors
colors = {
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "BLACK": (0, 0, 0)
}
SQUARE = 2720
Main(display, clock)  # Run Main Loop
