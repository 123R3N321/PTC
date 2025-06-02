'''
given n candies and limit among of upper limit of candies per kid
find all permutations of distributing the candies
among 3 kids
eg: n=5, limit=2
return 3
because:
1-2-2
2-1-2
2-2-1

are all the possible answers
'''

'''
thinking:
simple dfs

state1: 0:min(limit, n) #give the first kid between 0 and either all, or limit number of candies, whiever is smaller (limiting factor)

state2: 0: min(limit, n-state1)

state3: 0: n-state1-state2

check: if state 3 is legal (state 1 and 2 guaranteed legal)
        0<=state3<=limit, and state1+state2+state3 == n

update from hints:
    approach correct, for loop logic not necessary, can
    replace with math logic of O(1) runtime
'''

def candyDFS(n, limit):
    total = 0
    for i in range(min(limit+1,n+1)):
        for j in range(i,min(limit+1, n-i+1)):
            if n-i-j<=limit:
                if i==j:
                    total += 1
                else:
                    total+=2
                # print(f'debug: {i},{j},{n-i-j} : {total}')
    return total

def candyMath(n,limit): #derived from hint
    total = 0
    #for loop range: first kid can get from 0 to the most candies, limiting factor either n or limit
    for i in range(min(limit+1,n+1)):
        #min(limit,n-i) computes max amount of candies that can be gien to second child
        #inside the same iteration,n-i-limit<0 means the third child won't get
        #too many candies, since n-i indicates all candies remaining to be shared by
        # the two kids, thus we can safely count as solution
        # on the other hand, when n-i-limit>0, n-i>limit,
        # the remaining candie to be shared between two kids is greater than limit
        # we now check if the amount of candies taken by the second kid alone
        # allows the remianing candies to decrease below limit, of course now
        # we want 2nd child to get max candies so third child won't risk
        # getting too many. when:
        # (max candies possibly taken by 2nd child) - (total amount taken by 3rd child)<0
        # it means the 3rd child will have to take more than even the max possible
        # for one single kid, we cannot count this as solution.
        total+=max(min(limit, n-i)-max(0,n-i-limit)+1,0)
    return total


#TODO: read this comprehensive version of solution
#developed by myself and is wayyy more readable than the crap above.
def candyMathComprehensive(n,limit):
    total = 0
    # first kid can get any number of candies between 0 and upper bound inclusive, which has limiting factor either n or limit
    for i in range(min(limit+1,n+1)):
        if n-i<=limit:  #remaining candy for two kids combined is below limit
            # also n-i guaranteed positive since i is in range of limit or n whichever is smaller
                total += n-i+1    #for each i value (each amount given to first kid) we have "remaining candy+1" number of ways to give to the other two kids
        else:   #remaining candies to be shared is greater than limit, but we might be able to do it right
            if n-i<=2*limit:    #as long as total remaining candies do not exceed double the limit, we have solutions
                    # give the 2nd child most candies (which is limit) and remaining is definitely <=limit, this is one way
                    # give the 2nd child least acceptable candies, which is k, such that n-i-k==limit, this is one way
                    # any distribution in between where k<= 2nd kid candies <= limit, is a solution
                    # essentially we have limit-k+1 number additional solutions.
                    # obviously n-i-limit==k from above math,
                    # so we have limit-k+1 == limit- (n-i-limit)+1 ==2*limit + i-n+1 additional solutions
                total+= 2*limit+i-n+1
    return total



#TODO: think: what if the number of kids is also parametrized?
'''
theory: every additional kid adds complexity by factor of n:

both one and two kids, O(1) because one mathematical operation give you the answer
three kids, O(n), because for each possible number of candy given the third child, you solve the one and two kids problem once
four kids will be O(n^2) for each possible number of candy given to the fourth child, solve three-children problem once.
Thus we can construct recursive solution.
'''


if __name__ == '__main__':
    n=3
    limit=3
    print(candyDFS(n,limit))
    print(candyMath(n,limit))
    print(candyMathComprehensive(n,limit))