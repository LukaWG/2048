import time
import pygame
import random
import logic_working as logic

FPS = 50

SCREENSIZE = [500, 500]

LEFT = "LEFT"
RIGHT = "RIGHT"
UP = "UP"
DOWN = "DOWN"

MAP = (
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
    )

#region
class Board(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()

        self.col = (187, 173, 160)

        self.image = pygame.Surface(size)
        self.image.fill(self.col)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        board.add(self)

class Vertical(Board):
    def __init__(self, x, y):
        super().__init__([20, 500], x, y)

class Horizontal(Board):
    def __init__(self, x, y):
        super().__init__([500, 20], x, y)
#endregion

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, num=None):
        super().__init__(tiles) # Adds to the group called tiles

        self.myfont = pygame.font.Font(pygame.font.get_default_font(), 40)

        self.image = pygame.Surface([100, 100])
        
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.dir = None
        self.lastdir = None
        self.speed = None
        self.dx = 0
        self.dy = 0

        if num == None:
            if len(tiles.sprites()) > 5:
                self.text(random.choice([2, 4]))
            else:
                self.text(2)
        else:
            self.text(num)

        self.pos = self.get_pos()
        edit_map(self.pos[0], self.pos[1], self.num)

    def text(self, num):
        self.num = num
        if self.num == 2:
            self.image.fill((238, 228, 218))
        elif self.num == 4:
            self.image.fill((237, 224, 200))
        elif self.num == 8:
            self.image.fill((242, 177, 121))
        elif self.num == 16:
            self.image.fill((245, 149, 99))
        elif self.num == 32:
            self.image.fill((246, 124, 95))
        elif self.num == 64:
            self.image.fill((247, 97, 72))
        elif self.num == 128:
            self.image.fill((239, 207, 114))
        elif self.num == 256:
            self.image.fill((237, 204, 97))
        elif self.num == 512:
            self.image.fill((237, 200, 80))
        elif self.num == 1024:
            self.image.fill((237, 197, 63))
        elif self.num == 2048:
            self.image.fill((237, 194, 46))
        else:
            self.image.fill((60, 58, 50))
        if self.num != 2 and self.num != 4:
            col = (249, 246, 242)
        else:
            col = (119, 110, 101)
        to_display = self.myfont.render(str(self.num), True, col)
        to_display_rect = to_display.get_rect()
        size = to_display_rect.size
        pos = (50-size[0]//2, 50-size[1]//2)
        self.image.blit(to_display, pos)

    def update(self):
        if self.dir == LEFT and self.dx != 0:
            if self.speed == "accelerate":
                self.dx -= 1
            else:
                self.dx += 1
        elif self.dir == RIGHT and self.dx != 0:
            if self.speed == "accelerate":
                self.dx += 1
            else:
                self.dx -= 1
        elif self.dir == UP and self.dy != 0:
            if self.speed == "accelerate":
                self.dy -= 1
            else:
                self.dy += 1
        elif self.dir == DOWN and self.dy != 0:
            if self.speed == "accelerate":
                self.dy += 1
            else:
                self.dy -= 1


        if abs(self.dx) == 11 or abs(self.dy) == 11:
            self.speed = "decelerate"
        elif self.dx == 0 and self.dy == 0 and self.speed:
            self.speed = None
            self.dir = None
            self.update_map()

        self.rect.x += self.dx
        self.rect.y += self.dy

    def left(self):
        if not self.dir and self.check(LEFT):
            # self.pos = self.get_pos()
            # edit_map(self.pos[0], self.pos[1], 0)
            self.lastdir = LEFT
            self.dir = LEFT
            self.dx = -1
            self.speed = "accelerate"

    def right(self):
        if not self.dir and self.check(RIGHT):
            # self.pos = self.get_pos()
            # edit_map(self.pos[0], self.pos[1], 0)
            self.lastdir = RIGHT
            self.dir = RIGHT
            self.dx = 1
            self.speed = "accelerate"

    def up(self):
        if not self.dir and self.check(UP):
            # self.pos = self.get_pos()
            # edit_map(self.pos[0], self.pos[1], 0)
            self.lastdir = UP
            self.dir = UP
            self.dy = -1
            self.speed = "accelerate"

    def down(self):
        if not self.dir and self.check(DOWN):
            # self.pos = self.get_pos()
            # edit_map(self.pos[0], self.pos[1], 0)
            self.lastdir = DOWN
            self.dir = DOWN
            self.dy = 1
            self.speed = "accelerate"

    def check(self, dir):
        if dir == LEFT:
            return True
        elif dir == RIGHT:
            return True
        elif dir == UP:
            return True
        elif dir == DOWN:
            return True

    def get_pos(self):
        self.tile = (((self.rect.x%100)//20)-1, ((self.rect.y%100)//20)-1)
        return self.tile

    def update_map(self):
        self.pos = self.get_pos()
        edit_map(self.pos[0], self.pos[1], self.num)

def find_empty_square(map):
    options = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 0:
                options.append((j, i))
    x, y = random.choice(options)
    return x, y


def new_block(map):
    square = find_empty_square(map)
    Tile(((square[0]*100)+(20*(square[0]+1)), (square[1]*100)+(20*(square[1]+1))))

def edit_map(x:int, y:int, num:int):
    MAP[y][x] = num

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)

board = pygame.sprite.Group()
tiles = pygame.sprite.Group()

for i in range(0, 500, 120):
    Vertical(i, 0)
    Horizontal(0, i)

new_block(MAP)

clock = pygame.time.Clock()

def run(MAP=MAP):

    done = False

    while not done and len(tiles.sprites()) != 16:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_LEFT:
                    # for i in tiles:
                    #     i.left()
                    MAP = logic.left(MAP)
                    new_block(MAP)
                elif event.key == pygame.K_RIGHT:
                    # for i in tiles:
                    #     i.right()
                    MAP = logic.right(MAP)
                    new_block(MAP)
                elif event.key == pygame.K_UP:
                    # for i in tiles:
                    #     i.up()
                    MAP = logic.up(MAP)
                    new_block(MAP)
                elif event.key == pygame.K_DOWN:
                    # for i in tiles:
                    #     i.down()
                    MAP = logic.down(MAP)
                    new_block(MAP)
                elif event.key == pygame.K_SPACE:
                    print(f"{MAP[0]}\n{MAP[1]}\n{MAP[2]}\n{MAP[3]}\n")

        for i in tiles:
            i.kill()
        
        for i in range(len(MAP)):
            for j in range(len(MAP[i])):
                if MAP[i][j] != 0:
                    Tile(((j*100)+(20*(j+1)), (i*100)+(20*(i+1))), MAP[i][j])

        tiles.update()

        screen.fill((205,192,180))

        board.draw(screen)
        tiles.draw(screen)

        pygame.display.flip()

    time.sleep(1)
    pygame.quit()

if __name__ == "__main__":
    run()