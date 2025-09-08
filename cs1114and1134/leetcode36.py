'''
sudoku validator

given the fixed 9x9 board size, brute force solution possible
'''

def brute(board):
    ctArr = [0 for i in range(10)]
    for eachRow in board:   #row rule
        for eachCell in eachRow:
            if not check(ctArr, eachCell):
                return False
        reset(ctArr)

    for i in range(9):  #col rule
        for j in range(9):
            if not check(ctArr, board[j][i]):
                return False
        reset(ctArr)
    for h in range(3):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if not check(ctArr, board[3*h+j][3*i+k]):
                        return False
            reset(ctArr)
    return True


'''
tally and check if we are exceeding
'''
def check(ctArr, val):
    if not val.isdigit():
        return True
    if ctArr[int(val)]>=1:
        return False
    ctArr[int(val)]+=1
    return True

def reset(ctArr):
    ctArr[:] = [0 for i in range(10)]



'''
update: efficient solution by chatgpt is here
I was massively overthinking. We can simply
use a set, and then use pair (and a triple for the grid) to 
indicate unique row/column/9x9grid
'''
def smart(board):
    seen = set()
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v == '.':
                continue
            if ((r, v) in seen or   #checks entire row
                (c, v) in seen or   #checks entire col, smart overlap for row-col intersection cell
                (r//3, c//3, v) in seen):   #now use a triple tup to avoid collition with row-col check
                return False
            seen.add((r, v))
            seen.add((c, v))
            seen.add((r//3, c//3, v))
    return True



if __name__ == '__main__':
    # board = [[".",".",".",".","5",".",".","1","."],[".","4",".","3",".",".",".",".","."],[".",".",".",".",".","3",".",".","1"],["8",".",".",".",".",".",".","2","."],[".",".","2",".","7",".",".",".","."],[".","1","5",".",".",".",".",".","."],[".",".",".",".",".","2",".",".","."],[".","2",".","9",".",".",".",".","."],[".",".","4",".",".",".",".",".","."]]
    # for eachRow in board:
    #     for eachCell in eachRow:
    #         print(eachCell, end = "\t")
    #     print()
    #

