'''
the non-overlapping interval question

we should look at the intervals which are short
first before looking at longer intervals
for obvi reasons

-> sort input array by interval length
    -> not even necessarily sorting, heap approach will do

-> among the short intervals, how to determine which ones we go to?
    -> start from edge dates. the earliest day / latest day events
        will definitely contribute to a solution

what if we just simply start with edge dates?

-> whatever event has the earliest day / latest day definitely
    contributes to a solution
    -> let's say we use the earliest days.

-> what if multiple events start on such an earliest day?
    -> select the one with shortest interval. eliminate that earliest day as selection critirion,
        use next day to determine start order
        e.g events: 1-2. 1-5. 1-9, 2-6
            select 1-2, use 1. remaining events become:

            2-5, 2-9, 2-6
            select 2-5, use 2. remaining events become:

            3-9, 3-6
            select 3-6, use 3. remaining events become:

            4-9
            select 4-9, use 4. remaining events become:

            empty
            we done.
            note we potentially have a post-processing interval a-b where
            a>b, which implies the event is not attendable

next question is, how to implement the double-sort:
first sort by starting day, then sort again by ending day

intuitive approach: stable radix sort
concern: 10^5 possible days, both runtime and memory concern

'''

def q1353(arr):
    processedArr = myCtSort(myCtSort(arr,1),0)  #this is double sorted
    ct = 0
    start = 0
    # produced = []
    while len(processedArr)>0:
        for i in range(len(processedArr)):
            processedArr[i][0] = max(start+1, processedArr[i][0])
        processedArr= myCtSort(myCtSort(processedArr,1),0)
        cur = processedArr.pop(0)
        if cur[0]<=cur[1]:
            ct+=1
            # produced.append(cur)
            start = cur[0]
    return ct

'''
near-trivial memory optimization
'''
def findMax(arr):
    res = -1
    for eachPair in arr:
        if eachPair[-1]> res:
            res = eachPair[-1]
    return res

'''
given an array, use a particular
sub-element to sort
pin = 0 or 1
'''
def myCtSort(arr,pin):
    if len(arr)<=1:
        return arr
    n = findMax(arr)    # don bother checking lower bound
    ctArr = [0 for _ in range(n+1)]
    for eachPair in arr:
        ctArr[eachPair[pin]]+=1
    snowBall = 0
    for i in range(len(ctArr)):
        ctArr[i] += snowBall
        snowBall= ctArr[i]
    for i in range(len(ctArr)):
        ctArr[i] -= 1
    resArr = [None for _ in range(len(arr))]
    for eachPair in arr[::-1]:  #backward is stable
        resArr[ctArr[eachPair[pin]]]=eachPair
        ctArr[eachPair[pin]]-=1
    return resArr

'''
update: approach correct. Runtime exceeds. It is ok.
we are very close.
Instead of re-label the intervals,
treat the first element as max(start+1, first elem) when sorting
and do not apply full sorting, do heap approach

problem is we need to avoid repeated full heapify
after each extraction which seems impossible
as each extraction does potentially modify the starting 
date of all remaining events 

waaaiit! I'm dumb with the incremental date tracking!
we do not have to increment day number 1 at a time,
as long as events are attended on non-repeating days!

starting day pigeonhole approach:
start and end: earliest start and latest end (linear probe)

sort array by starting day  (easily done already)

for each day within range:
    -> scan array till starting day exceeds current day
        -> compare the ending day of each of such elem scanned,
            pick the one with earliest ending day and is 
            not attended yet to attend, label as attended
            
'''

'''
standard solution, which honestly is strange
I never seen sort and then heapify before
'''

import heapq

