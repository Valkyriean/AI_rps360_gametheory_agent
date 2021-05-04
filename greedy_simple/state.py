from greedy_simple.action import *

import random
import copy
import collections

MAX_THOROWN = 8


class State():
    player = ""
    def __init__(self):
        self.friendly_list = []
        self.enemy_list = []
        self.friendly_thrown = 0
        self.enemy_thrown = 0
        
    
def q_copy(state):
    new_state = State()
    new_state.friendly_thrown = state.friendly_thrown
    new_state.enemy_thrown = state.enemy_thrown
    for friendly in state.friendly_list:
        new_state.friendly_list.append(Token(friendly.symbol, friendly.cord))
    
    for enemy in state.enemy_list:
        new_state.enemy_list.append(Token(enemy.symbol,enemy.cord))
    return new_state

def simple_eval_state(state):
    friendly = (8-state.friendly_thrown)*1.1 + len(state.friendly_list)
    enemy = (8-state.enemy_thrown)*1.1 + len(state.enemy_list)
    return friendly - enemy


# action list to state list


def best_action(state):
    best_score = -9999
    best_action_list = []
    for action in action_list(state, True):
        #print(str(state.score) + " "+str(action.action)+" " + str(action.token.symbol))
        new_state = q_copy(state)
        update_state(action.to_tuple(), new_state, True)
        settle(new_state)
        score = simple_eval_state(new_state)

        if score > best_score:
            best_action_list = [action]
            best_score = score
        elif score == best_score:
            best_action_list.append(action)
    return random.choice(best_action_list)

# action + state to new state
