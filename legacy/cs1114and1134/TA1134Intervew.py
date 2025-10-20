'''
this is the workspace for
1134 interview, fall 2025
'''

'''
Q1: ADT duplicate stack: tracks consecutive elements

approach: instead of single value elements, store a list of len 2
    -> choice of list instead of tuple: mutable (trivial choice)
'''


class DupStack:
    def __init__(self):
        self.stack = []  # the stack itself is a list, note we push/pop from ind -1
        self.length = 0  # allows const time size check

    def is_empty(self):
        return self.length == 0

    def __len__(self):
        return self.length

    def push(self, value):
        if self.is_empty():
            self.stack.append([value, 1])
        else:  # in the case stack not empty
            if value == self.stack[-1][0]:  # in the case new val is same as top val
                self.stack[-1][1] += 1  # tally
            else:  # new val is distinct
                self.stack.append([value, 1])  # same as if case, readable style
        self.length += 1

    def top(self):
        if self.is_empty():
            raise Exception('stack is empty')
        else:
            return self.stack[-1][0]

    def top_dups_count(self):
        if self.is_empty():
            raise Exception("the dup stack is empty! No dup count!")
        else:
            return self.stack[-1][1]  # simply check the count of top elem

    def pop(self):
        if self.is_empty():
            raise Exception("the dup stack is empty! Nothing to pop!")
        else:
            self.length -= 1
            val = self.stack[-1][0]  # the value to be returned
            if self.stack[-1][1] <= 1:  # top elem has count of 1
                self.stack.pop()  # just pop it
            else:  # count more than 1
                self.stack[-1][1] -= 1  # reduce dup count
            return val

    def pop_dups(self):
        if self.is_empty():
            raise Exception("the dup stack is empty! Nothing to pop!")
        else:
            self.length -= self.stack[-1][1]  # all dup count at top level subtracted
            val = self.stack[-1][0]  # still keep track of the top val
            self.stack.pop()  # remove entire thing
            return val


'''
recursive bst construction from preorder traversal
simple DP approach, dfs manner

note that assuming no duplicate eliminates ambiguous case (nice!)

assume the tree is just the root note (instead of wrapped in a ADT), leetcode style
'''


class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


'''
essentially dfs approach
'''


def recur(lst, ind, bound):
    if ind >= len(lst) or lst[ind] > bound:
        return ind, None  # return pair of curr ind pos and the cur node
    root_val = lst[ind]
    # node = TreeNode(root_val)
    root_ind, left = recur(lst, ind + 1,    #scan forward one at a time
                           root_val)  # left traversal until either end of list or reach node of value above bound
    root_ind, right = recur(lst, root_ind, bound)  # root_ind updated by left recurse, bound not.
    return root_ind, Node(root_val, left, right)  # we only interested in the second in the pair


def bstFromPreorder(preorder):
    _, root = recur(preorder, 0, float('inf'))
    return root


# do a post order reconstruction cuz why not
def recurP(lst, end, bound):
    if end < 0 or lst[end] < bound:
        return end, None
    root_val = lst[end]
    end, right = recurP(lst, end - 1, root_val)
    end, left = recurP(lst, end, bound)
    return end, Node(root_val, left, right)


def bstFromPostorder(postorder):
    _, root = recurP(postorder, len(postorder) - 1, float('-inf'))
    return root


def print_tree(node, indent=0):
    if node is not None:
        print_tree(node.right, indent + 4)
        print(" " * indent + f"{node.val}")
        print_tree(node.left, indent + 4)


'''
some after thought on Q2, chat-gpt-ed
I think this approach is very elegant
'''


def bst_from_preorder(pre):
    i = 0  # shared index into pre

    def build(lo, hi):
        nonlocal i  # this syntax means it is not global, but in an outer scope
        # if next value is out of allowed range, it doesn't belong here
        if i == len(pre) or not (lo < pre[i] < hi):  # no repeating element, strict comparison is ok
            return None

        root_val = pre[i]
        i += 1
        node = Node(root_val)
        # left subtree: values < root_val
        node.left = build(lo, root_val)
        # right subtree: values > root_val
        node.right = build(root_val, hi)  # every element either falls to left or right, universal set achieved
        return node

    return build(float("-inf"), float("inf"))

'''
after interview with prof Tal, he prefers a
sub-optimal solution that might be closer
to the scope of the class
call it: passing in ind 0 and length of lst (upperbound exclusive)
'''

def subOptimal(lst, start, end):
    if start>=end:   #strictly greater than
        return None
    local = Node(lst[start])
    subStart = start+1
    while subStart < end and lst[subStart] < lst[start]:    #we skip to the end of left subtree
        subStart +=1
    local.left = subOptimal(lst, start+1, subStart)
    local.right = subOptimal(lst, subStart, end)
    return local

'''
Q3: re-write a remove_all(lst, val) func
such that it has linear runtime (instead of n^2)
I'll also add that it should be const extra space
(we can easily do a dumb comprehension that uses linear space)

approach: linear scan with bubbling, two pointer
'''


def remove_all(lst, val):
    top = 0
    for i in range(len(lst)):
        if lst[i] != val:  # keep only non-val elements
            lst[top] = lst[i]
            top += 1
    del lst[top:]  # remove trailing junk, alternatively lst = lst[:top]


# stupid approach to check result only
def dumb_remove_all(lst, val):
    lst[:] = [each for each in lst if each != val]


# test code
if __name__ == "__main__":
    dupS = DupStack()
    dupS.push(4)
    dupS.push(5)
    dupS.push(5)
    dupS.push(5)
    dupS.push(4)
    dupS.push(4)
    print("answer:  6\t4\t2\t4\t4\t5\t3\t5\t4")
    # print(len(dupS))
    # print(dupS.top())
    # print(dupS.top_dups_count())
    # print(dupS.pop())
    # print(dupS.pop())
    # print(dupS.top())
    # print(dupS.top_dups_count())
    # print(dupS.pop_dups())
    # print(dupS.top())
    ans = [6, 4, 2, 4, 4, 5, 3, 5, 4]
    check = []
    check.append(len(dupS))
    check.append(dupS.top())
    check.append(dupS.top_dups_count())
    check.append(dupS.pop())
    check.append(dupS.pop())
    check.append(dupS.top())
    check.append(dupS.top_dups_count())
    check.append(dupS.pop_dups())
    check.append(dupS.top())
    if check == ans:
        print("Q1: all tests passed")
    else:
        print("Q1: mistake.")

    print("=========End of Q1 Start of Q2===================")

    preorder = [9, 7, 3, 1, 5, 13, 11, 15]
    postorder = [1, 5, 3, 7, 11, 15, 13, 9]
    root = bstFromPreorder(preorder)
    rootP = bstFromPostorder(postorder)
    rootS = subOptimal(preorder, 0, len(preorder))
    print_tree(root)
    print("\n------------------------------------------------\n")
    print_tree(rootP)
    print("\n------------------------------------------------\n")
    print_tree(rootS)
    print("=========End of Q2 Start of Q3===================")

    lst = [9, 7, 13, 1, 5, 13, 11, 15]
    dupLst = lst.copy()
    val = 13  # try: single occur, diverse data type, multi occur, non-occur
    remove_all(lst, val)
    dumb_remove_all(dupLst, val)
    if dupLst == lst:
        print("Q3: all tests passed")
    else:
        print("Q3: mistake.")
