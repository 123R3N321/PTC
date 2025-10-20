'''
This is a leetcode daily qn
deals with diagonal manipulation of square mat
'''

'''
my naive solution:
extract diagonals, sort them, put back in diagonal in a new mat
'''

'''
given the input mat and the starting coord
(starting coord must be first row and first col)
return a list containing all extracted elems from the diag
'''
def extraction(mat, startX, statY):
    n = len(mat)
    res = []
    while startX < n and statY < n:
        res.append(mat[startX][statY])
        startX += 1
        statY += 1
    return res

'''
fill in a mat made of Nones in diag manner
'''
def completion(mat, startX, statY, lst):
    for eachElem in lst:
        mat[startX][statY] = eachElem
        startX += 1
        statY += 1

'''
consists of 2 loops
first one iterating on row 0
    extract each diag exclude main diag
    sort the extracted data
    fill into res mat consisting of only none
another loop thru col 0
    extract, this time including main diag
    sort
    fill
'''
def naive(mat):
    res = [[None for _ in range(len(mat))]for __ in range(len(mat))]
    #row op
    for i in range(1,len(mat[0])):  #exlude elem 0 which is main diag start
        localLst = extraction(mat, 0, i)
        localLst.sort()
        completion(res, 0, i, localLst)
        localLst.clear()    #not necessary but whatev

    #col op
    for j in range(len(mat)):
        localLst = extraction(mat, j, 0)
        localLst.sort(reverse=True)
        completion(res, j, 0, localLst)
        localLst.clear()

    return res

def printMat(mat):
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            print(mat[i][j], end="\t")
        print()
    print("\n")

if __name__ == '__main__':
    mat = [[1,7,3],[9,8,2],[4,5,6]]
    res = naive(mat)
    printMat(res)

'''
afterthought:
too easy... I donno how this qualifies as a medium bruh
'''
