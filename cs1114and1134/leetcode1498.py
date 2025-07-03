'''
today's daily is more a lesson to me than anything else

observe example 3: in an arr of 6 length, totoal
amount of subarr is (2**6) - 1

thus all we need to do is:

sort, find the "critical point" when the
sub arr beyond definitely is bad
then total amount of subarr - amount of
sub arr that will break the condition
also each individual elem k such that 2k>limit
contributes to the diminish of 1
which is equiv to overlapping double pointer
the diminish starting point:
case 1: if only one elem -> 1 -> 2**n -1 (absorb into case 3)
case 2: if more than 1, but lower bound not inclusive -> diminish by 2**n - 1 - 1
case 3: more than 1, lower bound inclusive -> 2**n -1
'''

def countWays(arr,bound):
    if len(arr)==1:
        if 2*arr[0]>bound:
            return 0
        return 1
    arr = sorted(arr)
    clip = len(arr)-1
    while arr[0]+arr[clip]>bound:
        clip-=1
    #abandon everything above the clip
    stopper = 0
    setflag = False
    for i in range(clip+1):
        if arr[i]+arr[clip]>bound:
            stopper = i
            setflag = True
            break

    if not setflag:
        return ( (2**(clip+1))-1)%(10**9 + 7)

    if 2*arr[stopper]>bound:    #case 3
        return ( (2**(clip+1))-1 - (2**(clip-stopper+1)-1) )%(10**9 + 7)
    else:
        return ( (2**(clip+1))-1 - (2**(clip-stopper+1)-1-1) )%(10**9 + 7)

'''
ok above solution wrong. Standard solution, trimmed down for readability
'''

class Solution:
    def numSubseq(self, nums, target):
        nums.sort()

        subseqCtArr = [2**i for i in range(len(nums))] #number of seubseq with input size n is (2**n)-1 (if not counting empty)

        left = 0
        right = len(nums)-1

        result = 0

        while left <= right:
            if nums[left] + nums[right] <= target:
                result += subseqCtArr[right - left]
                left += 1   #this is bumping the starting point of a subsequence forward

            #
            # we are counting the number of subsequences formed in such a way:
            # 1. it starts with the current minimal element, nums[left]
            # 2. it contains any number of any element up to and including nums[right]
            #
            # e.g suppose nums = [1,2,3,4]
            # we first account for all subsequences that starts with 1 and contains anything out of 2,3,4, to any length
            # then bump forward, repeat with 2 as starting point
            # ...
            # until we reach 4.


            else:
                right -= 1

        return result

if __name__ == '__main__':
    arr = [7,10,7,5,6,7,3,4,9,6]
    bound = 9
    print(countWays(arr, bound))