# upper = 1

p = 1
thrown_count = 8

valid_q_dict = {4:(-4,0), 3:(-4,1), 2:(-4,2),1:(-4,3),
    0:(-4,4),-1:(-3,4),-2:(-2,4),-3:(-1,4),-4:(0,4)}


for r in range(4*p, (4-thrown_count)*p - p, -1*p):
    pos = 1 if r>0 else -1
    for q in range(-1*pos*4, pos*4-r+pos, pos):
        print(str(r)+","+str(q))