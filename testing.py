
import sys
from io import StringIO
import contextlib
from referee.main import *

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

# script_descriptor = open("referee/__main__.py")
# game = script_descriptor.read()
sys.argv =  ["referee","ACCESS_GRANTED", "greedy_simple"]

upper = 0
lower = 0
draw = 0



result = []

for x in range(0,100):
    out = main()
    result.append(out)
    print(out)
    if "upper" in out:
        upper +=1
    elif "lower" in out:
        lower +=1
    else:
        draw += 1
    print("Upper win: ", upper)
    print("lower win:", lower)
    print("draw: ", draw)


print(result)
print("Upper win: ", upper)
print("lower win:", lower)
print("draw: ", draw)

