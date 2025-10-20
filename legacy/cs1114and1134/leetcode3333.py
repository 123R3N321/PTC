
'''
update: this is actually dp,
that is above my current knowledge
copy-paste code and analyse here
minimalize the code by ignoring the mod

summary:
1. complimentary set thinking: find correct answer by subtracting away all the wrong values
    essentially computing all possible numbers of strings formed for every single
    possible k value going from 0 till the actual k, then total - all the cases where k value is below the actual k
    dp table holds the prefix sums of such k values
2. exaggeration-then-compensate: assume each group has inifite letters, then subtract away
    all the actual impossibly values

this is prehaps the hardest leetcode in the entire past month, and
I have to say the solution approach is really, really smart and tricky

(btw, this solution assumes small k which is the case for this question)
'''
class Solution: # simply ignore all the way until we reach dp becasue the rest of the code is easy.

    def possibleStringCount(self, word: str, k: int) -> int:
        if not word:
            return 0

        groups = []
        count = 1
        for i in range(1, len(word)):
            if word[i] == word[i - 1]:
                count += 1
            else:
                groups.append(count)
                count = 1
        groups.append(count)

        total = 1
        for num in groups:
            total *= num

        if k <= len(groups):
            return total

        '''
        code above very simple and straightforward.
        DP begins below.
        '''

        dp = [0] * k    # we only care about up till length k (exclusive);
                        # whatever string formation shorter than length k is to be subtracted away from total ct
        dp[0] = 1       # before using any group, one way to form string of len 0

        for eachGroupSize in groups:  # for each group
            new_dp = [0] * k
            sum_val = 0
            for everyLength in range(k):
                if everyLength > 0: #because we bulding from everyLength - 1 ind position so we need this check
                                    # also implies new_dp[0] == 0 always

                    sum_val += dp[everyLength - 1]  #we can do at least as good as when we constructed a
                                                    # string of the current size - 1
                                                    # because we are now adding a new group
                                                    # in other words, for each possible string with current size -1
                                                    # we can at least produce such a string append one letter
                                                    # from new group to make a string of current size

                                                    # we are also making the assumption that we have infinite numbers
                                                    # of letters from the new group, thus that sum_val snowballs
                                                    # from each and every size from 0 to current size - 1
                                                    # and for each of them, denoted as current size - x,
                                                    # we add x amount of letters from new group to make it to current size

                if everyLength > eachGroupSize: # however, of course we do not have infinite amount of letters from new group
                                                # in fact we only need to check and make compensations when the current size
                                                # is greater than the amount of letters we have in new grouo:
                                                # for we cannot really construct a string of current size when we are dealing with
                                                # a previous string of size 0, which is to say x == current size in current size - x
                                                # because obviously when we do not have enough letters in the current group to
                                                # use as every single letter in the current string, we must subtract this case from
                                                # sum_val

                    sum_val -= dp[everyLength - eachGroupSize - 1]  # this is precisely what is discussed above
                                                                    # dp[everyLength - eachGroupSize -1] represents
                                                                    # the total amount of strings possibly formed with length
                                                                    # current size - amount of letters existing in new group - 1
                                                                    # this is a string that cannot possibly reach current length
                                                                    # by adding letters from the new group
                                                                    # because we are short of one letter from the amount we have
                                                                    # in the new group

                                                                    # and since each ind pos in dp holds the cumulative
                                                                    # of amount of strings formed, this also
                                                                    # takes care of all the strings that new group cannot form
                                                                    # for each string size from 0 to everyLength - eachGroupSize - 1

                new_dp[everyLength] = sum_val   #simply set the value there, now it is the correct sum after adjustments.
            dp = new_dp     #overwrite previous dp table

        invalid = sum(dp[len(groups):k])    # in theory, also correct by simply sum(dp[:k]) since everything before len(groups) is 0
        return total - invalid



'''
forward computing
correct, but too slow (assumes huge k)
'''
class Solution:
    MOD = 10**9 + 7

    def possibleStringCount(self, word: str, k: int) -> int:
        if not word:
            return 0

        # Group word into blocks of same character
        groups = []
        count = 1
        for i in range(1, len(word)):
            if word[i] == word[i - 1]:
                count += 1
            else:
                groups.append(count)
                count = 1
        groups.append(count)

        # Total combinations = product of group sizes
        total = 1
        for g in groups:
            total = (total * g) % self.MOD

        n = len(word)

        # Forward DP: dp[length] = ways to form original string of length 'length'
        dp = [0] * (n + 1)
        dp[0] = 1  # One way to form empty string

        for group_size in groups:
            new_dp = [0] * (n + 1)
            window_sum = 0
            for length in range(1, n + 1):
                window_sum = (window_sum + dp[length - 1]) % self.MOD
                if length - group_size - 1 >= 0:
                    window_sum = (window_sum - dp[length - group_size - 1]) % self.MOD
                new_dp[length] = window_sum
            dp = new_dp

        return sum(dp[k:]) % self.MOD


'''
now just re-create the solution to test own understanding
'''

def preprocessing(msg):
    groupArr = []
    ct = 1
    for i in range(1,len(msg)):
        if msg[i] == msg[i - 1]:
            ct+=1
        else:
            groupArr.append(ct)
            ct = 1
    groupArr.append(ct)
    return groupArr

def solution(msg,k):
    limit = 10**9 + 7

    groupArr = preprocessing(msg)
    total = 1
    for eachGroupSize in groupArr:
        total = (total * eachGroupSize) % limit

    if len(groupArr) >= k:
        return total

    #and when k> total number of groups, we need dp!
    '''
    it's as the standard solution goes, we
    compute number of strings possibly formed 
    from size 0 till k-1
    '''
    dp = [0 for _ in range(k)]
    dp[0] = 1   #there is one way to form a string of size 0 given no group

    #we do a total of group number of iterations, each time computing prefix sum
    for eachGroupSize in groupArr:  #this accounts for every group once
        prefixSum = 0
        newDP = [0 for _ in range(k)]   #to replace existing dp
        for eachSize in range(len(newDP)):  #fill cumulatively the size that can be formed
            if eachSize > 0:
                prefixSum = (prefixSum+dp[eachSize-1])%limit
            if eachSize > eachGroupSize:    #we do not have enough number of the letters in current group to fill everything
                prefixSum = (prefixSum-dp[eachSize-1-eachGroupSize])%limit
            #adjustment is done
            newDP[eachSize] = prefixSum
        dp = newDP
    return (total - sum(dp[:k])) % limit



if __name__ == '__main__':
    msg = "aaaaabbcddeeesssss"
    print(preprocessing(msg))

