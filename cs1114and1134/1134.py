'''
summer 2024 midterm 2234 recursion problem:
count the number of ways you can represent a number as
sum of 1s and 2s

tested concepta:
    recursion
    runtime analysis

'''
def recur(num):
    if 2 > num:
        return 1
    return recur(num-1) + recur(num-2)

'''
dp improvement, by chatgpt
'''
def recur(num, memo={}):
    if num in memo:
        return memo[num]
    if num < 2:
        return 1

    memo[num] = recur(num-1, memo) + recur(num-2, memo)
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