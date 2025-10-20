'''
summer 2024 midterm 1134 recursion problem:
count the number of ways you can represent a number as
sum of 1s and 2s

tested concepta:
    recursion
    runtime analysis

'''
import copy


def recur(num):
    if 2 > num:
        return 1
    return recur(num - 1) + recur(num - 2)


'''
dp improvement, by chatgpt
'''


def recur(num, memo={}):
    if num in memo:
        return memo[num]
    if num < 2:
        return 1

    memo[num] = recur(num - 1, memo) + recur(num - 2, memo)
    return memo[num]


'''
alternative of non recursion
'''


def count_ways(n):
    if n == 0:
        return 1
    if n == 1:
        return 1

    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


'''
below is some simple trials on tree node related func
'''


class Node:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def cut(node, bar):
    if not node:
        return
    # by this point we have a node for sure
    if (node.val > bar):
        if node.parent.left == node:
            node.parent.right = node.left
        recur(node.left, bar)  # we only care what is on the left
    else:  # not too big
        cut(node.right, bar)  # no need to recurse on the left since no modifications whatsoever


def inspect(root):
    if root is None:
        return
    print(root.val, end=' ')
    inspect(root.left)
    inspect(root.right)


'''
This will be a good mock paper problem
'''


def fac(n):
    def recur(n, i):
        if n > i ** 0.5:
            if not i % n:
                yield n
            else:
                return
        else:
            if not i % n and not i / n == n:
                yield n
            yield from recur(n + 1, i)  # yield from, not yield
            if not i % n:
                yield i / n

    for i in recur(1, n):
        print(i, end='  ')


# main
fac(100)


def p136(arr):
    if len(arr) == 1:
        return arr[0]
    start = arr[0]
    for each in arr[1:]:
        start = start ^ each
    return start


'''
I read the solution for this one

key takeaways:
    constrain satisfaction problem, I can develop a dfs backtrack solution (worse than linear runtime tho)
    DI min string is leetcode 2375, but there isn't a DI max string, I can use on ptc 1134 paper
    
actual solution thinking:

ultimate "human way" of solving CSF, semi-greedily (to say incrementally is to say semi-greedily):
pinpoint the part of the puzzle that is deterministic
then use those as prereq/additional constraint to make the rest deterministic, incrementally
(think of sudoku and mine sweeper, it is the same idea, except mine sweeper has luck in it)

what does that teach us?
1. Intuitively, the moment you see "I" you know what to fill in already
but when you see "D" it is not certain yet, because:
    I:  constrains that current num must be smaller than next, but also implicitly 
        the current num is also as small as possible (since we want overall result to be minimum)
        thus each "I" element is deterministic
    D:  constrains that the current num must be bigger than the next. This is non-deterministic on
        its own. Because you do not know how small you could afford this number to be (you want it
        as small as possible but, it is further constrained by next element)
2. Intuitively any best solution will use consecutive digits from 1 onwards, and the solution will
use small digits first then use bigger digits. Obviously a "1354" is better than "1453" if the 
input is "IIDI" (or "IIDD", because final input doesnt constrain anything) Thus, try to start with 
1 at the first element position.

Other thoughts:

Crystal: the instruction input mode can be optimized to take n-1 inputs for a string of n length:
    -   empty input indicates "single number, smallest possible" implying answer "1"
    -   otherwise: "IDI" means: 1324, "IDD" means 1432, etc (so we don have useless trailing 
    final input letter)
    turns out the above interpretation is correct
    -   we can also test our own understanding of this puzzle by trying to design a function
    that produces the largest possible number string. This is not a puzzle found on leetcode
    and worth putting on PTC paper.
 



'''

'''
use lists of chars to store result, and convert to string and
then join them together in the end
'''


def p2375(arr):
    cap = 1  # keep track of the cap
    res = []
    buffer = []  # the non-deterministic part by "D"
    for each in arr:
        if 'I' == each:  # when we see "I", the element here is deterministic
            res.append(cap)
            addBackwardAndClearBuffer(res, buffer) if len(buffer) > 0 else None
        elif 'D' == each:  # when we see D, non deterministic
            buffer.append(cap)
        cap += 1  # no matter we see D or I, cap increases because
        # each consecutive new instruction letter
        # indicates we need a consecutively larger
        # digit to be added to the result,
        # "DD" means we need "21" added, and
        # "ID" means we need "12",
        # whatever the additional instruction is, the cap rises by one.
        # the only difference is, I and D will determine if the new number
        # is appended to result straightaway (I) or should be stored in
        # buffer first (D) and we should move on to next instruction before
        # determining if this current digit is to be added
    res.append(cap)
    addBackwardAndClearBuffer(res, buffer) if len(buffer) > 0 else None  # this line is only needed when the
    # instruction set ends with a "D" with undetermined number of "D"s before it.
    return ''.join(map(str, res))  # convert each element from digit to char(string) then concatenate


