
import sys


script_descriptor = open("referee/__main__.py")
a_script = script_descriptor.read()
sys.argv =  ["-l", "ACCESS_GRANTED", "greedy_simple"]

exec(a_script)


script_descriptor.close()