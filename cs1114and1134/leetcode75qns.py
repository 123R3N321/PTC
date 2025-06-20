'''
This is the "scratchbook" for the
leetcode 75 collections.

problems which are too easy are just deleted after I finished them here
mildly hard ones, I might leave behind notes
truly hard and intersting ones, I will have implementation and
in-detail analysis
'''


'''
leet 238 is the first question I encounter in leet75
that has me puzzled for a bit

below is the "naive" solution I get from a hint in discussion section
and it is an ugly solution haha

compute the cumulative product from left side 
and from right side
and at each ind position you just need the product of the left
and right side.

update: this is the correct solution. Lame.
'''
def l238hint(arr):
    prod = 1
    left = [1]  # put a dummy 1 there makes the code easier
    right = []
    res = []
    for i in arr:
        prod*=i
        left.append(prod)
    prod=1
    for i in arr[::-1]:
        prod*=i
        right.append(prod)
    right.reverse() #remember to flip it!
    right.append(1) # makes the code easier. really trivial

    for i in range(len(arr)):
        res.append(left[i]*right[i+1])
    return res

'''
now, the question also claims there is a way to make the
solution O(1) extra space

my idea from the hint:
trivial improvement by
first put all values from input to a res arr
and the convert the input in-place to right arr
and the output array is in-place computed to be left arr
and then "absorb" the now mutated input arr into res arr
pretty dumb, I gotta say

update: yeah this is indeed the correct solution. lame lame.
'''



'''
The discrete math logic:    (my real failure in developing the best answer is the failure in discrete math)

# edge case of fewer than 3 elems, automatically fail
 start with the first two elements in the array,
 start walking toward the right one by one
 if the current is smaller or equal to the first:
    set current to be the first
    we do not need to bother with anything else. Move on to next element
if the current is bigger than the first (this simply means "else") AND the current is smaller than the second element:
    set the current to be the second element
    we do not need to bother with anything else. Move on to next element
if the current is bigger than the first, AND bigger than the second, (else. By this point we filled out the universal set):
    set the current to be the third, which is unnecessary because by now we can return True.


'''
def q334(arr):
    if len(arr)<3: return False
    first = max(arr)+1
    second = max(arr)+1
    for each in arr:
        if each<=first:
            first = each
        elif each<=second:  #the "elif" implies that current element is bigger than "first", but not bigger than the second
            # but you also have to think FORWARD
            # when a current element is indeed smaller than second
            # we go on to next iteration while remembering
            # the current element to be the one to pass the "second check"
            second = each
        else:   # the else implies an element is bigger than both first and second
            return True
    return False


'''
sliding window approach
we have k quota amount of 
good check

iterate thru array

    if ct > currentMAx, currentMax set to ct
    
    if we see 0 and there is quota left,
        pass good check, add ct by 1, remember where we flipped (use queue)
    else:
        if we see 1:
        simply add ct by 1 
        
        otherwise we see 0: # implied no quota left
            abandon previous flip,
            remember ind pos previous flip+1 till right here as ct

'''
from collections import deque
def q1004(arr,k):
    if k==0: return edgeCase(arr)
    curMax = 0
    ct = 0
    flipRecord = deque()
    for i in range(len(arr)):
        if ct>curMax:
            curMax = ct

        if arr[i]==0 and k>0:
            flipRecord.append(i)
            k-=1
            ct+=1
        else:
            if arr[i]==1:
                ct+=1
            else:   #implied: arr[i] != 1 and k<=0
                ct = i-flipRecord.popleft()
                flipRecord.append(i)
    if ct>curMax:
        curMax = ct
    return curMax

def edgeCase(arr):  #edge case k==0
    curMax = 0
    cur = 0
    for i in arr:
        if cur>curMax:
            curMax = cur
        if i==1:
            cur+=1
        else:
            cur = 0
    if cur>curMax:
        curMax = cur
    return curMax

def q1493(arr):
    return q1004(arr, 1)-1
'''
I think q1493, which uses q1004, should lead to
both of them preserved in my record
while 1004 is very easy, it is a stunningly
creative solution if you develop q1493
without doing 1004 firsthand.
This is worth remembering.

the lesson here?
literally remove/add in element
in an array is costly and difficult (as if 
disrupts the index length and order)
instead think of modification of 
elements to replace the need of removal/addition 
of elements. Good lesson.
'''

