"""
New version to try and incorporate the tiles moving to their new position
DOES NOT WORK
"""

from copy import deepcopy


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
                if map[i][j][0] == map[i][j+1][0] and map[i][j][0] != 0 and map[i][j+1][0] != 0:
                    map[i][j][0] = map[i][j][0]*2
                    map[i][j+1] = (0, (None, None))
        map = left(map, __merged=True)
    elif dir == __RIGHT:
        for i in range(len(map)):
            for j in range(len(map[i])-1, 0, -1):
                if map[i][j] == map[i][j-1]:
                    map[i][j] = map[i][j]*2
                    map[i][j-1] = 0
        map = right(map, __merged=True)
    elif dir == __UP:
        for i in range(len(map)-1):
            for j in range(len(map)):
                if map[i][j] == map[i+1][j]:
                    map[i][j] = map[i+1][j]*2
                    map[i+1][j] = 0
        map = up(map, __merged=True)
    elif dir == __DOWN:
        for i in range(len(map)-1, 0, -1):
            for j in range(len(map)):
                if map[i][j] == map[i-1][j]:
                    map[i][j] = map[i-1][j]*2
                    map[i-1][j] = 0
        map = down(map, __merged=True)

    return map

def left(map, __merged=False):
    """
    Move all the items in the map as far left as they should go. 
    Then calls the merge function and will then run again
    """
    if not __merged:
        for i in range(len(map)):
            for j in range(len(map)):
                if map[i][j] != 0:
                    map[i][j] = [map[i][j], (j, i)]
                else:
                    map[i][j] = [map[i][j], (None, None)]
    change = True
    while change:
        change = False
        for i in range(len(map)):
            for j in range(len(map[i])-1):
                if map[i][j][0] == 0 and map[i][j+1][0] != 0:
                    map[i][j], map[i][j+1] = map[i][j+1], map[i][j]
                    change = True
    if not __merged:
        map = merge(__LEFT, map)
        # print(f"MERGED MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    if __merged:
        move_map = deepcopy(map)
        for i in range(len(move_map)):
            for j in range(len(move_map[i])):
                map[i][j] = move_map[i][j][0]
        return map, move_map
    else:
        return map
    
def right(map, __merged=False):
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
    if not __merged:
        map = merge(__RIGHT, map)
        # print(f"MERGED MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    return map

def up(map, __merged=False):
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
    if not __merged:
        map = merge(__UP, map)
        # print(f"MERGED MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    return map

def down(map, __merged=False):
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
    if not __merged:
        map = merge(__DOWN, map)
        # print(f"MERGED MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    return map