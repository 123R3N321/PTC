'''
I have no clue how to solve this so checked answer
'''

'''
update: surprisingly straightforward solution approach

my thoughts:
1.  the key is to reduce the problem into
    a greedy process: think that: in the order
    of "acceptable" to "best" answers:
    A: a letter that appears at least k times, AND is lexically small ->
    B: a letter that appears at least k times, AND is lexically big ->
    C: a sequence starting with A, with length +1 ->
    D: a sequence  starting with B, with length +1 ->
    E: repeate C but length +1 ->
    F: repeate D but length +1 ->
    ...
    
    The smart thing is that, you are certain that you can abandon A when B exists, B when C 
    exists, so on. This strongly imply a queue structure:
    enqueue in the order of single letter lexi increasing order that appear at least k times
    in the input
    
    Next, pop each and attempt to build one more letter into it, and of course try the additional
    letter in increasing lexi order, and if no such extension exists, we can simply abandon this
    popped letter 
    (because 1. if a seq of this letter plus one other letter does not exist, there wll be no
    more further seq that starts with this letter, and 2. from 1, we know that the next single
    letter in the queue is already a better answer, so we abandon the current letter)
    
    However, if a seq formed by adding one more letter does exist, simply enqueue this result
    (and we thus have a cycle of process that finds all answers)
    
2.  Trivial improvement: the moment we found all the letters that occur at least k times each,
    we know all possible final answer seq must be formed exclusively with these letters
    
    instead of trialing with all letters a-z, simply try in the lexi increasing order of all 
    these confirmed letters.

3. Trivial improvement: when in step 1, strip the string of the letters below k occurrences

*the most important part of this puzzle is: find the greedy approach*
*in other words, find the deterministic part and use that
to reduce the input size/amoung of indeterministic possibilities*

'''

'''
note we do not need the fancy kmp algo
since the matching is subseq matching
not exact sequence matching
'''
def seqMatch(fullStr, seq, amount):
    matchPos = 0
    ct = 0
    for eachLetter in fullStr:
        if eachLetter == seq[matchPos]:
            matchPos += 1
            if matchPos >= len(seq):
                matchPos = 0
                ct+=1
                if ct >= amount:
                    return True
    return False

from collections import deque
def qProcess(msg, k):
    #count letters in msg and only keep track of those ct>=k
    #at the same time construct inputStr made only of those letters
    ctArr = [0 for _ in range(26)]
    for eachLetter in msg:
        ctArr[ord(eachLetter) - ord('a')] += 1

    minimalArr = [] #use array not string for faster incremental building
    for eachLetter in msg:
        if ctArr[ord(eachLetter) - ord('a')] >= k:  #shows up at least k times
            minimalArr.append(eachLetter)   #order follows that of msg
    if not minimalArr:  #edge case: none of the letters show up k times at least
        return ""
    bag = []
    for i in range(len(ctArr)):
        if ctArr[i] >= k:
            bag.append(chr(ord('a') + i))   #build a minimal bag of letters

    #queue process: start with first letter in the bag
    #attempt to build extension one at a time by using one letter
    #from the bag and see if the extension result has k repetitions
    #which means seqMatch returns True
    q = deque()
    for eachLetter in bag:
        q.append([eachLetter])
    cur = [bag[-1]]   #at first, the lexi biggest single letter is the best answer
    while q:
        cur = q.popleft()
        if len(cur) >= len(msg)//k:
            continue    #skip cuz this is getting too long
        for eachLetter in bag:
            cur.append(eachLetter)  #try a letter from the bag
            if seqMatch(minimalArr, cur, k):
                q.append(cur.copy())  #it does have k repetitions or more, add (a deepcopy) to q
            cur.pop()   #restore it so we can try next possible extension
    return ''.join(cur)



'''
below is the dfs approach which is
exactly the opposite of my
incremental, greedy approach.
there is much to learn from it
'''

from collections import Counter #a dictionary subclass that counts hashable objects
                                # e.g Counter("banana") -> {'b':1, 'a':3, 'n':2}
class Solution:
    def longestSubsequenceRepeatedK(self, s: str, k: int) -> str:
        # n < k * 8 => n <= 250
        s = [ord(c) - ord('a') for c in s]  #index map of chars
        cnt = Counter(s)
        possible = {c for c, v in cnt.items() if v >= k}    # unordered index map of those with enough frequency
        possible_sort = sorted(possible)
        s = tuple(c for c in s if c in possible)    #index map following input order AND is frequent enough
        n = len(s)
        poses = [-1] * 26
        nextchar = []
        stat = [0] * 26
        for i in reversed(range(n)): # necessarily scanning backward
            c = s[i]
            stat[c] += 1    #stat[c] tracks the freq
            nextchar.append(poses[:])   # building matrix, dimension len(input) by 26
            poses[c] = i    #poses tracks ind pos of each char (char mapped to index)
        nextchar = nextchar[::-1]   #reverse it back to forward order
        nextchar.append(poses[:])
# nextchar matrix with query nextchar[i][c] is: "at ind pos i of original input string, find the
        # ind pos of the NEXT character c from i onwards not including i itself"

        def check(word, idx=-1, tot=k):
            nonlocal n, nextchar
            for _ in range(tot):
                for c in word:
                    idx = nextchar[idx][c]
                    if idx < 0:
                        return False
            return True

        result = []

        def prep(idx, word, wordstat):
            nonlocal result
            for c in reversed(possible_sort):
                word.append(c)
                wordstat[c] += 1
                if stat[c] >= wordstat[c] * k and check(word, -1, k):
                    if len(word) > len(result) or len(word) == len(result) and word > result:
                        result = word[:]
                    prep(idx, word, wordstat)
                wordstat[c] -= 1
                word.pop()

        prep(0, [], [0] * 26)

        return ''.join(chr(c + ord('a')) for c in result)


if __name__ == '__main__':
    msg = "etsleetcode"
    print(qProcess(msg, 2))