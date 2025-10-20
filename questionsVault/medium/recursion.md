When I was first introduced the concept of recursion, I had my mind blown, and
I struggled badly, badly with it. My observation when running labs nowadays is that,
actually, most people are pretty comfortable with it even when they are first exposed
to it. Which is a relief to a TA, but makes me can't-help-but-feel-so-ever-slightly-jealous.
Kids are so smart nowadays!

---

### Recursive VS Iterative
In general, iterative solutions are better in performance, while recursive code looks short
and stylish (sometimes). A good, cheap trick is to give a question that involves a for/while loop,
and ask the candidate to give the recursive version, or vice versa by using ``stack``.

---

### Really good recursion use case: recursive file search
The classic example from 1134 homework4 is the flattening of a
nested list. A even-better sample given by Evan for lab7 is as
follows:

> Write a recursive function that reverses the order of values of each list in the hierarchy.
> 
> Example:
> If lst =
> 
>[ [1, 2], 3, [4, [5, 6, [7], 8 ] ], [ [ [ [9] ] ] ]  ], 
> 
>deep_reverse(lst) should modify it so that it now has: 
>
> [ [ [ [ [9] ] ] ] , [ [8, [7], 6, 5 ], 4], 3, [2, 1] ], 

And the pseudo code is elegant:
```python
def recurNestedRev(lst):
    '''for each element in lst, if it is a list, then:'''
    recurNestedRev(lst[i])
    '''after recursive modification on next level, we:'''
    reverseTopLevel(lst)    #which honestly is just .reverse()
```
---