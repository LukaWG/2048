__LEFT = "LEFT"
__RIGHT = "RIGHT"
__UP = "UP"
__DOWN = "DOWN"

def __merge(dir, map, __id_map):
    '''
    Merges tiles in a given direction
    '''
    if dir == __LEFT:
        for i in range(len(map)):
            for j in range(len(map[i])-1):
                if map[i][j] == map[i][j+1] and map[i][j] != 0 and map[i][j+1] != 0:
                    map[i][j] = map[i][j]*2
                    map[i][j+1] = 0
                    __id_map[i][j] = (__id_map[i][j], __id_map[i][j+1])
                    __id_map[i][j+1] = (None, None)
        map, __id_map = left(map, __merged=True, __id_map=__id_map)
        return map, __id_map
    elif dir == __RIGHT:
        for i in range(len(map)):
            for j in range(len(map[i])-1, 0, -1):
                if map[i][j] == map[i][j-1]:
                    map[i][j] = map[i][j]*2
                    map[i][j-1] = 0
                    __id_map[i][j] = (__id_map[i][j], __id_map[i][j-1])
                    __id_map[i][j-1] = (None, None)
        map, __id_map = right(map, __merged=True, __id_map=__id_map)
        return map, __id_map
    elif dir == __UP:
        for i in range(len(map)-1):
            for j in range(len(map)):
                if map[i][j] == map[i+1][j]:
                    map[i][j] = map[i+1][j]*2
                    map[i+1][j] = 0
                    __id_map[i][j] = (__id_map[i][j], __id_map[i+1][j])
                    __id_map[i+1][j] = (None, None)
        map, __id_map = up(map, __merged=True, __id_map=__id_map)
        return map, __id_map
    elif dir == __DOWN:
        for i in range(len(map)-1, 0, -1):
            for j in range(len(map)):
                if map[i][j] == map[i-1][j]:
                    map[i][j] = map[i-1][j]*2
                    map[i-1][j] = 0
                    __id_map[i][j] = (__id_map[i][j], __id_map[i-1][j])
                    __id_map[i-1][j] = (None, None)
        map, __id_map = down(map, __merged=True, __id_map=__id_map)

    return map, __id_map

def left(map, __merged=False, __id_map=None):
    """
    Move all the items in the map as far left as they should go.
    Then calls the merge function and will then run again
    """
    if not __merged:
        __id_map = []
        for i in range(4):
            __id_map.append([])
            for j in range(4):
                if map[i][j] != 0:
                    __id_map[i].append((j, i))
                else:
                    __id_map[i].append((None, None))
    change = True
    while change:
        change = False
        for i in range(len(map)):
            for j in range(len(map[i])-1):
                if map[i][j] == 0 and map[i][j+1] != 0:
                    map[i][j], map[i][j+1] = map[i][j+1], map[i][j]
                    __id_map[i][j], __id_map[i][j+1] = __id_map[i][j+1], __id_map[i][j]
                    change = True
    if not __merged:
        map, __id_map = __merge(__LEFT, map, __id_map)
        # print(f"MERGED MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    return map, __id_map

def right(map, __merged=False, __id_map=None):
    """
    Move all the items in the map as far right as they should go.
    Then calls the merge function and will then run again
    """
    if not __merged:
        __id_map = []
        for i in range(4):
            __id_map.append([])
            for j in range(4):
                if map[i][j] != 0:
                    __id_map[i].append((j, i))
                else:
                    __id_map[i].append((None, None))
    change = True
    while change:
        change = False
        for i in range(len(map)):
            for j in range(len(map[i])-1):
                if map[i][j+1] == 0 and map[i][j] != 0:
                    map[i][j], map[i][j+1] = map[i][j+1], map[i][j]
                    __id_map[i][j], __id_map[i][j+1] = __id_map[i][j+1], __id_map[i][j]
                    change = True
    # print(f"FINAL MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    if not __merged:
        map, __id_map = __merge(__RIGHT, map, __id_map)
        # print(f"MERGED MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    return map, __id_map

def up(map, __merged=False, __id_map=None):
    """
    Move all the items in the map as far up as they should go.
    The merge function is then called before this is run again
    """
    if not __merged:
        __id_map = []
        for i in range(4):
            __id_map.append([])
            for j in range(4):
                if map[i][j] != 0:
                    __id_map[i].append((j, i))
                else:
                    __id_map[i].append((None, None))
    change = True
    while change:
        change = False
        for i in range(len(map)-1):
            for j in range(len(map[i])):
                if map[i][j] == 0 and map[i+1][j] != 0:
                    map[i][j], map[i+1][j] = map[i+1][j], map[i][j]
                    __id_map[i][j], __id_map[i+1][j] = __id_map[i+1][j], __id_map[i][j]
                    change = True
    # print(f"FINAL MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    if not __merged:
        map, __id_map = __merge(__UP, map, __id_map)
        # print(f"MERGED MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    return map, __id_map

def down(map, __merged=False, __id_map=None):
    """
    Move all the items in the map as far down as they should go.
    The merge function is then called before this is run again
    """
    if not __merged:
        __id_map = []
        for i in range(4):
            __id_map.append([])
            for j in range(4):
                if map[i][j] != 0:
                    __id_map[i].append((j, i))
                else:
                    __id_map[i].append((None, None))
    change = True
    while change:
        change = False
        for i in range(len(map)-1):
            for j in range(len(map[i])):
                if map[i+1][j] == 0 and map[i][j] != 0:
                    map[i+1][j], map[i][j] = map[i][j], map[i+1][j]
                    __id_map[i][j], __id_map[i+1][j] = __id_map[i+1][j], __id_map[i][j]
                    change = True
    # print(f"FINAL MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    if not __merged:
        map, __id_map = __merge(__DOWN, map, __id_map)
        # print(f"MERGED MAP:\n{map[0]}\n{map[1]}\n{map[2]}\n{map[3]}\n")
    return map, __id_map

def check_merge(map):
    '''Checks if there are any tiles that can be merged
    Returns a boolean value
    '''
    merge = False
    for i in range(len(map)-1):
        for j in range(len(map[i])-1):
            if map[i][j] in [map[i][j+1], map[i+1][j]]:
                merge = True
    return merge