'''
this one seems genuinely tricky
get the minimum number of sub sequence partition needed

observations:
    -> for arr size n, n subsequences always work
    -> starting point of each subsequence implies an upper-lower bound of plusminus k
    ->ah, order does not matter!
        -> each element generates there own upper-lower bound, check overlapping bounds!
        -> could this be a dp problem with overlapping spans?
            -> ah! we also do not need actual sequencing
            -> whenever we have a need of expanding exisiting bound, ct +=1!
            ->problem: what if there is a gap? we need some kind of range map
            -> ah, we can make a compromise: sort, and that makes sure nothing
                goes into the "gap", runtime is worsen by a log(n)
'''

def q2294(arr, k):
    sorted_arr = ctSort(arr)
    upperbound = sorted_arr[0]+k    # we do not need to worry about lowerbound
    ct = 1
    for each in sorted_arr:
        if each>upperbound:
          ct += 1
          upperbound = each+k
    return ct

'''
lmao, that did it.
but what if we sacrifice memory for linear solution?
ah, solution says counting sort works. Lets do it then
'''

'''
not in-place. We produce another arr
'''
def ctSort(arr):
    prefixArr = [0 for i in range(max(arr)+1)]
    for each in arr:
        prefixArr[each] +=1
    roll = 0
    for i in range(len(prefixArr)):
        roll += prefixArr[i]
        prefixArr[i] = roll #accumulative is done thus
    resArr = [-1 for i in range(len(arr))]
    for each in arr[::-1]: #we do not have to stable sort but why not
        resArr[prefixArr[each]-1] = each
        prefixArr[each]-=1
    final = []
    for each in resArr:
        if each != -1:
            final.append(each)
    return final

'''
further update: an-wen uses a super,super blunt approach
that is basically what I thought of as the space-for-time tradeoff

->make bitmap of 10^5 + 1 zeros (0-> num of val ind pos not seen, 1-> seen)
-> find max of the arr, we do not need scanning beyond that (optimization possible: do this before prev step and have an array of max+1 len instead of 10^5 +1 len)
-> start scanning the bit map and skip k steps at a time, when we see 0, bump forward 1 place untill we see 1,
    that is when we need to add the ct and skip another k steps
    -> this step is worst case runtime len(bitmap) which is not very nice in theory but nice in practice
'''

def anWen(arr, k):
    if len(arr)==1:return 1
    mapBound = max(arr)+1
    bitmap = [0 for i in range(mapBound)]
    ct = 0
    for each in arr:
        bitmap[each] = 1
        skipper = 0
    while skipper<len(bitmap):
        if skipper>=len(bitmap):
            break
        if bitmap[skipper]==1:
            ct += 1
            skipper+=k+1
        else:   #skip by one
            while bitmap[skipper]==0 and skipper<len(bitmap):
                skipper += 1
    return ct

if __name__ == '__main__':
    arr = [3,6,1,2,5]
    k = 2
    print(q2294(arr, k))