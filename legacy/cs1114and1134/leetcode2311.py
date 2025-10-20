'''
stack approach?
or:
    -> check sequence total length, denote as n
    ->check k limit bit length, denote l
    build a sequence incrementally, length x
    while n-x>l, only add 0
    (note that if we do not have enough zero we do not
    even have an existing answer at all)
    once we reach n-x == l, add 0 and 1 freely
    problem: might not produce best

greedy solution just add zeros from backward

'''

def q2311(msg, k):
    ct = msg.count('0')
    accum = 0
    for i in range(len(msg)-1,-1,-1):
        if k< 2**(len(msg)-i-1)+accum:
            break   #cannot add more one
        if msg[i]=='1':
            ct+=1
            accum+= 2**(len(msg)-i-1)
    return ct
'''
update: my solution is correct and,
honestly, this apporach is more
readable than those given answers...
also this time Anwen totally used 
some weird and complicated approach
verma has the same idea as I.
'''