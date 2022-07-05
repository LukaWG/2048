# \u2611 tick ☑
# \u2610 box  ☐

from collections import defaultdict
import math
import os
from enum import Enum
import pygame
from pygame.locals import (
    QUIT,
    KEYDOWN,
    KEYUP,
    K_ESCAPE,
    K_LSHIFT,
    K_RSHIFT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
    RESIZABLE,
    VIDEORESIZE
)

keys = { # A list of all keys with their codes
    pygame.K_q: "q",
    pygame.K_w: "w",
    pygame.K_e: "e",
    pygame.K_r: "r",
    pygame.K_t: "t",
    pygame.K_y: "y",
    pygame.K_u: "u",
    pygame.K_i: "i",
    pygame.K_o: "o",
    pygame.K_p: "p",
    pygame.K_a: "a",
    pygame.K_s: "s",
    pygame.K_d: "d",
    pygame.K_f: "f",
    pygame.K_g: "g",
    pygame.K_h: "h",
    pygame.K_j: "j",
    pygame.K_k: "k",
    pygame.K_l: "l",
    pygame.K_z: "z",
    pygame.K_x: "x",
    pygame.K_c: "c",
    pygame.K_v: "v",
    pygame.K_b: "b",
    pygame.K_n: "n",
    pygame.K_m: "m",
    pygame.K_SPACE: " ",
    pygame.K_UNDERSCORE: "_",
    pygame.K_MINUS: "-",
    pygame.K_PERIOD: ".",
    pygame.K_0: "0",
    pygame.K_1: "1",
    pygame.K_2: "2",
    pygame.K_3: "3",
    pygame.K_4: "4",
    pygame.K_5: "5",
    pygame.K_6: "6",
    pygame.K_7: "7",
    pygame.K_8: "8",
    pygame.K_9: "9",
    pygame.K_KP0: "0", # num pad numbers
    pygame.K_KP1: "1",
    pygame.K_KP2: "2",
    pygame.K_KP3: "3",
    pygame.K_KP4: "4",
    pygame.K_KP5: "5",
    pygame.K_KP6: "6",
    pygame.K_KP7: "7",
    pygame.K_KP8: "8",
    pygame.K_KP9: "9",
    pygame.K_KP_PERIOD: ".",
    pygame.K_BACKSPACE: "<BACKSPACE>",
    pygame.K_DELETE: "<DELETE>",
    pygame.K_RETURN: "<ENTER>",
}

class MenuStates(Enum):
    main = 0
    pause = 1

