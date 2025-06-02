'''
This is the "scratchbook" for the
leetcode 75 collections.

problems which are too easy are just deleted after I finished them here
mildly hard ones, I might leave behind notes
truly hard and intersting ones, I will have implementation and
in-detail analysis
'''


'''
leet 238 is the first question I encounter in leet75
that has me puzzled for a bit

below is the "naive" solution I get from a hint in discussion section
and it is an ugly solution haha

compute the cumulative product from left side 
and from right side
and at each ind position you just need the product of the left
and right side.

update: this is the correct solution. Lame.
'''
def l238hint(arr):
    prod = 1
    left = [1]  # put a dummy 1 there makes the code easier
    right = []
    res = []
    for i in arr:
        prod*=i
        left.append(prod)
    prod=1
    for i in arr[::-1]:
        prod*=i
        right.append(prod)
    right.reverse() #remember to flip it!
    right.append(1) # makes the code easier. really trivial

    for i in range(len(arr)):
        res.append(left[i]*right[i+1])
    return res

'''
now, the question also claims there is a way to make the
solution O(1) extra space

my idea from the hint:
trivial improvement by
first put all values from input to a res arr
and the convert the input in-place to right arr
and the output array is in-place computed to be left arr
and then "absorb" the now mutated input arr into res arr
pretty dumb, I gotta say

update: yeah this is indeed the correct solution. lame lame.
'''



'''
The discrete math logic:    (my real failure in developing the best answer is the failure in discrete math)

# edge case of fewer than 3 elems, automatically fail
 start with the first two elements in the array,
 start walking toward the right one by one
 if the current is smaller or equal to the first:
    set current to be the first
    we do not need to bother with anything else. Move on to next element
if the current is bigger than the first (this simply means "else") AND the current is smaller than the second element:
    set the current to be the second element
    we do not need to bother with anything else. Move on to next element
if the current is bigger than the first, AND bigger than the second, (else. By this point we filled out the universal set):
    set the current to be the third, which is unnecessary because by now we can return True.


'''
def q334(arr):
    if len(arr)<3: return False
    first = max(arr)+1
    second = max(arr)+1
    for each in arr:
        if each<=first:
            first = each
        elif each<=second:  #the "elif" implies that current element is bigger than "first", but not bigger than the second
            # but you also have to think FORWARD
            # when a current element is indeed smaller than second
            # we go on to next iteration while remembering
            # the current element to be the one to pass the "second check"
            second = each
        else:   # the else implies an element is bigger than both first and second
            return True
    return False



def q11(arr):
    i1 = 0
    i2 = len(arr)-1
    res = findArea(arr, i1, i2)
    while i1<i2:
        curr1 = arr[i1]
        curr2 = arr[i2]
        if curr1<curr2:
            i1 += 1
            res = max(res, findArea(arr, i1, i2))
        elif curr2<=curr1:
            i2 -= 1
            res = max(res, findArea(arr, i1, i2))
    return res



def findArea(arr, i1, i2):
    return (i2-i1)*min(arr[i1], arr[i2])

# test code
if __name__ == '__main__':
    arr = [1,8,6,2,5,4,8,3,7]
    print(q11(arr))
