'''
this seems a super interesting puzzle
first thought:
write a (recursive) omni-number system converter (into string, of course)
and just do a place by place comparison

update: brute solution works but too slow
'''

def omniBase(decinum, base, res):
    if decinum<base:
        res.append(str(decinum))
        return
    omniBase(decinum//base, base, res)
    res.append(str(decinum%base))

def recurPali(resLst,start):
    if start>=len(resLst)-start:
        return True
    return recurPali(resLst, start+1) and resLst[start]==resLst[len(resLst) - start - 1]

def q2081(amount, base):
    if amount<base:
        return amount*(amount+1)//2
    if amount==base:
        return (amount)*(amount+1)//2 + 1

    # now we can work on quick paligen with decimal
    if base<9:
        startDeci = base+1
        ct = base   #base amount of pali already generated
        accum = base*(base+1)//2 + 1    #this amount of sum we already have
    else:   #base can only be 9 in this case
        startDeci = 8
        ct = 8
        accum = 36
    while ct<amount:
        curPaliDeci = paliGen(startDeci)
        startDeci = curPaliDeci
        res = []
        omniBase(curPaliDeci, base, res)
        if recurPali(res, 0):
            ct+=1
            accum+=curPaliDeci
    return accum
'''
wait, let's rethink this
since we are interested in the sum of first n-th such numbers,
there are the following obvious cases:
    -> first k-1 such numbers are definitely good (they are single digits)
    -> the k-th such number has value k+1 (they are obviously "11", k*1 + 1)
so in theory If I can get a kind of common formula for numbers beyond k,
I can solve this in constant runtime. Especially with the promise of n<=30

update:
    -> I do not see such a pattern. However
    can I find all pali decimal numbers fast 
    so that the runtime is significantly reduced?
        ->11,22,33,.....
        101, 111, 121, 131, ...
        202, 212, 222,...
        303, 313, 323,...
        ...
        1001, 1111, 1221, 1331,...
        2002, 2112, 2222, 2332,...
        ...
        10001, 10101, 10201, ...
        11011, 11111, 11211. ...
        12021, 12121, 12221, 12321, 12421, ...
        13031, 13131, 13231, 13331, ...
        
common pattern: 
for even amount of digits, first half is deterministic (easy)
for odd amount of digits, len//2 first digits deterministic,
and plus one free "pivot" digit

problem: ensure increment order
solution: amount of digit is represented by x where 10^x gives
        a rough scope of the number, AND ensures increment order
        
almost certainly list approach
digit increment->list append
alternatve existence of "pivot"
    -> single, triple, quinta digits have middle pivot
signal to bump: prev+1 = 10^x -> logBase10 is int

        
'''

'''
given a previous pali decimal num, generate the next one
'''
def paliGen(prev):
    if isPow10(prev+1):
        return prev+2   #going from 99...9 to 100...1 easycase

    #at this point we ruled out possibility of a num 9...9
    #two pointer approach will work
    numLst = digitSeparation(prev)
    symmetricBump(numLst)
    return digitCombination(numLst)

'''
return bool
check if a number is exact power of 10
'''
def isPow10(num):
    if num<=1:
        return True
    return num%10==0 and isPow10(num//10)

'''
separate a number into individual digits return list
'''
def digitSeparation(num):
    res = []
    while num>0:
        res.append(num%10)
        num//=10
    res.reverse()
    return res

def digitCombination(numLst):
    res = 0
    mul = 1
    for each in numLst[::-1]:
        res += mul*each
        mul *= 10
    return res
'''
given a list of digits that forms pali
in-place produce the next one
does not work on 9...9 
'''
def symmetricBump(numLst):
    if len(numLst)%2 != 0 and numLst[len(numLst)//2] !=9:
        numLst[len(numLst) // 2] +=1
    else:
        if(len(numLst)%2 != 0): #odd length list but middle ind is 9
            numLst[len(numLst) // 2] = 0
            startInd = len(numLst) // 2 + 1
        else:   #even length list
            startInd = len(numLst)//2
        while numLst[startInd] == 9:
            numLst[startInd] = 0
            numLst[-startInd-1] = 0
            startInd += 1
        numLst[startInd] +=1
        numLst[-startInd-1] += 1


'''

'''

if __name__ == '__main__':
    k = 9
    n = 10
    print(q2081(n,k))
    # print(isPow10(1000))
    # print(paliGen(1292921))