from gametheory_simple_throw.action import *
from gametheory import *
import random
import copy
import time
import collections
MAX_THOROWN = 8
MAX_DEPTH = 8

global settle_t
settle_t = 0

def settle(state, f_token, e_token):
    start = time.process_time()
    f_list = state[0].copy()
    if e_token != None:
        e_list = state[1].copy()
    lost = 0
    kill = 0

    for player_token in f_list:
        if f_token[1] == player_token[1]:
            defeat = can_defeat(f_token[0], player_token[0])
            if defeat is 1 and player_token in state[0]:
                state[0].remove(player_token)
                lost += 1
            elif defeat is -1 and f_token in state[0]:
                state[0].remove(f_token)
                lost += 1                
        if e_token != None and e_token[1] == player_token[1]:
            defeat = can_defeat(e_token[0], player_token[0])
            if defeat is 1 and player_token in state[0]:
                state[0].remove(player_token)
                lost += 1
            elif defeat is -1 and e_token in state[1]:
                state[1].remove(e_token)
                kill += 1       

    for opponent_token in e_list:
        if f_token[1] == opponent_token[1]:
            defeat = can_defeat(f_token[0], opponent_token[0])
            if defeat is 1 and opponent_token in state[1]:
                state[1].remove(opponent_token)
                kill += 1
            elif defeat is -1 and f_token in state[0]:
                state[0].remove(f_token)
                lost += 1                
        if e_token != None and  e_token[1] == opponent_token[1]:
            defeat = can_defeat(e_token[0], opponent_token[0])
            if defeat is 1 and opponent_token in state[1]:
                state[1].remove(opponent_token)
                kill += 1
            elif defeat is -1 and e_token in state[1]:
                state[1].remove(e_token)
                kill += 1   

    global settle_t 
    settle_t += (time.process_time() - start)
    return kill, lost

def print_settle_time():
    global settle_t
    print("Settle time is: " + str(settle_t))





global copy_time
copy_time = 0
      
def print_copy_time():
    print("copy time is :" + str(copy_time))


def state_copy(state):
    start = time.process_time()
    enemy_list = state[0].copy()
    friendly_list = state[1].copy()
    friendly_thrown = state[2]
    enemy_thrown = state[3]
    global copy_time
    copy_time += (time.process_time() - start)
    return [enemy_list,friendly_list, friendly_thrown, enemy_thrown]




def simple_eval_state(state):
    friendly = (8-state[2])*1.08 + len(state[0])
    enemy = (8-state[3])*1.08 + len(state[1])
    base = (friendly - enemy)*100 + 1000
    return base


def dist_to(friednly, enemy):
    (r_o, q_o) = friednly.cord
    (r_e, q_e) = enemy.cord
    return max(abs(r_e - r_o), abs(q_e - q_o), abs(q_o - q_e + r_o - r_e))


# def dist_to_friendly(token, friendly_list):
#     min_dist = 999
#     for friendly in friendly_list:
#         if can_defeat(token, friendly) == -1:
#             dist = dist_to(token,friendly)
#             if dist < min_dist:
#                 min_dist = dist
#     return min_dist

# def complex_eval_state(state):
#     friendly = (8-state.friendly_thrown)*1.01 + len(state.friendly_list)
#     enemy = (8-state.enemy_thrown)*1.01 + len(state.enemy_list)
#     base = (friendly - enemy*0.99)*100 + 1000
#     for enemy in state.enemy_list:
#         dist = dist_to_friendly(enemy, state.friendly_list)
#         # print(dist)
#         if dist != 999 and (10 - dist) > 0:
#             base += (10 - dist)
#     return base

# def random_throw(state):
#     thrown_count = state.friendly_thrown
#     throw_list = []
#     symbols = ['s','r','p']
#     p = -1
#     if state.player == "upper":
#         p = 1
#     r = (4-thrown_count)*p

#     pos = 1 if r>0 else -1
#     q = random.choice(range(-1*pos*4, pos*4-r+pos, pos))
#     return ("THROW", symbols[thrown_count%3], (r,q))




def game_theory_simple(state, upper):

    matrix = []
    friendly_action_list = get_action_list(state, True, upper)
    enemy_action_list = get_action_list(state, False, not upper)
    if len(friendly_action_list) is 0 or len(enemy_action_list) is 0:
        return
    duplicate = []
    for friendly_action in friendly_action_list:
        row = []
        new_state1 = state_copy(state)
        f_token = update_state(new_state1, friendly_action, True)
        for enemy_action in enemy_action_list:
            new_state2 = state_copy(new_state1)
            e_token = update_state(new_state2, enemy_action, False)
            kill, lost = settle(new_state2, f_token, e_token)

            if not check_duplicated_state(new_state2, False):
                row = []
                duplicate.append(friendly_action)
                break

            # friendly_action_list2 = get_action_list(new_state2, True, upper)
            # enemy_action_list2 = get_action_list(new_state2, False, not upper)
            
            # m2 = []
            # for friendly_action2 in friendly_action_list2:
            #     new_state3 = state_copy(new_state2)
            #     f_token2 = update_state(new_state3, friendly_action2, True)
            #     r2 = []
            #     for enemy_action2 in enemy_action_list2:
            #         new_state4 = state_copy(new_state3)
            #         e_token2 = update_state(new_state4, enemy_action2, False)
            #         kill, lost = settle(new_state4, f_token2, e_token2)
            #         r2.append(simple_eval_state(new_state4))
            #     m2.append(r2)
            # s1, v1 = solve_game(m2)
            row.append(simple_eval_state(new_state2))
        if len(row) != 0:
            matrix.append(row)
    # print(matrix)
    s,v = solve_game(matrix)
    for action in duplicate:
        friendly_action_list.remove(action)
    # print(s)
    return random.choices(friendly_action_list, weights = s,k = 1)[0]
    

def greedy(state, upper):
    best_score = -9999
    best_action_list = []
    action_list = get_action_list(state, True, upper)
    for action in action_list:
        new_state2 = state_copy(state)
        update_state(new_state, action, True)
        f_token = update_state(new_state2, friendly_action, True)
        kill, lost = settle(new_state2, f_token, None)       
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