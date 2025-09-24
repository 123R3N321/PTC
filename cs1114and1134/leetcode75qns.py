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


'''
question is vague: can we actually go to visited rooms?

braindead...
'''

def q841(arr):
    status = [1 for i in range(len(arr))]
    # 1 -> not visited, 0->visited. Success at sum(status)==0
    stack = []
    stack.append(arr[0])
    status[0] = 0
    while len(stack)>0:
        node = stack.pop()
        for each in node:
            if status[each]==1: #not visited yet
                stack.append(arr[each])
                status[each]=0
    return sum(status)==0

'''
ok lets do this recursively
update: recursive is slightly more fun.
'''

def recur841(arr, cur):
    if not cur:
        return
    for each in cur:
        if arr[each]:   #not visited yet
            cur = arr[each]
            arr[each] = None
            recur841(arr, cur)
        elif arr[each]==[]:
            arr[each] = None

def final841(arr):
    if len(arr)<1: return True
    recur841(arr, arr[0])
    for each in arr[1:]:
        if each is not None:
            return False
    return True


'''
unionFind and application on testing the
connectivity of graph when given
adjacency matrix
'''

'''
* recursively find the correct representative * 
for each element along a path
1. only works for monotonic mapping/array
2. returns that representative value
'''
def trace(lst, elem1):
    if lst[elem1] == elem1: #end of a path: element key leading to itself
        return elem1
    lst[elem1]= trace(lst, lst[elem1])
    return lst[elem1]   #at the end of function call, return the representative

'''
* set two elements onto the same path *
and also set the smaller one in the front
of the path correctly

note this is not complete mapping/array
processing. After calling union()
must call trace() on entire mapping/array
once and we are done.
'''
def union(lst, elem1, elem2):
    root1 = trace(lst, elem1)   #first make sure all elems long the 2 paths have correct representative
    root2 = trace(lst, elem2)
    if root1==root2:    #two paths ending at a common key
        return
    if root1<=root2:    #if-else set the correct front order for the two merging paths
        lst[root2] = root1
    else:
        lst[root1] = root2
    #after this function call, need to trace all
    #elements in the mapping/array once to merge these two paths

'''
use union find on leetcode qn 547
theoretical runtime: size(mat)
in other words n*n where n is the 
dimension of the input square matrix
(because unionfind is, per call, const runtime)
'''

def unionFind547(mat):
    repMap = [_ for _ in range(len(mat))]
    for i in range(len(mat)):   #go row by row
        rowProcessing(mat, repMap, i)   #each row we union them

        for j in range(len(mat[i])):    #a tracing scan on each row
            trace(repMap, repMap[j])
    #now we just need to see what is present in repMap
    ct = len(repMap)
    for i in range(len(repMap)):
        if repMap[i]!=i:    #element has a representative somewhere else
            ct-=1
    return ct

'''
deals with a single row in the matrix
note the row ind is also current ind pos
in repMap, which is nice
'''
def rowProcessing(mat, repMap, rowInd):
    for i in range(len(mat[rowInd])):
        if mat[rowInd][i] ==1:   #we see a connection here!
            union(repMap, repMap[i], rowInd)
    # note that we still need one more scan on
    # the entire row and trace before processing next row

'''
update:
yep totally works. Nice.
I think this is a really elegant solution
although it only beats 9.96% submissions

now, this section of the leetcode 75 is actually
on dfs in the vanilla sense.
Even though the trace() function is essentially
dfs, we are kinda overkilling it.

Let's see if we can do a minimal version
that is just dfs
'''
def vanilla547(mat):
    visited = [False for _ in range(len(mat))]
    ct = 0

    for i in range(len(mat)):
        if visited[i]==False:
            ct+=1
            visited[i] = True
            dfs(mat, visited, i)
    return ct

def dfs(mat, visited, i):
    for j in range(len(mat)):
        if mat[i][j] == 1:  #connection
            if visited[j] == False: #check if it is already visited
                visited[j] = True
                dfs(mat, visited, j)
