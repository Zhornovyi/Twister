import random

limbs_str = {0: "Left hand", 1: "Right hand ", 2: "Left foot", 3: "Right foot"}
color_str = {0: 'red', 1: 'blue', 2: 'yellow', 3: 'green'}


class Game():
    def __init__(self, players, mode):
        self.players = players
        self.field = [[0] * 6] * 4
        self.mode = mode

    def point_priority(self, coords, player):
        result = 0
        # if position is occupied, it`s priority equal 0
        for i in self.players:
            if i.occupied_pos(coords) == True:
                return 0
        #  перевіряє яка довжина між занятими точками гравця
        len_to_point = 0
        for i in self.players:
            for j in range(4):
                dist = i.dist_between(coords, j)
                if dist > len_to_point:
                    len_to_point = dist
        result += len_to_point
        # TODO: check if you cross rival's lines
        # TODO : check if you turn over
        return result

    # можна оптимізувати додаючи менше варіантів до можливих ходів
    def get_move(self, player_inx):
        possible_choices = []  # [limb, color, priority]
        for l in range(4):  # limbs
            for c in range(4):  # colors
                min_p = 0  # priorities
                for p in range(6):  # position in raw
                    val = self.point_priority([c, p], player_inx)
                    if val > min_p & val > 0:
                        min_p = val
                    possible_choices.append([l, c, min_p])

        possible_choices = sorted(possible_choices, key=lambda x: x[2])
        for el in possible_choices:
            if el[2] > possible_choices[0][2]:
                possible_choices.remove(el)

        # returns random move with minimum priority
        return possible_choices[random.randint(0, len(possible_choices))]

    def get_move_str(self, player_inx):
        move = self.get_move(player_inx)
        return limbs_str[move[0]] + ' on ' + color_str[move[1]]
