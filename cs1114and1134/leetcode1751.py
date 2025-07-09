'''
sort the events based on starting day

sort events based on starting days

->we will have a multi-root search trea of uncertain number of branches at each level
    ->scan and compare current event ending time with next event starting time
        ->note whenever we find such an event update ending time to that event's ending time
        ->if this train goes on, each event is a starting node

    ->  use a starting event, scan forward for remaining events with starting time later
        than the current event ending time, that will be *one potential next event*
        ->  essentially repeating step one, scan forward and each event with overlapping
            starting time with prev event is a potential next event

    ->  keep doing this till the end of all possible events, then pick a subsequence
        of maximized sum (essentially we will have multiple arrays containing a
        long sequence of "what if we attend all events the time allows" and then
        pick from there the subsequence of length k that results in best sum, which is
        simply just sort - pick k top choices)
'''

'''
given 2d array containing multiple potential
best solutions, pick best subsequence of k elements,
return that subseq sum
'''
def bestSeq(arr, k):
    bestSum = 0 #overall sum guaranteed better than 0
    for eachSeq in arr:
        topSeq = sorted(eachSeq)
        localSum = 0
        if len(topSeq) <= k:
            localSum = sum(eachSeq)
        else:
            localSum = sum(eachSeq[-k:])
        if localSum> bestSum:
            bestSum = localSum
    return bestSum


'''
given array of all events,
generate 2D array of all possible event-attending sequences
'''
def arrayGen(events):
    sortedArr = sorted(events)  #now we know auto-sort with first nested elem. Can also counting sort
    bumper = 0
    res = []
    while bumper < len(sortedArr)-1:
        starterLst = []
        while sortedArr[bumper][-1]>=sortedArr[bumper+1][0]:
            starterLst.append([sortedArr[bumper], bumper])
            bumper += 1
        for eachStaringPoint, eachStartingInd in starterLst:
            localBumper = eachStartingInd
            while sortedArr[localBumper][-1]>=sortedArr[localBumper+1][0]:
                ...

'''
counting sort based on given nested index position
'''
def ctSort(arr, pos):
    ctArr = [0 for _ in range(findMax(arr,pos)+1)]
    for eachPair in arr:
        ctArr[eachPair[pos]] += 1

    roll = 0
    for i in range(len(ctArr)):
        ctArr[i] +=roll
        roll = ctArr[i]

    for i in range(len(ctArr)): #personal habit
        ctArr[i] -= 1

    res = [0 for _ in range(len(arr))]
    for eachPair in arr[::-1]:  #stable sort not necessary but does not hurt
        res[ctArr[eachPair[pos]]] = eachPair
        ctArr[eachPair[pos]] -= 1
    return res

def findMax(arr, pos):
    curMax = arr[0][pos]
    for eachPair in arr:
        if eachPair[pos] > curMax:
            curMax = eachPair[pos]
    return curMax



''''
standard solution. 2 dimensional dp
'''
def maxValue(events, k):
    events.sort(key=lambda x: x[1])
    n = len(events)
    dp = [[0 for __ in range(k + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        start, end, value = events[i - 1]
        prev = findLastNonOverlapping(events, i - 1, start) #binary search locate prev available event
        for j in range(1, k + 1):
            # Option 1: skip current event
            # Option 2: take current event and add to prev best
            dp[i][j] = max(dp[i - 1][j], dp[prev + 1][j - 1] + value)
    return dp[n][k] #this is the element that is the best sum with seq of k length when considering all n events

def findLastNonOverlapping(events, right, targetStart):
    left = 0
    res = -1
    while left <= right:
        mid = (left + right) // 2
        if events[mid][1] < targetStart:
            res = mid
            left = mid + 1
        else:
            right = mid - 1
    return res



'''
ok, I think I get it. 
Let's try to implement this from scratch
'''

'''
helper function to quickly locate the
index of the closest event that has ending
day earlier than current event starting day
pass in cap: current event ind pos
return ind pos

remember, this is only useful after we sort by ending time
else we might have:
    arr = [[1,1,1],[2,2,2],[3,7,3],[4,4,4],[5,5,5]]
    then:
    arr[binarySearchLeft(arr, 4)] gives [2,2,2] instead of [4,4,4]

'''
def binarySearchLeft(events, capInd):
    left = 0
    right = capInd
    res = -1    #-1 is convenient
    while left <= right:
        mid = (left + right) // 2
        if events[mid][1] < events[capInd][0]:  #indeed ends before current event starting day
            left = mid+1
            res = mid
        else:
            right = mid - 1
    return res

def q1751(events, k):
    n = len(events)
    events = sorted(events, key=lambda x: x[1]) #sort by ENDING TIME
    # create 2D dp table with:
    #top-bottom: incremental scan of all elements in events arr
    #left-right: keep track of subseq of 0,1,2,...,k length
    #dp table will contain answers to the best solutions for:
    # pick any length k of events to attend among any in the first n events
    # we can also, ofc, modify the dp content to backtrack exactly which events are attended
    # and, ofc, the dp has one dummy row one dummy column at the left-top edges, as usual
    dp= [[0 for __ in range(k + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):   #fill row by row left to right
        prevInd = binarySearchLeft(events, i-1)
        for j in range(1, k + 1):
            dp[i][j] = max(dp[i-1][j], dp[prevInd+1][j-1]+events[i-1][2])
    return dp[n][k]

def charSort(msg):
    return ''.join([chr(ord('a')+each) for each in sorted([(-ord('a')+ord(letter.lower()))for letter in msg])])

if __name__ == '__main__':
    # arr = [[11, 32, 3], [4, 25, 6], [97, 8, 99]]
    arr = [[1,1,1],[2,2,2],[3,7,3],[4,4,4],[5,5,5]]
    k = 3
    # print(arr[binarySearchLeft(arr, 4)])
    print(maxValue(arr, k))
    print(q1751(arr, k))
    print(charSort('JuanRyein')==charSort('JayEunirn')==charSort('RyanJeuni'))
    # print(ctSort(arr, 1))
    # print(ctSort(arr, 2))