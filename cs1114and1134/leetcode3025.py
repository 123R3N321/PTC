'''
this one should not be that hard for me

manual double ct sort (defacto radix)
then sliding window look at two elems at a time
'''

def solution(arr):
    ctArr = [0 for _ in range(51)]
    #first, do a reverse ct sort based on arr[i][1]
    for each in arr:
        val = 50 - each[1]
        ctArr[val]+=1

    snowball = 0
    for i in range(51):
        ctArr[i] += snowball
        snowball = ctArr[i]
    for i in range(51):
        ctArr[i] -= 1   # pre decrement

    res = [None for _ in range(ctArr[-1]+1)]
    for each in arr[::-1]:
        val = 50 - each[1]
        res[ctArr[val]] = each
        ctArr[val] -= 1
    # print(f"test layer1 sort: ctArr = {res}")

    ctArr = [0 for _ in range(51)]
    for each in res:
        ctArr[each[0]]+=1
    snowball = 0
    for i in range(51):
        ctArr[i] += snowball
        snowball = ctArr[i]

    finalRes = [None for _ in range(len(res))]
    for each in res[::-1]:
        finalRes[ctArr[each[0]]-1] = each
        ctArr[each[0]]-=1
    # print(f"final res: {finalRes}")

    #pre processing complete
    ct = 0
    if len(finalRes) <= 1: return ct    #super tiny arr early return
    for i in range(len(finalRes)):
        leftPeak = finalRes[i][1]
        top = -1
        for j in range(i+1,len(finalRes)):
            curPeak = finalRes[j][1]
            if curPeak <= leftPeak:
                if curPeak > top:
                    ct+=1
                    top=curPeak
    return ct


if __name__ == "__main__":
    # arr = [[1,2],[0,8],[7,3],[2,9],[33,39],[33,1]]
    # solution(arr)
    arr = [[3,1],[1,3],[1,1]]
    print(solution(arr))
