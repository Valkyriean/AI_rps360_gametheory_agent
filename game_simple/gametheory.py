"""
Solver for single-stage, zero-sum matrix-form games using scipy default
linear programming routines.

Original by Matthew Farrugia-Roberts, 2021

Students
* please note this implementation is not guaranteed to be free of errors,
  for example it has not been extensively tested.
* please report bugs to <matt.farrugia@unimelb.edu.au>.
* please feel free adapt for your own use-case.
"""

import numpy as np
import scipy.optimize as opt
import random
from game_simple.evaluation import *
from game_simple.state import *
from game_simple.util import *
from game_simple.greedy import *

def solve_game(V, maximiser=True, rowplayer=True):
    """
    Given a utility matrix V for a zero-sum game, compute a mixed-strategy
    security strategy/Nash equilibrium solution along with the bound on the
    expected value of the game to the player.
    By default, assume the player is the MAXIMISER and chooses the ROW of V,
    and the opponent is the MINIMISER choosing the COLUMN. Use the flags to
    change this behaviour.

    Parameters
    ----------
    * V: (n, m)-array or array-like; utility/payoff matrix;
    * maximiser: bool (default True); compute strategy for the maximiser.
        Set False to play as the minimiser.
    * rowplayer: bool (default True); compute strategy for the row-chooser.
        Set False to play as the column-chooser.

    Returns
    -------
    * s: (n,)-array; probability vector; an equilibrium mixed strategy over
        the rows (or columns) ensuring expected value v.
    * v: float; mixed security level / guaranteed minimum (or maximum)
        expected value of the equilibrium mixed strategy.

    Exceptions
    ----------
    * OptimisationError: If the optimisation reports failure. The message
        from the optimiser will accompany this exception.
    """
    V = np.asarray(V)
    # lprog will solve for the column-maximiser
    if rowplayer:
        V = V.T
    if not maximiser:
        V = -V
    m, n = V.shape
    # ensure positive
    c = -V.min() + 1
    Vpos = V + c
    # solve linear program
    res = opt.linprog(
        np.ones(n),
        A_ub=-Vpos,
        b_ub=-np.ones(m),
        options={'tol':1e-8},
    )
    if res.status:
        raise OptimisationError(res.message) # TODO: propagate whole result
    # compute strategy and value
    v = 1 / res.x.sum()
    s = res.x * v
    v = v - c # re-scale
    if not maximiser:
        v = -v
    return s, v


class OptimisationError(Exception):
    """For if the optimiser reports failure."""


def game_theory(state, upper):
    matrix = []
    friendly_action_list = get_action_list(state, True, upper)
    enemy_action_list = get_action_list(state, False, upper)
    if len(friendly_action_list) is 0 or len(enemy_action_list) is 0:
        return
    duplicate = []
    for friendly_action in friendly_action_list:
        row = []
        new_state1 = state_copy(state)
        f_token = update_state(new_state1, friendly_action, True)
        for enemy_action in enemy_action_list:
            new_state2 = state_copy(new_state1)
            e_token = update_state(new_state2, enemy_action, False)
            kill, lost = settle(new_state2, f_token, e_token)
            if not check_duplicated_state(new_state2, False):
                row = []
                duplicate.append(friendly_action)
                break
            # friendly_action_list2 = get_action_list(new_state2, True, upper)
            # enemy_action_list2 = get_action_list(new_state2, False, not upper)
            
            # m2 = []
            # for friendly_action2 in friendly_action_list2:
            #     new_state3 = state_copy(new_state2)
            #     f_token2 = update_state(new_state3, friendly_action2, True)
            #     r2 = []
            #     for enemy_action2 in enemy_action_list2:
            #         new_state4 = state_copy(new_state3)
            #         e_token2 = update_state(new_state4, enemy_action2, False)
            #         kill, lost = settle(new_state4, f_token2, e_token2)
            #         r2.append(simple_eval_state(new_state4))
            #     m2.append(r2)
            # s1, v1 = solve_game(m2)
            row.append(simple_eval_state(new_state2))
        if len(row) != 0:
            matrix.append(row)
    try:
        s,v = solve_game(matrix)
    except:
        print("OptimisationError")
        return greedy(state, upper)
    for action in duplicate:
        friendly_action_list.remove(action)
    return random.choices(friendly_action_list, weights = s,k = 1)[0]