class MenuComponent:
    def __init__(self, text, fontsize, menu, posx, posy, paddingx=10, paddingy=10, backgroundcol=(255,255,255), foregroundcol=(0,0,0), activebgcol=(200,200,200), activefgcol=(0,0,0), centered=True, shouldrender=True, width=None):
        '''
        Base class for all menu components to inherit from
        '''
        self.text = text
        self.fontsize = fontsize
        self.menu = menu
        self.posx = posx
        self.posy = posy
        self.paddingx = paddingx
        self.paddingy = paddingy
        self.bgcol = backgroundcol
        self.fgcol = foregroundcol
        self.activebgcol = activebgcol
        self.activefgcol = activefgcol
        self.centered = centered
        self.shouldrender = self.needtorender = shouldrender # Keeps empty space if not rendered
        self.width = width

        self.selected = False # True when item has been clicked on
        self.active = False # True when mouse hovers over

        self.set_size()

    def render(self):
        '''
        Function for rendering menu components
        Will only render if the component has changed
        '''
        if self.shouldrender and self.needtorender:
            self.needtorender = False
            if self.active: # Mouse hovering over
                self.image = pygame.Surface(self.size) # Create surface
                self.image.fill(self.activebgcol)
                self.textsurf = self.font.render(self.text, True, self.activefgcol) # Create text
                if self.centered:
                    x = (self.size[0]-self.textsurf.get_width())//2
                    y = (self.size[1]-self.textsurf.get_height())//2
                else:
                    x = self.paddingx
                    y = self.paddingy
                self.image.blit(self.textsurf, (x, y))
            else:
                self.image = pygame.Surface(self.size) # Create surface
                self.image.fill(self.bgcol)
                self.textsurf = self.font.render(self.text, True, self.fgcol) # Create text
                if self.centered:
                    x = (self.size[0]-self.textsurf.get_width())//2
                    y = (self.size[1]-self.textsurf.get_height())//2
                else:
                    x = self.paddingx
                    y = self.paddingy
                self.image.blit(self.textsurf, (x, y))

    def active_check(self): #! IS NOT USED
        mousepos = pygame.mouse.get_pos()
        if self.posx < mousepos[0] < self.posx+self.size[0] and self.posy < mousepos[1] < self.posy+self.size[1] and not self.selected and not self.active:
            self.set_active()
        else:
            self.set_inactive()

    def set_active(self):
        '''
        Changes settings to render object again as if the mouse is hovering over
        '''
        self.needtorender = True
        self.menu.needtorender = True
        self.active = True

    def set_inactive(self):
        '''
        Changes settings to render object again as if the mouse is not hovering over
        '''
        self.needtorender = True
        self.menu.needtorender = True
        self.active = False

    def set_size(self):
        '''
        Caclulates dimensions for the object
        '''
        self.font = pygame.font.Font(os.path.join("data", "menufont.ttf"), self.fontsize) # Load font
        sizex, sizey = self.font.size(self.text)
        if self.width:
            sizex = self.width
        self.size = (sizex+self.paddingx*2, sizey+self.paddingy*2) # Calculate size of textbox

    def select(self, mousepos):
        '''
        Sets the object to the colour for when it is clicked on
        '''
        if self.posx <= mousepos[0] <= self.posx+self.size[0] and self.posy < mousepos[1] < self.posy+self.size[1]:
            self.selected = True
            self.bgcol = self.selectbgcol
            self.fgcol = self.selecttextcol
            self.active = False
            self.needtorender = True
            self.menu.needtorender = True
        else:
            self.deselect()

    def deselect(self):
        '''
        Deselects the menu component when the object is clicked off
        '''
        self.selected = False
        self.bgcol = self.ogbgcol
        self.fgcol = self.ogtextcol
        self.needtorender = True
        self.menu.needtorender = True

    def scroll(self, dist):
        self.posx += dist[0]
        self.posy += dist[1]
        self.needtorender = True

class Text(MenuComponent):
    def __init__(self, text, fontsize, menu, posx, posy, paddingx=10, paddingy=10, backgroundcol=(255,255,255), textcol=(0,0,0), centered=True, shouldrender=True):
        '''
        Creates a text object

        :param text: Text to display
        :param fontsize: Size of font
        :param menu: Menu object to add the text to
        :param posx: X position of the text
        :param posy: Y position of the text
        :param paddingx: Padding on the x axis
        :param paddingy: Padding on the y axis
        :param backgroundcol: Colour of the background
        :param textcol: Colour of the text
        :param centered: Whether the text should be centered
        :param shouldrender: Whether the text should be rendered
        '''
        super().__init__(text, fontsize, menu, posx, posy, paddingx=paddingx, paddingy=paddingy, backgroundcol=backgroundcol, foregroundcol=textcol, centered=centered, shouldrender=shouldrender)

    def active_check(self): #! IS NOT USED
        pass # Text does not need to be clicked

class Button(MenuComponent):
    def __init__(self, text, fontsize, menu, posx, posy, function, paddingx=10, paddingy=10, backgroundcol=(255,255,255), textcol=(0,0,0), activebgcol=(200,200,200), activefgcol=(0,0,0), centered=True, shouldrender=True, _width=None, _height=None):
        '''
        Creates a button object

        :param text: Text to display
        :param fontsize: Size of font
        :param menu: Menu object to add the text to
        :param posx: X position of the text
        :param posy: Y position of the text
        :param function: Function to call when the button is clicked
        :param paddingx: Padding on the x axis
        :param paddingy: Padding on the y axis
        :param backgroundcol: Colour of the background
        :param textcol: Colour of the text
        :param activebgcol: Colour of the background when the mouse is over the button
        :param activefgcol: Colour of the text when the mouse is over the button
        :param centered: Whether the text should be centered
        :param shouldrender: Whether the text should be rendered
        '''
        self._height = _height
        self._width = _width
        super().__init__(text, fontsize, menu, posx, posy, paddingx, paddingy, backgroundcol, textcol, activebgcol, activefgcol, centered, shouldrender)
        self.ogbgcol = backgroundcol
        self.ogtextcol = textcol
        self.selectbgcol = backgroundcol
        self.selecttextcol = textcol
        self.function = function.function
        self.args = function.args

    def set_size(self):
        '''
        Sets the size of the object
        '''
        super().set_size()
        if self._height:
            self.size = (self._width, self._height)

    def write(self, *args):
        pass

    def select(self, mousepos):
        '''
        Checks if the button is cliked on, and if so, calls the function

        :param mousepos: Mouse position
        '''
        self.selected = False
        if self.posx < mousepos[0] < self.posx+self.size[0] and self.posy < mousepos[1] < self.posy+self.size[1]:
            self.click()

    def click(self):
        '''
        Calls the function
        '''
        self.function(*self.args)

