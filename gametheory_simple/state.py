from gametheory_simple.action import *
from gametheory import *
import random
import copy

MAX_THOROWN = 8
MAX_DEPTH = 8

class State():
    player = None
    def __init__(self):
        self.friendly_list = []
        self.enemy_list = []
        self.friendly_thrown = 0
        self.enemy_thrown = 0
        self.score = -9999


def simple_eval_state(state):
    friendly = (8-state.friendly_thrown)*1.1 + len(state.friendly_list)
    enemy = (8-state.enemy_thrown)*1.1 + len(state.enemy_list)
    return friendly - enemy


def random_throw(state):
    return random.choice(throw_list(state))



def game_theory_simple(state):
    matrix = []
    friendly_action_list = action_list(state, True)
    for friendly_action in friendly_action_list:
        row = []
        new_state1 = copy.deepcopy(state)
        update_state(friendly_action.to_tuple(), new_state1, True)
        for enemy_action in action_list(state, False):
            new_state2 = copy.deepcopy(new_state1)
            update_state(enemy_action.to_tuple(), new_state2, False)
            settle(new_state2)
            row.append(simple_eval_state(new_state2))
        matrix.append(row)
    s,v = solve_game(matrix)
    best_score = -9999
    best_action_list = []
    i = 0
    for score in s:
        if score > best_score:
            best_action_list = [friendly_action_list[i]]
            best_score = score
        elif score == best_score:
            best_action_list.append(friendly_action_list[i])
        i+=1
    return random.choice(best_action_list)