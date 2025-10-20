'''
this seems a stack use case

we keep an int that indicates:
    upflag = (the i-1 th elem < ith element)? ith element smallest possible val so far : 1

    upflag is used to indicate ith element val.

add dummy  at end of arr, max(arr)+1 val (guaranteed increasing from -1th elem)

iterate left to right in original arr len (curr len-1),
check ith and i+1 th element, and only set ith element when deterministic:

if i-1 th >= ith:   #up flag==1, false

    if ith<i+1th:  #ith element is smaller equal to both its left and right element, easy

        if there is a "stack", and stack top val goes above up flag val,
            add entire stack to total (stack does not include ith val)
            reset stack
        now set up flag, up flag+=1


    elif ith==i+1th:
        if there is a "stack", and stack top val goes above up flag val,
            add entire stack to total (stack does not include ith val)
            reset stack

        then, set up flag false, up flag = 1 because this is also "add one" case.


    then simply add 1 to total (this accounts for else case)
    # because as long as from i-1 th to ith there is no increment,
    # we always add a one, the only thing that might change is if there is a stack to be added

    else:   # ith > i+1 th element, and since up flag==1, i-1th >= ith > i+1th
        not deterministic, calculate stack


else:   # i-1th < ith, up flag>1, true, we are going up
    if ith<=i+1th:  # i-1th < ith <= i+1th, deterministic
        add upflag value to total
        upflag value+=1

    else:   # i-1th < ith > i+1 th, ith is for sure the biggest compared to left and right, not deterministic
        calculate stack
        set up flag to false, up flag = 1


'''

'''
update:
remember to read other solutions, 
I think some of them are
much much more elegant than mine.
'''

def q135(arr):
    theRange = len(arr)
    if theRange < 2:
        return 1
    upflag = False
    upval = 1
    stack = 1
    total = 0
    arr.append(max(arr) + 1)
    for i in range(theRange):
        first = arr[i]
        second = arr[i + 1]

        if not upflag:  # i-1th element >= ith element
            if first < second:  # deterministic at i th
                if stack >= upval:
                    total += stack * (stack + 1) // 2  # add stack including ith elem
                    stack = 1  # stack reset
                else:
                    total += (stack - 1) * stack // 2 + upval
                    stack = 1
                upval = 1  # shortly reset, then immediately go up
                upflag = True
                upval += 1  # keep flag up

            elif first == second:  # also deterministic
                if stack >= upval:
                    total += stack * (stack + 1) // 2  # add stack including ith elem
                    stack = 1
                else:
                    total += (stack - 1) * stack // 2 + upval
                    stack = 1
                upval = 1
                upflag = False  # flag reset.we are not incrementing anymore
            else:  # first > second, not deterministic, calculate stack
                stack += 1
                upflag = False

        else:  # i-1th element < ith element, we are going up from before, no stack
            if first < second:  # deterministic
                total += upval
                upval += 1
            elif first == second:
                total += upval
                upflag = False  # not going up anymore
                upval = 1
            else:  # first > second, not deterministic, calculate stack, also reset upflag
                stack += 1
                upflag = False
    return total


'''
Topological sort solution

not the most elegant in approach
but very elegant code
besides it is good to familiarize with Kahn's Algo

approach:
for three consecutive elements at i-1th, ith and i+ith ind pos
suppose their values are a, b, and c
each element knows two things: 

1.  if I should maintain an edge pointing 
    to my neighbor(s). Supposedly a>b<c, then b points toward both a and c

2.  the indgree, in other words how many other elements are ppointing to
    myself. it could only be 0, 1, or 2 in this question
    
'''
def q135toposort(arr):
    if len(arr) < 2:    #edge case
        return 1

    indegreeArr = [0] * (len(arr))    #indicating the number of edges going into each elem

    #   0 - not pointing; 1 -   yes point to neighbor
    # essentially this makes the need of indegreeArr obsolete, but whatev
    outdegreeArr = [[-1,-1] for i in range(len(arr))]     #whether we should point toward the neighbor

    for i in range(len(arr)-1):
        if arr[i]<arr[i+1]:
            indegreeArr[i+1] += 1
            outdegreeArr[i][1] = i+1    #indicate where to go
        elif arr[i]>arr[i+1]:
            indegreeArr[i] += 1
            outdegreeArr[i+1][0] = i    #where to go
    q = []  #yeah Im lazy. Use list as if it is queue
    val = [0]* len(arr) # stacking up value for each pointed-at elem
    for i in range(len(indegreeArr)):
        if indegreeArr[i]==0:  #we have nobody pointing to us
            q.append([0,outdegreeArr[i]])   #element [0]keeps track how much to add
    #in the q, we know where to go, also guaranteed indegreeArr[outdegreeArr[i][0 or 1]] has value >0


    res = len(arr)  #each element in arr means at least one candy
    while len(q) > 0:
        front = q.pop(0)    #yeah should really fix this haha this is runtime costly
        #kahn algo: if we point to something, we decrease the indegree of that thing
        if front[1][0]>-1:
            indegreeArr[front[1][0]]-=1
            val[front[1][0]]=(1+front[0])
        if front[1][1]>-1:
            indegreeArr[front[1][1]]-=1
            val[front[1][1]]=(1+front[0])   #overwrite, not accumulative +=, because whoever gets to this node last has the longer topological chain and should dominate.
        if front[1][0] > -1:
            if indegreeArr[front[1][0]]==0: #element not pointed by anywhere else
                q.append([val[front[1][0]],outdegreeArr[front[1][0]]])
        if front[1][1] > -1:
            if indegreeArr[front[1][1]]==0:
                q.append([val[front[1][1]],outdegreeArr[front[1][1]]])

        res+= front[0]

    return res


if __name__ == '__main__':
    arr = [58, 21, 72, 77, 48, 9, 38, 71, 68, 77, 82, 47, 25, 94, 89, 54, 26, 54, 54, 99, 64, 71, 76, 63, 81, 82, 60,
           64, 29, 51, 87, 87, 72, 12, 16, 20, 21, 54, 43, 41, 83, 77, 41, 61, 72, 82, 15, 50, 36, 69, 49, 53, 92, 77,
           16, 73, 12, 28, 37, 41, 79, 25, 80, 3, 37, 48, 23, 10, 55, 19, 51, 38, 96, 92, 99, 68, 75, 14, 18, 63, 35,
           19, 68, 28, 49, 36, 53, 61, 64, 91, 2, 43, 68, 34, 46, 57, 82, 22, 67, 89]

    # myArr = [1,2,3,4,1]

    # print(q135(myArr))
    print(q135toposort(arr))
