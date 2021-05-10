import sys
from io import StringIO
import contextlib
from referee.main import *



sys.argv =  ["referee", "-v 0","ACCESS_GRANTED", "minimax_ab"]

exp_score = 50
t_weight = 100
f_weight = 1
e_weight = 1


def test_score(rounds):
    upper = 0
    lower = 0
    draw = 0
    result = []
    for x in range(0,rounds):
        out = main()
        result.append(out)
        print(out)
        if "upper" in out:
            upper +=1
        elif "lower" in out:
            lower +=1
        else:
            draw += 1
        print("turn: ", x)
        print("Upper win: ", upper)
        print("lower win:", lower)
        print("draw: ", draw)
    print(result)
    print("Upper win: ", upper)
    print("lower win:", lower)
    print("draw: ", draw)
    return upper+0.5*draw



def learn_weight(weight, exp_score):
    hist = 0
    score = 0
    test_weight = weight
    step_size = 10
    increase = True
    while(score < exp_score):
        score = test_score(100)
        if (score<hist):

            if increase:
                weight -= step_size/2
                increase = False
            else:
                weight += step_size/2
                increase = True
        hist = score

        
test_score(100)