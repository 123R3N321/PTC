'''
this is very interesting and a very
important lesson:
the corect approach does not check
any specific pairing of elements
that forms the answer,
but rather probes for the existence
of a solution and look for
the tightest bound for that to
happen--when it does, the bound itself
is the answer.

also, remember your Algo exam1,
it was quite the precursor of this problem:

    given a sorted arr, find kth smallest element and return its ind pos:

    answer: look at mid and if len(arr[left:mid])>=k
    if so, we search on left:mid because we do not need anything on the mid:right
    else,  search on mid:right and k-=(len(arr[left:mid])) because the left side is too small

'''
def givenSolution(nums, p):
    if p == 0:
        return 0
    nums.sort()
    n, left, right = len(nums), 0, nums[-1] - nums[0]
    while left < right:
        mid, pairs = left + (right - left) // 2, 0
        i = 1
        while i < n:    #scan entire array
            if nums[i] - nums[i-1] <= mid:
                pairs += 1
                i += 1
            i += 1
        if pairs >= p:
            right = mid
        else:
            left = mid + 1  #note we do NOT reset pairs count
    return left



if __name__ == '__main__':
    arr = [3,0,5,0,0,1,6]
    rank = 3
    print(givenSolution(arr, rank))