class Input(MenuComponent):
    def __init__(self, width, fontsize, menu, posx, posy, paddingx=10, paddingy=10, backgroundcol=(255,255,255), textcol=(0,0,0), activebgcol=(200,200,200), activefgcol=(0,0,0), selectbgcol=(225,225,225), selecttextcol=(10,10,10), centered=True, shouldrender=True, max_len=None):
        '''
        An input object

        :param width: Width of the input box
        :param fontsize: Size of the font
        :param menu: Menu object to add the input box to
        :param posx: X position of the text
        :param posy: Y position of the text
        :param paddingx: Padding on the x axis
        :param paddingy: Padding on the y axis
        :param backgroundcol: Colour of the background
        :param textcol: Colour of the text
        :param activebgcol: Colour of the background when the mouse is over the object
        :param activefgcol: Colour of the text when the mouse is over the object
        :param selectbgcol: Colour of the background when the object is selected
        :param selecttextcol: Colour of the text when the object is selected
        :param centered: Whether the text should be centered
        :param shouldrender: Whether the text should be rendered
        :param max_len: Maximum length of the input
        '''
        super().__init__("", fontsize, menu, posx, posy, paddingx, paddingy, backgroundcol, textcol, activebgcol, activefgcol, centered, shouldrender, width)
        self.ogbgcol = backgroundcol
        self.ogtextcol = textcol
        self.selectbgcol = selectbgcol
        self.selecttextcol = selecttextcol
        self.maxlen = max_len

    def write(self, key, upper=False):
        '''
        Writes to the input box
        '''
        if self.selected and key in keys:
            if keys[key] == "<BACKSPACE>":
                self.text = self.text[:-1]
            elif keys[key] == "<ENTER>":
                self.deselect()
            elif keys[key] == "<DELETE>":
                self.text = ""
            else:
                if upper:
                    self.text += keys[key].upper()
                else:
                    self.text += keys[key]
            self.verify_input()
            self.needtorender = True
            self.menu.needtorender = True

    def verify_input(self):
        '''
        Checks that the input is valid
        '''
        if self.maxlen:
            while len(self.text) > self.maxlen:
                self.text = self.text[:-1]

