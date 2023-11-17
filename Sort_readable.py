#merge sort code
def merge_sort(a_list):
    if (len(a_list) <= 1):
        return a_list
    else:
        first_half = a_list[: len(a_list)//2]
        second_half = a_list[len(a_list)//2:]
        first_half = merge_sort(first_half)
        second_half = merge_sort(second_half)
        return merge(first_half,second_half)
#
#
def merge(list1, list2):
    first_iter = second_iter = 0
    result = []
    while (first_iter < len(list1) and second_iter < len(list2)):#careful, we do not cover edge cases here.
        if (list1[first_iter] < list2[second_iter]):
            result.append(list1[first_iter])
            first_iter += 1
        else:
            result.append(list2[second_iter])
            second_iter += 1
    result.extend(list1[first_iter:])
    result.extend(list2[second_iter:])
    return result

#heap sort code

def iterative_heapify(lst, size): # this is reverse max heap building. This is a more intuitive iterative approach
    begin = size - 1
    while begin >= 0:
        branch_end = begin
        while branch_end != 0:
            prev = branch_end // 2
            if lst[branch_end] > lst[prev]:
                lst[branch_end], lst[prev] = lst[prev], lst[branch_end]
            branch_end //=2
        begin -= 1




def recursive_branch_swap(lst, size):
    if(size <= 1):
        return
    node = size//2 - 1
    if lst[size-1] > lst[node]:
        lst[size-1], lst[node] = lst[node], lst[size-1]
    recursive_branch_swap(lst, size//2)


def recursive_heapify(lst, size): # this is a fancier looking recursve max heap building
    if(size <= 1):
        return
    recursive_branch_swap(lst, size)
    recursive_heapify(lst, size - 1)


# def recursive_heapify(lst): # this is a fancier looking recursve max heap building
#     if(len(lst) <= 1):
#         return
#     recursive_branch_swap(lst, len(lst))
#     recursive_heapify(lst[:-1])
#the above approach is simply wrong cuz slicing creates copy. recursion fails to modify in place

def iterative_extract(lst): #this time, however, the iterative approach is less intuitive compared to the recursive one
    begin = len(lst) - 1
    while begin >= 0:
        iterative_heapify(lst, begin + 1)
        lst[begin], lst[0] = lst[0], lst[begin]
        begin -= 1


def recursive_extract(lst, size): # the last step in recursive max heap building
    if(size <= 1):
        return
    recursive_heapify(lst, size)
    lst[size - 1], lst[0] = lst[0], lst[size - 1]
    recursive_extract(lst, size - 1)


# lst = [1,3,2,4,5,7,9,8,6]
# #recursive_extract(lst,9)
# iterative_extract(lst)
# print(lst)



def recursive_ruler(n):
    if n <= 1:
        print("-")
        return
    recursive_ruler(n-1)
    print("-"*n)
    recursive_ruler(n-1)
#
# recursive_ruler(4)
























































class BinartSearchTreeMap:
    class Item:
        def __init__(self, key, value=None):
            self.key = key
            self.value = value


    class Node:
        def __init__(self, item):
            self.item = item
            self.parent = None
            self.left = None
            self.right = None

        def num_children(self):
            count = 0
            if(self.left is not None):
                count += 1
            if(self.right is not None):
                count += 1
            return count

        def disconnect(self):
            self.item = None
            self.parent = None
            self.left = None
            self.right = None


    def __init__(self):
        self.root = None
        self.n = 0

    def __len__(self):
        return self.n

    def is_empty(self):
        return (len(self) == 0)


    # returns value, or raises exception if not found
    def __getitem__(self, key):
        node = self.find_node(key)
        if(node is None):
            raise KeyError(str(key) + " not found")
        else:
            return node.item.value

    # return node with key, or None if not found
    def find_node(self, key):
        cursor = self.root
        while(cursor is not None):
            if(cursor.item.key == key):
                return cursor
            elif(cursor.item.key > key):
                cursor = cursor.left
            else: # (cursor.item.key < key
                cursor = cursor.right
        return None


    # updates value if key already exists
    def __setitem__(self, key, value):
        node = self.find_node(key)
        if(node is not None):
            node.item.value = value
        else:
            self.insert(key, value)

    # assumes that key is not in the tree
    def insert(self, key, value):
        new_item = BinartSearchTreeMap.Item(key, value)
        new_node = BinartSearchTreeMap.Node(new_item)
        if(self.is_empty() == True):
            self.root = new_node
            self.n = 1
        else:
            parent = None
            cursor = self.root
            while(cursor is not None):
                parent = cursor
                if(key < cursor.item.key):
                    cursor = cursor.left
                else:
                    cursor = cursor.right
            if(key < parent.item.key):
                parent.left = new_node
            else:
                parent.right = new_node
            new_node.parent = parent
            self.n += 1


    # raises an exceprion if ket not in the tree
    def __delitem__(self, key):
        node = self.find_node(key)
        if (node is None):
            raise KeyError(str(key) + " not found")
        else:
            self.delete_node(node)

    # assumes the key is in the tree + returns item that was removed from the tree
    def delete_node(self, node_to_delete):
        item = node_to_delete.item
        num_children = node_to_delete.num_children()

        if(node_to_delete is self.root):
            if (num_children == 0):
                self.root = None
                node_to_delete.disconnect()
                self.n -= 1

            elif (num_children == 1):
                if (self.root.left is not None):
                    self.root = self.root.left
                else:
                    self.root = self.root.right
                self.root.parent = None
                node_to_delete.disconnect()
                self.n -= 1

            else:  # num_children == 2
                max_of_left = self.subtree_max(node_to_delete.left)
                node_to_delete.item = max_of_left.item
                self.delete_node(max_of_left)

        else:
            if(num_children == 0):
                parent = node_to_delete.parent
                if(node_to_delete is parent.left):
                    parent.left = None
                else:
                    parent.right = None

                node_to_delete.disconnect()
                self.n -= 1

            elif(num_children == 1):
                parent = node_to_delete.parent
                if(node_to_delete.left is not None):
                    child = node_to_delete.left
                else:
                    child = node_to_delete.right

                if(node_to_delete is parent.left):
                    parent.left = child
                else:
                    parent.right = child
                child.parent = parent

                node_to_delete.disconnect()
                self.n -= 1

            else: #(num_children == 2)
                max_in_left = self.subtree_max(node_to_delete.left)
                node_to_delete.item = max_in_left.item
                self.delete_node(max_in_left)

        return item

    def subtree_max(self, subtree_root):
        cursor = subtree_root
        while(cursor.right is not None):
            cursor = cursor.right
        return cursor


    def inorder(self):
            if (self.root is None):
                return
            else:
                yield from self.inorder(self.root.left)
                yield self.root
                yield from self.inorder(self.root.right)


    def __iter__(self):
        for node in self.inorder():
            yield node.item.key



#below to be deleted
# Python program to show working
# of has_key() method in Dictionary

# Dictionary with three items
Dictionary1 = {'A': 'Geeks', 'B': 'For', 'C': 'Geeks'}

# Dictionary to be checked
print("Dictionary to be checked: ")
print(Dictionary1)






