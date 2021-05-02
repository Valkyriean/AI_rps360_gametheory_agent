from ACCESS_GRANTED.action import *
import random
import copy

MAX_THOROWN = 8
MAX_DEPTH = 3

class State():
    player = None
    def __init__(self):
        self.friendly_list = []
        self.enemy_list = []
        self.friendly_thrown = 0
        self.enemy_thrown = 0
        self.score = -9999
    

# action list to state list
def actions_to_states(state, action_list):
    state_list = []
    for action in action_list:
        new_state = copy.deepcopy(state)
        update_state(action.to_tuple(), new_state, True)
        settle(new_state)
        new_state.score = simple_eval_state(new_state)
        state_list.append((new_state,action))
    return state_list

def simple_eval_state(state):
    friendly = (8-state.friendly_thrown)*1.1 + len(state.friendly_list)
    enemy = (8-state.enemy_thrown)*1.1 + len(state.enemy_list)
    return friendly - enemy


def best_action(state):
    best_score = -9999
    best_action_list = []
    for action in action_list(state):
        new_state = copy.deepcopy(state)
        update_state(action.to_tuple(), new_state, True)
        settle(new_state)
        # score = minimax(False, new_state, 1)
        score = simple_eval_state(new_state)
        if score > best_score:
            best_action_list = [action]
            best_score = score
        elif score == best_score:
            best_action_list.append(action)
    return random.choice(best_action_list)

# action + state to new state





# def minimax(isMaxTurn,state, depth):
#     if depth >= MAX_DEPTH:          
#         return simple_eval_state(state)

#     scores = []
#     for action in action_list(state):
#         new_state = copy.deepcopy(state)
#         update_state(action.to_tuple(), new_state, isMaxTurn)

#     return max(scores) if isMaxTurn else min(scores)