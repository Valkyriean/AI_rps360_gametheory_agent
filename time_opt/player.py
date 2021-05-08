from time_opt.action import *
from time_opt.state import *
import time



class Player:
    def __init__(self, player):
        self.state = {}
        self.throw = [0,0]
        if player == 'upper':
            self.player = 0
        else:
            self.player = 1
        self.time_spent = 0
    def action(self):
        start = time.process_time()

        # if self.state.friendly_thrown < 3:
        #     action = random_throw(self.state)
        # else:
        if self.time_spent < 55:
            action = game_theory_simple(self.state).to_tuple()
        else:
            action = greedy(self.state).to_tuple()
        self.time_spent += (time.process_time() - start)
        return action


    def update(self, opponent_action, player_action):


        sim_update_state(player_action, opponent_action, self.state, True)
        check_duplicated_state(self.state, True)
        print_copy_time()
        print_update_time()
        print_list_time()

