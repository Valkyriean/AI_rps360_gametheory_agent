import collections
import time

global history
history = collections.Counter()
# global update_time
# update_time = 0

move_vector_list = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0)]

# check whether can eliminate enemy token
def can_defeat(player, opponent):
    if (player == "p" and opponent == "r") or (player == 'r' and opponent == 's') or (player == 's' and opponent == 'p'):
        return 1
    elif player == opponent:
        return 0
    else:
        return -1

def update_state(state, action, isFriendly):
    # start = time.process_time()
    act_t = action[0]
    token = ()
    token_list = state[1]
    thrown_index = 3
    if isFriendly:
        token_list = state[0]
        thrown_index = 2
    if act_t == "THROW":
        symbol = action[1]
        tar = action[2]
        token = (symbol, tar)
        token_list.append(token)
        state[thrown_index] += 1
    else:
        cord = action[1]
        tar = action[2]
        for token1 in token_list:
            if token1[1] == cord:
                symbol = token1[0]
                index = token_list.index(token1)
                token = (symbol, tar)
                token_list[index] = token
                break
    # global update_time
    # update_time += (time.process_time() - start)
    return token


# global settle_t
# settle_t = 0

def settle(state, f_token, e_token):
    # start = time.process_time()
    f_list = state[0].copy()
    e_list = state[1].copy()
    lost = 0
    kill = 0
    for player_token in f_list:
        if f_token != None and f_token[1] == player_token[1]:
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
        if f_token != None and f_token[1] == opponent_token[1]:
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

    # global settle_t 
    # settle_t += (time.process_time() - start)
    return kill, lost

# def print_settle_time():
#     global settle_t
#     print("Settle time is: " + str(settle_t))


def out_bound(cord):
    if abs(cord[0]) > 4 or abs(cord[1]) > 4 or abs(cord[0] + cord[1]) > 4:
        return True
    else:
        return False

# global list_time
# list_time = 0

def get_action_list(state, friednly, upper):
    # start = time.process_time()
    action_list = []
    slide_list = []
    throw_cord_list = []
    throw_list = []
    swing_list = []
    token_list = state[0]
    opponent_list = state[1]
    thrown = state[2]
    if not friednly:
        token_list = state[1]
        opponent_list = state[0]
        thrown = state[3]
        upper = not upper
    for token in token_list:
        surrounding_list = []
        swing_cord_list = []
        cord = token[1]
        throw_cord_list.append(cord)
        # Get slide list
        for move_vector in move_vector_list:
            tar = (cord[0] + move_vector[0], cord[1] + move_vector[1])
            if not out_bound(tar):
                surrounding_list.append(tar)
                slide_list.append(("SLIDE", cord, tar))
                throw_cord_list.append(tar)

        # Get swing list
        for token2 in token_list:
            cord2 = token2[1]
            if cord2 in surrounding_list:
                for move_vector in move_vector_list:
                    tar2 = (cord2[0] + move_vector[0], cord2[1] + move_vector[1])
                    if (not out_bound(tar2)) and (tar2 not in surrounding_list) and (tar2 not in swing_cord_list) and tar2 != cord:
                        swing_cord_list.append(tar2)
                        swing_list.append(("SWING", cord, tar2))
    # get throw list
    for opponent in opponent_list:
        cord = opponent[1]
        throw_cord_list.append(cord)
        for move_vector in move_vector_list:
            tar = (cord[0] + move_vector[0], cord[1] + move_vector[1])
            if not out_bound(tar):
                throw_cord_list.append(tar)
    if thrown <= 8:
        symbols = ['s', 'r', 'p']
        # Add furthest throw row to list
        p = -1
        if upper:
            p = 1
        maxr = (4-thrown)*p
        pos = 1 if maxr > 0 else -1
        for q in range(-1*pos*4, pos*4-maxr+pos, pos):
            throw_cord_list.append((maxr, q))
        throw_cord_list = list(set(throw_cord_list))
        for cord in throw_cord_list:
            if (p == 1 and cord[0] < maxr) or (p == -1 and cord[0] > maxr):
                continue
            for s in symbols:
                throw_list.append(("THROW", s, cord))
    action_list = swing_list + slide_list + throw_list
    # global list_time
    # list_time += (time.process_time() - start)
    return action_list
    

# def print_list_time():
#     global list_time
#     print("Listing time is: " + str(list_time))


# def print_update_time():
#     global update_time
#     print("update time is: " + str(update_time))


def check_duplicated_state(state, real):
    global history
    curr = snap(state)
    if real:
        history[curr] +=1
    if history[curr] >= 2:
        return False
    return True


def snap(state):
    f_tuple = tuple(state[0])
    e_tuple = tuple(state[1])
    return (f_tuple, e_tuple, state[2], state[3])