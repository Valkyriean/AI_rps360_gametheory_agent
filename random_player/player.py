from random_player.action import *
import random

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
        self.friendly_list = []
        self.enemy_list = []
        self.thrown_count = 0
        self.player = player

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # put your code here
        action_list = []
        if self.thrown_count < 9:
            action_list += throw_list(self.thrown_count, self.player)
        action_list += slide_list(self.friendly_list)
        action_list += swing_list(self.friendly_list)

        # list of all valid action
        return random.choice(action_list).toTuple()
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
        update_enemy(opponent_action, self.enemy_list)
        update_player(player_action, self.friendly_list, self)
        
        settle(self.friendly_list, self.enemy_list)
