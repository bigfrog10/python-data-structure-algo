
# LC1021. Remove Outermost Parentheses

# LC1111. Maximum Nesting Depth of Two Valid Parentheses Strings
def maxDepthAfterSplit(self, seq: str) -> List[int]:
    A = B = 0 # max opens for 2 groups
    res = [0] * len(seq) # we split into sequences, not continuous subarrays
    for i, c in enumerate(seq):
        v = 1 if c == '(' else -1
        if (v > 0) == (A < B): A += v
        else:
            B += v
            res[i] = 1
    return res
def maxDepthAfterSplit(self, seq: str) -> List[int]:
    depth = 0
    ans = list()
    for c in seq:
        if c == "(":
            ans.append(depth % 2)
            depth += 1
        else:
            depth -= 1
            ans.append(depth % 2)
    return ans

# LC22. Generate Parentheses
def generateParenthesis(self, n: int) -> List[str]:
    ret = {''}
    for _ in range(n):
        ret = {s[:i] + '()' + s[i:] for s in ret for i in range(len(s)+1)}
    return ret

# LC20. Valid Parentheses - {} () []
def isValid(self, s: str) -> bool:
    PAIRS = {'(': ')', '{': '}', '[': ']'}
    stack = []  # to store unprocessed
    for c in s:
        if c in PAIRS.keys(): stack.append(c) # open parentheses
        else:  # closed parentheses
            if stack and PAIRS[stack[-1]] == c: stack.pop() # matched
            else: return False # no suppose to have other chars or ) has no (
    return len(stack) == 0

# LC32. Longest Valid Parentheses - longest substring  long parentheses long valid parenth
def longestValidParentheses(self, s: str) -> int:  # O(n) time, O(1) space
    maxl = left = right = 0  # ())
    for c in s:  # from left to right
        if c == '(': left += 1
        else: right += 1
        if left == right: maxl = max(maxl, 2 * right)
        elif left < right: left = right = 0  # start over with new
    left = right = 0  # (()
    for c in s[::-1]:
        if c == '(': left += 1
        else: right += 1
        if left == right: maxl = max(maxl, 2 * left)
        elif left > right: left = right = 0
    return maxl
def longestValidParentheses(self, s: str) -> int:  # O(n) time and space
    res, stack = 0, [-1]
    for i in range(len(s)):
        if s[i] == "(": stack.append(i)
        else:  # )
            stack.pop()
            if not stack: stack.append(i)
            else: res = max(res, i - stack[-1])
    return res


# LC1249. Minimum Remove to Make Valid Parentheses - with letters, return one string result  min remove  min paren remove
def minRemoveToMakeValid(self, s: str) -> str:  # O(n) runtime and space
    stack, remove = [], []  # find all indices to remove
    for i, c in enumerate(s):
        if c not in '()': continue  # others, keep it
        elif c == '(': stack.append(i)  # record it
        # now c == ')'
        elif not stack: remove.append(i)  # mo matching ( for ), add to remove
        else: stack.pop()  # matched, remove old record
    remove.extend(stack)  # whatever left is no match
    idx, ret = 0, ''
    for i in remove:  # remove those
        ret += s[idx:i]  # up to removed
        idx = i + 1  # skip removed
    ret += s[idx:]  # add leftover
    return ret

# LC921. Minimum Add to Make Parentheses Valid - return num of operations   min add paren min insert paren
def minAddToMakeValid(self, S: str) -> int:  # O(n)
    left = bal = 0  # bal = # of '(' - # of ')'
    for s in S:
        bal += 1 if s == '(' else -1  # cancel out balanced
        if bal == -1:  # there is ) unmatched
            left += 1  # expected ( needs 1 more
            bal += 1  # diff needs +1 too
    return left + bal  # "(((" -> left=0, bal=3

