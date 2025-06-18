'''
I just casually came upon this
it is of special interest because
kmp algo string matching disregards the
size of alphabet (whereas Boyer-Moore algo, what is being used in english keyboard, cares)
thus it is especially good for something like chinese string matching
'''

def preprocessing(pattern):
    lps = [0 for _ in range(len(pattern))]
    length = 0  # length of the previous longest prefix suffix

    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:   #length is still growing
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                # fallback in the prefix pattern
                length = lps[length - 1]
                # don't increment i here
            else:
                lps[i] = 0
                i += 1
    return lps


'''
key takeaway:
we are still using the raw input arr when producing final result
the ctArr will be reduced to some useless jumbo
iterate backeward in original input array!
'''
def ctSort(arr):    #assume numbers 0-9
    ctArr = [0 for _ in range(10)]
    for each in arr:
        ctArr[each] += 1
    roll = 0
    for i in range(len(ctArr)):
        roll+= ctArr[i]
        ctArr[i] = roll
    res = [0 for _ in range(len(arr))]
    for each in arr[::-1]:  # we only need backward traversal for stability. In the context of digits 0-9, doesn't matter.
                            # the stability-preservation also assumes a stack structure when multiple items of same ordering are added/accounted for
        res[ctArr[each]-1] = each
        ctArr[each] -=1
    return res
if __name__ == "__main__":
    ...
    # pattern = "aacaaa"
    # print("preprocessed is", preprocessing(pattern))
    # num = 110325
    # print(digitSeparation(num))
    arr = [9,9,9,8,8,2,1,0,7,3,2]
    # this has cumulative array: 0, 1, 2, 2, 2, 2, 2, 2, 4, 7
                            #    0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    print(ctSort(arr))