'''
update after submission:
yeah super fast lol.
but hey we do not retain the representative info
with union find you retain the info of the 
representative of each row
'''

'''
ok Im actually not sure what is the approach
here. Since all nodes guratanteed to work
in the end, we must have:
    -> nodes connected to 0, either direction
    ->all the rest connected, either direction
in other words, if this is undirected graph
everything is already connected
why do I feel that this is bfs lol
use bfs to eliminate redundant edges 
(suppose 0 -- 1 -- 2 -- 3 -- 0, with bfs
we only have 0--1 and 0--2 and either 0--1--2 or 0--3--2)
but no. Then maybe you accidentally reverse an edge that does not need to be

the hint says do a dfs and pretend the graph is undirected. 
Huh. honestly it just sounds wrong lmao

nah who cares. Let's do adjacency matrix conversion see where this goes
'''
'''
given a list of connectivity (that is on-directional left-right)
create bidirectional adjacency matrix of 0 cost forward and 1 cost
backward. Traverse completely and total cost is answer
'''
from collections import defaultdict
def makeMat(lst):
    resMat = defaultdict(list)
    for eachPair in lst:
        resMat[eachPair[0]].append((eachPair[1], 1))
        resMat[eachPair[1]].append((eachPair[0], 0))
    return resMat

def dfsWithCost(graph, visited, start, curCost):
    visited[start] = True
    for eachPair in graph[start]:
        if visited[eachPair[0]]==False:
            visited[eachPair[0]] = True
            curCost[0]+=eachPair[1]
            dfsWithCost(graph, visited, eachPair[0], curCost)

def bfsWithCost(graph, visited, lvl, costArr):
    if len(lvl)==0:
        return
    nextlvl = []
    for eachNode in lvl:
        visited[eachNode] = True
        for eachPair in graph[eachNode]:
            if visited[eachPair[0]]==False:
                visited[eachPair[0]] = True
                nextlvl.append(eachPair[0])
                costArr[0]+= eachPair[1]
    bfsWithCost(graph, visited, nextlvl,costArr)

def q1466(n, lst):
    adjMat = makeMat(lst)
    visited = [False for _ in range(n)]
    costArr = [0]   #to fool the memory image of course
    #dfsWithCost(adjMat, visited, 0, costArr)   ##this is alternative solution.
    bfsWithCost(adjMat, visited, [0], costArr)
    return costArr[0]


'''
q 399 is like a new genre that I have not encountered before
after checking hint:
create adjacency mat, where forward gives multiplicant num
and backward is divisive num, so when we do down a path
we multiply them together
'''
def makeDivMat(adjLst, valLst):
    adjMat = defaultdict(list)  #better than literally matrix when graph is sparsely connected and big.
    for i in range(len(adjLst)):    #promised adjLst and valLst same len
        f = adjLst[i][0]    #node parent
        t = adjLst[i][1]    #node child
        adjMat[f].append((t, valLst[i]))    #append a tup containing destination and cost
        adjMat[t].append((f, 1/valLst[i]))  #promised valLst does not contain 0
    return adjMat

'''
search for the correct path going from f to t in adjMat and return the total cost
if path cannot be found we return float -1

dfs bfs no diff here. DFS is more intuitive for path cost

also note we do NOT do unmarking in visited here
because the problem is math in essence and you
CANNOT go from a variable to another variable 
AND end up with diff calculation result
(in other words, even if other paths exist, they all 
produce the same final result)

e.g. a = 2b, b = 2c, d = 3c
then: can be represented by a only in one way,
    or it can be represented by a, or b, or c, but
    they all mean the same value
'''
def seek(adjMat,visited, f, t, curCost):
    if f == t:  #we reached destination! no need further exploration
        return curCost

    visited[f] = True
    if not adjMat[f]:   #dead end!
        return float(-1)

    for dst, val in adjMat[f]:
        if visited[dst] == False:   #only explore if not visited yet
            #no need to mark visited as the top line of next recursive call handles it
            res = seek(adjMat, visited, dst, t, curCost * val)
            if res != float(-1):    #only return if target is found
                return res
    return float(-1)    #if map exhausted and no result, fail here

