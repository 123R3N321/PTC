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
'''
essentially dfs approach
'''
def recur(lst, start, bound):
    if start >= len(lst) or lst[start] > bound:
        return start, None
    root_val = lst[start]
    # node = TreeNode(root_val)
    root_ind, left = recur(lst, start + 1, root_val)
    root_ind, right = recur(lst, root_ind, bound)
    return root_ind, TreeNode(root_val, left, right)

def bstFromPreorder(preorder):
    _, root = recur(preorder, 0, float('inf'))
    return root




def recurP(lst, end, bound):
    if end < 0 or lst[end] < bound:
        return end, None
    root_val = lst[end]
    end, right = recurP(lst, end - 1, root_val)
    end, left = recurP(lst, end, bound)
    return end, TreeNode(root_val, left, right)

def bstFromPostorder(postorder):
    _, root = recurP(postorder, len(postorder) - 1, float('-inf'))
    return root



def print_tree(node, indent=0):
    if node is not None:
        print_tree(node.right, indent + 4)
        print(" " * indent + f"{node.val}")
        print_tree(node.left, indent + 4)





'''
constructing binary tree from two given traversals
is straightforward:

rule: no repeating elem (otherwise tree shape nondeterministic)

approach: look where the preorder first elem is in inorder
all the element sandwiched between that position and ind 0 in inorder
are left children (grandchildren, etc) of the preorder ind pos 0 elem
and all those on the right are the right children
recursively do this. essentially two pointer approach in a recursive way

also, always stick with the left-bound-inclusive, right-bound-exclusive rule.
'''

def buildTree(preorder, inorder):
    inorder_index_map = {val: idx for idx, val in enumerate(inorder)}#reverse mapping, very useful

    def helper(pre_start, pre_end, in_start, in_end):
        if pre_start >= pre_end or in_start >= in_end:
            return None

        root_val = preorder[pre_start]
        root = TreeNode(root_val)

        in_root_index = inorder_index_map[root_val]
        left_size = in_root_index - in_start

        root.left = helper(pre_start + 1, pre_start + 1 + left_size, in_start, in_root_index)
        root.right = helper(pre_start + 1 + left_size, pre_end, in_root_index + 1, in_end)

        return root

    return helper(0, len(preorder), 0, len(inorder))





if __name__ == '__main__':

    # preorder = [8, 5, 1, 7, 10, 12]
    preorder = [4,2,1,3,2.5, 6,5]
    postorder = [1,2.5,3,2,5,6,4]
    root = bstFromPreorder(preorder)
    rootP = bstFromPostorder(postorder)
    print_tree(root)
    print()
    print_tree(rootP)

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
