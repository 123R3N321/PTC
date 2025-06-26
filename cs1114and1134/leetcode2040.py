'''
I like this puzzle. Very straightforward description
brute force: max(M*N, (M+N)log(M+N)) runtime by generating
all products and sort them,
completely disregard the fact that the two input arrays are
already sorted

linear probing solution:
    let the two inputs be m and n
    ->m[0] * n[0] guaranteed to be smallest
    ->m[0] * n[1] or m[1] * n[0] to be second smallest

ah, set two pointers and just crawl. I think it is straightforward

wait wait wait but my logic is getting jumbled up
suppose one array reaches the end and the other array has not,
suppose:
    m0n-1 <= m1nx where 1<=x<(len(n)-1)
    then we have two conclusions:
    1. we do not need comparison for immediate next, which has to be m1nx
    2. for the next-next, the comparison has to be:
        m2nx -- m1n(x+1)

summarized rules:
we actually will have 4 iterators, A, B, C, D
at any moment in time, either A==C OR B==D strictly
each time we make comparison between mAnB and mCnD:
    Case1 :-> if A==C AND B==D (the starting case and right after the wrap-around case):
        ->after we get current result, A++m and D++
        (which is equiv to B++ and C++, doesn't make a difference)
    Case 2: -> else: (now we have exclusive or, only A==C, or otherwise B==D)
        if A reaches len(m) (which is to say C has the same problem):
            ->reset A, C to 0, no change to B, D (trigger Case1 in next iteration)
        elif B reaches len(n) (which is to say D has the same problem):
            -> reset B, D to 0, no change to A, C (trigger Case 1 in next iteration))
        else:   #implied we are good
            if mAnB <= mCnD:


'''
import heapq


def q2040(m, n, k):
    if k == 1: return m[0] * n[0]
    heap = []
    visited = set()
    visited.add(cantor(0, 0))  # customize hash m*n + m + n
    start = [0, 0]
    res = m[0] * n[0]
    heapq.heappush(heap, (res, start))  # use start[0] for comparison, store entire start
    while k > 0:
        res, cur = heapq.heappop(heap)
        k -= 1
        if cur[0] + 1 < len(m) and cantor(cur[0] + 1, cur[1]) not in visited:
            visited.add(cantor(cur[0] + 1, cur[1]))
            heapq.heappush(heap, (m[cur[0] + 1] * n[cur[1]], [cur[0] + 1, cur[1]]))
        if cur[1] + 1 < len(n) and cantor(cur[0], cur[1] + 1) not in visited:
            visited.add(cantor(cur[0], cur[1] + 1))
            heapq.heappush(heap, (m[cur[0]] * n[cur[1] + 1], [cur[0], cur[1] + 1]))

    return res


'''
cantor only works for non neg
'''


def cantor(i, j):
    return (i + j) * (i + j + 1) // 2 + j


'''
just for the sake of practicing
'''


def heapify(lst):
    start = len(lst) // 2
    for i in range(start, -1, -1):
        siftDown(lst, i)


def siftDown(lst, start):
    left = 2 * start + 1
    right = 2 * start + 2
    parent = start
    if left < len(lst) and lst[left] < lst[start]:
        parent = left
    if right < len(lst) and lst[right] < lst[start]:  # triangle swap
        parent = right

    if parent != start:
        lst[start], lst[parent] = lst[parent], lst[start]
        siftDown(lst, start)  # looks very, very like inifite recursion at a glance


'''
update after checking discussion and chatgpt:
this is a weird question that uses binary search
based on value instead of index position
starting from some number, binary narrow down the range
and each time compute how many possible products are
below the rank. Repeatedly narrow down by half.
'''

'''
suppose we can always find the number of elements that is possible below a certain value
'''


def correct2040(m, n, k):
    # the most extreme values could only be possibly produced at the ends of two arrays
    lower = min(m[0] * n[0], m[-1] * n[-1], m[0] * n[-1], m[-1] * n[0])
    upper = max(m[0] * n[0], m[-1] * n[-1], m[0] * n[-1], m[-1] * n[0])
    while lower < upper:  # we stop when a call to hlper() gives us exactly k numbers
        mid = (lower + upper) // 2
        if helper(m, n, mid) < k:  # there are fewer than k elements below mid, mid must go higher
            lower = mid + 1
        else:  # implied too many
            upper = mid
    return lower


'''
we know both m and n are sorted,
there are three possible cases when
we look at an individual element in m and look across n:
    m<0: 
        as elements in n increases, prod decreses (scan right to left in n)
    m>0:
        as element in n increases, prod increases (scan left to right in n)
    m==0:
        always 0, since we look for number of elements < value
'''


def helper(m, n, value):
    ct = 0
    for eachElemInM in m:
        if eachElemInM > 0:
            ct += binarySearch(eachElemInM, n,  value)
        elif eachElemInM < 0:
            ct += binarySearch(eachElemInM, n, value, True)
        else:  # implied 0
            if value >= 0:
                ct += len(n)
            # implied when value<=0 do not increase ct
    return ct


def binarySearch(elemInM, n, value, reversed=False):
    lo = 0
    hi = len(n)
    if reversed:
        while lo < hi:
            mid = (lo + hi) // 2
            if elemInM * n[mid] <= value:
                hi = mid
            else:
                lo = mid + 1
        return len(n) - lo

    else:
        while lo < hi:
            mid = (lo + hi) // 2
            if elemInM * n[mid] <= value:
                lo = mid + 1
            else:
                hi = mid
        return lo


'''
update: correct solution exceeds runtime limit still
below is copy-paste of standard answer
'''
import math
import bisect
class Solution:
    def kthSmallestProduct(self, nums1, nums2, k: int) -> int:

        def count_pairs(x: int) -> int:
            count = 0
            for a in nums1:
                if a > 0:
                    count += bisect.bisect_right(nums2, x / a)
                elif a < 0:
                    count += len(nums2) - bisect.bisect_left(nums2, math.ceil(x / a))
                else:
                    if x >= 0:
                        count += len(nums2)  # zero * anything <= x
                    # else, 0 * any b > negative => contributes nothing
            return count

        # Define search bounds
        low = min(nums1[0]*nums2[0], nums1[-1]*nums2[-1], nums1[0]*nums2[-1], nums1[-1]*nums2[0])
        high = max(nums1[0]*nums2[0], nums1[-1]*nums2[-1], nums1[0]*nums2[-1], nums1[-1]*nums2[0])

        while low < high:
            mid = (low + high) // 2
            if count_pairs(mid) < k:
                low = mid + 1
            else:
                high = mid

        return low


if __name__ == '__main__':
    m = [2, 5]
    n = [3, 4]
    k = 2
    print(q2040(m, n, k))
