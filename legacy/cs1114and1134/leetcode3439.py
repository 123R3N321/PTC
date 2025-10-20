'''
this I think I can figure out

can we incrementally solve the puzzle when k increases from 1 to n?
 -> k = n,    implies all free times in bewtween meetings and in event not in meeting
            is good (essentially event time - total mtting duration)
-> k = n-1  ONE meeting cannot be shuffled... I donno how to pick this one meeting

    ...

-> k = 1    ONE meeting IS shuffled, note every meeting can be shuffled left or right
            before we consider meeting back-to-back or at edge of event duration


what we know for certain: when k>1, we definitely want to move meetings in consec manner
that is to say, all the meetings being moved that result in best answer, are
meetings one after the other, never skipping a meeting in middle

That also further implies: are we shoving them to one side, or do a "pivot" and
split the meetings from a center point? the former seems a better coding option
while the latter seems a bit more human-intuitive

wait, isn't this essentially a sub-sequence problem that requires consecutive selection?
I do not need to care HOW I move them, but only know that given k movable events I can
potentially deal with k+1 gaps in between them and just select the best sum!

example 1 re-phrased:
    when k = 1, we can pick consec seq of length 2
    the overall sequence is 1, 1, 0, we pick 1,1 and get answer 2

example 2 re-phrased:
    k = 1, overall sequence 0,1,5,0, pick 1,5 and answer is 6

example 3 re-phrased:
    k = 2, sequence 0, 0, 0, 0, 0, pick anything we get 0,0,0 and answer 0

WE JUST NEED A SIMPLE SLIDING WINDOW
'''

'''
given total timeline, starting time arr and ending time arr, return list of gaps
'''
def genSeq(total, starts, ends):
    res = [starts[0]]   #first event start time might not be time 0, that contributes to a gap
    for i in range (1, len(starts)):
        res.append(-ends[i-1]+starts[i]) #the diff between end of i-1th event and start if ith
    res.append(total-ends[-1])
    return res

'''
sliding window find best consec sub seq of length k, return sum of that seq
'''
def slidingWindow(arr, k):
    start = sum(arr[:k])    #find the first k sums
    best = start
    for i in range(k, len(arr)):    #start with k and slide forward
        start = start-arr[i-k]+arr[i]
        best = max(start, best)
    return best

def q3439(total, k, starts, ends):
    seq = genSeq(total, starts, ends)
    return slidingWindow(seq, k+1)

'''
update: yep. Correct approach. Best performance approach is also this.
'''
if __name__ == '__main__':
    total = 21
    k = 1
    starts = [7,10,16]
    ends = [10,14,18]
    print(q3439(total, k, starts, ends))
    # print(genSeq(total, starts, ends))