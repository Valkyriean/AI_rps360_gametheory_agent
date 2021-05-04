from greedy_simple.token import *
import collections
global history
history = collections.Counter()
def update_state(action_tuple, state, friendly):
    global history
    action = action_tuple[0]
    if (action == "THROW"):
        symbol  = action_tuple[1]
        cord = action_tuple[2]
        if friendly:
            token = Token(symbol,cord)
            state.friendly_list.append(token)
            state.friendly_thrown += 1
            history.clear()
        else:
            enemy = Token(symbol,cord)
            state.enemy_list.append(enemy)
            state.enemy_thrown += 1
            history.clear()
    else:
        cord = action_tuple[1]
        if friendly:
            token_list = state.friendly_list
        else:
            token_list = state.enemy_list
        for token in token_list:
            if(token.cord == cord):
                token.cord = action_tuple[2]
                break



def throw_list(state):
    if state.friendly_thrown > 8:
        return []
    thrown_count = state.friendly_thrown
    throw_list = []
    symbols = ['s','r','p']
    p = -1
    if state.player == "upper":
        p = 1
    for r in range(4*p, (4-thrown_count)*p - p, -1*p):
        pos = 1 if r>0 else -1
        for q in range(-1*pos*4, pos*4-r+pos, pos):
            for s in symbols:
                throw_list.append(Throw(Token(s,(r,q))))
    return throw_list

def enemy_throw_list(state):
    if state.enemy_thrown > 8:
        return []
    thrown_count = state.enemy_thrown
    throw_list = []
    symbols = ['s','r','p']
    p = -1
    if state.player == "lower":
        p = 1
    for r in range(4*p, (4-thrown_count)*p - p, -1*p):
        pos = 1 if r>0 else -1
        for q in range(-1*pos*4, pos*4-r+pos, pos):
            for s in symbols:
                throw_list.append(Throw(Token(s,(r,q))))
    return throw_list


def slide_list(state):
    slide_list = []
    for friednly in state.friendly_list:
        potential_slide_list = potential_slide(friednly.cord)
        for potential_slide_move in potential_slide_list:
            slide_list.append(Slide(friednly, potential_slide_move))
    return slide_list

def enemy_slide_list(state):
    slide_list = []
    for enemy in state.enemy_list:
        for potential_slide_move in potential_slide(enemy.cord):
            slide_list.append(Slide(enemy, potential_slide_move))
    return slide_list


def swing_list(state):
    swing_list = []
    for friednly in state.friendly_list:
        potential_swing_list = potential_swing(friednly.cord, state.friendly_list)
        for potential_swing_move in potential_swing_list:
            swing_list.append(Swing(friednly, potential_swing_move))
    return swing_list

def enemy_swing_list(state):
    swing_list = []
    for enemy in state.enemy_list:
        for potential_swing_move in potential_swing(enemy.cord, state.enemy_list):
            swing_list.append(Swing(enemy, potential_swing_move))
    return swing_list

def action_list(state, isFriendlyTurn):
    action_list = []
    if isFriendlyTurn:
        action_list += swing_list(state)
        action_list += slide_list(state)
        action_list += throw_list(state)

    else:
        action_list += enemy_swing_list(state)
        action_list += enemy_slide_list(state)
        action_list += enemy_throw_list(state)
    return action_list

# def remove_friendly_fire(state,action_list):
#     action_list_copy = action_list.copy()
#     for action in action_list_copy:
#         for friendly in state.friendly_list:
#             if action.token != friendly and action.tar == friendly.cord and can_defeat(action.token,friendly) != 0:
#                 action_list.remove(action)
def check_duplicated_state(state):
    global history
    temp = []
    for i in state.friendly_list:
        temp.append((i.cord, i.symbol))
    temp.append(state.friendly_thrown)
    history[tuple(temp)] += 1
    if history[tuple(temp)] >= 3:
        return False
    return True

class Action:
    def __init__(self, token, tar):
        self.tar = tar
        self.token = token


class Throw(Action):
    action = "THROW"

    def __init__(self, token):
        super().__init__(token, token.cord)
        
    def to_tuple(self):
        return (self.action, self.token.symbol, self.tar)


class Swing(Action):
    action = "SWING"

    def __init__(self, token, tar):
        super().__init__(token, tar)
    
    def to_tuple(self):
        return (self.action, self.token.cord, self.tar)

class Slide(Action):
    action = "SLIDE"
    
    def __init__(self, token, tar):
        super().__init__(token, tar)

    def to_tuple(self):
        return (self.action, self.token.cord, self.tar)
        