class SpinWheel(MenuComponent):
    def __init__(self, state, number, width, fontsize, menu, posx, posy, step=1, minval=None, maxval=None, paddingx=10, paddingy=10, backgroundcol=(255,255,255), textcol=(0,0,0), activebgcol=(200,200,200), activefgcol=(0,0,0), selectbgcol=(225,225,225), selecttextcol=(10,10,10), centered=True, shouldrender=True):
        '''
        An input component for integers

        :param state: Menu state that the spin wheel is added to
        :param number: The number displayed in the component
        :param width: Width of the spin wheel box
        :param fontsize: Size of the font
        :param menu: Menu object to add the component to
        :param posx: X position of the box
        :param posy: Y position of the box
        :param step: Increment value of the spin wheel. Must be an integer
        :param minval: Minimum value of the spinwheel
        :param maxval: Maximum value of the spinwheel
        :param paddingx: Padding on the x axis
        :param paddingy: Padding on the y axis
        :param backgroundcol: Colour of the background
        :param textcol: Colour of the text
        :param activebgcol: Colour of the background when the mouse is over the object
        :param activefgcol: Colour of the text when the mouse is over the object
        :param selectbgcol: Colour of the background when the object is selected
        :param selecttextcol: Colour of the text when the object is selected
        :param centered: Whether the text should be centered
        :param shouldrender: Whether the text should be rendered
        '''
        super().__init__(str(number), fontsize, menu, posx, posy, paddingx, paddingy, backgroundcol, textcol, activebgcol, activefgcol, centered, shouldrender, width)
        self.ogbgcol = backgroundcol
        self.ogtextcol = textcol
        self.selectbgcol = selectbgcol
        self.selecttextcol = selecttextcol
        self.maxval = maxval
        self.minval = minval
        self.step = step

        # Create buttons for up and down (↑↓)
        size1 = self.size[1]//2
        size2 = self.size[1] - size1
        self.up = Button("^", self.fontsize, menu, posx+self.size[0], posy, Bound_Function(self.increment_up), _width=20, _height=size1) # Need to bind to function to adjust value
        self.down = Button("v", self.fontsize, menu, posx+self.size[0], posy+(size1), Bound_Function(self.increment_down), _width=20, _height=size2)

        self.menu.components[state].append(self.up)
        self.menu.components[state].append(self.down) 
        self.menu.selectable[state].append(self.up)
        self.menu.selectable[state].append(self.down)

    def increment_up(self):
        self.text = str(int(self.text)+self.step)

    def increment_down(self):
        self.text = str(int(self.text)-self.step)

    def write(self, key, *args):
        if self.selected and key in keys:
            if keys[key] == "<BACKSPACE>": # Check if a character needs to be removed
                self.text = self.text[:-1]
            else:
                self.text += keys[key]
            self.verify_input() # Check input is valid
            self.needtorender = True
            self.menu.needtorender = True

    def verify_input(self):
        if len(self.text) == 0:
            self.text = "0"
        if not self.text[-1].isnumeric():
            if self.text[-1] == "-":
                if self.text[0] == "-":
                    self.text = self.text[1:]
                else:
                    self.text = "-" + self.text
            self.text = self.text[:-1]
        elif self.text[0] == "0" and len(self.text) > 1:
            self.text = self.text[1:]

    def deselect(self):
        super().deselect()
        if self.maxval:
            if int(self.text) > self.maxval:
                self.text = str(self.maxval)
        if self.minval:
            if int(self.text) < self.minval:
                self.text = str(self.minval)

class TickBox(MenuComponent):
    def __init__(self, bool, size, menu, posx, posy, paddingx=10, paddingy=10, backgroundcol=(255,255,255), tickcol=(0,0,0), activebgcol=(200,200,200), activetickcol=(0,0,0), shouldrender=True):
        super().__init__("\u2611" if bool else "\u2610", size, menu, posx, posy, paddingx, paddingy, backgroundcol, tickcol, activebgcol, activetickcol, shouldrender=shouldrender)
        self.bool = bool

    def set_size(self):
        '''
        Caclulates dimensions for the object
        '''
        try:
            self.font = pygame.font.Font(os.path.join("data", "menufont2.otf"), self.fontsize) # Load font
        except FileNotFoundError:
            self.font = pygame.font.Font(os.path.join("N:", "!Sixth Form", "Computer Science", "Course Work", "Code", "data", "menufont2.otf"), self.fontsize)
        sizex, sizey = self.font.size(self.text)
        if self.width:
            sizex = self.width
        self.size = (sizex+self.paddingx*2, sizey+self.paddingy*2) # Calculate size of textbox

    def select(self, mousepos):
        self.selected = False
        if self.posx < mousepos[0] < self.posx+self.size[0] and self.posy < mousepos[1] < self.posy+self.size[1]:
            self.change_val()

    def change_val(self):
        self.bool = not self.bool
        self.text = "\u2611" if self.bool else "\u2610"
        self.needtorender = True
        self.menu.needtorender = True

    def write(self, *args):
        pass