'''
helper function, modification in place
input: list (supports .append)
addend: list (supports []operator)
'''


def addBackwardAndClearBuffer(input, addend):
    for i in range(len(addend) - 1, -1, -1):
        input.append(addend[i])
    addend.clear()


'''
twist on leetcode 2375:
same problem description, but instead of min num,
generate max num
'''


def flip2375(arr):
    bot = 9
    res = []
    buffer = []
    for each in arr:
        if each == 'I':
            buffer.append(bot)
        elif each == 'D':
            res.append(bot)
            addBackwardAndClearBuffer(res, buffer) if len(buffer) > 0 else None
        bot -= 1
    res.append(bot)
    addBackwardAndClearBuffer(res, buffer) if len(buffer) > 0 else None
    return ''.join(map(str, res))


'''
objective:
generic dfs for "highest combined score"
    -   this is only doable i 2^n runtime (need to explore all paths)

curScore is a list of a single elem to cheat the copy issue of python
curScore is inplace storage of the max score
'''


def dfsTotalScore(root):
    if not root:
        return 0
    else:
        return root.val + max(dfsTotalScore(root.left), dfsTotalScore(root.right))


'''
leetcode 1092 involves a good understanding and application of LCS
my foundaton in Algo is shaky.
need to work on it
'''


# p1092
class Solution:
    def shortestCommonSupersequence(self, str1: str, str2: str) -> str:
        # Step 1: Find the longest common subsequence using dynamic programming
        m, n = len(str1), len(str2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Fill the dp table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i - 1] == str2[j - 1]:
                    dp[i][j] = 1 + dp[i - 1][j - 1]
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        # Step 2: Construct the shortest common supersequence
        # Start from the bottom right of the dp table
        i, j = m, n
        result = []

        while i > 0 and j > 0:
            if str1[i - 1] == str2[j - 1]:
                # If the characters are the same, add it once
                result.append(str1[i - 1])
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                # If coming from top has higher value, take character from str1
                result.append(str1[i - 1])
                i -= 1
            else:
                # Otherwise, take character from str2
                result.append(str2[j - 1])
                j -= 1

        # Add remaining characters from str1 (if any)
        while i > 0:
            result.append(str1[i - 1])
            i -= 1

        # Add remaining characters from str2 (if any)
        while j > 0:
            result.append(str2[j - 1])
            j -= 1

        # Reverse the result to get the final supersequence
        return ''.join(result[::-1])


'''
side note: LCS func as given in algo textbook
'''


def genLCSTable(str1, str2):
    '''
    adopted from P397 of textbook
    :param str1:
    :param str2:
    :return: c, 2-d list of lcs score
             b, 2-d list of backtracking direction
    '''
    m = len(str1)
    n = len(str2)
    c = [[0] * (n + 1) for _ in range(m + 1)]  # we only need first row and first column to be 0, but might as well
    b = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                c[i][j] = 1 + c[i - 1][j - 1]
                b[i][j] = "diag"
            else:
                if c[i - 1][j] >= c[i][j - 1]:  # the equal condition is an arbitrary choice
                    c[i][j] = c[i - 1][j]
                    b[i][j] = "up"
                else:  # implied left-greater-than-up
                    c[i][j] = c[i][j - 1]
                    b[i][j] = "left"
    return b


def printLCS(b, str1, i, j):
    if not i or not j:
        return
    if "diag" == b[i][j]:
        printLCS(b, str1, i - 1, j - 1)
        print(str1[i - 1], end='')  # print after recursive call
    else:
        if "up" == b[i][j]:
            printLCS(b, str1, i - 1, j)
        else:  # implied "left"
            printLCS(b, str1, i, j - 1)


def LCS(str1, str2):
    printLCS(genLCSTable(str1, str2), str1, len(str1), len(str2))


'''
leetcode 2523
native approach: find nearest primes via n**0.5 runtime algo
            and that heuristically, left side primes are closer

naive approach breaches runtime limit,
improvements (minor, no algorithmic change)
 - know that adjacent primes are 2+ places apart ()
 - do not generate complete prime array, generate along the way
 - special case of 2 -> 3

Adopt Katz coding style

--above solution is good.
'''
import math


