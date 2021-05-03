from ACCESS_GRANTED.action import *
from ACCESS_GRANTED.state import *

class Player:
    def __init__(self, player):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).
        """
        # put your code here
        State.player = player
        self.state = State()
        self.player = player

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # put your code here
        # list of all valid action
        # if self.state.friendly_thrown < 9:
        #     return random_throw(self.state).to_tuple()


        return simle_game_theory(self.state).to_tuple()
        # choose one
    
    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        # put your code here
        update_state(player_action, self.state, True)
        update_state(opponent_action, self.state, False)
        
        settle(self.state)
