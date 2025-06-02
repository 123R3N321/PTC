'''
a leetcode daily
'''

'''
plan:
dictionary approach to pair up elems which can extend palindrome
for the "keystone" (the center of the pali), use a 
palindrome checker-helper to simply find the longest pali
'''

'''
first we need a method to determin max pali length
'''


def lenPali(msg):
    total = 0
    for i in range(len(msg)):
        if msg[i] != msg[-i - 1]:
            return 0
        else:
            total += 1
    return total


# # test code
# lst = ['12321','1233521','k','abba']
# for i in lst:
#     print(lenPali(i))

'''
ok now that we can find the keystone,
next step is to find match-ups of 
other parts. They must be pairs
'''


def flip(msg):
    res = ''
    for i in msg[::-1]:
        res += i
    return res


##test code
# print(flip('abc'))

'''
now this is like a match-cancel game
you see something for the first time,
add to dict
see its flip, eliminate
each time eliminate, add 2*len(elem) to total
in what remains, look for keystone
'''
def dictQuery(lst):
    dict = {}
    total = 0  # total length we can produce
    for i in lst:
        if i not in dict and flip(i) not in dict:   #neither it nor its flip is in
            dict[i] = 1
        else:
            if flip(i) in dict:   #found a match!
                dict[flip(i)] -=1   #cancel out
                total += 2* len(i)  #add to total
                if dict[flip(i)] == 0:
                    del(dict[flip(i)])
            else:   #note this implies also if the flip is NOT identical to the i, such as "mm"
                #the else could only mean that i is in dict
                dict[i] +=1


    cur = 0
    for i in dict: # now we check whats left
        if dict[i] >0:  #not cancelled out
            if lenPali(i)>cur:
                cur = lenPali(i)
    total+=cur
    return total





### test code
cands = ["mm","mm","yb","by","bb","bm","ym","mb","yb","by","mb","mb","bb","yb","by","bb","yb","my","mb","ym"]
print(dictQuery(cands))