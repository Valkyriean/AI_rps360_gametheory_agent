from gametheory_simple.action import *
from gametheory_simple.state import *
import time



class Player:
    def __init__(self, player):
        State.player = player
        self.state = State()
        self.player = player
        self.time_spent = 0
    def action(self):
        start = time.process_time()

        # if self.state.friendly_thrown < 9:
        #     return random_throw(self.state).to_tuple()

        if self.state.friendly_thrown < 3:
            action = random_throw(self.state)
        else:
            if self.time_spent < 55:
                action = game_theory_simple(self.state).to_tuple()
            else:
                action = greedy(self.state).to_tuple()
        self.time_spent += (time.process_time() - start)
        return action


    def update(self, opponent_action, player_action):
        # start = time.process_time()
        # update_state(player_action, self.state, True)
        # update_state(opponent_action, self.state, False)

        sim_update_state(player_action, opponent_action, self.state)
        # check_duplicated_state(self.state)
        # settle(self.state)
        # self.timer.update += (time.process_time() - start)
        # self.timer.prt()

# class Timer:
#     def __init__(self):
#         self.settle = 0
#         self.copy = 0
#         self.action = 0
#         self.update = 0

#     def prt(self):
#         print("action: " + str(self.action))
#         print("update: " + str(self.update))
#         print("settle: " + str(self.settle))
#         print("copy: " + str(self.copy))