'''
seems pretty easy.
iterate backward,
    if it is star:
        accumulate power
    if it is char:
        if power>0:
            eliminate
            power-=1
        else:
            add to result
    result.reverse()
    return result
'''
def q2390(msg):
    res = []
    powa = 0    # powaaaaaa!
    for each in msg[::-1]:
        if '*' == each:
            powa+=1
        else:   #must be a non-asterisk char
            if powa>0:
                powa-=1
            else:   # no powa, and also a letter char
                res.append(each)
    res = res[::-1]
    res = ''.join(res)
    return res

def elegant2390(msg):
    msg = list(msg)
    iter = 0
    for each in msg:
        if '*' == each:
            iter-=1
        else:   #must be non-asterisk char
            msg[iter]=each
            iter+=1
    return ''.join(msg[:iter])

def pop2390(msg):
    res = []
    for each in msg:
        if '*' == each:
            res.pop()
        else:
            res.append(each)
    return ''.join(res)

'''
ok, not as easya s first seems.
do a blunt recursion approach
below is designed by chatgpt
'''
def decodeString(s):
    def helper(s, idx):
        res = []
        num = 0
        while idx < len(s):
            char = s[idx]
            if char.isdigit():
                num = num * 10 + int(char)
            elif char == '[':   #note: guaranteed that '[' does not appear as last char in s
                idx, decoded = helper(s, idx + 1)  # Recurse into the bracket
                res.extend(decoded * num)
                num = 0  # Reset number after use
            elif char == ']':
                return idx, res
            else:   #implied char has to be a letter
                res.append(char)
            idx += 1

        return idx, res

    _, result = helper(s, 0)
    return ''.join(result)

'''

below is my own implementation of 394
based on understanding of the chatgpt ver
'''
def recurS(msg, multiplier, pos):
    arr = []    #a local arr is created inside recursive call
    # note there is no memory issue as we are not doing arr.clear() which clears arr across callstack.
    while pos<len(msg):
        cur = msg[pos]
        if cur.isdigit():
            multiplier = multiplier * 10+int(cur)   #keep track of current multiplier
        elif cur == '[':    #we should recurse
            pos, res = recurS(msg, 0, pos+1)    #inside, multiplier reset
            arr.extend(multiplier* res) #after recursion is done, expand the res arr
            multiplier = 0 #reset
        elif cur.isalpha():
            arr.append(cur)
        elif cur == ']':    #by now we should have exhausted all possibilities
            #do not bump since recursive call did it already
            return pos, arr
        else:
            raise Exception("unknown char detected in msg input")
        pos += 1    #bump iterator
    return pos, arr

def doIt(msg):
    _, res = recurS(msg, 0, 0)
    return ''.join(res)



'''
649 is very peculiar
double stack?
ah, try this:
    one stack for D, another for R
        -> if we see D and R is empty:
            add to Dstack
        -> elif we see R and D is empty:
            add to Rstack
        -> elif we see D and R stack is not empty:
            that means we have a R preceeding D
            ->do not add D, because it is being canceld
            -> also pop R but remember to add it back for next round
        ->elif we see R and D is not empty
            ->same thing as the above situation
        now we have a queue for D and R that got poped
            ->add them back to the two stacks following the same logic as above cycle
            -> algorithm ends when the queue only has R or D (can keep track per operation)
update:
    a simple 2 queue solution will do hahhahaa
    I was so close hahahaahha
    but isok my answer also works

update: can be used for 1134:
    first ask student to solve anyhow
    then ask to solve with only stack (two stack makes a queue!)
    (plus, in this question, overall runtime will not increase!)

'''

