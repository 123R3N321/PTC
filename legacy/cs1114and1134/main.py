import sys, hmac, hashlib, base64

# Unpack command line arguments
username = "b40854b8-80b1-70cd-c62f-3cb69806472f"

app_client_id = "7o8uqs65f60has4bohtth888sl"

key = "11ovugh5r1kob44ui2591e7ml4atm17o7219o6m9mfc2bip9rdqe"

# Create message and key bytes
message, key = (username + app_client_id).encode('utf-8'), key.encode('utf-8')

# Calculate secret hash
secret_hash = base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode()

print(f"Secret Hash for user '{username}': {secret_hash}")

print("------------")
# def test(n):
#     i = n
#     res = 0
#     ct = 0
#     while i>1:
#         for j in range(i):
#             res+=7
#             print(f"did {ct}th time")
#             ct+=1
#         i//=2
#     return res

# this is just some dummy stuff
print("---------")
#the func below is some random geeksforgeeks intro to recursion
# def recur(lst, bp, k, res):
#     if k<=0:
#         print(res)
#         return
#     for i in range(bp, len(lst)):
#         recur(lst, i+1, k-1, res+str(lst[i]))
# 
# def doubleCt(word, left, right):
#     if left>=right:
#         return (0,0)
#     cur = word[left]
#     localA, localB = cur in "aeiou",cur not in "aeiou"
#     a,b = doubleCt(word, left+1, right)
#     return tuple([localA+a, localB+b])
# 
# def weird(lst):
#     if len(lst)<=1:
#         print(lst)
#         return
#     local = [a+b for a,b in zip(lst, lst[1:])]
#     weird(local)
#     print(lst)
# 
# def expNarrow(nums,target,bp=1):
#     if bp>=len(nums)//2:
#         return bp
#     if nums[bp]>=target:
#         return bp
#     return expNarrow(nums,target,2*bp)

# note on reversal:

def recurNestedRev(lst):
    for i in range(len(lst)):
        if isinstance(lst[i], list):
            recurNestedRev(lst[i])
    reverseTopLevel(lst)    #which honestly is just .reverse()

def reverseTopLevel(lst):
    for i in range(len(lst)//2):
        lst[i], lst[len(lst)-i-1] = lst[len(lst)-i-1], lst[i]

'''
treat nested lst like a tree and use dfs to generate bfs to check
itentical-ness
-----
nah that wastes too much space
let's do pre-in-place double iteration test
'''
def DFScheck(lst1,lst2):
    inres1,inres2,pres1,pres2 = [],[],[],[]
    inorder(lst1,inres1)
    inorder(lst2,inres2)
    preorder(lst1,pres1)
    preorder(lst2,pres2)
    return inres1 == inres2 and pres1 == pres2

def inorder(nestedLst,res):
    for each in nestedLst:
        addend = None
        if isinstance(each, list):
            addend = "lst"
            preorder(each,res)
        else:
            addend = each
        res.append(addend)

def preorder(nestedLst,res):
    for each in nestedLst:
        if isinstance(each, list):
            res.append("lst")
            preorder(each,res)
        else:
            res.append(each)
import copy
if __name__ == "__main__":
    # lst = ['a','b','c','d']
    # k = 3
    # recur(lst, 0, k, "")
    word = "aeeeioucxcsxc" # 7 and 6
    # print(doubleCt(word, 0, len(word)))
    # lst = [i+1 for i in range(10)]
    # # weird(lst)
    # print(f"lst: {lst}")
    # print(expNarrow(lst,5))
    # print(expNarrow(lst,5))
    lst = [1,[2],[[3],4],[[[[5]]]],6,7,[8,[9]],10]
    lst2 = copy.deepcopy(lst)
    recurNestedRev(lst)
    recurNestedRev(lst)
    print(DFScheck(lst,lst2))