def isPrime(n):
    '''
    this does something
    :param n:
    :return:
    '''
    for i in range(2, math.floor(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return n!=1

'''return immediate next prime'''
def linearProbe(num):
    while not isPrime(num):
        num += 2  # bump 2 at a time is good enough
    return num

def linearProcess(left, right):
    fail = [-1,-1]  # return fail whenever we breach the rules
    if left<=2 and right>=3:    # the very special 2-3 prime pair. The only case of 1-apart primes
        return [2,3]
    if right-left<2: return fail    # the bound is not far enough
    else:
        '''
        num1 and num2 starts as the first two primes
        if num2 - num1 == 2, straightaway return (we cannot hope to do better)
        otherwise, keeptrack of current minimum diff and move num1, num2 forward
        note that we can move 2 places at a time because, again, minimal gap 2
        and NEVER odd gaps (prime + odd = even)
        keep updating the minimum until either:
            1. reach a diff == 2
            2. num2 is beyond right bound
        '''
        num1 = left
        while not isPrime(num1):
            num1 += 1
            if num1>=right: # means there is only one or fewer primes in the desired range, fail
                return fail
        # print(f"init num1: {num1} must be prime in range")
        num2 = linearProbe(num1+2)
        if num2>right: return fail  #make sure we didn't go beyond
        '''
        the above code sets num1, num2 on the correct starting points
        '''
        res = [num1, num2]
        diff = num2 - num1  #current prime gap
        while num2 <= right:    # scan left to right till beyond bound
            if diff <=2: return [num1, num2]    # 2 is the best we can get, just return it then
            num1 = num2 #num1 becomes the current num2
            num2 = linearProbe(num2+2)  #num2 goes to the next prime possible
            if num2-num1<diff:
                diff = num2-num1
                if num2<=right: #if it is too far we do not update
                    res = [num1, num2]
        # print(f"num2 complete to be: {num2} must be bigger than num1: {num1}, current res: {res}")
        return res


def p2843brute(lo, hi):
    res=0
    for each in range(lo, hi):

        if(checkSumSymmetry(each)):
            res+=1
    return res

def checkSumSymmetry(num):
    numStr = str(num)
    lenStr = len(numStr)
    sumHi, sumLo = 0, 0
    for i in range(lenStr//2):
        sumHi+= int(numStr[i])
    for j in range(lenStr//2, lenStr):
        sumLo+= int(numStr[j])
    return num>10 and not lenStr%2 and sumHi==sumLo

'''
below are 1114 list and dictionary comprehension problems
note that both are inspired by prof arfaoui's exercise sheet
'''
def extract_netids(email_string):
    return [email[:email.find('@')] for email in email_string.split()]

def map_values_to_coords(matrix):
    return {
        matrix[i][j]: (i, j)
        for i in range(len(matrix))
        for j in range(len(matrix[i]))
    }


if __name__ == '__main__':
    print()
    print(f"the2375 flipped: {flip2375('DDD')}")
    #
    # matrix = [
    #     [1, 2, 3],
    #     [4, 5, 6],
    #     [7, 8, 9]
    # ]
    #
    # print(f"mat dict is: {map_values_to_coords(matrix)}")
    #
    # lst = "abc123@lyu.edu cba321@lyu.edu"
    # print(f"extract netid: {extract_netids(lst)}")
    # p2843brute(35,237)
    # print()
    # nodeA = Node(0)
    # nodeB = Node(7)
    # nodeC = Node(5, nodeA, nodeB)
    # nodeD = Node(8)
    # nodeE = Node(1, nodeC, nodeD)
    # # print("answer:",dfsTotalScore(nodeE))
    #
    # str1 = "ABCBDAB"
    # str2 = "BDCABA"
    # print("LCS result is:\t",end = '')
    # LCS(str1, str2)
    # print(p2523helper(10, 10+1, [0, 99], 19))
    # left = 69346
    # right = 69379
    # print(linearProcess(left, right))
    # print(isPrime(10))
    # n = 11
    # m = 17
    # print()
    # print("the recursion version:")
    # notsilly(n, m)
    # print()
    # print("now the iterative version:")
    # silly(n, m)

    # a = [1,2,3,[4,5,6]]
    # b = copy.deepcopy(a)
    # c = a
    # c[3][1] *= 10
    # a[0] = 0
    # b[3][2] = 1
    # print(f"a is: {a}\nb is: {b}\nc is: {c}")
    '''
            8


    '''