class ScrollBar:
    def __init__(self, width, height, menu):
        self.width = width
        self.height = height
        self.horselect = False
        self.verselect = False
        self.menu = menu
        self.hpos = None
        self.vpos = None
        self.hdist = 0
        self.vdist = 0
        self.hscroll = False
        self.vscroll = False

    def resize(self, dim, change):
        distancex = 0
        if change[0] > 0 and self.hdist > 0:
            distancex = min(change[0], self.hdist)
            for key in self.menu.components.keys():
                for item in self.menu.components[key]:
                    item.scroll((distancex, 0))
        if self.width > dim[0]:
            self.horizontal_scroll(self.width-dim[0], dim, distance_from_edge=self.hdist-distancex)
        else:
            self.horizontal_scroll(False, None)
        distancey = 0
        if change[1] > 0 and self.vdist > 0:
            distancey = min(change[1], self.vdist)
            for key in self.menu.components.keys():
                for item in self.menu.components[key]:
                    item.scroll((0, distancey))
        if self.height > dim[1]:
            self.vertical_scroll(self.height-dim[1], dim, distance_from_edge=self.vdist-distancey)
        else:
            self.vertical_scroll(False, None)

    def horizontal_scroll(self, dist, dim, distance_from_edge=None):
        if dist == False:
            self.hscroll = False
            self.hdist = 0
        else:
            self.hdist = distance_from_edge if distance_from_edge else 0
            self.hscroll = True
            self.hdim = (dim[0], 10)
            self.himage = pygame.Surface(self.hdim)
            self.himage.fill((160, 160, 160))
            self.hpos = (0, dim[1]-10)
            self.hscrollimage = pygame.Surface((dim[0]-dist, 10))
            self.hscrollimage.fill((100, 100, 100))
            if distance_from_edge:
                self.hscrollpos = (distance_from_edge, dim[1]-10)
            else:
                self.hscrollpos = (0, dim[1]-10)
            self.hscrolldim = (dim[0]-dist, 10)

    def vertical_scroll(self, dist, dim, distance_from_edge=None):
        if dist == False:
            self.vscroll = False
            self.vdist = 0
        else:
            self.vdist = distance_from_edge if distance_from_edge else 0
            self.vscroll = True
            self.vdim = (10, dim[1])
            self.vimage = pygame.Surface(self.vdim)
            self.vimage.fill((160, 160, 160))
            self.vpos = (dim[0]-10, 0)
            self.vscrollimage = pygame.Surface((10, dim[1]-dist))
            self.vscrollimage.fill((100, 100, 100))
            if distance_from_edge:
                self.vscrollpos = (dim[0]-10, distance_from_edge)
            else:
                self.vscrollpos = (dim[0]-10, 0)
            self.vscrolldim = (10, dim[1]-dist)
    
    def horscroll(self, dist):
        if self.hscroll:
            oghorpos = self.hscrollpos
            self.hscrollpos = (self.hscrollpos[0] + dist, self.hscrollpos[1])
            if self.hscrollpos[0] < 0:
                self.hscrollpos = (0, self.hscrollpos[1])
            if self.hscrollpos[0] + self.hscrolldim[0] > self.hdim[0]:
                self.hscrollpos = (self.hdim[0]-self.hscrolldim[0], self.hscrollpos[1])

            dist = oghorpos[0] - self.hscrollpos[0]
            self.hdist -= dist

            for key in self.menu.components.keys():
                for item in self.menu.components[key]:
                    item.scroll((dist, 0))
                    self.menu.needtorender = True
    
    def verscroll(self, dist):
        if self.vscroll:
            ogvorpos = self.vscrollpos
            self.vscrollpos = (self.vscrollpos[0], self.vscrollpos[1] + dist)
            if self.vscrollpos[1] < 0:
                self.vscrollpos = (self.vscrollpos[0], 0)
            if self.vscrollpos[1] + self.vscrolldim[1] > self.vdim[1]:
                self.vscrollpos = (self.vscrollpos[0], self.vdim[1]-self.vscrolldim[1])

            dist = ogvorpos[1] - self.vscrollpos[1]
            self.vdist -= dist

            for key in self.menu.components.keys():
                for item in self.menu.components[key]:
                    item.scroll((0, dist))
                    self.menu.needtorender = True

