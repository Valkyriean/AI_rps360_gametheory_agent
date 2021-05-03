from gametheory_simple.action import *
from gametheory_simple.state import *



class Player:
    def __init__(self, player):
        State.player = player
        self.state = State()
        self.player = player

    def action(self):

        # if self.state.friendly_thrown < 9:
        #     return random_throw(self.state).to_tuple()

        if self.state.friendly_thrown < 3:
            return random_throw(self.state)


        return game_theory_simple(self.state).to_tuple()
    
    def update(self, opponent_action, player_action):

        update_state(player_action, self.state, True)
        update_state(opponent_action, self.state, False)
        
        settle(self.state)
