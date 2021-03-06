from gametheory_complex.action import *
from gametheory_complex.state import *
import time



class Player:
    def __init__(self, player):
        State.player = player
        self.state = State()
        self.player = player
        self.timer = Timer()

    def action(self):

        # if self.state.friendly_thrown < 9:
        #     return random_throw(self.state).to_tuple()
        start = time.process_time()

        if self.state.friendly_thrown < 3:
            ret = random_throw(self.state)
            self.timer.action += (time.process_time() - start)
            return ret
        ret = game_theory_simple(self.state, self.timer).to_tuple()

        self.timer.action += (time.process_time() - start)
        return ret


    def update(self, opponent_action, player_action):
        start = time.process_time()
        update_state(player_action, self.state, True)
        update_state(opponent_action, self.state, False)
        settle(self.state)
        self.timer.update += (time.process_time() - start)
        self.timer.prt()

class Timer:
    def __init__(self):
        self.settle = 0
        self.copy = 0
        self.action = 0
        self.update = 0

    def prt(self):
        print("action: " + str(self.action))
        print("update: " + str(self.update))
        print("settle: " + str(self.settle))
        print("copy: " + str(self.copy))
