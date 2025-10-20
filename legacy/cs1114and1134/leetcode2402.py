'''
more meeting room stuff lol
note number of rooms n is within 100 (small factor)

possible approach:
scan all rooms at each possible time point
each room should know two things:
if there is a meeting, and if so when it will end
this approach is n* time-scale runtime
ah, also, need to sort the meetings by starting time

waaaiiitt, do I even need a heap queue?

    ->  check every meeting, they can either take place right
        away, or I can locate the next available meeting toom for it

    ->  if available right away, indicate in status[i] the ending time,
        tally freq[i]+=1
    ->  otherwise, give the meeting to the next available room,
        still tally freq[i]+=1,
        but also indicate the status[i] ending time for this
        meeting should be status[i]-newMeeting start time + newMeeting end time
        (because the room has a current meeting , the delay should be added to next end time)

'''

'''
scan through the array that stores 
the number of times a room is used 
find the first max and return its ind
'''
def findRes(freqArr):
    curBest = 0
    bestPos = 0
    for i in range(len(freqArr)):
        if freqArr[i]>curBest:  #strictly greater than gives first max
            curBest = freqArr[i]
            bestPos = i
    return bestPos

'''
check all n rooms left to right to see if a meeting has ended
return the index position of already available room
if non available, return the index position of the next 
immediate available room
'''
def roomScan(roomArr, curTime):
    availability = float('inf')
    availPos = 0
    for i in range(len(roomArr)):
        if roomArr[i]<=curTime: #smaller or equal both means room available
            return i    #return the ind pos of room
        if roomArr[i]<availability: #strictly less than gives leftmost
            availability = roomArr[i]
            availPos = i
    return int(availPos)   #all occupied, return the position of next available room


'''
two arrays:
status[i] = meeting time end time in room i
    
    when each meeting is added, if current time>meeting start time,
    pad the end time accordingly    (or simply check if the meeting added comes from waiting queue)
    
    
    
freq[i] = number of meetings taken place in room i

one heap:
waiting -> stores meetings with start time within current time, 
'''
def brute(n, m):
    m = sorted(m, key=lambda x: x[0])   #again the lambda is redundant
    status = [0 for _ in range(n)] #at first all meeting ends at time 0 (no meeting happens)
    freq = [0 for _ in range(n)]    # keep track how many times each room is used

    for eachPair in m:
        availability = roomScan(status, eachPair[0])    #eachPair[0] stores meeting start time
        freq[availability] += 1 #tally we have a meeting in this room
        status[availability] = eachPair[1] +max(0, status[availability]-eachPair[0])
    return findRes(freq)

'''
update:
lol easily passed. This question is surprisingly easy
(still took me nearly an hour lol)
my runtime is bad becasue we have n*m runtime (even tho n is small so really O(m))

let's see if we can do better

roomScan can be turned into a heap process
    -> top element is always the best option
    ->we do not even need current time in heap, but need to make sure stable heap build
    (which is ok, because we can manually build heap, or simply double heapsort based
    on index position as secondary key)
'''
import heapq
def smart(n,m):
    waiting = []
    for i in range(len(m)):
        heapq.heappush(waiting, (m[i][0], m[i][1]))   #use start time as sorting key, also store its ending time

    roomHeap = []
    for i in range(n):   #pre-processing of occupying all rooms
        if not waiting: #more rooms than meetings, good!
            return 0    #each room used at most once so far, straightaway return first room ind
        heapq.heappush(roomHeap, (heapq.heappop(waiting)[1], i)) #at first, each room hosts a meeting till rooms deplete
    if not waiting: return 0    #check one more time
    freq = [1 for _ in range(n)] #each room used at least once already
    while waiting:  #as long as there is more meeting not done yet
        prevMeetingEndTime, roomInd = heapq.heappop(roomHeap)   #roomHeap will never deplete as we will heappush
        curMeetingStartTime, curMeetingEndTime = heapq.heappop(waiting) #safeguarded by the while loop control var
        heapq.heappush(roomHeap, (curMeetingEndTime +max(0, prevMeetingEndTime-curMeetingStartTime), roomInd))
        freq[roomInd] += 1
    return findRes(freq)
