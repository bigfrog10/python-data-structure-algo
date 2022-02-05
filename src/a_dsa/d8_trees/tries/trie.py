
# LC211. Design Add and Search Words Data Structure
class WordDictionary:  # much faster
    def __init__(self): self.trie = {}
    def addWord(self, word: str) -> None:
        node = self.trie
        for ch in word: node = node.setdefault(ch, {})
        node['$'] = True  # mark end of word
    def search(self, word: str) -> bool:
        def search_in_node(word, node) -> bool: # recursion on dot
            for i, ch in enumerate(word):
                if ch in node: node = node[ch] # char found, go down
                else:
                    if ch == '.':  # we need to check all but $
                        for x in node:
                            if x != '$' and search_in_node(word[i + 1:], node[x]):
                                return True
                    return False
            return '$' in node
        return search_in_node(word, self.trie)

# LC208. Implement Trie (Prefix Tree)
class Trie:
    def __init__(self): self.trie = {}
    def insert(self, word: str) -> None:
        node = self.trie
        for c in word: node = node.setdefault(c, {})
        node["-"] = True
    def search(self, word: str) -> bool:
        t = self.trie
        for c in word:
            if c not in t: return False
            t = t[c]
        return "-" in t
    def startsWith(self, prefix: str) -> bool:
        t = self.trie
        for c in prefix:
            if c not in t: return False
            t = t[c]
        return True

# LC1233. Remove Sub-Folders from the Filesystem
def removeSubfolders(self, folder: List[str]) -> List[str]:
    trie = {}
    for path in folder: # build trie from input
        dirs = path[1:].split('/')
        node = trie
        for di in dirs: node = node.setdefault(di, {})
        node['end'] = path # save path to end
    ret = [] # collect top folders
    def dfs(node):
        if 'end' in node:
            ret.append(node['end']) # earliest end is top folder
            return
        for d in node: dfs(node[d])
    dfs(trie)
    return ret

# LC1178. Number of Valid Words for Each Puzzle
def findNumOfValidWords(self, words: List[str], puzzles: List[str]) -> List[int]:
    res = [0] * len(puzzles) # O(n)
    trie = {}
    for word in words:
        cur = trie
        for letter in sorted(set(word)): cur = cur.setdefault(letter, {})
        if '*' not in cur: cur['*'] = 1 # if this is the only word with these letters
        else: cur['*'] += 1 # if there is already other word with same letter sets
    def dfs(trie, idx, first_matched):
        p = puzzles[idx]
        if '*' in trie and first_matched:
            res[idx] += trie['*'] # collect counts, we need i here
        for key in trie:
            if key in p:
                if p[0] == key or first_matched: dfs(trie[key], idx, True)
                else: dfs(trie[key], idx, False)
    for i in range(len(puzzles)): dfs(trie, i, False)
    return res


