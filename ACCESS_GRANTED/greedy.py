from ACCESS_GRANTED.evaluation import *
from ACCESS_GRANTED.state import *
from ACCESS_GRANTED.util import *
import random

def greedy(state, upper):
    best_score = -9999
    best_action_list = []
    action_list = get_action_list(state, True, upper)
    for action in action_list:
        new_state = state_copy(state)
        f_token = update_state(new_state, action, True)
        kill, lost = settle(new_state, f_token, None)       
        if not check_duplicated_state(new_state, False):
            continue
        score = simple_eval_state(new_state)

        if score > best_score:
            best_action_list = [action]
            best_score = score
        elif score == best_score:
            best_action_list.append(action)
    if len(best_action_list) == 0:
        return random.choice(action_list)
    return random.choice(best_action_list)