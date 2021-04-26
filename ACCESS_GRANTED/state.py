from ACCESS_GRANTED.action import *
from ACCESS_GRANTED.evaluation import *
import random
import copy

MAX_THOROWN = 8


class State():
    def __init__(self):
        self.friendly_list = []
        self.enemy_list = []
        self.friendly_thrown = 0
        self.enemy_thrown = 0
        self.friendly_score = 0
    
    def copy(self):
        new_state = State()
        new_state.friendly_list = copy.deepcopy(self.friendly_list)
        new_state.enemy_list = copy.deepcopy(self.enemy_list)
        new_state.friendly_thrown = self.friendly_thrown
        new_state.enemy_thrown = self.enemy_thrown
        new_state.friendly_score = self.friendly_score
        return new_state
# action list to state list
def actions_to_states(state, action_list):
    state_list = []
    for action in action_list:
        new_state = copy.deepcopy(state)
        update_state(action.to_tuple(), new_state, True)
        eval_state(new_state)
        state_list.append((new_state,action))
    return state_list


def best_action(state_list):
    best_score = -9999
    best_action_list = []
    for (state,action) in state_list:
        #print(str(state.score) + " "+str(action.action)+" " + str(action.token.symbol))
        if state.score > best_score:
            best_action_list = [action]
            best_score = state.score
        elif state.score == best_score:
            best_action_list.append(action)
    return random.choice(best_action_list)

# action + state to new state


