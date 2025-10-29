# def allPlaces(curLvl):
#     allp = [i for i in range(len(curLvl[0])+1)]
#     # print(f"check all places: {allp}")
#     return allp
#
# def putElemsInPlaces(allPlaces, curLvl, elem):
#     res = []
#     for eachState in curLvl:
#         # print(f"heres each state: {eachState}", end = '  ')
#         for eachInd in allPlaces:
#             # print(f"heres each ind: {eachInd}", end = "   ")
#             curState = eachState.copy()
#             curState.insert(eachInd, elem)
#             res.append(curState)
#         # print()
#     return res
#
# def startF(curLvl):
#     netNum = max(curLvl[0]) + 1
#
#     return putElemsInPlaces(allPlaces(curLvl), curLvl, netNum)
#
# def repeat(init,total):
#     start = 1
#     res = []
#     while start < total:
#         start = start + 1
#         res = startF(init).copy()
#     return res
#


def solve(start, total):
    curElem = max(start[0])+1
    res = []
    while curElem < total+1:
        if curElem == total:
            return res
        inds = [i for i in range(len(start[0])+1)]
        res = []
        for eachState in start:
            cur = eachState.copy()
            print(f"cur is {cur}")
            for i in inds:
                cur.insert(i,cur)
                res.append(cur)
        start = res.copy()
        curElem+=1
    return res
import copy
def solve(start, total):
    # start like [[0]], total like 3 -> permutations of [0,1,2]
    curElem = max(start[0])+1

    curLvl = copy.deepcopy(start)  # copy the starting states

    while curElem < total:
        nextLvl = []
        for eachState in curLvl:
            for i in range(len(eachState) + 1):
                seq = eachState.copy()   # fresh copy per insertion
                seq.insert(i, curElem)   # insert the next element value
                nextLvl.append(seq)
        curLvl = nextLvl
        curElem += 1

    return curLvl


def recur(cur,total,num):
    if num >= total:
        return cur
    next = []
    for eachState in cur:
        for i in range(len(eachState) + 1):
            seq = eachState.copy()  # fresh copy per insertion
            seq.insert(i, num)  # insert the next element value
            next.append(seq)
    return recur(next,total,num+1)


def fac(n):
    start = 1
    for i in range(1,n+1):
        start *= i
    return start


def sort_stack(stack):
    temp_stack = []

    while stack:
        # Pop the top element
        tmp = stack.pop()

        # Move elements from temp_stack back to stack until tmp is in the right place
        while temp_stack and temp_stack[-1] > tmp:
            stack.append(temp_stack.pop())

        # Place tmp in sorted position
        temp_stack.append(tmp)

    # Move everything back to original stack (sorted)
    while temp_stack:
        stack.append(temp_stack.pop())
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # Move elements greater than key one position ahead
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

if __name__ == '__main__':
    stack = [1,3,2,7,0]
    insertion_sort(stack)
    print(stack)
    # start = [[1]]
    # total = 5
    # res = solve(start, total)
    # seen = set()
    # for each in res:
    #     if tuple(each) not in seen:
    #         seen.add(tuple(each))
    #     else:
    #         print("we have repeated answer!")
    # for each in res:
    #     print(each)
    # print(f"total: {len(res)}, which should be: {fac(total-1)}")
    # print("-------")
    # for each in recur(start,total,2):
    #     print(each)