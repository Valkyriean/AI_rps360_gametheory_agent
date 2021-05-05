from gametheory_simple.token import *
import collections
import time

global history
history = collections.Counter()

global update_time
update_time = 0

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
        

def print_update_time():
    global update_time
    print("Action time is: " + str(update_time))

def print_list_time():
    global list_time
    print("Listing time is: " + str(list_time))


def sim_update_state(f_action_tuple, e_action_tuple, state):
    global update_time
    start = time.process_time()

    fa = f_action_tuple[0]
    ea = e_action_tuple[0]

    global history

    if fa == "THROW":
        symbol  = f_action_tuple[1]
        cord = f_action_tuple[2]
        ft = Token(symbol,cord)
        state.friendly_list.append(ft)
        state.friendly_thrown += 1
        history.clear()
    else:
        cord = f_action_tuple[1]
        for token in state.friendly_list:
            if token.cord == cord:
                ft = token
                ft.cord = f_action_tuple[2]
                break
    
    if ea == "THROW":
        symbol  = e_action_tuple[1]
        cord = e_action_tuple[2]
        et = Token(symbol,cord)
        state.enemy_list.append(et)
        state.enemy_thrown += 1
        history.clear()
    else:
        cord = e_action_tuple[1]
        for token in state.enemy_list:
            if token.cord == cord:
                et = token
                et.cord = e_action_tuple[2]
                break

    token_list = state.friendly_list + state.enemy_list
    for token in token_list:
        if ft.cord == token.cord:
            deft = can_defeat(ft,token)
            if deft is 1:                
                if token in state.enemy_list:
                    state.enemy_list.remove(token)
                elif token in state.friendly_list:
                    state.friendly_list.remove(token)
            elif deft is -1:
                if ft in state.friendly_list:
                    state.friendly_list.remove(ft)
        
        if et.cord == token.cord:
            deft = can_defeat(et,token)
            if deft is 1:                
                if token in state.enemy_list:
                    state.enemy_list.remove(token)
                elif token in state.friendly_list:
                    state.friendly_list.remove(token)
            elif deft is -1:
                if et in state.enemy_list:
                    state.enemy_list.remove(et)
    update_time += (time.process_time() - start)



def update_state(action_tuple, state, friendly):
    action = action_tuple[0]
    global history
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

global list_time
list_time = 0

def action_list(state, isFriendlyTurn):
    global list_time
    start = time.process_time()

    action_list = []
    if isFriendlyTurn:
        action_list += swing_list(state)
        action_list += slide_list(state)
        action_list += throw_list(state)

    else:
        action_list += enemy_swing_list(state)
        action_list += enemy_slide_list(state)
        action_list += enemy_throw_list(state)
    list_time += (time.process_time() - start)
    return action_list

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


