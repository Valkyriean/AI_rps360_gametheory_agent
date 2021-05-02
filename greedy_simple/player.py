from greedy_simple.action import *
from greedy_simple.state import *

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

        self.state = State()
        self.player = player

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # put your code here
        action_list = []
        action_list += throw_list(self.state, self.player)
        action_list += slide_list(self.state)
        action_list += swing_list(self.state)
        # remove_friendly_fire(self.state,action_list)
        state_list = actions_to_states(self.state, action_list)


        # list of all valid action
        return best_action(state_list).to_tuple()
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
        check_duplicated_state(self.state)
        settle(self.state)
