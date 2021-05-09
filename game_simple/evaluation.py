from game_simple.util import *

def simple_eval_state(state):
    friendly = (8-state[2])*1.08 + len(state[0])
    enemy = (8-state[3])*1.08 + len(state[1])
    base = (friendly - enemy)*100 + 1000
    return base


def dist_to(friednly, enemy):
    (r_o, q_o) = friednly
    (r_e, q_e) = enemy
    return max(abs(r_e - r_o), abs(q_e - q_o), abs(q_o - q_e + r_o - r_e))


def dist_to_friendly(token, friendly_list):
    min_dist = 999
    for friendly in friendly_list:
        if can_defeat(token[0], friendly[0]) == -1:
            dist = dist_to(token[1],friendly[1])
            if dist < min_dist:
                min_dist = dist
    return min_dist

def complex_eval_state(state):
    throw_adv = (8-state[2]) - (8-state[3])
    field_adv = len(state[0]) - len(state[1])
    # friendly = (8-state[2])*1.01 + len(state[0])
    # enemy = (8-state[3])*1.01 + len(state[1])
    base = (throw_adv*1.01 + field_adv) * 100
    for enemy in state[1]:
        dist = dist_to_friendly(enemy, state[0])
        if dist != 999 and (10 - dist) > 0:
            base += (10 - dist)
    for friendly in state[0]:
        dist = dist_to_friendly(friendly, state[0])
        if dist != 999 and (10 - dist) > 0:
            base += (10 - dist)*0.1
    return base