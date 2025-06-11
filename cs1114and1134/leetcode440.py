'''
rank integer lexically.

I can think of naive solution that has horrible runtime
now think: the lexi order "wraps around" when
the range hits 10,100,1000
observe:

1 > 1x > 1xx > ... > 2 > 2x > 2xx > ...

we can do reverse radix sort, div by 10 to isolate each digit

update: problem is, sorting at increasing digit positions overwrites previous work:
consider sorting [15,21], we will get result [21,15] as 21 has "1" and 15 has "5"

Guess:
after sorting at pos [0], first a elements all have starting 1,
sort within these m elements at pos[1], and first b elements all
start with 1,1, so on and so forth... problem is:
1.finding such indices a, b, ... (seems recursive)
2. cost of finding such indices.

more observations:

inside counting sort algo, the prefix arr at ind i-1 seems to be the boundaries
conveniently, intermediateSortedArr[prefix[i]:prefix[j]] is exactly correct

update: my solution is no good. Do dfs for q386, that leads to the right solution

'''


def dumb(n,k):
    sortedArr = flipRadix([i for i in range(1,n+1)])
    print(f"final result: {sortedArr}")
    return sortedArr[k-1]



'''
given an array of arr of ints, where all elems k>=0 in the inner arr
sort based on leading digits (essentially lexi sort or arrays)
'''
def flipRadix(arr):
    for i in range(9):
        arr = ctSort(arr,i)
        print(f"intermediate at pos{i} : {arr}")
        print()
    return arr


'''
given an int, return an arr containing all its digits, backward then rev
(because code looks cleaner)
'''
def digitIsolation(num):
    if 0==num: return [0]
    res = []
    while num>0:
        res.append(num%10)
        num = num//10
    res.reverse()   #.reverse returns None, remember this!

    while len(res)<10:
        res.append(0)   #modify each list of digits to be 10 places long

    return res


'''
assume base 10 
assume each elem: -1< k <10, k is int
'''
def ctSort(arr, pos):
    ctArr = [0 for i in range(10)]  #0 thru 9, we need 10 places
    for each in arr:
        ctArr[digitIsolation(each)[pos]]+=1
    roll = 0
    for i in range(len(ctArr)): #prefix sum
        ctArr[i]+= roll
        roll = ctArr[i]
    print(f"prefix pos arr: {ctArr}")
    pinpoint1 = ctArr[1]
    pinpoint2 = ctArr[2]
    pinpoint3 = ctArr[3]

    interm = [-1 for i in range(len(arr))]  # note
    for i in range(len(arr)-1,-1,-1):
        interm[ctArr[digitIsolation(arr[i])[pos]]-1] = arr[i]
        ctArr[digitIsolation(arr[i])[pos]]-=1
    #now the intermediate array is filled with sorted arr and -1
    res = []
    for each in interm:
        if each != -1:
            res.append(each)
    for i in range(len(arr)):
        arr[i] = res[i] #in-place modification
    print(f"pinpoint range boundary 0 : {pinpoint1}: {arr[:pinpoint1]}")
    print(f"pinpoint range boundary {pinpoint1} : {pinpoint2}: {arr[pinpoint1:pinpoint2]}")
    print(f"pinpoint range boundary {pinpoint2} : {pinpoint3}: {arr[pinpoint2:pinpoint3]}")

    return res

'''
special helper method
given entire array, only sort range [lo:hi] (lo inc, hi exc)
based on place, which is ind from 0 to 9
'''
def chunckedSort(arr, lo, hi, place):
    tempo = arr[lo:hi]
    ctSort(tempo, place)
    arr[lo:hi] = tempo[lo:hi]



if __name__ == '__main__':
    n = 121
    k = 3
    print(dumb(n,k))

    arr = [i for i in range(1,n+1)]
    chunckedSort(arr, 0, 33, 0)
    print(arr)
    # for i in range(3):
    #     arr = ctSort(arr,i)
    #     print(f"sorted at ind {i}: {arr}")

    # arr = ctSort(arr,0)
    # print(f"after sorting at pos 0: {arr}")
    # partialArr = arr[0:22]
    # print(f"try to seperate all those beginning with 1: {partialArr}")
    # experiment = ctSort(partialArr,1)
    # print(f"after sorting at pos 1 on partial array: {experiment}")