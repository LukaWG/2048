from time import sleep
import menu
import pygame
import random
from copy import deepcopy

import logic
import error

SPEED_FACTOR = 15 # 15 recommended

assert (120/SPEED_FACTOR).is_integer(), ("SPEED_FACTOR is not a factor of 120")

FPS = 50 # 50 recommneded

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

PREVENT_CLOSE = True

#region - classes
class Board(pygame.sprite.Sprite):
    '''
    Parent class for the borders of each square
    '''
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
    '''
    Vertical borders
    '''
    def __init__(self, x, y):
        super().__init__([20, 500], x, y)

class Horizontal(Board):
    '''
    Horizontal borders
    '''
    def __init__(self, x, y):
        super().__init__([500, 20], x, y)

class Tile(pygame.sprite.Sprite):
    '''
    Class for the tiles containing the numbers
    '''
    def __init__(self, pos, num=None):
        super().__init__(tiles) # Adds to the group called tiles

        self.myfont = pygame.font.Font(pygame.font.get_default_font(), 40)

        self.image = pygame.Surface([100, 100])

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.dir = None
        self.counter = 0

        if num == None:
            if len(tiles.sprites()) > 5:
                self.text(random.choice([2, 4]))
            else:
                self.text(2)
        else:
            self.text(num)

        
        MAP[((self.rect.y%100)//20)-1][((self.rect.x%100)//20)-1] = self.num

    def text(self, num):
        '''Writes text to the center of the tile
        '''
        self.num = num
        if self.num == 2:
            self.image.fill((238, 228, 218))
        elif self.num == 4:
            self.image.fill((237, 224, 200))
        elif self.num == 8:
            self.image.fill((242, 177, 121))
        elif self.num == 16:
            self.image.fill((245, 149, 99 ))
        elif self.num == 32:
            self.image.fill((246, 124, 95 ))
        elif self.num == 64:
            self.image.fill((247, 97 , 72 ))
        elif self.num == 128:
            self.image.fill((239, 207, 114))
        elif self.num == 256:
            self.image.fill((237, 204, 97 ))
        elif self.num == 512:
            self.image.fill((237, 200, 80 ))
        elif self.num == 1024:
            self.image.fill((237, 197, 63 ))
        elif self.num == 2048:
            self.image.fill((237, 194, 46 ))
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
        '''Updates tile position
        '''
        if self.counter < 120//SPEED_FACTOR:
            if self.dir == LEFT or self.dir == RIGHT:
                self.rect.x += self.speed*SPEED_FACTOR
            elif self.dir == UP or self.dir == DOWN:
                self.rect.y += self.speed*SPEED_FACTOR
            self.counter += 1
        else:
            self.dir = None


    def move(self, dir, num):
        '''
        Sets direction and speed of the tile to be moved
        '''
        self.counter = 0
        self.speed, self.dir = dir.split()
        self.speed = int(self.speed)
        self.num = num

class End_Text(pygame.sprite.Sprite):
    '''
    Class for the text at the end of the game
    '''
    def __init__(self, state):
        super().__init__(text)
        if state == "LOSE":
            self.text = ["Game over", "Press any key to exit"]
        elif state == "WIN":
            self.text = ["You won!", "Press any key to exit"]
        self.myfont = pygame.font.Font(pygame.font.get_default_font(), 40)
        self.to_display1 = self.myfont.render(self.text[0], False, (1, 1, 1))
        self.to_display1_rect = self.to_display1.get_rect()
        self.to_display2 = self.myfont.render(self.text[1], False, (1, 1, 1))
        self.to_display2_rect = self.to_display2.get_rect()

        self.sizex = self.to_display2_rect.size[0]
        self.sizey = self.to_display1_rect.size[1] + self.to_display2_rect.size[1]

        self.image = pygame.Surface((self.sizex, self.sizey)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREENSIZE[0]//2
        self.rect.centery = SCREENSIZE[0]//2

        pos = (0, 0)
        self.image.blit(self.to_display1, pos)
        self.image.blit(self.to_display2, (pos[0], pos[1]+self.sizey//2))
#endregion - classes

#region - functions
def find_empty_square(map):
    '''
    Finds an empty square in the map (for a new tile)
    '''
    options = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 0:
                options.append((j, i))
    x, y = random.choice(options)
    return x, y


def new_block(map):
    '''
    Creates a new tile with no number value
    '''
    square = find_empty_square(map)
    Tile(((square[0]*100)+(20*(square[0]+1)), (square[1]*100)+(20*(square[1]+1))))

def find_changes(movemap, tilemap, map):
    '''
    Finds changes in the map, and updates each tile with there speed and direction
    '''
    movelist = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    change = False
    for i in range(len(movemap)):
        for j in range(len(movemap[i])):
            if movemap[i][j] != (None, None) and movemap[i][j] != ((None, None), (None, None)):
                if len(str(movemap[i][j][0])) == 1:
                    if movemap[i][j] != (j, i):
                        change = True
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
                            change = True
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
    return change

def create_tiles(map):
    '''
    Destroys all tiles, and replaces them with tiles based on the map
    Ensures there are not two tiles on top of each other
    '''
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
#endregion - functions

pygame.init()
logo = pygame.image.load("2048_logo.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("2048")
screen = pygame.display.set_mode(SCREENSIZE)

board = pygame.sprite.Group()
tiles = pygame.sprite.Group()
text = pygame.sprite.Group()

for i in range(0, 500, 120):
    Vertical(i, 0)
    Horizontal(0, i)

new_block(MAP)
new_block(MAP)

clock = pygame.time.Clock()

class Game:

    def resume(self):
        self.paused = False

    def run(self, MAP=MAP):
        '''
        Main function to run the game
        '''

        self.MAP = MAP

        self.counter = 119
        self.ttfe = False
        self.game_completed = False

        self.event_loop()

    def event_loop(self):

        self.done = False
        self.paused = False
        self.tilemap = create_tiles(self.MAP)

        while not self.done:

            if self.paused:
                self.menuscreen.changestate(menu.MenuStates.pause)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        if PREVENT_CLOSE:
                            pygame.display.iconify()
                        else:
                            self.done = True
                    else:
                        self.menuscreen.event_check(event)

                self.menuscreen.render()

                screen.blit(self.menuscreen.image, (0,0))

                pygame.display.flip()

            else:

                clock.tick(FPS)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        if PREVENT_CLOSE:
                            pygame.display.iconify()
                        else:
                            self.done = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.paused = True
                        elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN] and self.counter >= 120//SPEED_FACTOR:
                            if event.key == pygame.K_LEFT:
                                self.MAP, MOVE_MAP = logic.left(self.MAP)

                                if find_changes(MOVE_MAP, self.tilemap, self.MAP):
                                    self.counter = 0
                            elif event.key == pygame.K_RIGHT:
                                self.MAP, MOVE_MAP = logic.right(self.MAP)

                                if find_changes(MOVE_MAP, self.tilemap, self.MAP):
                                    self.counter = 0
                            elif event.key == pygame.K_UP:
                                self.MAP, MOVE_MAP = logic.up(self.MAP)

                                if find_changes(MOVE_MAP, self.tilemap, self.MAP):
                                    self.counter = 0
                            elif event.key == pygame.K_DOWN:
                                self.MAP, MOVE_MAP = logic.down(self.MAP)

                                if find_changes(MOVE_MAP, self.tilemap, self.MAP):
                                    self.counter = 0
                            for i in self.MAP:
                                for j in i:
                                    if j == 2048:
                                        self.ttfe = False if self.game_completed else True
                                        self.game_completed = True
                                        print(self.ttfe)

                self.counter += 1
                if self.counter == 120//SPEED_FACTOR:
                    if self.ttfe:
                        self.done = True
                    new_block(self.MAP)
                    self.tilemap = create_tiles(self.MAP)
                if self.counter == 120//SPEED_FACTOR + 1:
                    if len(tiles.sprites()) == 16:
                        if not logic.check_merge(deepcopy(self.MAP)):
                            self.done = True

                tiles.update()

                screen.fill((205,192,180))

                board.draw(screen)
                tiles.draw(screen)

                pygame.display.flip()
        print("HERE")
        if self.ttfe:
            finished = False
            End_Text("WIN")
            self.menuscreen.changestate(menu.MenuStates.win)
            self.gamefinished = True
            while not finished:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    elif event.type == pygame.KEYDOWN:
                        finished = True
                text.draw(screen)

                pygame.display.flip()

        if len(tiles.sprites()) == 16:
            finished = False
            End_Text("LOSE")
            text.draw(screen)
            pygame.display.flip()

            sleep(1)

            while not finished:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    elif event.type == pygame.KEYDOWN:
                        finished = True
                        self.quit_menu()

    def quit(self):
        self.done = True
        exit()

    def quit_menu(self):
        self.donemenu = True

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode(SCREENSIZE)
        
        self.menuscreen = menu.Menu(menu.MenuStates.main, *SCREENSIZE, bgcolour=(205, 192, 180))

        self.menuscreen.addtext(menu.MenuStates.main, "2048", 30, 210, 20)
        self.menuscreen.addbutton(menu.MenuStates.main, "Start", 22, 220, 100, menu.Bound_Function(self.run))
        self.menuscreen.addbutton(menu.MenuStates.main, "Exit", 22, 222, 180, menu.Bound_Function(self.quit_menu))

        self.menuscreen.addtext(menu.MenuStates.pause, "2048", 30, 210, 20)
        self.menuscreen.addbutton(menu.MenuStates.pause, "Resume", 22, 215, 100, menu.Bound_Function(self.resume))
        self.menuscreen.addbutton(menu.MenuStates.pause, "Exit", 22, 222, 180, menu.Bound_Function(self.quit))

        self.menuscreen.addtext(menu.MenuStates.win, "2048", 30, 210, 20)
        self.menuscreen.addbutton(menu.MenuStates.win, "Continue", 22, 215, 100, menu.Bound_Function(self.event_loop))
        self.menuscreen.addbutton(menu.MenuStates.win, "Exit", 22, 222, 180, menu.Bound_Function(self.quit))

        self.donemenu = False
        while not self.donemenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.donemenu = True
                else:
                    self.menuscreen.event_check(event)

            self.menuscreen.render()
            screen.blit(self.menuscreen.image, (0,0))
            
            pygame.display.update()
        try:
            pygame.quit()
        except:
            pass

if __name__ == "__main__":
    game = Game()
    game.start()
    try:
        pygame.quit()
    except:
        pass