# LC301. Remove Invalid Parentheses - with letters, return all results remove parenth make it valid
def removeInvalidParentheses(self, s): # O(2^n) return all possible results
    def isvalid(s):  # worst case is all (, e.g., ((((( -> valid below is ''
        ctr = 0
        for c in s:  # O(n)
            if c == '(': ctr += 1
            elif c == ')': ctr -= 1
            if ctr < 0: return False
        return ctr == 0
    level = {s}
    while True:  # O(2^(n-1)), no need to check single char sets.
        valid = list(filter(isvalid, level))
        if valid: return valid  # we want min num of removals
        level = {s[:i] + s[i+1:] for s in level for i in range(len(s)) if s[i] in '()'}

# LC1614. Maximum Nesting Depth of the Parentheses
def maxDepth(self, s: str) -> int:
    # https://leetcode.com/problems/maximum-nesting-depth-of-the-parentheses/discuss/888949/JavaC%2B%2BPython-Parentheses-Problem-Foundation
    res = cur = 0
    for c in s:
        if c == '(':
            cur += 1
            res = max(res, cur)
        if c == ')': cur -= 1
    return res



# LC1541. Minimum Insertions to Balance a Parentheses String - unbalanced ( to ))
def minInsertions(self, s: str) -> int:
    open_missing = close_missing = close_needed = 0  # miss (, miss ), and miss ))
    for c in s:
        if c == '(':
            if close_needed % 2:  # if we have odd ) in the last step
                close_missing += 1  # for previous invalid, have to add one closing bracket to make it valid
                close_needed -= 1  # no need to track the last invalid case
            close_needed += 2
        else:  # it's )
            close_needed -= 1
            if close_needed < 0: # previously we have ")))"
                open_missing += 1  # so increment this for ( to balance )))
                close_needed += 2  # no need to track the last invalid
    return open_missing + close_missing + close_needed



# LC1963. Minimum Number of Swaps to Make the String Balanced - parenthesis '[] balance' min swap parenth
def minSwaps(self, s: str) -> int:
    bal = 0
    for ch in s:
        if ch == '[': bal += 1
        else:
            if bal > 0: bal -= 1
    return (bal + 1) // 2  # ceiling

# LC856. Score of Parentheses  parenth score parenth
def scoreOfParentheses(self, s: str) -> int:
    ans = bal = 0
    for i, x in enumerate(s):
        if x == '(': bal += 1
        else:  # )
            bal -= 1
            if s[i-1] == '(': ans += 1 << bal # only when seeing ()
    return ans

# LC241. Different Ways to Add Parentheses - return results expr group num diff expr add parenth diff add paren
def diffWaysToCompute(self, s: str) -> List[int]:  # O(n*2^n) time, O(2^n) space
    # runtime is: http://people.math.sc.edu/howard/Classes/554b/catalan.pdf
    # runtime is C_(n-1) = (select n-1 from 2(n-1)) / n, n = len(expr)
    # pn = sum(p_i * p_(n-i)) for i in 1 to n-1
    @cache
    def dfs(i, j):
        if i == j: return [int(s[i])]
        if i == j - 1 and s[j] not in '+-*':  # need 3 chars to form an expression
            return [int(s[i: j + 1])]
        res = []
        for k in range(i, j + 1):
            ch = s[k]
            if ch in '+-*':
                left = dfs(i, k - 1)
                right = dfs(k + 1, j)
                res.extend(a+b if ch == '+' else a-b if ch =='-' else a*b for a in left for b in right)
        return res
    return dfs(0, len(s) - 1)



# LC678. Valid Parenthesis String - parenth with *, par with *, par *  valid paren *
def checkValidString(self, s):
    n = len(s)  # O(n) time and O(1) space
    open_count = close_count = 0
    for i in range(n):  # Traverse the string from both ends simultaneously
        if s[i] == '(' or s[i] == '*': open_count += 1
        else: open_count -= 1
        if s[n - 1 - i] == ')' or s[n - 1 - i] == '*': close_count += 1
        else: close_count -= 1
        if open_count < 0 or close_count < 0: return False
    return True

















