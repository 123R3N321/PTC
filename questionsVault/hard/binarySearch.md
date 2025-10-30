### Binary search can be pretty hard too
even though we brush through this topic
close to the beginning of 1134
<sub>This topic can be particularly 
useful for AlgoI, as 
binary search is a recurring 
theme in that class</sub>

The question:

> Koko eats banana (a leetcode classic)
> you are given a list of ints,
> representing multiple piles of bananas
> given a time limit h, find the speed,
> integer k, at which Koko must be 
> eating the bananas
> such that he has enough time to eat all
> the bananas in all the piles.
> Note that Koko spends at least 1 hr 
> at a pile of banana,
> and that even if Koko could in theory
> eat a pile of banana in less than an hour,
> we need to round it up. For example:
> piles = [0,1,2,3,3], h = 6
> then k = 2 is necessary, because:
> Koko spends no time with the first pile,
> which is empty (0 bananas)
> Koko spends one hour with the second pile 
> because there is 1 banana and he has to 
> spend at least one hour.
> Koko spends 1 hour with the third pile,
> because there are 2 bananas and he can eat
> 2 bananas per hour, just nice.
> And lastly, he spends 2 hours with each of the
> last two piles, as he cannot finish 3 bananas
> within 1 hour.
> So total time spent is 0+1+1+2+2 = 6
> if Koko eats at any rate that is slower
> (which can only be 1), then he will spend
> 0+1+2+3+3 = 8 hours to each all the bananas
> You must find the smallest number k
> such that when Koko eats k bananas per hour,
> he can eat all the bananas within h hours.

---

You must be able to see that:
- this is mission impossible if
h<len(piles), because Koko spends
at least one hour per pile
and if there are more number of
piles than the hours given, Koko
cannot finish all the bananas in 
time
- k = 1 is the smallest possible 
value unless there is no banana
at all; and that when k = 1,
it is implied that sum(piles)<=h:
there are at most as many bananas
as there are hours allowed for 
Koko to eat, so Koko only has to
leisurely eat one banana per hour
- And if we consider how fast Koko
has to eat the bananas in the worst
case, it is k = max(piles), because
eating any faster and Koko won't 
be able to finish all the bananas
anytime sooner; he is only spending
one hour with each non-0 pile already
and this time cost cannot be reduced 
any further.

---

After the above analysis, we de facto
do not have any additional strategy
to make the problem even simpler.
we have: 

- k_max = max(piles)
- k_min = 1

and, let's just say the best answer is k_star,
(note that, in AI CS6063, something_star
is the standard lingo to indicate the optimal
value for some task.)
then:

** h>=sum(math.ceil(each/k_star) for each in piles) **

and the rest is really just "brute force"
the best solution. And by "brute force"
I mean to binary search within the range of 
1 and max(piles).

---

recall the code structure of vanilla, standard bianry search:
```python
def bSearch(target,arr):
    l = 0
    r = len(arr)-1
    while l<r:
        m = (l+r)//2
        val = arr[m]
        if val<target:
            l = m+1
        elif val>target:
            r = m-1
        else:   # implied val == target exactly
            return m
    return -1   #indicate failure of the search
```
The above structure is the most braindead approach to
bianry search, and there is a lot of space for us to 
make the code more robust (search for closest match when
``target`` is not in ``arr``, this is how ``bisect``
module works.) or run with fewer lines. But the 
above structure is very, very intuitive and readable:
look at the middle element. If it is too small, we
abandon the entire left half of the array and only 
look at the right half, and of course we abandon
the middle element too, hence ``l = m+1``; else if 
it is too big, we abandon the entire right side of 
the array and look at the left side, and of course 
we abandon ``mid`` as well, hence ``r = m-1``
The loop control condition, ``l<r``, is lenient:
it will work even if we choose ``l<=r`` because
as long as the loop continues, l always goes up
and r always goes down.

---

The above solution will not suffice at all, but it
will be able to find us ONE solution to the question:
it will find a k value that will satisfy the conditions:

```python
import math
def calculateTime(k,piles):
    return sum(math.ceil(each/k) for each in piles)

def dumbBSearch(h, piles):
    k_min = 1
    k_max = max(piles)
    while k_min<k_max:
        k_star = (k_min+k_max)//2
        time_needed = calculateTime(k_star,piles)
        if time_needed<h:
            k_min = k_star+1
        elif time_needed>h:
            k_max = k_star - 1
        else:
            return k_star
    return -1
```
which is non-sensical: the moment we have
``time_needed<h``, the ``k_star`` value is 
one possible answer, just that we do not know 
if it is the best (a.k.a smallest possible) 
``k_star`` value.

---

### the thinking approach:

we agree that as k increases from 1 
to max(piles), at some point the k
value is big enough such that
time needed is less than h,
and we want to find the smallest such 
k value. Keep in mind, k goes up and
time needed will go down. Thus, let's
look at the correct solution
(I also deliberately renamed the
varaibles to make is 1. more abstract
and 2. adhering to bSearch structure 
better)

```python

def calcT(k,piles):
    return sum((each+k-1)/k for each in piles)

def edgeCase(h,piles):
    return len(piles)>h

def correctbSearch(h, piles):
    if edgeCase(h,piles):
        return -1
    l = 1
    r = max(piles)
    while l<r:
        m =(l+r)//2
        t = calcT(m,piles)
        if t>h:
            l=m+1
        else:  #implied t<=h
            r = m
    return l
```

This solution looks highly abstract, but we can 
build incrementally strong mathematical argument
for each step we take.

(tbc ...)
