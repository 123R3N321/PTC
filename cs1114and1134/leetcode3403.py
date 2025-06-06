'''
Not as easy as it seems at first glance.
first estabilish max single word length: maxLength = len(msg)-split+1

eg: msg = "abcde" (len 5)
    split = 2
    maxLength is 4 (a, and bcde)

and since we are doing lexicongraphic
the intuitive approach is:
scan entire string once look for max letter
    1.if there is a single such letter, we done

    2.else if we have multiple such letters:
        ->add all their indices+1 to a collection
        iterate through this collection, which has guaranteed len>1
            ->if there is a single max letter, we done
            ->if there are multiple max letters:
                ->repeat step 2 onwards

    edge case:
        1. multiple max words of max possible length achieved:
            ->use any of them. Can be arbitrarily the first one
        2. indices+1 reach the end of msg:
            2.1. when other indices are ok: auto lose filter out
            2.2. when all other indices have the same problem: not possible
                (consider ind x is len(msg)-1, then there
                DOES NOT exist y where y != x, 0<=y<x, and that y+1>=len(msg))
    return value:
        when the collection has one letter left only, backtrack starting point,
        return msg[starting point, min(maxLength+starting point, length of msg)]
'''
def q3403(msg, split):
    if(1==split):
        return msg
    maxLetter = ''   #smallest dummy word
    maxLength = len(msg)-split+1    #the longest possible length of the best substring
    arr= [] #array holding indices of maxLetters

    for i in range (len(msg)):
        curLetter = msg[i]
        if curLetter>maxLetter:
            maxLetter = curLetter
            arr.clear() #old max is superseded
            arr.append(i)
        elif curLetter==maxLetter:  # the undesirable case but ok
            arr.append(i)

    iteration = 0   #how many times have we done subsequent compare
    #first, the starting assumpitons:
        #len(arr)>1, more than one maxLetter
    #iteration<maxLength-1 where maxLength>1

    #second, the final conditions:
        #lenArr==1, we have singluar best answer
        #or, iteration==maxLength-1, we have a tie,
            #in that case, use any (ind 0 will do)
    while len(arr)>1 and iteration<maxLength-1:
        iteration += 1
        lexiCompare(msg,arr)    #modifies arr in-place

    return msg[arr[0]-iteration:min(maxLength+arr[0]-iteration,len(msg))]




'''
helper function that
assumes we have more than one best letter and that maxLength>1
in the msg. this function:

iterates through the collection, named arr, which has guaranteed len>1 
    ->attempt to check eachIndex+1 location (guaranteed to succed at least once)
        ->if overreaching, do nothing
        ->look for lexic best and add to another collection to be returned
    ->keep doing so until either the other collection is len==1 or
    when we reach maxLength of substring
    
    ->if collection length 1 we good
    ->if maxLength reached, blindly return 0-th elem in collection
    UPDATE: instead of return, modify in-place

update: modularization by using the fucn for one iteration each
        in that case we do not even take care of maxLength
        
 
'''
def lexiCompare(msg, arr):
    maxWord = '' #a dummy word that is smallest possible
    res = []    #result array
    for eachInd in arr: #arr holds multiple indices of best letters (all of them the same letter lmao)
        if eachInd+1<len(msg):  #check for overreach
            if maxWord<msg[eachInd+1]:
                maxWord=msg[eachInd+1]
                res.clear() #old collection is superseded!
                res.append(eachInd+1) #add this to be returned later
            elif maxWord==msg[eachInd+1]: #multiple hits again, sigh
                res.append(eachInd+1)
    #then replace arr eith res. This saves a bit of memory
    arr.clear()
    for each in res:
        arr.append(each)

if __name__ == '__main__':
    msg = "aann"
    split = 2
    print(q3403(msg, split))
    print("ab">"b")