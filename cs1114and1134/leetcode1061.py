'''
checked soltion for this

adjacency list blunt dfs approach

'''



def q1061(s1, s2, msg):
    # char as key, list of connected chars as val
    adjLst = {chr(i): [chr(i)] for i in range(ord('a'), ord('a') + 26) }
    for i in range(len(s1)):    #guaranteed len(s1)==len(s2)
        if s1[i] != s2[i]:  # no point in appending if they equal
            adjLst[s1[i]].append(s2[i])
            adjLst[s2[i]].append(s1[i])
    res = []
    for eachChar in msg:
        visited = set()
        res.append(dfsMin(eachChar,adjLst,visited))
    return ''.join(res)




def dfsMin(start, adjLst, visited):
    if start not in adjLst:
        return start    #entire base case not needed actually because at minimum an elem has itself as next node
    visited.add(start)
    current = start #use current to track the smallest elem, but we still need starting point unchanged
    for eachChild in adjLst[start]:
        if eachChild not in visited:
            candidate = dfsMin(eachChild, adjLst, visited)
            current = min(candidate, current)
    return current



'''
while the dfs approach gives a 
super intuitive, super blunt solution

checking the answers also suggest
union find is a good approach

Union Find concept:
for any iterable collection (let's stick with list since it is easy)

where for any arbitrary element inside 0<=arr[i]<len(arr) is always an ind pos inside the arr,
and that arr[i] != i for all elements.
we defacto have an infinite loop if we try to trace any element

where for one and only one element k == arr[i]==i, and the rest 
are monotonic: suppose arr[i]>i always, or (exclusively or)
arr[i]<i always, then k is the "common sink" of the entire
array. Where every element eventually traces to element k

e.g.    if given f->c, f->b, b->a
        where f is ind 5 (6th letter in alphabet), c is 2, b is 1, a is 0
        then a sink array is constructed thus:
        
        1.  initalize the array such that arr[i]==i, we have no sink
            (or, in other words, every element is a sink for itself and only for itself)
                [0,1,2,3,....,25]   # suppose we have all 26 possible letters
        2.  map pair by pair, when f->c, check both where f and c "sinks" to
            and select the smaller one as the "common sink":
                [0,1,2,3,4,2,6,7,8,...25] 
                # because between f and c, f sinks to c, so arr[5]=2
                # and c sinks to itself (not sinking somewhere else) because arr[2] == 2
                # so c and f will not "common sink" to another letter, 
        3. do the same for f->b:
            check both where f and b "sinks" to:
                f sinks to c,
                b sinks to b,
            then we update by:
                c sinks to b
                b sinks to b
            now arr = [0,1,1,3,4,2,6,7,8...25]
            
            see, arr[2] == 1, which represents c sinks to b
            and notice arr[5] == 2, f sinks to c is unchanged.
            ...
        
        when all the "sinking" are done, we (could, but do not have to)
        scan the entire array one more time and all the "sinking" will be correct:
        with arr ==  [0,0,1,3,4,2,6,7,8...25],
        suppose we do right to left, when we scan to arr[5] 
        (by the way, it does not even matter we scan left to right or right to left
        both gives you the right answer, but left-to-right has linear runtime
        while right to left might result in n^2 runtime)
        it first points to 2, and we immediately check arr[2] == 1,
        again check arr[1]==0, so we can go further: next arr[0]==[0],
        it sinks onto itself, and we have found the final "common sink"!
        now we can update the array:
        arr = [0,0,1,3,4,0,6,7,8...25]
        and you can see that when we reach arr[2], same thing happens:
        arr = [0,0,0,3,4,0,6,7,8...25]
        
        so obviously scan left to right is better:
        iterator i = 0: no change because arr[0] == 0, sinking into itself, label 0 as sunken
        iterator i = 1: no change because arr[1] == 0, where we know 0 is already sunken, now label 1 as sunken
        iterator i = 2: [0,0,1,...] becomes [0,0,0,...] because 2 not sunken, arr[2]==1, 1 is sunken, arr[1]==0, now label 2 as sunken
        ...
        iterator i = 5: [0,0,0,3,4,1...] becomes [0,0,0,3,4,0,...] where 5 is not sunken, arr[5]==1, where 1 is sunken, arr[1]==0, now label 5 as sunken
        
        this approach requires maximum linear auxiliary space but allows the "sunking" process to be linear runtime
        whereas if we scan right to left, const auxiliary space, but runtime n^2 worst case.
 
'''

def solution(s1, s2, msg):
    arr = list(range(26))  # arr[i] is the root of character i

    def charInd(c):
        return ord(c) - ord('a')

    def getChar(i):
        return chr(i + ord('a'))

    for a, b in zip(s1, s2):
        x, y = charInd(a), charInd(b)
        root_x, root_y = arr[x], arr[y] #either themselves, or ponting at something smaller
        if root_x != root_y:
            smaller, larger = min(root_x, root_y), max(root_x, root_y)
        # global update to merge components
            for i in range(26): #consider f->c and f->b both present (from default val f->f)
                if arr[i] == larger:
                    arr[i] = smaller

    result = [getChar(arr[charInd(c)]) for c in msg]
    return ''.join(result)


if __name__ == "__main__":
    s1 = "leetcode"
    s2="programs"
    msg="sourcecode" #should get "aauaaaaada"
    print(q1061(s1, s2, msg))
    print(solution(s1, s2, msg))
