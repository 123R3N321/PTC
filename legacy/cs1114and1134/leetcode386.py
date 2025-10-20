'''
I am thinking of counting sort applied on lexi number sort again
which allows runtime linear

update: my solution is not good
    it is better to do dfs
    observe the lexi order closer and you will see
'''

def ctSortK(arr,ind):
    ...

'''
given a number and ind pos
retrieve only that digit
lsd -> 0
msb -> n
'''
def digitIsolation(num, ind):
    if num==0: return 0
    if 10**ind>num: return 0
    return (num//(10**ind))%10


def lexicalOrder(n):
    """
    :type n: int
    :rtype: List[int]
    """
    result = []
    current = 1

    for _ in range(n):
        result.append(current)
        if current * 10 <= n:
            current *= 10  # Go deeper in lexicographical tree
        else:
            if current >= n:
                current //= 10  # Go back up if out of range
            current += 1
            while current % 10 == 0:
                current //= 10  # Skip trailing zeros

    return result


if __name__ == '__main__':
    # print(digitIsolation(342,2))
    print(lexicalOrder(12))