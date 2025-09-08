import math


'''
this solution is a mix of my effort and chatgpt
in particular, derive sigma(i*4**i) from here: 
https://math.stackexchange.com/questions/2966250/summation-of-sum-i-1n-i2i#:~:text=Then%202S=n%E2%88%91,1)%E2%88%92n+12
'''

# your original closed form kept intact
def sigma(n):
    # sum_{i=0}^{n-1} (4^{i+1} - 4^i) * (i+1) = (n - 1/3) * 4^n + 1/3
    return int((n - 1/3) * (4 ** n) + 1/3) # note the math is already guaranteed to result in int, we just type-cast it to make sure it is int type.

def prefix_total(n: int) -> int:
    """Total ops over [1..n]. Constant ops with a log4 + small correction."""
    if n <= 0:
        return 0
    # floor(log_4 n) via float, then correct at most one step to remove FP drift
    t = int(math.log(n, 4)) #this is just floor(log base 4 of n)
    p = 4 ** t
    # if p > n:              # rare under-shoot, due to float point drift, not mathematical but CS in nature
    #     t -= 1; p //= 4
    # elif 4 * p <= n:       # rare over-shoot, also machine error not mathematical
    #     t += 1; p *= 4
    # full completed 4-blocks (your sigma) + partial top block
    full_blocks = sigma(t)              # safe: t is small integer
    return full_blocks + (n - p + 1) * (t + 1)

def range_answer(l: int, r: int) -> int:
    """Answer for one [l, r] interval."""
    total = prefix_total(r) - prefix_total(l - 1)
    return (total + 1) // 2                  # ceil(total/2)

def solution(pairs):
    """pairs: iterable of (l, r)."""
    return sum(range_answer(a, b) for a, b in pairs)

'''
reflection:
I could identify the flaw in my solution: did not account for partial block
but couldn't figure out a fix.

chatgpt fix:
it is simply an input size of n- (4** floor(logBase4Ofn))+1
each single element in this partial block requires (4** floor(logBase4Ofn)) + 1 operations to be reduced to 0
let's set variable t = (4** floor(logBase4Ofn)) #(which is what chatgpt did in the code fix),
we simply add (n-4**t+1)(t+1) to the sigma function result

the logic: eg: n = 30
formula catches full blocks [1,3] and [4,15]
partial block calculate the total cost of [16, 30] note this partial block require operation 3 times,
which can be simply calculated as t+1 (t being the per-element cost of the highest full block, in 
this case the elements in block [4-15])
and we simply have n-4**t+1 such elements.

add them up then overall result floor div by 2 and we have final answer

So I was actually very, very close to getting the actual solution. Yikes!
'''


if __name__ == '__main__':
    queries = [[1, 2], [2, 4]]
    print(solution(queries))
    pass