import queue
def vote(msg):
    Dstack = []
    Rstack = []
    q = queue.Queue()   # has put and get operations
    hasD = True
    hasR = True
    for each in msg:
        q.put(each)

    while hasD and hasR:    #either one goes out, we done
        hasR = False    #set to False, because very soon we will empty out the q
        hasD = False
        while not q.empty():
            each = q.get()  #empty out the q
            if "D" == each:
                if len(Rstack)<=0:
                    Dstack.append(each)
                else:   #implied Rstack not empty
                    q.put(Rstack.pop())
                    hasR = True #this means the senator survives till next round
            else:   #implied "R" == each
                if len(Dstack)<=0:
                    Rstack.append(each)
                else:
                    q.put(Dstack.pop())
                    hasD = True
    if hasR or len(Rstack)>0:
        return "Radiant"
    if hasD or len(Dstack)>0:
        return "Dire"
    return "wtf I don get it"


from collections import deque

# use a delay to indicate we are doing next round
def recurVote(rad, dire, delay):
    # Base case: one party is gone
    if not rad:
        return "Dire"
    if not dire:
        return "Radiant"

    # Remove both, totoally ok cuz we do empty queue check above
    curR = rad.popleft()
    curD = dire.popleft()

    if curR < curD:
        rad.append(curR + delay)
    else:
        dire.append(curD + delay)

    return recurVote(rad, dire, delay)

def recur649(arr):
    Rq = deque(ind for ind, cha in enumerate(arr) if cha == 'R')
    Dq = deque(ind for ind, cha in enumerate(arr) if cha == 'D')
    return recurVote(Rq, Dq, len(arr))

'''
note the code below DOES NOT WORK
even though it seems to be the same logic
as the deque version:
    because queue.Queue SHOULD NOT BE USED FOR RECURSION
    it simply unravels.
'''
def recurVoteFail(rad, dire, delay):
    # Base case: one party is gone
    if not rad:
        return "Dire"
    if not dire:
        return "Radiant"

    # Determine who acts first
    curR = rad.get()    #this crashes beyond one level of callstack
    curD = dire.get()
    if curR < curD:
        rad.put(curR + delay)
    else:   #implied rad[0]>dire[0], they are never equal
        dire.put(curD+delay)
    return recurVoteFail(rad, dire, delay)

'''
omg this one is breain dead lol

update:
trivial runtime improvement:
    have a bumper that bumps 2 at a time
    and another 1 at a time
    when first bumper reaches end
    second bumper is at our target
    (this makes runtime go from 1.5n to 0.5n)
'''
def getLen(start):
    ct = 0
    while start:
        ct += 1
        start = start.next
    return ct

def rmNode(prev, next):
    prev.next = next
    next.prev = prev
    #simply ignore the middle node
    #does not work for edge case

#0-indexed linear traversal
def locate(start, n):
    dst = start
    while n > 0:
        dst = dst.next
        n -= 1
    return dst

