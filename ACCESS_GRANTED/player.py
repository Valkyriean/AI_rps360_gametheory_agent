from ACCESS_GRANTED.greedy import *
from ACCESS_GRANTED.gametheory import *
import time

class Player:
    def __init__(self, player):
        self.state = [[], [], 0, 0]
        self.upper = True
        if player == "lower":
            self.upper = False
        self.time_spent = 0

    def action(self):
        start = time.process_time()
        # Use gametheory when time allows
        if self.time_spent < 55:
            action = game_theory(self.state, self.upper)
        else:
            action = greedy(self.state, self.upper)
        self.time_spent += (time.process_time() - start)
        return action

    def update(self, opponent_action, player_action):
        f_token = update_state(self.state, player_action, True)
        e_token = update_state(self.state, opponent_action, False)
        kill, lost = settle(self.state, f_token, e_token)
        check_duplicated_state(self.state, True)
        # print_copy_time()
        # print_settle_time()
        # print_list_time()
        # print_update_time()


