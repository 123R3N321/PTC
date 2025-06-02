'''
reconstruct bst from pre-order traversal
note this problem is of significance for CS1134 TA application
'''

'''
the tree definition. The root node is used as entry point of the tree
'''
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def recur(lst, start, bound):
    if start >= len(lst) or lst[start] > bound:
        return start, None
    root_val = lst[start]
    # node = TreeNode(root_val)
    left_ind, left = recur(lst, start + 1, root_val)
    right_ind, right = recur(lst, left_ind, bound)
    return right_ind, TreeNode(root_val, left, right)

def bstFromPreorder(preorder):
    _, root = recur(preorder, 0, float('inf'))
    return root

def print_tree(node, indent=0):
    if node is not None:
        print_tree(node.right, indent + 4)
        print(" " * indent + f"{node.val}")
        print_tree(node.left, indent + 4)

# preorder = [8, 5, 1, 7, 10, 12]
# # preorder = [4,2,1,3,6,5]
# root = bstFromPreorder(preorder)
# print_tree(root)

# control = 13
# dict = {}
# col1 = [chr(ord('a')+i) for i in range(control)]
# col2 = [i for i in range(control)]
# for i in range(len(col1)):
#     dict[col1[i]] = col2[i]
#
#
# print(f"whats n our collections?\n\tcollection1: {col1}\n\tcollection2: {col2}\n")
# print(f"whats in the dictionary now?\n\tdict: {dict}")
lst = [[i for i in range(1,6)] for j in range(1,6)]
print(f"lst before modification: {lst}")

for i in range(len(lst)):
    lst[i] = []

# for i in lst:
#     i = []

print(f"lst after modification: {lst}")