class Menu:
    def __init__(self, state, width, height, bgimagefp=None, bgcolour=None): # State is the name of the menu screen (different screens will have a different state)
        '''
        Class for any menuscreens
        All screens stored here with different screens having a different state
        '''
        self.width = width
        self.height = height
        self.state = state
        self.components = defaultdict(list)
        self.selectable = defaultdict(list)
        self.needtorender = True
        self.bgcolour = bgcolour
        self.bgimagefp = bgimagefp
        self.set_background()

        self.upper = False

        self.scrollbar = ScrollBar(width, height, self)

    def render(self):
        if self.needtorender:
            self.needtorender = False
            self.image = pygame.Surface((self.width, self.height))
            if self.bgcolour:
                self.image.fill(self.bgcolour)
            if self.bgimagefp:
                self.image.blit(self.bgimage, (0, 0))
            for item in self.components[self.state]:
                if item.shouldrender:
                    item.render()
                    self.image.blit(item.image, (item.posx, item.posy))

        if self.scrollbar.hscroll:
            self.image.blit(self.scrollbar.himage, self.scrollbar.hpos)
            self.image.blit(self.scrollbar.hscrollimage, self.scrollbar.hscrollpos)

        if self.scrollbar.vscroll:
            self.image.blit(self.scrollbar.vimage, self.scrollbar.vpos)
            self.image.blit(self.scrollbar.vscrollimage, self.scrollbar.vscrollpos)

    def addtext(self, state, text, fontsize, posx, posy, paddingx=10, paddingy=10, backgroundcol=(255,255,255), textcol=(0,0,0), centered=True, shouldrender=True):
        self.components[state].append(Text(text, fontsize, self, posx, posy, paddingx, paddingy, backgroundcol, textcol, centered, shouldrender))

    def addbutton(self, state, text, fontsize, posx, posy, function, paddingx=10, paddingy=10, backgroundcol=(255,255,255), textcol=(0,0,0), activebgcol=(200,200,200), activefgcol=(0,0,0), centered=True, shouldrender=True):
        self.components[state].append(Button(text, fontsize, self, posx, posy, function, paddingx, paddingy, backgroundcol, textcol, activebgcol, activefgcol, centered, shouldrender))
        self.selectable[state].append(self.components[state][-1])

    def addinput(self, state, width, fontsize, posx, posy, paddingx=10, paddingy=10, backgroundcol=(255,255,255), textcol=(0,0,0), activebgcol=(200,200,200), activefgcol=(0,0,0), selectbgcol=(225,225,225), selecttextcol=(10,10,10), centered=True, shouldrender=True, maxlen=None):
        self.components[state].append(Input(width, fontsize, self, posx, posy, paddingx, paddingy, backgroundcol, textcol, activebgcol, activefgcol, selectbgcol, selecttextcol, centered, shouldrender, maxlen))
        self.selectable[state].append(self.components[state][-1])

    def addspinwheel(self, state, number, width, fontsize, posx, posy, step=1, minval=None, maxval=None, paddingx=10, paddingy=10, backgroundcol=(255,255,255), textcol=(0,0,0), activebgcol=(200,200,200), activefgcol=(0,0,0), selectbgcol=(255,255,255), selecttextcol=(10,10,10), centered=True, shouldrender=True):
        self.components[state].append(SpinWheel(state, number, width, fontsize, self, posx, posy, step, minval, maxval, paddingx, paddingy, backgroundcol, textcol, activebgcol, activefgcol, selectbgcol, selecttextcol, centered, shouldrender))
        self.selectable[state].append(self.components[state][-1])

    def addtickbox(self, state, bool, size, posx, posy, paddingx=10, paddingy=10, backgroundcol=(255,255,255), tickcol=(0,0,0), activebgcol=(200,200,200), activetickcol=(0,0,0), shouldrender=True):
        self.components[state].append(TickBox(bool, size, self, posx, posy, paddingx, paddingy, backgroundcol, tickcol, activebgcol, activetickcol, shouldrender))
        self.selectable[state].append(self.components[state][-1])

    def changestate(self, state):
        if self.state != state:
            for item in self.selectable[self.state]:
                item.deselect()
            self.state = state
            self.needtorender = True

    def check_select(self, mousepos):
        for item in self.selectable[self.state]:
            item.select(mousepos)

    def typing(self, key):
        for item in self.selectable[self.state]:
            item.write(key, self.upper)

    def check_active(self, mousepos):
        for item in self.selectable[self.state]:
            if item.posx <= mousepos[0] < item.posx+item.size[0] and item.posy <= mousepos[1] < item.posy+item.size[1] and not item.selected:
                if not item.active:
                    item.set_active()
            elif item.active or item.selected:
                item.set_inactive()

    def set_background(self):
        '''
        Loads the background image and calculates dimensions for it
        Scales image to the correct size
        '''
        if self.bgimagefp:
            image = pygame.image.load(self.bgimagefp)
            width = self.width
            height = int((width/image.get_width())*image.get_height())
            if height < self.height: # Image needs to be transformed in the other direction
                height = self.height
                width = int((height/image.get_height())*image.get_width())
            self.bgimage = pygame.transform.smoothscale(image, (width, height))

    def resize(self, dim):
        '''
        Called when the window is resized to adjust the size of the screen
        '''
        change = (dim[0]-self.width, dim[1]-self.height)
        self.scrollbar.resize(dim, change)
        self.width, self.height = dim
        self.set_background()
        self.needtorender = True
        self.render()

    def check_scroll(self, event):
        if self.scrollbar.hscroll:
            if event.buttons[0] == 0:
                self.scrollbar.horselect = False
                self.scrollbar.hscrollimage.fill((100, 100, 100))
            if self.scrollbar.horselect:
                self.scrollbar.horscroll(event.rel[0])
        if self.scrollbar.vscroll:
            if event.buttons[0] == 0:
                self.scrollbar.verselect = False
                self.scrollbar.vscrollimage.fill((100, 100, 100))
            if self.scrollbar.verselect:
                self.scrollbar.verscroll(event.rel[1])

    def scrollselect(self, pos):
        if self.scrollbar.hpos:
            if self.scrollbar.hpos[0] < pos[0] < self.scrollbar.hpos[0]+self.scrollbar.hdim[0] and self.scrollbar.hpos[1] < pos[1] < self.scrollbar.hpos[1]+self.scrollbar.hdim[1]:
                self.scrollbar.horselect = True
                self.scrollbar.hscrollimage.fill((50, 50, 50))
        if self.scrollbar.vpos:
            if self.scrollbar.vpos[0] < pos[0] < self.scrollbar.vpos[0]+self.scrollbar.vdim[0] and self.scrollbar.vpos[1] < pos[1] < self.scrollbar.vpos[1]+self.scrollbar.vdim[1]:
                self.scrollbar.verselect = True
                self.scrollbar.vscrollimage.fill((50, 50, 50))
        
    def scrolldeselect(self):
        if self.scrollbar.hscroll:
            self.scrollbar.horselect = False
            self.scrollbar.hscrollimage.fill((100, 100, 100))
        if self.scrollbar.vscroll:
            self.scrollbar.verselect = False
            self.scrollbar.vscrollimage.fill((100, 100, 100))

    def event_check(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.check_select(pygame.mouse.get_pos())
            self.scrollselect(event.pos)
        elif event.type == MOUSEBUTTONUP:
            self.scrolldeselect()
        elif event.type == KEYDOWN and (event.key == K_RSHIFT or event.key == K_LSHIFT):
            self.upper = True
        elif event.type == KEYUP and (event.key == K_RSHIFT or event.key == K_LSHIFT):
            self.upper = False
        elif event.type == KEYDOWN:
            self.typing(event.key)
        elif event.type == MOUSEMOTION:
            self.check_active(pygame.mouse.get_pos())
            self.check_scroll(event)
        elif event.type == VIDEORESIZE:
            if event.size[0] < (self.width // 2) + 10:
                event.size = (math.ceil(self.width/2) + 10, event.size[1])
            if event.size[1] < (self.height // 2) + 10:
                event.size = (event.size[0], math.ceil(self.height/2) + 10)
            self.resize(event.size)
            return event.size

class Bound_Function:
    def __init__(self, function, *args):
        self.function = function
        self.args = args

def exit():
    pygame.quit()

def change_menu(menu, state):
    menu.changestate(state)
    menu.needtorender = True

def run():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    
    menu = Menu(MenuStates.main, 500, 500, bgcolour=(205, 192, 180))

    menu.addtext(MenuStates.main, "2048", 30, 210, 20)
    menu.addbutton(MenuStates.main, "Start", 22, 200, 100, Bound_Function(run))

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                done = True
            else:
                menu.event_check(event)

        screen.fill((205,192,180))

        menu.render()
        screen.blit(menu.image, (0,0))
        
        pygame.display.update()
    

if __name__ == "__main__":
    run()