def maxEvents(events: list[list[int]]) -> int:
    # Step 1: Sort events by start day
    events.sort()

    # Step 2: Min-heap to track events by their end day
    min_heap = []
    eventCt = 0
    n = len(events)
    count = 0

    # Step 3: Determine the last day we need to simulate
    last_day = max(end for _, end in events)

    # Step 4: Simulate each day
    for day in range(1, last_day + 1):
        # Step 4.1: Add all events starting today to heap
        while eventCt < n and events[eventCt][0] == day:
            heapq.heappush(min_heap, events[eventCt][1])
            eventCt += 1

        # Step 4.2: Remove events that already ended
        while min_heap and min_heap[0] < day:
            heapq.heappop(min_heap) #note that when this happens, the if block below will not happen

        # Step 4.3: Attend the event that ends earliest
        if min_heap:
            heapq.heappop(min_heap)
            count += 1  #we only go to one event a day, so one iteration can only bump count by 1 max.

        # Step 5: Break early if no events remain
        if eventCt == n and not min_heap:
            break

    # Step 6: Return the number of events attended
    return count



'''
ok, I think I get it. Let's see if
we can do this from scratch
'''

def heapPop(heap):
    if len(heap)<1: raise IndexError
    if len(heap)==1: return heap.pop()
    heap[-1], heap[0] = heap[0], heap[-1]   #inplace swap with top
    res = heap.pop()
    topHeapify(heap)
    return res

def heapPush(heap, elem):
    heap.append(elem)
    if len(heap)<=1:
        return
    start = len(heap)-1
    while start>0: #equate zero gives infinite loop!
        if heap[start]<heap[start//2]:
            heap[start//2], heap[start] = heap[start], heap[start//2]
            start //= 2
        else:
            break

'''
assume entire heap ok except top element
'''
def topHeapify(arr):
    start = 0
    swap = start
    while start<len(arr):
        left = 2*start+1
        right = 2*start+2
        if left<len(arr) and arr[left]<arr[swap]:
            swap = left
        if right<len(arr) and arr[right]<arr[swap]: #do not use if-elif logic: we need to make sure the parent is always smaller than both children. Elif does not ensure that (consider parent 1, left 9, right 2)
            swap = right
        if swap != start:
            arr[swap], arr[start] = arr[start], arr[swap]
            start = swap
        else:
            break

def mySolution(arr):
    # sortedArr = sorted(arr)
    sortedArr = myCtSort(arr,0)   #sort based on starting date
    eventEndDayHeap = []
    ct = 0
    currentEventInd = 0

    lastDay = findMax(arr)

    for today in range(1, lastDay+1):
        while currentEventInd <len(arr) and today == sortedArr[currentEventInd][0]:    #assume currentEventInd does not overreach
            heapPush(eventEndDayHeap,sortedArr[currentEventInd][1])
            currentEventInd += 1   #keep track how many

        while eventEndDayHeap and eventEndDayHeap[0] < today: #the top event ended before today
            heapPop(eventEndDayHeap)    #and if this happens it will empty out the heap

        if len(eventEndDayHeap)>0:  #this is only possible if current event end day is not before today
            ct+=1                   # and the while loop above must have not happened at all
            heapPop(eventEndDayHeap)

        # if currentEventInd >=len(arr):   #ensure currentEventInd does not overreach
        #     break
    return ct


if __name__ == '__main__':
    arr = [[27,27],[8,10],[9,11],[20,21],[25,29],[17,20],[12,12],[12,12],[10,14],[7,7],[6,10],[7,7],[4,8],[30,31],[23,25],[4,6],[17,17],[13,14],[6,9],[13,14]]
    # arr = [[6, 10], [6, 9], [6, 8], [6, 7]]
    # arr = [[1, 2], [1, 2], [1, 2]]
    print(mySolution(arr))

    print(maxEvents(arr))
    # print(q1353_fixed(arr))
    # print(q1353_heap(arr))
    lst = [1,3,5,2,4,0]
    heap = []
    for i in range(len(lst)):
        heapPush(heap, lst[i])
    print(heap)

    for i in range(len(lst)):
        print(heapPop(heap), end = '\t')