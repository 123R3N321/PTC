'''
update:

the problem actually allows partial taken
out from both 1st and 2nd step
do a stack solution

1.scan msg till we find first lexi min char, k

2.check top of the stack see if that elem is smaller than or equal to k
    -> if so, pop that elem, check next top elem in stak
    ->if not, move onto step3

3.push from beginning of msg till k, inclusive, into stack



repeat step 1 till we have entire msg cleared out

empty the stack and append each one into res

'''


def q2434(msg):
    if len(msg) <= 1: return msg
    start = 0  # start with ind pos 0 of msg
    end = minScan(msg, 0)  # remember the upperbound exclusive, we need to go up by one later
    stack = []  # stack for intermediate
    res = []
    while start < len(msg):  # scan entire msg
        for i in range(start, end + 1):  # upperbound exclusive, need +1
            stack.append(msg[i])  # push all chars between prev min char (exc) and cur min char (inc)

        res.append(stack.pop())  # garanteed min char
        start = end + 1  # the min char position +1 is where next scan starts
        if start < len(msg):
            end = minScan(msg, start)  # find ind pos of next min char, set that as upperbound

            while len(stack) > 0 and stack[-1] <= msg[
                end]:  # check if the top of the stack is smaller than next min char in msg
                res.append(stack.pop())  # if so, that is better answer before we put next min char into stack
        else:  # we are at last elem of msg
            while len(stack) > 0 and stack[-1] <= msg[-1]:
                res.append(stack.pop())

    while len(stack) > 0:
        res.append(stack.pop())
    return ''.join(res)


'''
scan iterable collection msg for lexi minimal char
between starting point and end of msg
and return its ind pos
when more than one such ind pos found,
return the smallest ind pos

len(msg)>start required.
'''


def minScan(msg, start):
    minInd = start
    for i in range(start, len(msg)):
        if msg[i] < msg[minInd]:  # only update when strictly smaller
            minInd = i
    return minInd


'''
update: runtime exceeded, but hint: there are only a-z lowercase letters

checked the solutions:
we were actually so close lol
iterate through msg once, tally how many of each letter
iterate through msg again, push every letter onto stack
and diminish on the tally to indicate letter used.
then check if the top of the stack is smaller or equal
to the smallest possible letter in the remaining msg not
scanned yet (i.e. smallest on the right side of the iter)
and if so straightaway that is appended to res, and check 
the next top elem in the stack, keep doing it and you get the solution

'''
def faster2434(msg):
    res = []
    stack = []
    arr = [0 for i in range(26)]
    for eachChar in msg:   #populate frequency array
        arr[ord(eachChar) - ord('a')] += 1

    for eachChar in msg:
        stack.append(eachChar)
        arr[ord(eachChar) - ord('a')] -= 1  #indicate char accounted for. diminish tally
        remainingMin = constMinScan(arr)
        while len(stack) > 0 and stack[-1] <= remainingMin:
            res.append(stack.pop())
    while len(stack) > 0:
        res.append(stack.pop())
    return ''.join(res)


'''
a constant runtime cost method to determine remaining minimal char 
'''
def constMinScan(arr):    #arr = [a,b,c,...,d] where len(arr) == 26, arr[i] is number of chars at order ord('a')+i
    for i in range(len(arr)):   #const since len(arr) == 26 always
        if arr[i]>0:
            return chr(ord('a')+i)
    return chr(ord('z')+1)   #when all characters are used, indicate any character is good (basically jus to capture 'z')



if __name__ == '__main__':
    msg = "vzhofnpo"
    print(q2434(msg))
    print(faster2434(msg))
