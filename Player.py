from math import hypot

# according to the rooles the starting position of player is Y and B for LF and RF
start_pos = {0: [[-1, -1], [-1, -1], [2, 1], [3, 1]],
             1: [[-1, -1], [-1, -1], [2, 6], [3, 6]]}


class Player:

    def __init__(self, name, numb):
        self.name = name
        self.pos = start_pos.get(numb)  # LH, RH, LF, RF

    # change position
    def move(self, coords, limb):
        self.pos[limb] = coords

    # check if position is occupied by this player
    def occupied_pos(self, coords):
        for i in self.pos:
            if i == coords:
                return True
        return False

    def dist_between(self, point, limb):
        max_d = 0
        for i in self.pos:
            if i == [-1, -1]:
                continue
            if self.pos.index(i) == limb:
                continue
            dist = hypot(point[0] - i[0], point[1] - i[1])
            if dist > max_d:
                max_d = dist
        return round(max_d)