'''
initialize/refresh visited array after a query
'''
def refreshVisited(adjLst, visited):
    for f, t in adjLst: #super simple: mark EVERYTHING as not visited yet lol
        visited[f] = False
        visited[t] = False

def doQueries(adjLst, valLst, queries):
    adjMat = makeDivMat(adjLst, valLst)
    res = []
    visited = {}
    refreshVisited(adjLst, visited)
    for eachQuery in queries:   #each query is a list of 2 elems, from and to
        f = eachQuery[0]
        t = eachQuery[1]
        # first check if either one is not registered, we use -1 float as dummy val
        if not adjMat[f] or not adjMat[t]:
            res.append(float(-1))
            #implied continue onto next iteration
        else:   #implied both from and to are connected
            res.append(seek(adjMat, visited, f, t, float(1)))
            refreshVisited(adjLst, visited) #when we do next query we start clean
    return res

'''
q 1926 makes me think... isn't this just djkstra?
'''

'''
probing helper function,
given a player location (coord), check left/right/up/down
and exclude the direction the player comes from (coord)

need vertical and horizontal boundary info to make sure
we don't get out of the game map. (bound is dimension, which means ind exclusive)

return a list of coords to go to
'''
def probe(gameMap, loc):
    res = []
    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # up, down, left, right
    for dy, dx in directions:
        ny, nx = loc[0] + dy, loc[1] + dx
        if 0 <= ny < len(gameMap) and 0 <= nx < len(gameMap[0]):
            if gameMap[ny][nx] == '.':
                res.append([ny, nx])
    return res

def checkWin(loc, width, height):
    return loc[0] == 0 or loc[0] == height - 1 or loc[1] == 0 or loc[1] == width - 1

class Node1926:
    def __init__(self, y, x, cost):
        self.loc = [y, x]
        self.cost = cost
    def __gt__(self, other):
        return self.cost > other.cost

def q1926(gameMap, start):
    height, width = len(gameMap), len(gameMap[0])
    visited = [[False] * width for _ in range(height)]
    heap = [Node1926(start[0], start[1], 0)]

    while heap:
        node = heapPop(heap)
        y, x = node.loc

        if visited[y][x]:
            continue
        visited[y][x] = True

        if node.loc != start and checkWin(node.loc, width, height):
            return node.cost

        for ny, nx in probe(gameMap, [y, x]):
            if not visited[ny][nx]:
                heapPush(heap, Node1926(ny, nx, node.cost + 1))

    return -1


'''
and lets do heap from scratch cuz why not lol
'''

