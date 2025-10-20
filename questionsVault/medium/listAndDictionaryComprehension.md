comprehension, to be honest, is a trivial field. I will be talking
about the pragmatic usage under the two situations I encounter.

### convenient setup of array/nested array. The most rominent case is for dynamic programming related questions. In particular:
```python
n = 10
lst = [[] for _ in range(n)]
anotherLst = [[]*n]
```
raises the question of shallow vs deep copy

### Very specific case when comprehension gives performance edge
very niched case but used in ``Lab5`` of 1134, where:

```python

import ctypes

def make_array(n):
    return (n * ctypes.py_object)()

class ArrayList:
    
    def __init__(self, iter_collection = None):
        self.data = make_array(1)
        self.n = 0
        self.capacity = 1
    
    ...# some code
    
    def __repr__(self):
        return ("[" + ", ".join("'"+val+"'" if isinstance(val, str) else str(val) for val in self.data) + "]")
        # the if statement adds ' ' if type is str else convert it to str( )
```
Is a highly unusual case that demonstrates the necessity of list comprehension for runtime performance reasons.

## And lastly, for index-value mapping inversion
which is very specifically used for restoration of tree structure using two
traversals (pre + in or post + in ), such as [leetcode105](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/description/)
where an inversion is needed for the final solution:
```python
inorder = [...]

inmap = {val:ind for ind, val in enumerate(inorder)}
anotherInmap = {inorder[j]: i for i in range(len(inorder)) for j in range(len(inorder)) if inorder[j] == inorder[i]}
```
where the second approach, without ``enumerate()`` function, is inefficient.

---
<sup>side note: even though leetcode105 is considered too difficult for the course to code,
manual re-construction when given two traversals is an expected skill on the final.</sup>