'''
update: the above "smart" solution is wrong
in the sense that when multiple rooms become available,
the next meeting will go to the room that became available first

which, honestly, in real life, IS a better solution:
if you have people over-timing, wrapping-up, or just cleaning the
rooms in between meetings, it is better to adapt an algorithm
that maximizes the time between a prev meeting and a next meeting
whenever possible.

BUT: the standard solution uses the fewest number of rooms
overall, if we want to minimize the occupancy of the rightmost room!

I think this would be a good twist for a CS1134 question.

below is standard solution from leetcode
'''


def mostBooked(n: int, meetings) -> int:
    counts = [0 for _ in range(n)]
    rooms= [_ for _ in range(n)]    #heap containing room ind pos only. This is the smart step
    meetings = sorted(meetings, key=lambda x: x[0]) # it is tempting to just heap extract this, but hey we need to check all meeting pairs eventually so might as well sort it
    ongoingMeetings = []    #heap containing pairs of meeting ending time and room ind pos, ranked by soonest end time

    for start, end in meetings:
        while ongoingMeetings and ongoingMeetings[0][0] <= start:   #current meeting starts after some meeting end time
            heapq.heappush(rooms, heapq.heappop(ongoingMeetings)[1])    #rooms now contain the smallest ind available room
        if rooms:   #have available room
            room = heapq.heappop(rooms) #simply remove to indicate room occupied, save the room ind information for the ongoingMeetings heap
        else:   #implied all rooms were occupied, t>start guaranteed
            t, room = heapq.heappop(ongoingMeetings)    #pop the pair that ends soonest
            end += t - start    #same formula I had

        counts[room] += 1
        heapq.heappush(ongoingMeetings, (end, room))

    return max(range(n), key=lambda x: (counts[x], -x)) #this is just lazy way of doing my findRes

'''
reflection: initialize rooms = [0,1,2,3...n-1] is very smart
because in the problem description, 0 <= start time < end time
strictly, the moment room [0] is occupied for a meeting
the best we can hope for for it to be available will be time 1,
which is at best in tie with room [1], and since 
heapq will not bubble it up when it is freshly pushed,
this smartly enforces leftmost room used first rule

my second solution was very, very close to this smart correct solution

also note how the standard solution removes the room from available rooms
heap whenever it is occupied, and just put it back
when it becomes available. I should have thought of this.

(btw, this solution is m logm logn, which is asymptotically same as my solution as n approaches a small const
but when n->m, my answer will be m squared while this answer remains good.)
'''

'''
test my own understanding
'''
def doubleHeap(n,m):
    freq = [0 for _ in range(n)]    #tally the frequency each room is used
    roomHeap = [_ for _ in range(n)]    #simply all the rooms, each elem is its ind pos
    occupiedHeap = []   #all the rooms in use by meetings, ranked by ending time and know which room is in use

    for startTime, endTime in sorted(m, key = lambda x: x[0]):
        while occupiedHeap and occupiedHeap[0][0]<= startTime:
            _, roomInd = heapq.heappop(occupiedHeap)
            heapq.heappush(roomHeap, roomInd)
        if roomHeap:    #we have available room
            roomInd = heapq.heappop(roomHeap)
            heapq.heappush(occupiedHeap, (endTime, roomInd))
        else:   #no available room right away, need to wait
            prevEndTime, roomInd = heapq.heappop(occupiedHeap)
            heapq.heappush(occupiedHeap, (prevEndTime-startTime+endTime, roomInd))
        freq[roomInd] += 1
    return findRes(freq)

if __name__ == '__main__':
    n = 4
    m = [[18,19],[3,12],[17,19],[2,13],[7,10]]

    n = 4

    m = [[19,20],[14,15],[13,14],[11,20]]


    print(brute(n,m))
    print(mostBooked(n,m))
    print(smart(n,m))
    print(doubleHeap(n,m))


