# Moving left works. Now implement with other directions

import time
import pygame
import random

import logic
import error

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
        self.counter = 0
        self.state = "KEEP"

        if num == None:
            if len(tiles.sprites()) > 5:
                self.text(random.choice([2, 4]))
            else:
                self.text(2)
        else:
            self.text(num)

        edit_map(((self.rect.x%100)//20)-1, ((self.rect.y%100)//20)-1, self.num)

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
        if self.counter < 120:
            if self.dir == LEFT or self.dir == RIGHT:
                self.rect.x += self.speed
            elif self.dir == UP or self.dir == DOWN:
                self.rect.y += self.speed
            self.counter += 1
        else:
            self.dir = None
            if self.state == "KEEP":
                # print(f"{int(time.time())} - CHANGING NUMBER")
                self.text(self.num)
            elif self.state == "DELETE":
                self.kill()
            else:
                print("UNKNOW STATE\n\nUNKNOW STATE\n\nUNKNOW STATE\n\nUNKNOW STATE\n\nUNKNOW STATE\n\nUNKNOW STATE\n\n")


    def move(self, dir, num, state="KEEP"):
        self.counter = 0
        self.speed, self.dir = dir.split()
        self.speed = int(self.speed)
        self.num = num
        self.state = state
        if self.state == "DELETE":
            if self.dir == RIGHT or self.dir == DOWN:
                self.speed += 1
            elif self.dir == LEFT or self.dir == UP:
                self.speed -= 1

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

def find_changes(movemap, tilemap, map):

    movelist = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(len(movemap)):
        for j in range(len(movemap[i])):
            if movemap[i][j] != (None, None):
                if len(str(movemap[i][j][0])) == 1:
                    if movemap[i][j] != (j, i):
                        dir = None

                        hor = j - movemap[i][j][0]
                        if hor < 0:
                            dir = f"{hor} {LEFT}"
                        elif hor > 0:
                            dir = f"{hor} {RIGHT}"
                        
                        ver = i - movemap[i][j][1]
                        if ver < 0:
                            dir = f"{ver} {UP}"
                        elif ver > 0:
                            dir = f"{ver} {DOWN}"

                        if not dir:
                            raise error.Dir_Not_Definied("dir is not definied")

                        movelist[movemap[i][j][1]][movemap[i][j][0]] = dir # number followed by direction e.g 2 LEFT (means move 2 left)
                        tilemap[movemap[i][j][1]][movemap[i][j][0]].move(movelist[movemap[i][j][1]][movemap[i][j][0]], map[i][j])
                elif len(movemap[i][j][0]) == 2:
                    for k in range(2):
                        if movemap[i][j][k] != (j, i):
                            dir = None

                            hor = j - movemap[i][j][k][0]
                            if hor < 0:
                                dir = f"{hor} {LEFT}"
                            elif hor > 0:
                                dir = f"{hor} {RIGHT}"
                            
                            ver = i - movemap[i][j][k][1]
                            if ver < 0:
                                dir = f"{ver} {UP}"
                            elif ver > 0:
                                dir = f"{ver} {DOWN}"

                            if not dir:
                                raise error.Dir_Not_Definied("dir is not definied")

                            movelist[movemap[i][j][k][1]][movemap[i][j][k][0]] = dir # number followed by direction e.g 2 LEFT (means move 2 left)
                            tilemap[movemap[i][j][k][1]][movemap[i][j][k][0]].move(movelist[movemap[i][j][k][1]][movemap[i][j][k][0]], map[i][j])

def create_tiles(map):
    for i in tiles:
        i.kill()

    tilemap = []
    
    for i in range(len(map)):
        for j in range(len(map[i])):
            tilemap.append([])
            if map[i][j] != 0:
                tilemap[i].append(Tile(((j*100)+(20*(j+1)), (i*100)+(20*(i+1))), map[i][j]))
            else:
                tilemap[i].append(None)

    return tilemap

pygame.init()
logo = pygame.image.load("2048_logo.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("2048")
screen = pygame.display.set_mode(SCREENSIZE)

board = pygame.sprite.Group()
tiles = pygame.sprite.Group()

for i in range(0, 500, 120):
    Vertical(i, 0)
    Horizontal(0, i)

new_block(MAP)

clock = pygame.time.Clock()

def run(MAP=MAP):

    counter = 119

    tilemap = []

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
                    MAP, MOVE_MAP = logic.left(MAP)

                    find_changes(MOVE_MAP, tilemap, MAP)
                                
                    counter = 0
                elif event.key == pygame.K_RIGHT:
                    MAP = logic.right(MAP)
                                
                    counter = 119
                elif event.key == pygame.K_UP:
                    MAP = logic.up(MAP)
                                
                    counter = 119
                elif event.key == pygame.K_DOWN:
                    MAP = logic.down(MAP)
                                
                    counter = 119
                elif event.key == pygame.K_SPACE:
                    print(f"{MAP[0]}\n{MAP[1]}\n{MAP[2]}\n{MAP[3]}\n")
                elif event.key == pygame.K_RETURN:
                    tilemap = create_tiles(MAP)

        counter += 1
        if counter == 120:
            new_block(MAP)
            tilemap = create_tiles(MAP)

        tiles.update()

        screen.fill((205,192,180))

        board.draw(screen)
        tiles.draw(screen)

        pygame.display.flip()

    time.sleep(1)
    pygame.quit()

if __name__ == "__main__":
    run()