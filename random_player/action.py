from random_player.token import *

def update_enemy(opponent_action, enemy_list):
    action = opponent_action[0]
    if (action == "THROW"):
        symbol  = opponent_action[1]
        cord = opponent_action[2]
        enemy = Token(symbol,cord)
        enemy_list.append(enemy)
    else:
        cord = opponent_action[1]
        for enmey in enemy_list:
            if(enmey.cord == cord):
                enmey.cord = opponent_action[2]
                break

def update_player(player_action, friendly_list, player):
    action = player_action[0]
    if (action == "THROW"):
        symbol  = player_action[1]
        cord = player_action[2]
        token = Token(symbol,cord)
        friendly_list.append(token)
        player.thrown_count += 1
    else:
        cord = player_action[1]
        for token in friendly_list:
            if(token.cord == cord):
                token.cord = player_action[2]
                break

def throw_list(thrown_count ,player):
    # if thrown_count is 9:
    #     return [Throw(Token('r',(0,0)))]
    throw_list = []
    valid_q_dict = {4:(-4,0), 3:(-4,1), 2:(-4,2),1:(-4,3),
    0:(-4,4),-1:(-3,4),-2:(-2,4),-3:(-1,4),-4:(0,4)}
    symbols = ['s','r','p']
    p = -1
    if player == "upper":
        p = 1
    for r in range(4*p, (4-thrown_count)*p - p, -1*p):
        (q_min,q_max) = valid_q_dict[r]
        for q in range(q_min, q_max + 1):
            for s in symbols:
                #print(s + str(r) + "," + str(q))
                throw_list.append(Throw(Token(s,(r,q))))
    return throw_list


def slide_list(friendly_list):
    slide_list = []
    for friednly in friendly_list:
        potential_slide_list = potential_slide(friednly.cord)
        for potential_slide_move in potential_slide_list:
            slide_list.append(Slide(friednly, potential_slide_move))
    return slide_list

def swing_list(friendly_list):
    swing_list = []
    for friednly in friendly_list:
        potential_swing_list = potential_swing(friednly.cord, friendly_list)
        for potential_swing_move in potential_swing_list:
            swing_list.append(Swing(friednly, potential_swing_move))
    return swing_list

class Action:
    def __init__(self, token, tar):
        self.tar = tar
        self.token = token


class Throw(Action):
    action = "THROW"

    def __init__(self, token):
        super().__init__(token, token.cord)
        
    def toTuple(self):
        return (self.action, self.token.symbol, self.tar)


class Swing(Action):
    action = "SWING"

    def __init__(self, token, tar):
        super().__init__(token, tar)
    
    def toTuple(self):
        return (self.action, self.token.cord, self.tar)

class Slide(Action):
    action = "SLIDE"
    
    def __init__(self, token, tar):
        super().__init__(token, tar)

    def toTuple(self):
        return (self.action, self.token.cord, self.tar)
        

