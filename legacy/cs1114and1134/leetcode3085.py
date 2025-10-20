'''
brute force approach
count letters into array of at most 26 places
sort it and use each element as anchor

dictate that, from the biggest to smallest elem
    ->each element smaller than this element-k is just removed  (elements on left)
    ->each element bigger than this element reduced to this element (elements on right)

next question is, is this universal set?
    ->could we have the situation that:
        each element on left does not need to be removed
        yet we shave off elements on the right for no reason

            -> ah, further improvement: use k as sliding window
                -> if at any anchor l

'''

def morph(msg):
    ctArr = [0 for i in range(26)]
    for each in msg:
        ctArr[charInd(each)]+=1
    return sorted([each for each in ctArr if each!=0])

def sliding(msg, k):
    tally = morph(msg)
    ctArr = []  # we don have to save space here, again 26 entries max
    drop = 0    #the elements on the left to be dropped
    for i in range(len(tally)):
        ct = 0  #how much in total to be removed
        for j in range(i+1,len(tally)):   #scan from ith position onward, we do not need to check i-th itself
            if tally[j]>tally[i]+k: #too big
                ct+=tally[j]-tally[i]-k #shave off, and account for it
        ct+=drop    #the element before us is being dropped
        drop+=tally[i]  #next iteration, cur element will be dropped
        ctArr.append(ct)
    return min(ctArr)

def charInd(char):
    return ord(char) - ord('a')

'''
ok above approach works, but is slow
let's see if we can do better
    ->one func
    ->do not sort, just use smaller-bigger logic
    ->no res arr, runtime compare
    ->no if logic for too big shave off, use max(0, shave_off_val)
'''

def trivial(msg, k):
    ctArr = [0 for i in range(26)]
    for each in msg:
        ctArr[ord(each)-ord('a')]+=1
    ct = float('inf')
    for anchor in ctArr:
        localCt = 0
        for each in ctArr:
            if each<anchor:
                localCt+=each #too small just drop
            else:
                localCt+=max(0,each-anchor-k)
        if localCt<ct:
            ct=localCt
    return ct

'''
update: lol standard solution is not better.
'''

if __name__ == '__main__':
    msg = "dabdcbdcdcd"
    print(sliding(msg,2))