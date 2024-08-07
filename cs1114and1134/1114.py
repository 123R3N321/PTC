'''
this is all 1114 problems
'''

#########################################################################################
'''
tested concepts: 
    dictionary
    ASCII and chr() func
    random, and randint() method
    list comprehension
'''

import random
# dictionary, the concept: you cannot modify the map while accessing (iterating thru) it

# first, create a dictionary with keys A-Z but missing random letters in the middle
map = {}

for i in range(26):
    map[chr(i+65)] = [i for i in range(0, random.randint(3,9))]

del map[chr(random.randint(0,12)+65)] #btw, randint upperbound is inclusive, one more trap!
del map[chr(random.randint(13,25)+65)] #btw, randint upperbound is inclusive, one more trap!
# we can ask the candidate to take out two randints, one in first half one in second half of 26

check = [chr(i+65) for i in range(26)]  #ask student to list comprehension 26 letters

# next, ask the candidtate to find missing letter key in map and fill it

def wrong():    # you cannot modify map when iterating it!
    for key in map:
        if len(map[key]) < 7:
            del map[key]
def right():    #this is how it is fixed!
    keys_to_delete = [key for key in map if len(map[key])<7]

    # Remove the keys after iteration
    for key in keys_to_delete:
        del map[key]


#####################################################################################
