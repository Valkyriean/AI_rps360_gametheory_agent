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
    alpha = -9999
    beta = 9999
    best_action_list = []
    for action in action_list(state,True):
        new_state = copy.deepcopy(state)
        update_state(action.to_tuple(), new_state, True)
        settle(new_state)
        score = min_value(state, alpha, beta, 1)
        if score > best_score:
            best_action_list = [action]
            best_score = score
        elif score == best_score:
            best_action_list.append(action)
        if best_score >= beta:
            return best_score
        if best_score > alpha:
            alpha = best_score


    return random.choice(best_action_list)

# action + state to new state





def minimax(isMaxTurn,state, depth):
    if depth >= MAX_DEPTH:          
        return simple_eval_state(state)

    scores = []
    for action in action_list(state):
        new_state = copy.deepcopy(state)
        update_state(action.to_tuple(), new_state, isMaxTurn)
        settle(new_state)
        scores.append(minimax(not isMaxTurn, new_state, depth+1))
    return max(scores) if isMaxTurn else min(scores)


def random_throw(state):
    return random.choice(throw_list(state))

def max_value(state, alpha, beta, depth):
    if depth >= MAX_DEPTH:
        return simple_eval_state(state)
    max_score = -9999
    bese_action = None
    for action in action_list(state, False):
        new_state = copy.deepcopy(state)
        update_state(action.to_tuple(), new_state, True)
        settle(new_state)
        score = min_value(new_state, alpha, beta, depth+1)

        if score > max_score:
            max_score = score

        if max_score >= beta:
            return max_score
        if max_score > alpha:
            alpha = max_score
    return max_score

def min_value(state, alpha, beta, depth):
    if depth >= MAX_DEPTH:
        return simple_eval_state(state)
    min_score = 9999
    for action in action_list(state,False):
        new_state = copy.deepcopy(state)
        update_state(action.to_tuple(), new_state, False)
        settle(new_state)
        score = max_value(new_state, alpha, beta, depth+1)

        if score < min_score:
            min_score = score
        
        if min_score<= alpha:
            return min_score
        if min_score < beta:
            beta = min_score
    return min_score