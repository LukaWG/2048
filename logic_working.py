"""
Working logic file, however the tiles do not "move" they "jump" to their new location
"""

__LEFT = "LEFT"
__RIGHT = "RIGHT"
__UP = "UP"
__DOWN = "DOWN"

def merge(dir, map):
    '''
    Merges tiles in a given direction
    '''
    if dir == __LEFT:
        for i in range(len(map)):
            for j in range(len(map[i])-1):
                if map[i][j] == map[i][j+1]:
                    map[i][j] = map[i][j]*2
                    map[i][j+1] = 0
        map = left(map, merged=True)
    elif dir == __RIGHT:
        for i in range(len(map)):
            for j in range(len(map[i])-1, 0, -1):
                if map[i][j] == map[i][j-1]:
                    map[i][j] = map[i][j]*2
                    map[i][j-1] = 0
        map = right(map, merged=True)
    elif dir == __UP:
        for i in range(len(map)-1):
            for j in range(len(map)):
                if map[i][j] == map[i+1][j]:
                    map[i][j] = map[i+1][j]*2
                    map[i+1][j] = 0
        map = up(map, merged=True)
    elif dir == __DOWN:
        for i in range(len(map)-1, 0, -1):
            for j in range(len(map)):
                if map[i][j] == map[i-1][j]:
                    map[i][j] = map[i-1][j]*2
                    map[i-1][j] = 0
        map = down(map, merged=True)

    return map

def left(map, merged=False):
    """
    Move all the items in the map as far left as they should go. 
    Then calls the merge function and will then run again
    """
    change = True
    while change:
        change = False
        for i in range(len(map)):
            for j in range(len(map[i])-1):
                if map[i][j] == 0 and map[i][j+1] != 0:
                    map[i][j] = map[i][j+1]
                    map[i][j+1] = 0
                    change = True
    # print(f"FINAL MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    if not merged:
        map = merge(__LEFT, map)
        # print(f"MERGED MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    return map
    
def right(map, merged=False):
    """
    Move all the items in the map as far right as they should go. 
    Then calls the merge function and will then run again
    """
    change = True
    while change:
        change = False
        for i in range(len(map)):
            for j in range(len(map[i])-1):
                if map[i][j+1] == 0 and map[i][j] != 0:
                    map[i][j+1] = map[i][j]
                    map[i][j] = 0
                    change = True
    # print(f"FINAL MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    if not merged:
        map = merge(__RIGHT, map)
        # print(f"MERGED MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    return map

def up(map, merged=False):
    """
    Move all the items in the map as far up as they should go.
    The merge function is then called before this is run again
    """
    change = True
    while change:
        change = False
        for i in range(len(map)-1):
            for j in range(len(map[i])):
                if map[i][j] == 0 and map[i+1][j] != 0:
                    map[i][j] = map[i+1][j]
                    map[i+1][j] = 0
                    change = True
    # print(f"FINAL MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    if not merged:
        map = merge(__UP, map)
        # print(f"MERGED MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    return map

def down(map, merged=False):
    """
    Move all the items in the map as far down as they should go.
    The merge function is then called before this is run again
    """
    change = True
    while change:
        change = False
        for i in range(len(map)-1):
            for j in range(len(map[i])):
                if map[i+1][j] == 0 and map[i][j] != 0:
                    map[i+1][j] = map[i][j]
                    map[i][j] = 0
                    change = True
    # print(f"FINAL MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    if not merged:
        map = merge(__DOWN, map)
        # print(f"MERGED MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    return map