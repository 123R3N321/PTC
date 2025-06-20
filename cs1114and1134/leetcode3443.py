'''
update after reading hint:

brute force directions! There are actually only 4 possibilities:
maximize NE, NW, SE, SW!

The lesson here? As a programmer YOU are thinking in a way that is too generalized
you have the mindset the four directions could really be N number of directions
which is a stupid, rigid mindset!

update on update:
One solution I read is brilliant: turns this problem into a pure math puzzle
'''


def manhattan(x,y):
    return abs(x)+abs(y)

def prefixMaxManhattan(path):
    curX = 0
    curY = 0
    curMax = 0
    for each in path:
        if each=='N':
            curY+=1
        if each=='S':
            curY-=1
        if each=='E':
            curX+=1
        if each=='W':
            curX-=1
        if manhattan(curX,curY)>curMax:
            curMax = manhattan(curX,curY)
    return curMax

def targetPair(direction):
    first = direction[0]
    second = direction[1]
    firstTarget = None
    secondTarget = None
    if first=='N':
        firstTarget = 'S'
    if first=='S':
        firstTarget = 'N'
    if first=='E':
        firstTarget = 'W'
    if first=='W':
        firstTarget = 'E'
    if second=='N':
        secondTarget = 'S'
    if second=='S':
        secondTarget = 'N'
    if second=='E':
        secondTarget = 'W'
    if second=='W':
        secondTarget = 'E'
    return first, second, firstTarget, secondTarget

def brute(path, direction,k):
    first, second, firstTarget, secondTarget = targetPair(direction)
    resPath = []
    for each in path:
        if k>0 and (each == firstTarget or each == secondTarget):
            if each==firstTarget:
                resPath.append(first)
            if each == secondTarget:
                resPath.append(second)
            k-=1
        else:
            resPath.append(each)
    return prefixMaxManhattan(resPath)

def q3443(path, k):
    return max(brute(path, "NE",k), brute(path, "NW",k), brute(path, "SE",k), brute(path, "SW",k))

'''
update: the brilliant math solution
'''

def supersmart(path,k):
    N,S,E,W = 0,0,0,0
    curMax = 0
    for i in range(len(path)):
        each = path[i]
        if each=='N':
            N+=1
        if each=='S':
            S+=1
        if each=='E':
            E+=1
        if each=='W':
            W+=1
        Manhattan = abs(N-S) + abs(E-W)
        cur = Manhattan+min(2*k, i+1-Manhattan) #at this step you might be like: "WHUUUUT???"
        #which is the same as curr = min(i+1, manhattan+2*k) if that is easier to understand
        if cur>curMax:
            curMax = cur
    return curMax

'''
what's a second lesson here? scary code
sometimes looks scary for no good reason at all
don't show off by making your code unreadable!

demo:
...and you can cook up some monstrous looking pasta like these below:
'''
from collections import defaultdict

def supershort(path,k):
    curMax = 0
    ct = defaultdict(int)   #overkill with hashmap since only 4 possible keys
    for i in range(len(path)):
        ct[path[i]]+=1
        curMax = max(curMax, min(i+1, abs(ct['N']-ct['S'])+abs(ct['E']-ct['W'])+2*k))   #WHY WOULD YOU DO THIS???!
    return curMax

'''
note the code below is correct but runtime n^2 so exceeds runtime limit
the "beauty" is that all the syntax used here are familiar, yet they make a monster
'''
def absoluteMonstrosity(s, k):
    return max(min(i + 1, abs(s[:i+1].count('N') - s[:i+1].count('S')) + abs(s[:i+1].count('E') - s[:i+1].count('W')) + 2 * k) for i in range(len(s)))

'''
now the code below is just...on a whole new level
(totally correct tho btw)
'''
def luvercraftian(s, k):
    return max(min(i + 1, abs(n - s_) + abs(e - w) + 2 * k)
               for i, c in enumerate(s)
               if not (n := (n if 'n' in locals() else 0) + (c == 'N')) is None
               if not (s_ := (s_ if 's_' in locals() else 0) + (c == 'S')) is None
               if not (e := (e if 'e' in locals() else 0) + (c == 'E')) is None
               if not (w := (w if 'w' in locals() else 0) + (c == 'W')) is None)



'''
detailed analysis:
whatever change we make, it will have an optimal result of:
    -> current manhattan distance += 2 
    because what originally could be a pair-wise "NS" whcih
    results in 0 now becomes either "NN" or "SS" (or "NE/NW/SE/SW" we really don care)
    which is 2. (it should be intuitive)

thus when we make k amount of changes, best result:
    ->current manhattan distance += (2*k)

BUT! what if k > the amount of changes we could make?
    -> eg. k = 1000, s = "NSEE"     (k bigger than entire path)
    -> eg. k = 2, s = "EEEE"        (we do not need k amount of changes, path already optimal)
    
Here is where min(2*k, i+1 - current manhattan distance) is ingenious:
    -> note at each iteration as i goes up by 1, current manhattan
    distance either goes up by 1 or goes down by 1
    -> hence i+1 == the number of steps we have performed 
    is also equivalent to the best possible manhattan distance
    if all directions are optimal, such as "EEEEE...." (or "ESESESES..." again we don care)

WAIT A MINUTE: doesn't that mean, if we are not given the constraint k,
instead rephrase the question as "what is the best manhattan distance possible
if you could change any amount of steps" the answer is simply len(path)???
    ->exactly. and in a prefix-increment manner, we simply look for i+1
    -> hence the answer is also simply min(i+1, current manhattan distance + 2*k)

'''