def q2095(start):
    n = getLen(start)
    if n==1:
        start = None
        return None
    if n==2:
        start.next = None
        return start

    #ok now we only dealing w 3 nodes ups yay
    prev = locate(start,n//2 - 1)
    next = prev.next.next
    rmNode(prev, next)
    return start



class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

'''
given a list of numbers
create singly linked list
return the starting point
'''
def makeSLL(lst, start = 0):
    if start == len(lst):
        return
    return ListNode(lst[start], makeSLL(lst, start+1))

def printSLL(start):
    while start:
        print(start.val, end=' ')
        start = start.next

'''
also braindead but more tedious now
'''
def q328(start):
    n = getLen(start)
    if n<=2:
        return start
    if n==3:
        node1 = start.next
        node2 = node1.next
        start.next = node2
        node2.next = node1
        node1.next = None
        return start
    else:   #now we only dealing w len 4 ups
        node1 = start
        node2 = start.next
        connection = start.next

        while node2.next:
            node1.next = node2.next
            if node2.next:
                node2.next = node2.next.next

            node1 = node1.next
            if node2.next:
                node2 = node2.next
        node1.next = connection
        return start


'''
rev SLL, recursion for sure
update: bro this is so dumb....
remember to use updated head!
_,start = recur...
then printSLL(start)
'''


def reverse_list(head):
    if head is None or head.next is None:
        return head
    revHead = reverse_list(head.next)
    head.next.next = head
    head.next = None
    return revHead

def q206(start):    #first return val for traversal, second one as anchor for starting point
    if not start.next:
        return start, start
    local, constStart = q206(start.next)
    local.next = start
    start.next = None
    return start, constStart

'''
edge case. Sigh.
'''
def complete206(start):
    if start is None:
        return None
    else:
        return q206(start)[1]


'''
ok now rev iterative cuz why not
'''
def q206iterative(start):
    n = getLen(start)
    if not start:
        return None
    if n==1:
        return start
    if n==2:
        node1 = start.next
        node1.next = start
        start.next = None
        return node1
    #since now we have guaranteed n>=3, while loop can check third node ahead
    node1 = start
    node2 = node1.next
    node1.next = None
    while node2:
        node3 = node2.next
        node2.next = node1
        node1 = node2
        node2 = node3
    return node1

'''
this immediately reminds me of:
create a copy of the list
reverse it
traverse the two lists and sum pair by pair
'''
def q2130helper(start, n,ct, arr):
    if not start:
        return
    arr[n-ct-1][0] = start.val
    q2130helper(start.next, n, ct+1, arr)
    arr[ct][1] = start.val

def q2130(start):
    n = getLen(start)
    arr = [[None, None] for i in range(n)]
    q2130helper(start, n, 0, arr)
    maxSum = float('-inf')
    for eachPair in arr:
        localSum = (eachPair[0]+eachPair[1])
        if localSum > maxSum:
            maxSum = localSum
    return maxSum

def recur(num,top, lst):
    if num<0:
        return
    lst[top-num][0] = num
    recur(num-1, top,lst)
    lst[num][1] =num

def fast2130(start):
    n = getLen(start)
    resArr = [float('-inf') for i in range(n)]
    curBest = [float('-inf')]
    def helper(start, n, ct, resArr,curBest):
        if not start:
            return
        resArr[n-ct-1] = start.val
        helper(start.next, n, ct+1, resArr, curBest)
        resArr[ct] += start.val
        if resArr[ct] > curBest[0]:
            curBest[0] = resArr[ct]
    helper(start, n, 0, resArr, curBest)
    return curBest[0]

'''
let's do an iterative ver
'''
def iterative2130(start):
    res = []
    scan1 = start
    while scan1:
        res.append(scan1.val)
        scan1 = scan1.next
    start = q206iterative(start)
    curBest = float('-inf')
    scan2 = start
    bumper = 0
    while scan2:
        local = res[bumper]+scan2.val
        if local>curBest:
            curBest = local
        bumper = bumper+1
        scan2 = scan2.next
    return curBest

'''
ok 437 is finally getting interesting
problem is I am not sure If there is
efficiency concern

tentatively:
each node knows all its consecutive parents' cumulative sum

suppose node 3 has parent 5 and grandpa 7, then
3 knows it could be alone, could be 3+5, or could be 3+5+7
where the 5+7 part is computed by its parent already
and at each node we need to make the calculation 
to see if we currently hit the target with any prefix sum
inherited from its parent

update:

yeah checked the answers there is no better solution smh.
'''

def recurPathSum(root, heritage, target, curSum):
    if root is None:
        return
    localHeritage = []
    for eachVal in heritage:
        localHeritage.append(eachVal+root.val)
    localHeritage.append(root.val)  #yourself is a possible one-level option
    for eachVal in localHeritage:
        if eachVal == target:
            curSum[0]+=1
    recurPathSum(root.left,localHeritage,target, curSum)
    recurPathSum(root.right,localHeritage,target, curSum)
def q437(root,target):
    resArr = [0]
    recurPathSum(root, [], target, resArr)
    return resArr[0]

'''
zigzag seems fun but not too hard either
whereFrom simply tracks which direction we came from
0->i am left child
1->i am right child
we run the recursion twice from root
'''

'''
assume algo starts at a child not overall root

update:
dumb question.
'''
def zigzag(root, curSum, bestSum, whereFrom):
    if root is None:
        return
    if 0==whereFrom:
        curSum+=1
        if curSum>bestSum[0]:
            bestSum[0] = curSum
        zigzag(root.right, curSum, bestSum, 1)
        zigzag(root.left, 0, bestSum, 0)
    if 1==whereFrom:
        curSum+=1
        if curSum>bestSum[0]:
            bestSum[0] = curSum
        zigzag(root.left, curSum, bestSum, 0)
        zigzag(root.right, 0, bestSum, 1)

def q1372(root):
    bestSumL = [0]
    bestSumR = [0]
    if root is None:
        return 0
    if root.left:
        zigzag(root.left, 0, bestSumL, 0)
    if root.right:
        zigzag(root.right, 0, bestSumR, 1)
    return max(bestSumL[0], bestSumR[0])



'''
common ancestor? still seems dumb
I do not see a super efficient solution
each node know all its ancestors,
olderst in arr[0] youngest in arr[-1]

traverse the tree to find both target nodes
compare their arrs backward till we find match?
that means we also do inverse mapping once
lol why not.
'''

'''
traverse a tree dfs looking for target
return a list of all it ancestors 
old -> young [0:len]
'''
def preprocessing(root, target, lst):
    if root is None:
        return False
    lst.append(root)    #add for the success case as a target can also be the common ancestor
    if root.val == target.val:
        return True #shortcircuit return to preserve the list
    if preprocessing(root.left, target, lst) or preprocessing(root.right, target, lst):
        return True
    lst.pop()   #backtrack removal
    return False

def q236(root, node1, node2):
    lst1 = []
    preprocessing(root, node1, lst1)

    lst2 = []
    preprocessing(root, node2, lst2)
    inverseMap = {j.val:i for i, j in enumerate(lst1)}  #only valid because values are unique
    for each in lst2[::-1]: #go backward for youngest ancestor
        if each.val in inverseMap:
            return each #first match return only works for unique valued nodes
    return None #guaranteed not to happen but a nice failsafe

'''
update after checking standard solution:
do a post-order recursion that focuses on finding the common targert only
note that my approach actually gives you the full path toward the common ancestor
(and also all the way to the root, btw)
while the elegant solution gives you precisely the common youngest ancestor
'''

def elegant236(root, node1, node2):
    if not root:
        return None #which is a false
    if root.val == node1.val:   #both left and right found treated as true
        return root
    if root.val == node2.val:
        return root

    leftFound = elegant236(root.left, node1, node2) #cannot literally return bool type cuz we need traversal
    rightFound = elegant236(root.right, node1, node2)
    if leftFound and rightFound:
        return root #eleganty locate the exact callstack level where result is obtained
    if leftFound:
        return leftFound    #pass up the fact that we found the target up the call stack
    else:
        if rightFound:
            return rightFound
        else:
            return None #guaranteed not going to happen but a good failsafe


'''
ahh, I accidentally spoilered myself by
looking at the sub header of the leetcode75
lesson here: do NOT look at those sub headers!

anyways, this problem is clearly a bfs problem
go level by level and only retain the last node
per level
'''

'''
ok, using queue would make this problem
stupid. 
'''
def recurRight(lvlLst,resLst):
    if len(lvlLst)==0:
        return
    resLst.append(lvlLst[-1].val)   #guaranteed not empty list
    localLst = []
    for each in lvlLst:
        if each.left:
            localLst.append(each.left)
        if each.right:
            localLst.append(each.right)
    recurRight(localLst,resLst)

def q199(root):
    if not root: return []
    resLst = []
    recurRight([root],resLst)
    return resLst

'''
ok, let's do a queue version
'''
from collections import deque

def qVer199(root):
    if not root: return []
    q = deque()
    q.append(root)
    res = [root.val]
    tempoQ = deque()
    while q:
        while q:
            cur = q.popleft()
            if cur.left:
                tempoQ.append(cur.left)
            if cur.right:
                tempoQ.append(cur.right)
        if tempoQ:
            res.append(tempoQ[-1].val)
        qtransfer(tempoQ,q)
    return res
def qtransfer(fromq, toq):
    if toq:
        raise Exception(f'target q {toq} is not empty')
    while fromq:    #need to empty it out
        toq.append(fromq.popleft())


'''
now q1161 seems straightaway boring...
'''
def levelSumRecur(lvlLst, bestVal, bestLvl, curLvl): #guaranteed root not None
    if len(lvlLst)==0:
        return bestLvl
    localLst = []
    curVal = getLvlSum(lvlLst)
    if curVal>bestVal:   #strictly greater than
        bestVal = curVal
        bestLvl = curLvl
    for each in lvlLst:
        if each.left:
            localLst.append(each.left)
        if each.right:
            localLst.append(each.right)
    return levelSumRecur(localLst, bestVal, bestLvl, curLvl+1)

'''
ok let's do a queue version
'''

from collections import deque

def Qver1161(root):
    q = deque()
    tempoQ = deque()
    q.append(root)  #guaranteed not None node
    curLvl = 0
    bestLvl = 1
    bestSum = float('-inf')
    while q:
        curLvl += 1
        curSum = 0
        while q:
            cur = q.popleft()
            curSum += cur.val
            if cur.right:   #left-right order does not matter here
                tempoQ.append(cur.right)
            if cur.left:
                tempoQ.append(cur.left)
        if curSum > bestSum:
            bestSum = curSum
            bestLvl = curLvl
        qtransfer(tempoQ,q)

    return bestLvl

def getLvlSum(lvlLst):
    res = 0
    for eachNode in lvlLst:
        res+=eachNode.val
    return res

'''
bst node deletion also dumb
'''

def findTargetParent(root, target, parent, side):
    if not root:
        return None, None   #if findable, should never happen
    if root.val == target:
        return parent, side
    if root.val > target:
        return findTargetParent(root.left, target, root, 0)
    if root.val < target:
        return findTargetParent(root.right, target, root, 1)
    return None, None #never gets here
'''
given a root, find its leftmost child
to be used on the right subtree of the kill target
'''
def findReplacement(root, parent=None, side=1):
    # Find the leftmost node in the subtree rooted at `root`
    while root and root.left:
        parent = root
        root = root.left
        side = 0
    return root, parent, side

#edge case overall root is target, return the new root
def edgeCase(root):
    if not root.left and not root.right:
        return None #simply have an empty tree now
    if not root.left:
        return root.right
    if not root.right:
        return root.left

    # In-order successor (leftmost in right subtree)
    replacement, parent, side = findReplacement(root.right, root, 1)

    # Detach replacement from its parent
    if parent != root:
        parent.left = replacement.right
        replacement.right = root.right  # attach full right subtree

    # Always attach left subtree
    replacement.left = root.left

    return replacement


def deleteNode(root, target):
    if not root:
        return None
    if root.val == target:
        return edgeCase(root)
    parent, side = findTargetParent(root, target, None, 0)  #side is a dummy value at the beginning
    if not parent:
        return root

    #simply replace the killed node with the leftmost child of right sub
    if 0==side: #kill target is left child
        kill = parent.left
        if not kill.right:
            parent.left = kill.left
            return root

        if not kill.left:
            parent.left = kill.right
            return root
        #kill target has both kids
        replacement, replacementParent, replacementSide =findReplacement(kill.right, kill, 1)

        # Detach replacement from its current location
        if replacementParent != kill:
            if replacementSide == 0:
                replacementParent.left = replacement.right
            else:
                replacementParent.right = replacement.right
            replacement.right = kill.right  # safe: replacement is deeper in right subtree

        replacement.left = kill.left

        # Reassign parent's child to replacement
        if side == 0:
            parent.left = replacement
        else:
            parent.right = replacement

        return root
    if 1==side:
        kill = parent.right
        if not kill.right:
            parent.right = kill.left
            return root

        if not kill.left:
            parent.right = kill.right
            return root
        #kill target has both kids
        replacement, replacementParent, replacementSide = findReplacement(kill.right, kill, 1)

        # Detach replacement from its current location
        if replacementParent != kill:
            if replacementSide == 0:
                replacementParent.left = replacement.right
            else:
                replacementParent.right = replacement.right
            replacement.right = kill.right  # safe: replacement is deeper in right subtree

        replacement.left = kill.left

        # Reassign parent's child to replacement
        if side == 0:
            parent.left = replacement
        else:
            parent.right = replacement

        return root

# test code
if __name__ == '__main__':
    start = makeSLL([i for i in range(7)])
    print("before: ", end='\t')
    printSLL(start)
    print()
    # _, start = q206(start)
    start = q206iterative(start)
    print("after: ", end='\t\t')
    printSLL(start)
    print("\n---------\n")
    lst = [[None, None] for i in range(11)]
    recur(10,10,lst)
    print("after: ",lst, end='\t\t')
    print("\n---------\n")
    print("test: ",fast2130(start))
