'''
this is all 1114 problems
'''
import copy

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
lst = [1,1,1]
lst.insert(1,3)
print(lst)
n = 5
# for i in range(n):
#     print(" "*(n-1-i),'X'*(2*i+1))
lst2 = [i*i if i%2==0 else i for i in range(1,n+1)]
print(f"lst2 is: {lst2}")

a = [1,2,3,[4,5,6]]
b = copy.deepcopy(a)
c = a
c[3][1]*=10
a[0] = 0
b[3][2] = 1
print(f"a is: {a}")
print(f"b is: {b}")
print(f"c is: {c}")
print("-------------------------")

total = 298.05
denom = 60

emma = 10
ms = 20
varya = 15
ren = 15

def calc(ra):
    global total, denom
    return (ra/denom)*total

print(f"emma is: {calc(emma)}\tms is: {calc(ms)}\tvarya is: {calc(varya)}\tren is: {calc(ren)}")

n = 6
k = n&(n-1)
if (k):
    print()
else:
    print("don work")

print()
lst = [x**2 if not x%2 else x for x in range(1,6) ]
print(lst)
lst.remove(3)
print(lst)

def recur(root):
    if not root:
        return
    root.left, root.right = root.right, root.left
    recur(root.left)
    recur(root.right)