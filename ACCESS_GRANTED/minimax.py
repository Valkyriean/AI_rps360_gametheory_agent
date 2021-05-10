from ACCESS_GRANTED.evaluation import *
from ACCESS_GRANTED.state import *
from ACCESS_GRANTED.util import *
import random

MAX_DEPTH = 4

# Minimax strategy with alpha-beta pruning
def mini_max(state, upper):
    best_score = -9999
    alpha = -9999
    beta = 9999
    best_action_list = []
    best_action = None
    action_list = get_action_list(state, True, upper)
    for action in action_list:
        new_state = state_copy(state)
        f_t = update_state(new_state, action, True)
        settle(new_state, f_t, None)
        score = min_value(new_state, alpha, beta, 1, upper)
        if score > best_score:
            best_action_list = [action]
            best_score = score
        elif score == best_score:
            best_action_list.append(action)
        if best_score > alpha:
            alpha = best_score
    return random.choice(best_action_list)


def max_value(state, alpha, beta, depth, upper):
    if depth >= MAX_DEPTH:
        return complex_eval_state(state)
    max_score = -9999
    action_list = get_action_list(state, True, upper)
    for action in action_list:
        new_state = state_copy(state)
        f_t = update_state(new_state, action, True)
        settle(new_state, f_t, None)
        score = min_value(new_state, alpha, beta, depth+1, upper)
        if score > max_score:
            max_score = score
        if max_score >= beta:
            return max_score
        if max_score > alpha:
            alpha = max_score
    return max_score

def min_value(state, alpha, beta, depth, upper):
    if depth >= MAX_DEPTH:
        return complex_eval_state(state)
    min_score = 9999
    action_list = get_action_list(state, False, upper)
    for action in action_list:
        new_state = state_copy(state)
        e_t = update_state(new_state, action, False)
        settle(new_state, None, e_t)
        score = max_value(new_state, alpha, beta, depth+1, upper)
        if score < min_score:
            min_score = score
        if min_score<= alpha:
            return min_score
        if min_score < beta:
            beta = min_score
    return min_score