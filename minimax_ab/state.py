from minimax_ab.action import *
import random
import copy

MAX_THOROWN = 8
MAX_DEPTH = 2

class State():
    player = None
    def __init__(self):
        self.friendly_list = []
        self.enemy_list = []
        self.friendly_thrown = 0
        self.enemy_thrown = 0
        self.score = -9999
    
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
    friendly = (8-state.friendly_thrown) + len(state.friendly_list)
    enemy = (8-state.enemy_thrown) + len(state.enemy_list)
    return friendly - enemy

def dist_to_enemy(token, enemy_list):
    min_dist = 999
    for enemy in enemy_list:
        if can_defeat(token, enemy) == 1:
            dist = dist_to(token,enemy)
            if dist < min_dist:
                min_dist = dist
    return min_dist

def complex_eval_state(state):
    friendly = (8-state.friendly_thrown)*1.05 + len(state.friendly_list)
    enemy = (8-state.enemy_thrown)*1.05 + len(state.enemy_list)
    base = (friendly - enemy)*100
    for friendly in state.friendly_list:
        dist = dist_to_enemy(friendly, state.enemy_list)
        if dist != 999 and 8-dist > 0:
            base += (8 - dist)
    return base



def best_action(state):
    best_score = -9999
    alpha = -9999
    beta = 9999
    best_action_list = []
    best_action = None
    for action in action_list(state,True):
        new_state = q_copy(state)
        update_state(action.to_tuple(), new_state, True)
        settle(new_state)
        score = min_value(state, alpha, beta, 1)
        if score > best_score:
            best_action = action
            best_score = score
        # elif score == best_score:
        #     best_action_list.append(action)
        if best_score >= beta:
            return best_score
        if best_score > alpha:
            alpha = best_score


    return best_action

# action + state to new state





# def minimax(isMaxTurn,state, depth):
#     if depth >= MAX_DEPTH:          
#         return simple_eval_state(state)

#     scores = []
#     for action in action_list(state):
#         new_state = copy.deepcopy(state)
#         update_state(action.to_tuple(), new_state, isMaxTurn)
#         settle(new_state)
#         scores.append(minimax(not isMaxTurn, new_state, depth+1))
#     return max(scores) if isMaxTurn else min(scores)


def random_throw(state):
    return random.choice(throw_list(state))

def max_value(state, alpha, beta, depth):
    if depth >= MAX_DEPTH:
        return simple_eval_state(state)
    max_score = -9999
    bese_action = None
    for action in action_list(state, False):
        new_state = q_copy(state)
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
        new_state = q_copy(state)
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