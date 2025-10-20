'''
more meeting scheduling questions

it is still good to create a list containing all the gaps
the goal is to merge only 2 gaps to create max best result
the catch is we now could entirely move one meeting to any gap
that implies:
    ->  we need to keep track of the meeting duration
        and determine if it could fit in a gap somewhere
    ->  also note that now the amount of consecutive free
        time we can create is gap A + gap B + meeting duration
        of the removed meeting

possible approach: create an array to track both meetings and
gaps, in original order. Look for max subsequence of length 3
that has to begin with a gap (we do not want meeting-gap-meeting)
OR simply pad the array with a gap to begin with and just look 3
at a time with 1 overlap (elem 0, 1, 2, then 2, 3, 4, so on.)

HOW WOULD I SOLVE IT AS A HUMAN?

    ->  Rank all the trios only if the middle can be moved and only know the best double
    ->  this WILL give a solution
'''

def maxheapPush(heap, elem):
    heap.append(elem)
    start = len(heap)-1
    while start>0:
        prev = (start-1)//2
        if heap[prev]>=heap[start]:
            break
        else:
            heap[start], heap[prev] = heap[prev], heap[start]
            start = prev

def maxheapPop(heap):
    if len(heap)==0: raise Exception('heap empty')
    if len(heap)==1: return heap.pop()

    heap[0], heap[-1] = heap[-1], heap[0]
    res = heap.pop()

    start = 0
    while start<len(heap):
        pin = start
        left = 2* start +1
        right = 2* start +2
        if left<len(heap) and heap[left]>=heap[pin]:
            pin = left
        if right<len(heap) and heap[right]>=heap[pin]:
            pin = right
        if pin==start:
            break
        else:
            heap[pin], heap[start] = heap[start], heap[pin]
            start = pin
    return res

def gapArrGen(total, starts, ends):
    res = [starts[0]]
    for i in range(1,len(starts)):
        res.append(starts[i]-ends[i-1])
    res.append(total - ends[-1])
    return res

def slidingWindowFindDouble(gapArr):
    res = gapArr[0] + gapArr[1] # gapArr has at least 2 elems as long as a meeting exists at all
    for i in range(2, len(gapArr)):
        local = gapArr[i-1] + gapArr[i]
        if local>res:
            res = local
    return res

'''
given one meeting duration and its index, check if it
could be moved elsewhere that is a gap NOT adjacent to the
meeting itself

need a structure of rev sorted gap length together with its
original ind pos info preserved

we only need linear probing in this arr:
check ind 0 elem in arr compare with meeting duration
if meeting duration> it -> exit. Cannot move
if ind>=len -> exit. Canoot move
if meeting duration <= it BUT ind pos of gap == meeting ind plusminus 1 -> bump ind by 1, repeat from first step
if meeting duration <= it AND ind pos of gap != meeting ind plusminus 1 -> exit. Yes we CAN move the meeting.
'''
def movabilityCheck(meetingDuration, meetingInd, taggedGapRank):

    for eachGap, gapInd in taggedGapRank:
        if meetingDuration>eachGap: return False
        if gapInd-meetingInd==1 or gapInd-meetingInd==0: continue   #skip current gap check next gap
        return True # meeting duration < gap, and meeting not sandwiched by this gap on either side, we good

def solution(totalTime, starts, ends):
    gapArr = gapArrGen(totalTime, starts, ends) #we know all the gaps

    taggedGapRank = []
    for i in range(len(gapArr)):
        taggedGapRank.append((gapArr[i], i))  #tag the ind pos
                                                # meeting 0 is adjacent to gap 0 and 1, so on.
    taggedGapRank = sorted(taggedGapRank, key=lambda x: x[0], reverse=True)   #key not necessary but good to have

    heap = []
    for i in range(len(starts)):    #guaranteed synched ind moving with ends
        if movabilityCheck(ends[i]-starts[i], i, taggedGapRank):
            maxheapPush(heap, ends[i]-starts[i]+gapArr[i]+gapArr[i+1]) #gapArr guaranteed len bigger by 1
    double = slidingWindowFindDouble(gapArr) #in hind sight could simply be the last two elements[0] sum for taggedGapRank
    return max(double, heap[0]) if heap else double

'''
update after checking the standard solution:

instead of sorting all the gaps and compare one by one
we sliding window keep track what is the 
biggest gap before the current gap-meeting-gap trio and
after the current gap-meeting-gap trio,
which essentially is constant runtime each time we do update
runtime will reduce by a factor of logn
'''

def fasterSolution(totalTime, starts, ends):
    gapArr = gapArrGen(totalTime, starts, ends)
    curBest = slidingWindowFindDouble(gapArr)

    leftSlots = leftSlotsGen(gapArr)
    rightSlots = rightSlotsGen(gapArr)

    for i in range(len(starts)):
        if leftSlots[i]>=ends[i]-starts[i] or rightSlots[i+1]>=ends[i]-starts[i]: #check if we could fit this into leftside or right
            curBest = max(curBest, ends[i]-starts[i]+gapArr[i]+gapArr[i+1])
    return curBest

'''
generate an array that at i-th position indicate best slot size up until i-1-th position inclusive
'''
def leftSlotsGen(gapArr):
    res = [0]   #at ind 0, best slot to left has size 0 (no slot)
    curBest = 0
    for i in range(1,len(gapArr)):
        if gapArr[i-1]>curBest:
            curBest = gapArr[i-1]
        res.append(curBest)
    return res

'''
same thing, generate all the best slots to the right
'''
def rightSlotsGen(gapArr):
    res = [0]
    curBest = 0
    for i in range(len(gapArr)-2,-1,-1):
        if gapArr[i+1]>curBest:
            curBest = gapArr[i+1]
        res.append(curBest)
    res.reverse()
    return res

if __name__ == '__main__':
    total = 37
    starts = [5,14,27,34]
    ends = [13,18,31,37]
    # print(solution(total, starts, ends))
    lst = [3,2,5,4,6,1,2,3,9]
    print(leftSlotsGen(gapArrGen(total, starts, ends)))
    print(rightSlotsGen(gapArrGen(total, starts, ends)))