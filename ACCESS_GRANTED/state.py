import time
MAX_THOROWN = 8

# global copy_time
# copy_time = 0 
# def print_copy_time():
#     print("copy time is :" + str(copy_time))

# Deep copy the state
def state_copy(state):
    # start = time.process_time()
    enemy_list = state[0].copy()
    friendly_list = state[1].copy()
    friendly_thrown = state[2]
    enemy_thrown = state[3]
    # global copy_time
    # copy_time += (time.process_time() - start)
    return [enemy_list,friendly_list, friendly_thrown, enemy_thrown]

