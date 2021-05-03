from greedy_complex.token import *

# score state
# calculate hexagonal Manhattan Distance
def dist_to(friednly, enemy):
    (r_o, q_o) = friednly.cord
    (r_e, q_e) = enemy.cord
    return max(abs(r_e - r_o), abs(q_e - q_o), abs(q_o - q_e + r_o - r_e))


def dist_to_enemy(token, enemy_list):
    min_dist = 999
    for enemy in enemy_list:
        if can_defeat(token, enemy) == 1:
            dist = dist_to(token,enemy)
            if dist < min_dist:
                min_dist = dist
    return min_dist

def defeat_score(token, enemy_list, win):
    for enemy in enemy_list:
        if can_defeat(token, enemy) == win:
            return 1
    return 0

def only_counter(token, state):
    count = 0
    the_enemy = None
    for enemy in state.enemy_list:
        if can_defeat(token, enemy) == 1:
            the_enemy = enemy
    if the_enemy == None:
        return 0
    for friendly in state.friendly_list:
        if can_defeat(friendly, the_enemy) == 1:
            count += 1
    if count == 1:
        return 1
    else:
        return 0

def eval_state(state):
    score = 0
    if state.enemy_thrown>state.friendly_thrown:
        score -= 10
    for friendly in state.friendly_list:
        hasEnemy = defeat_score(friendly, state.enemy_list, -1)
        if hasEnemy == 1 and dist_to_enemy(friendly, state.enemy_list, -1) < 2:
            score -= 50
        hasPrey = defeat_score(friendly, state.enemy_list, 1)
        if hasPrey ==1:
            score += 10 + 10*only_counter(friendly, state) - dist_to_enemy(friendly, state.enemy_list, 1)
    return score


def simple_eval_state(state):
    friendly = (8-state.friendly_thrown)*1.08 + len(state.friendly_list)
    enemy = (8-state.enemy_thrown)*1.08 + len(state.enemy_list)
    base = (friendly - enemy)*100
    for friendly in state.friendly_list:
        dist = dist_to_enemy(friendly, state.enemy_list)
        if dist != 999:
            base += (8 - dist)
    return base