def makeHeap(lst):
    for i in range(len(lst)//2+1,-1,-1):
        heapify(lst, i)

def heapPush(heap,elem):
    heap.append(elem)
    i = len(heap)-1 #which is exactly where elem is
    while i > 0:
        parentIndex = (i-1) // 2
        if heap[parentIndex] > heap[i]:
            heap[i], heap[parentIndex] = heap[parentIndex], heap[i]
            i = parentIndex
        else:   #no need further swap-up, terminate func
            break



def heapify(heap, i):
    parentInd = i
    leftInd = 2*i + 1
    rightInd = 2*i + 2
    if leftInd < len(heap) and heap[parentInd] > heap[leftInd]:
        parentInd = leftInd
    if rightInd < len(heap) and heap[parentInd] > heap[rightInd]:
        parentInd = rightInd
    if parentInd != i:  #a change chappened
        heap[i], heap[parentInd] = heap[parentInd], heap[i]
        heapify(heap, parentInd)

def heapPop(heap):
    heap[-1], heap[0] = heap[0], heap[-1]
    res = heap.pop()
    heapify(heap, 0)
    return res

'''
update:
the solution I have is pretty slow lol
go read the standard solutions!
'''

'''
sort, then sliding window

super simple but remember sliding the forward first 
is better here
'''
def daily(lst):
    lst.sort()
    ct = 0
    start = 0
    for i in range(len(lst)):
        if lst[i] - lst[start] ==1:
            ct = max(ct, i - start+1)
        while lst[i] - lst[start] >1:
            start += 1
    return ct

'''
there is prolly some
smart const runtime mathematical solution? especially since m, n values within 10

easy case: 
    no rotting, return -1, runtime linear

kinda funky case: 
    rotting, but "contained", AND
    there is clean oranges elsewhere

and majority case:
    blunt solution: bfs simulation (linear runtime)
    mathematical solution:
        could I do union find? And keep track how many steps are needed? That will optimal linear

observations:
    
    we could apply manhattan distance: diagonal cell takes two steps to reach
    
    a problem is that we potentially have multi-root: could start a connected graph from
    multiple rotten oranges
    
    blunt-force simulation? 
        -> optimzation: keep count of total good oranges so we do not have to scan 
            entire mat after each iteration
        
        -> termination: either count of remaining goes to 0, OR:
            there is no new state change (rotten orange increase) for an iteration
        
        the above two steps take care of the funky case. Good
                        

'''
def q994(mat):
    remaining = 0
    start = []
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == 1:
                remaining += 1  #count how mny good oranges
            elif mat[i][j] == 2:
                start.append((i,j)) #locate first starting point
    if remaining == 0: return 0
    ct = 0
    while len(start)>0: #when we see no further increase, stop code
        start, diminish = squarePropagation(mat, start)
        remaining -= diminish
        ct += 1
        if remaining == 0:
            return ct
    return -1


'''
given a list of starting points, propagate values 2,return a list of index position pairs for next frontier
'''
def squarePropagation(arr, lst):
    nextLst = []
    diminish = 0
    m = len(arr)
    n = len(arr[0])
    for x, y in lst:
        if x-1>=0 and arr[x-1][y]==1:   #down
            arr[x-1][y] = 2
            nextLst.append((x-1, y))
            diminish+=1
        if x+1<m and arr[x+1][y]==1:    #up
            arr[x+1][y] = 2
            nextLst.append((x+1, y))
            diminish += 1
        if y-1>=0 and arr[x][y-1]==1:   #left
            arr[x][y-1] = 2
            nextLst.append((x, y-1))
            diminish += 1
        if y+1<n and arr[x][y+1]==1:    #right
            arr[x][y+1] = 2
            nextLst.append((x, y+1))
            diminish += 1
    return nextLst,diminish  #the list containing the next frontier, and keep track decrease of the oranges

'''
chatgpt produces a more...academically BFS code based on my implementation
note the use of double while loop to separate queue stages. I think it is good syntax
'''
from collections import deque

def q994ChatGPT(grid):
    rows, cols = len(grid), len(grid[0])
    fresh = 0
    queue = deque()

    # Initialize the queue with all rotten oranges and count fresh ones
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1

    if fresh == 0:
        return 0

    minutes = 0
    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # up, down, left, right

    while queue:
        next_queue = deque()
        while queue:    #double while loop allows next_que -> queue swap that separates levels.
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    next_queue.append((nr, nc))
        if next_queue:
            minutes += 1
            queue = next_queue
        else:
            break

    return minutes if fresh == 0 else -1

'''
q215 seems a heap problem, I can do it in lineaer time 
(bruh and when k is large this is basically nlogn, not to mention nlogn isn't much worse than n anyways)
'''

def revheapPush(heap, elem):
    heap.append(elem)
    start = len(heap)-1
    while start>0:
        if heap[(start-1)//2] < heap[start]:
            heap[(start-1)//2], heap[start] = heap[start], heap[(start-1)//2]
            start = (start-1)//2
        else:
            break

def revheapPop(heap):
    if len(heap)==0: raise IndexError
    if len(heap)==1: return heap.pop()
    heap[0], heap[-1] = heap[-1], heap[0]
    res = heap.pop()
    revOrganize(heap, 0)
    return res

def revOrganize(heap, start):
    while start<len(heap):
        pin = start
        left = 2 * start + 1
        right = 2 * start + 2
        if left < len(heap) and heap[pin] < heap[left]:
            pin = left
        if right < len(heap) and heap[pin] < heap[right]:
            pin = right
        if pin != start:
            heap[pin], heap[start] = heap[start], heap[pin]
            start = pin
        else:   #instead of recursive call, simple while loop
            break
def q215(arr,k):
    heap = []
    for each in arr:
        revheapPush(heap, each)
    res = None
    for i in range(k):
        res = revheapPop(heap)
    return res

'''
I figured out.

Create a tagged array that contains 
pairs of elem-elem ind pos for array B,
sort it based on elem values

start scanning this tagged array from biggest to smallest,
and add the ind pos corres elems from array A into a heap,
keep track of current sum from A.
when we reach the k-th biggest,
we could compute the first candidate answer: 
k-th elem in tagged array multiply by the cumulative sum from A so far

and the important step is from here onwards:
when you keep going down from k-th biggest in tagged arr,
each step automatically means you are decreasing that multiplicant 
and we do sliding window comparison for the additional element coming
from A: check it against top of heap, if smaller or equal, do nothing
if bigger, the cumulative sume -= that top elem += current elem, heap
pop the old top elem and heappush our newly added elem

at any moment in time the heap has only k elems, as k -> n,
algo has nlogn runtime (already so when we sorted tagged array from B)
'''

def tagArrGen(arr):
    res = []
    for i in range(len(arr)):
        res.append((arr[i], i)) #elem val -- ind pos
    return sorted(res, reverse = True)

def heapPush(heap, elem):
    heap.append(elem)
    if len(heap)==1: return
    start = len(heap)-1
    while start>0:
        prev = (start-1)//2
        if heap[prev] <= heap[start]:
            break
        heap[prev], heap[start] = heap[start], heap[prev]
        start = prev

def heapPop(heap):
    if len(heap)==0: raise Exception("Empty heap!")
    if len(heap)==1: return heap.pop()
    heap[0], heap[-1] = heap[-1], heap[0]
    res = heap.pop()
    start = 0
    while start<len(heap):
        pin = start
        left = 2 * start + 1
        right = 2 * start + 2
        if left < len(heap) and heap[left] < heap[pin]:
            pin = left
        if right < len(heap) and heap[right] < heap[pin]:
            pin = right
        if pin==start: break
        heap[pin], heap[start] = heap[start], heap[pin]
        start = pin
    return res

def q2542(A,B,k):
    taggArr = tagArrGen(B)  #rev sorted. Contains elem-ind pairs
    heap = []
    curSum = 0
    for i in range(k):
        curSum += A[taggArr[i][1]]  #keep track the cumulative sum of A elems in heap
        heapPush(heap, A[taggArr[i][1]])    #put A elem in heap
    curBest = taggArr[k-1][0] * curSum
    for j in range(k, len(taggArr)):    #scan from kth onwards till depleted
        if A[taggArr[j][1]]>heap[0]:    #compare with smallest elem in heap, if so, modify heap
            curSum -= heap[0]
            heapPop(heap)
            heapPush(heap, A[taggArr[j][1]])
            curSum += A[taggArr[j][1]]
            # print(f"local operation: res: {taggArr[j][0] * curSum} from min: {taggArr[j][0]} times cur sum: {curSum}")
            curBest = max(curBest, taggArr[j][0] * curSum)
    return curBest
'''
update after checking standard solution: yep same approach
maybe re-write one more time with fast, python syntax using libs?
'''
import heapq
def minimal2542(B, A, k):
    #again the lambda expression is not necessary as default comparable is element at ind 0
    tagArr = sorted(list(zip(A,B)), reverse = True, key = lambda x:x[0])
    heap = []
    curSum = 0
    res = 0
    for eachPair in tagArr:
        heapq.heappush(heap, eachPair[1])
        curSum += eachPair[1]
        if len(heap)>k:
            curSum -= heapq.heappop(heap)
        if len(heap)==k:
            res = max(res, curSum * eachPair[0])
    return res

'''
q2462 is truly very poorly worded
Reading the discussion section helped a lot
It is a good lesson that sometimes don't
kill yourself over arcane leetcode descriptions!

first thoughts:
    -> two cases: 
        ->  easy case: the "candidate" selection combined with
            k total extraction provides full coverage of the 
            input arr. In other words all elements in arr
            will be checked, and the problem is simply
            looking for the sum of k smallest elements
        
        ->  funky case: we do not penetrate the entire 
            input arr. Some of the elements remain opaque
            to us. In that case simply heapify the
            elements visible to us and then select the best
            k elements
            
            ->  this leaves only one question: determining 
                exactly how much we can penetrate, and
                since penetration level only goes up
                one at a time, we do not have throttle 
                problem. Once we can determin the amount 
                reached, simply heapify all reached elements
                and we can get result
                ->  my answer: 2 * candidates + k-1 gives coverage
                
                ->  but in the case we DO NOT have full-penetration,
                    how to determine which elements will be accounted for?
                    ->  we cannot. Depending on where we get each previous 
                        selection, the next candidate and therefore 
                        selection can come from either end side of the
                        un-penetrated section of the input array. 
'''
def q2462(arr, k, c):
    res = 0
    if len(arr)<= 2*c+k-1:  #full coverage
        fullHeap = []
        for each in arr:
            heapq.heappush(fullHeap, each)
        for i in range(k):
            res += heapq.heappop(fullHeap)
        return res
    else:   #we cannot see everything in the arr
            #guaranteed no overlapping cursor -> no overreaching problem
        left = c-1
        right = -c  #use python's support of neg ind
        leftHeap = []
        rightHeap = []
        for i in range(left+1):
            heapq.heappush(leftHeap, arr[i])
        for j in range(-1, right-1,-1):  #go backward doesn't hurt
            heapq.heappush(rightHeap, arr[j])
        while k>0:
            k-=1
            if leftHeap and rightHeap:
                if leftHeap[0] <= rightHeap[0]:
                    res+= heapq.heappop(leftHeap)
                    left+=1 #guaranteed won't overreach
                    heapq.heappush(leftHeap, arr[left])
                else:   #take from right heap
                    res+= heapq.heappop(rightHeap)
                    right-=1
                    heapq.heappush(rightHeap, arr[right])
            else:
                if leftHeap:
                    res+= heapq.heappop(leftHeap)
                    left+=1
                    heapq.heappush(leftHeap, arr[left])
                else:   #implied only right heap is non-empty
                    res+= heapq.heappop(rightHeap)
                    right-=1
                    heapq.heappush(rightHeap, arr[right])
        return res
'''
trivial imporvement of code based on standard solution:

            st = heap_st[0] if heap_st else 1000000
            en = heap_en[0] if heap_en else 1000000

            if st <= en:
                ans += heappop(heap_st)
            else:
                ans += heappop(heap_en)

gist: use dummy value instead of actually checking one heap depletion
situation
'''
'''
another update: absolutely trolling behavior:

__import__("atexit").register(lambda: open("display_runtime.txt", "w").write("0"))

this makes your solution beat 100%. Does this count as injection attack?
'''
def recur(node, mul):
    if not node:
        return 0, -1
    if 1==node.val:
        return 2**recur(node.next)[1]+recur(node.next)[0], recur(node.next)[1]+1
    else:
        return recur(node.next)[0], recur(node.next)[1]+1

# def dailyOR(arr):
#     ...
'''
q 2300
forward sort spells
backward sort potions

also binary search?
'''

def q2300(spells, potions, threshold):
    # spells = sorted(spells) #forward scan
    potions = sorted(potions, reverse=True) #backward allows greedy approach

    res = [0 for i in range(len(spells))]   #instead of repeated append, do in-place tally
    for i in range(len(spells)):
        seed = spells[i]
        res[i] = binaryTally(seed,potions, threshold)
    return res
'''
helper func that will perform binary search and return tally
'''
def binaryTally(seed, potions, threshold):  #note potions are rev sorted here
    l = 0
    r = len(potions)-1
    res = 0
    while l<=r:
        mid = (l+r)//2
        local = potions[mid] * seed
        if local<threshold: #when we have a local result below threshold
            r = mid-1
        else:
            res+= mid-l+1
            l = mid+1
    return res

'''
same approach but way, way, way cleaner code and arguably smart

class Solution:
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        potions.sort()
        m = len(potions)
        res = []

        for spell in spells:
            required = ceil(success / spell)
            idx = bisect_left(potions, required)
            res.append(m - idx)
        return res
'''

'''
single-side scan approach, which is not very convoluted:
check the middle:
    -> if it is bigger than left and right, good
    else:   (at least left bigger or equal or right bigger or equal)
        -> if right is bigger or equal, go right look for middle repeat
        else:   (has to be left bigger or equal)
            ->  go left
'''
def q162(arr):
    if len(arr)<=1:
        return 0
    mid = (len(arr)-1)//2   #mid ind
    if arr[mid] > arr[mid+1] and arr[mid] > arr[mid-1]: #exactly good
        return mid
    l = 0
    r = len(arr)-1
    while l<=r:
        mid = (l+r)//2
        if arr[mid] > arr[mid + 1] and arr[mid] > arr[mid - 1]:  # exactly good
            return mid
        else:   #either left>= mid, or right >=mid
            if arr[mid]<=arr[mid+1]:
                l = mid + 1
            else:   #go left
                r = mid - 1
    return l

#super simple impelementation of heap for algoII hmk
def heapify(arr):
    bumper = len(arr)//2 - 1
    while bumper > 0:
        localBumper = bumper
        while True:
            left = 2*bumper+1
            right = 2*bumper+2
            smallest = localBumper
            if left < len(arr) and arr[left] < arr[smallest]:
                smallest = left
            if right < len(arr) and arr[right] < arr[smallest]:
                smallest = right

            if smallest == localBumper:
                break #nothing to do

            arr[smallest], arr[localBumper] = arr[localBumper], arr[smallest]
        bumper -= 1

class D:
    def __init__(self, name = "string", age = 0):
        self.name = name
        self.age = age
    def __str__(self):
        return self.name + "\t lol"
    def __iadd__(self, other):

        return self

def recur(num_str, place):
	if not num_str: #""
		return 0
	return (2**place)*int(num_str[-1])+recur(num_str[:-1],place+1)

def binary(num_str):
    return recur(num_str, 0)

# test code
if __name__ == '__main__':
    # seed = 2
    # potions = [_ for _ in range(19,0,-1)]
    # threshold = 11
    # # print(binaryTally(seed, potions, threshold))
    # spells = [15,8,19]
    # potions = [38,36,23]
    # success = 328
    # print(q2300(spells, potions, success))
    # arr = [31,25,72,79,74,65,84,91,18,59,27,9,81,33,17,58]
    # k = 11
    # c = 2
    # # print(q2462(arr, k, c))
    # # for i in range(0,-3,-1):
    # #     print(i, end = " ")
    # print(3|5)
    # arr = [3,7,15,4,25,1,20,8]
    # heapify(arr)
    # print(arr)
    # aD=  D(1)
    # anotherD = D(2)
    # # print(type(aD.name))
    # aD+= anotherD
    # print(aD.name)
    # print("------------------")


    # return self. decimal() < other.decimal()