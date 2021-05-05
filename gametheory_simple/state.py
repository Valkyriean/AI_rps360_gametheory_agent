from gametheory_simple.action import *
from gametheory import *
import random
import copy
import time
import collections
MAX_THOROWN = 8
MAX_DEPTH = 8

class State():
    player = None
    def __init__(self):
        self.friendly_list = []
        self.enemy_list = []
        self.friendly_thrown = 0
        self.enemy_thrown = 0


global copy_time
copy_time = 0
      
def print_copy_time():
    print("copy time is :" + str(copy_time))

def q_copy(state):
    start = time.process_time()
    new_state = State()
    new_state.friendly_thrown = state.friendly_thrown
    new_state.enemy_thrown = state.enemy_thrown
    for friendly in state.friendly_list:
        new_state.friendly_list.append(Token(friendly.symbol, friendly.cord))
    
    for enemy in state.enemy_list:
        new_state.enemy_list.append(Token(enemy.symbol,enemy.cord))
    global copy_time 
    copy_time += (time.process_time() - start)
    return new_state


def dist_to_enemy(token, enemy_list):
    min_dist = 999
    for enemy in enemy_list:
        if can_defeat(token, enemy) == 1:
            dist = dist_to(token,enemy)
            if dist < min_dist:
                min_dist = dist
    return min_dist


def simple_eval_state(state):
    friendly = (8-state.friendly_thrown)*1.08 + len(state.friendly_list)
    enemy = (8-state.enemy_thrown)*1.08 + len(state.enemy_list)
    base = (friendly - enemy)*100
    # for friendly in state.friendly_list:
    #     dist = dist_to_enemy(friendly, state.enemy_list)
    #     if dist != 999:
    #         base += (8 - dist)
    return base


def random_throw(state):
    thrown_count = state.friendly_thrown
    throw_list = []
    symbols = ['s','r','p']
    p = -1
    if state.player == "upper":
        p = 1
    r = (4-thrown_count)*p

    pos = 1 if r>0 else -1
    q = random.choice(range(-1*pos*4, pos*4-r+pos, pos))
    return ("THROW", symbols[thrown_count%3], (r,q))




def game_theory_simple(state):
    # global timer
    # start = time.process_time()
    matrix = []
    # time_taken = 0
    friendly_action_list = action_list(state, True)
    enemy_action_list = action_list(state, False)
    if len(friendly_action_list) is 0 or len(enemy_action_list) is 0:
        return
    duplicate = []
    for friendly_action in friendly_action_list:
        row = []
        # start = time.process_time()
        # new_state1 = q_copy(state)
        # timer.copy += time.process_time() - start
        # start = time.process_time()
        # update_state(friendly_action.to_tuple(), new_state2, True)
        # if not check_duplicated_state(new_state2):
        #     continue
        # timer.settle += time.process_time() - start
        for enemy_action in enemy_action_list:
            # start1 = time.process_time()
            new_state2 = q_copy(state)
            # timer.copy += time.process_time() - start1
            sim_update_state(friendly_action.to_tuple(), enemy_action.to_tuple(), new_state2, False)
            if not check_duplicated_state(new_state2, False):
                row = []
                duplicate.append(friendly_action)
                break
            # start = time.process_time()
            # settle(new_state2)
            # timer.settle += time.process_time() - start

            # fal2 = action_list(new_state2,True)
            # eal2 = action_list(new_state2, False)
            
            # m2 = []
            # for fa in fal2:
            #     new_state3 = q_copy(new_state2)
            #     update_state(fa.to_tuple(), new_state3, True)
            #     r2 = []
            #     for ea in eal2:
            #         new_state4 = q_copy(new_state3)
            #         update_state(ea.to_tuple(), new_state4, False)
            #         settle(new_state4)
            #         r2.append(simple_eval_state(new_state4))
            #     m2.append(r2)
            # s1, v1 = solve_game(m2)
            row.append(simple_eval_state(new_state2))
        if len(row) != 0:
            matrix.append(row)
    s,v = solve_game(matrix)
    
    best_score = -9999
    best_action_list = []
    i = 0
    # if len(duplicate) != 0:
        # print(duplicate[0])
    for score in s:
        if friendly_action_list[i] not in duplicate:
            if score > best_score :
                best_action_list = [friendly_action_list[i]]
                # print(friendly_action_list[i])
                best_score = score
            elif score == best_score :
                best_action_list.append(friendly_action_list[i])
                # print(friendly_action_list[i])
        i+=1
    
    if len(best_action_list) == 0:
        random.choice(friendly_action_list)
    # print(time_taken)
    # timer.action += time.process_time() - start
    # timer.prt()
    return random.choice(best_action_list)


def greedy(state):
    best_score = -9999
    best_action_list = []
    for action in action_list(state, True):
        new_state = q_copy(state)
        update_state(action.to_tuple(), new_state, True)
        settle(new_state)
        if not check_duplicated_state(new_state, False):
            continue
        score = simple_eval_state(new_state)

        if score > best_score:
            best_action_list = [action]
            best_score = score
        elif score == best_score:
            best_action_list.append(action)
    if len(best_action_list) == 0:
        random.choice(acton_list)
    return random.choice(best_action_list)