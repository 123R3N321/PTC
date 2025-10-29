'''
let's see
'''

'''
just generate all valid ind pairs
'''
def pairGen(total, l1Len, l2Len):
    res = []
    for i in range(min(total+1, l1Len)):
        conj = total-i
        if conj<l2Len:
            res.append((i,conj))
    return res

def scoreCal(l1,l2,pair):
    return l1[pair[0]]+l2[pair[1]]

def unpack(l1,l2,scorePairPair):
    _,ind1_ind2 = scorePairPair
    ind1,ind2 = ind1_ind2
    return [l1[ind1],l2[ind2]]

import heapq
def solver(l1,l2,k):
    heap = []
    res = []

def blunt(l1,l2,k):
    heap = []
    for i in range(len(l1)):
        for j in range(len(l2)):
            heapq.heappush(heap,(scoreCal(l1,l2,(i,j)),(i,j)))
    res = []
    for z in range(k):
        topPairPair = heapq.heappop(heap)
        res.append(unpack(l1,l2,topPairPair))
    return res


if __name__ == '__main__':
    l1 = [1,2,4,5,6]
    l2 = [7,11,33]
    k = 6
    # print(solver(l1,l2,k))
    print(blunt(l1,l2,k))