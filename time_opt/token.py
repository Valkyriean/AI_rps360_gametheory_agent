class Token:
    def __init__(self, symbol, cord):
        self.symbol = symbol
        self.cord = cord





move_vector_list = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0)]
symbols = ['r','p','s']


# check whether can eliminate enemy token
def can_defeat(our, tar):
    if (our == "p" and tar == "r") or (our == 'r' and tar == 's') or (our == 's' and tar == 'p'):
        return 1
    elif our == tar:
        return 0
    else:
        return -1


# put all the possible move in a list
def potential_slide(cord):
    surrounding_list = []
    for move_vector in move_vector_list:
        tar = (cord[0] + move_vector[0], cord[1] + move_vector[1])
        surrounding_list.append(tar)
    surrounding_list = remove_out_bound(surrounding_list)
    return surrounding_list


# put possible swing coordinates in the list
def potential_swing(cord, friendly_list):
    surrounding_list = potential_slide(cord)
    swing_list = []
    for friendly in friendly_list:
        if friendly.cord in surrounding_list:
            swing_list += potential_slide(friendly.cord)
    swing_list = remove_out_bound(swing_list)
    # remove repetition
    swing_list = list(set(swing_list))
    if cord in swing_list:
        swing_list.remove(cord)
    for surrounding in surrounding_list:
        if surrounding in swing_list:
            swing_list.remove(surrounding)
    return swing_list



# check the movement is in the boundary
def remove_out_bound(potential_move_list):
    for cord in potential_move_list.copy():
        if abs(cord[0]) > 4 or abs(cord[1]) > 4 or abs(cord[0] + cord[1]) > 4:
            potential_move_list.remove(cord)
    return potential_move_list


def settle(state):
    token_list = state.friendly_list.copy() + state.enemy_list.copy()
    for token1 in token_list:
        for token2 in token_list:
            if token1.cord == token2.cord and can_defeat(token1,token2) == 1:
                if token2 in state.enemy_list:
                    state.enemy_list.remove(token2)
                elif token2 in state.friendly_list:
                    state.friendly_list.remove(token2)

# calculate hexagonal Manhattan Distance
def dist_to(friednly, enemy):
    (r_o, q_o) = friednly.cord
    (r_e, q_e) = enemy.cord
    return max(abs(r_e - r_o), abs(q_e - q_o), abs(q_o - q_e + r_o - r_e))

