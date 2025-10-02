'''
This is iterative solution
based on observation of Darren's
manual game play
'''

'''
Game rule summary:

glossary:
    relative left/right:
        if left == cur:
            rel. l = mid
            rel.r = right
            
        if mid == cur:
            rel. l = left
            rel.r = right
            
        if right == cur:
            rel. l = left
            rel.r = mid
    
    current disc size:
        -n initial state, kept track (no update)
            (given initial n discs, top is -n, second-top is -n+1, .., last is 0)


0. start from left pillar, from = None, to = None

1. check top stack size of left middle right see if move is legal
    if not legal, move to the pillar NOT TOUCHED (not from AND not to)
        repeat entire algo 
    else:   #implied we can move, legal: not empty current stack, and top elem not too big
        check current stack odd even property:
            if odd:
                move toward rightmost relative pillar
            else:   #implied even
                move toward leftmost relative pillar
                
2. endgame check: size(right) == n
        
'''

'''
generic helper, move
from one pillar to another,
assume legal operation all
'''
def move(current, target):
    try:
        target.append(current.pop())
    except:
        raise Exception('Cannot move from {} to {}'.format(current, target))

'''
step0 helper
left, mid, right: stack (lst)
return n
'''
def init(n,left,mid,right):
    if n < 1: raise ValueError('n is less than 1')

    for i in range(n):  #populate left pillar
        left.append(-i)

    top = left.pop()

    if n%2:  #odd
        right.append(top)
        return right
    else:   #implied even
        mid.append(top)
        return mid


'''
step1 helper:
given a current pillar, check
if we could move at all

return bool
'''
def legalCheck(current, left, mid, right):

    if not current: return False

    lTop = left[-1] if left else 1
    mTop = mid[-1] if mid else 1
    rTop = right[-1] if right else 1

    if current == left:
        return lTop<mTop or lTop<rTop
    if current == mid:
        return mTop<lTop or mTop<rTop
    if current == right:
        return rTop<lTop or rTop<mTop
    raise ValueError('current parameter fault')

'''
setp1 helper, called after legal check
given a current pillar, check which pillar to move to

return stack target (ref)
'''
def targetCheck(current, left, mid, right):
    if not current: raise ValueError('target Check fault: current pillar empty')

    target = None
    if len(current)%2:  #odd amount
        if current == left or current == mid:
            target = right  #odd amount and come from left pillar
        elif current == right:
            target = mid
        else:
            raise ValueError('target check fault: current is odd but something went wrong')
    else:   #even amount
        if current == mid or current == right:
            target = left
        elif current == left:
            target = mid
        else:
            raise ValueError('target check fault: current is even but something went wrong')
    if target is not None:
        return target
    raise ValueError('target is None, seg fault')

'''
step2 helper, called at the end of all else

return bool
'''
def endGameCheck(n, left, mid, right):
    return len(right)==n


'''
driver code for entire game
'''
def main(n):
    left = []
    mid = []
    goal = right = []
    target = init(n,left,mid,right)
    steps = 1   #after initial move, we took a step
    if endGameCheck(n, left, mid, goal): return steps  #edge case: one step game over
    current = left #current stack is the left stack
    while not endGameCheck(n, left, mid, goal):
        if legalCheck(current, left, mid, right):   #if we could make a move
            steps+=1    #tally
            target = targetCheck(current, left, mid, right)
            move(current, target)
        else:   #need to set current as the pillar NOT TOUCHED
            if (current == left or current == mid) and (target == left or target == mid):
                current = right
            elif (current == mid or current == right) and (target == mid or target == right):
                current = left
            elif (current == left or current == right) and (target == left or target == right):
                current = mid
            else:
                raise ValueError('Pillar target reassignment failed')
    return steps

def efficient(n):
    if n <1: return 0
    move = efficient(n-1)
    move+=1
    move = efficient(n-1)
    return move





if __name__ == '__main__':
    n = 19
    print(f"when we have {n} discs, we need {main(n)} steps")
    print(f"test recursive count, for {n} discs, need {efficient(n)} steps")
