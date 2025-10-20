'''
this is a notebook for dynamic programming, following the flow of understanding based on the text book
'''
from sys import orig_argv

'''
first, start with cutting rod problem
'''


def naive(price_list, rod_length):
    if rod_length == 0:
        return 0  # obviously, rod of total length 0 has a price 0
    q = 0  # we assume no negative price in this case
    for i in range(1,
                   rod_length + 1):  # upper and lower bound inclusive as we consider all possible length from ctting the rod (including no cut: sell entire rod as a whole)
        # note that we start from i==1 as: 1. no point considering zero-length rod and 2. 0 causes infinite recursion
        # q = max(q, price_list[i] + naive(price_list, rod_length - i))
        if q < price_list[i] + naive(price_list, rod_length - i):
            q = price_list[i] + naive(price_list, rod_length - i)   #this line is identical as using the max() func
    return q

def print_naive(price_list, rod_length):
    def lambda_naive(price_list, rod_length, best_cut):
        if rod_length==0:
            return 0
        q = 0
        for i in range(1, rod_length+1):
            if q < price_list[i] + lambda_naive(price_list, rod_length-i, best_cut):
                q = price_list[i]+lambda_naive(price_list, rod_length-i, best_cut)
                best_cut[i] = q #indication that a cut is made
        return q
    steps_table = []
    best_cut = [0]*(rod_length+1)
    while rod_length > 0:   # we run the algo on the rod. cut off that optimal length, then repeat
        q = lambda_naive(price_list, rod_length, best_cut)
        steps_table.append(best_cut.index(max(best_cut)))
        rod_length -= best_cut.index(max(best_cut))
        best_cut = [0]*(rod_length+1)   #clear out the list
    print(steps_table)

def dp(price_list, rod_length, dp_table):
    dp_table[0] = 0
    for i in range(1, rod_length + 1):
        q = 0
        for j in range(1, i + 1):
            if q < price_list[j] + dp_table[i - j]:
                q = price_list[j] + dp_table[i - j]
        dp_table[i] = q
    return dp_table[rod_length]  # also just simply dp_table[-1], final ind position


def dp_with_steps(price_list, rod_length, dp_table, steps_table):
    for i in range(1, rod_length + 1):
        q = 0
        for j in range(i + 1):
            if q < price_list[j] + dp_table[i - j]:
                q = price_list[j] + dp_table[i - j]
                steps_table[i] = j
        dp_table[i] = q
    return dp_table, steps_table


def print_steps(price_list, rod_length):
    dp_table, steps_table = dp_with_steps(price_list, rod_length, dp_table=[0] * (rod_length + 1),
                                          steps_table=[0] * (rod_length + 1))
    while rod_length > 0:
        print(steps_table[rod_length], end='\t')
        rod_length -= steps_table[rod_length]
    print()


'''
next, let's do the classic LCS
'''


if __name__ == '__main__':
    l = 12  # the entire length of a given rod
    p = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 26,29,33]  # rod length of i has a price of p[i]
    print(naive(p, l))
    print_naive(p, l)
    print(dp(p, l, [0] * (l + 1)))
    print_steps(p, l)
