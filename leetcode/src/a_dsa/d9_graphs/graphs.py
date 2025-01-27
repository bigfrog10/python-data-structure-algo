from typing import List
from collections import defaultdict

# LC1761. Minimum degree of a connected trio in a graph
def minTrioDegree(self, n: int, edges: List[List[int]]) -> int:  # O(EV) time, O(E+V) space
    graph = defaultdict(set) # must faster, but still
    for u,v  in edges:  # O(E) space
        graph[u].add(v)
        graph[v].add(u)
    ans = inf
    node_degrees = sorted([[len(graph[k]), k] for k in graph])  # sort for break below O(V) space
    for a, b in edges:  # O(E)
        w = len(graph[a]) + len(graph[b])
        for w1, c in node_degrees:  # O(V)
            if c in graph[a] and c in graph[b]:  # trio requirement
                ans = min(ans, w1+w)
                break # must have to shorten run time from 11 s to 0.66 s!!
    return ans - 6 if ans < inf else -1

# LC785. Is Graph Bipartite?
def isBipartite(self, graph: List[List[int]]) -> bool:  # O(V + E)
    n = len(graph)  # O(V + E)
    color = [0] * n
    for node in range(n):
        if color[node] != 0: continue
        q = deque([node])
        color[node] = 1  # paint color
        while q:  # DFS
            cur = q.popleft()
            for ne in graph[cur]:
                if color[ne] == 0:
                    color[ne] = -color[cur]
                    q.append(ne)
                elif color[ne] == color[cur]:
                    return False  # if child and parent have same color
    return True

# LC133. Clone Graph
def cloneGraph(self, node: 'Node') -> 'Node':  # O(V + E) runtime, O(V) space
    if not node: return None
    exist2new = {} # v is unique, new node references
    def dfs(node):
        if node in exist2new: return exist2new[node]
        nn = Node(node.val)
        exist2new[node] = nn
        for ne in node.neighbors:
            nn.neighbors.append(dfs(ne))
        return nn
    nr = dfs(node)
    return nr

# LC2076. Process Restricted Friend Requests
def friendRequests(self, n: int, restrictions: List[List[int]], requests: List[List[int]]) -> List[bool]:
    parents, ranks = [i for i in range(n)], [1] * n  ## much faster (N + Mlog*N)
    forbidden = collections.defaultdict(set)
    for i, j in restrictions:
        forbidden[i].add(j)
        forbidden[j].add(i)

    def find(i):
        if i != parents[i]: parents[i] = find(parents[i])
        return parents[i]

    def union(p1, p2):
        if ranks[p1] >= ranks[p2]:
            parents[p2] = p1
            ranks[p1] += ranks[p2]
        else:
            parents[p1] = p2
            ranks[p2] += ranks[p1]
            p1, p2 = p2, p1

        forbidden[p1] |= forbidden[p2]
        for i in forbidden[p2]:
            forbidden[i].remove(p2)
            forbidden[i].add(p1)
        del forbidden[p2]

    ans = []
    for i, j in requests:  # m requests on n object, takes O(N + Mlog*N), log* is almost constant
        p1, p2 = find(i), find(j)
        if p1 == p2: ans.append(True)
        elif p2 in forbidden[p1]: ans.append(False)
        else:
            union(p1, p2)
            ans.append(True)
    return ans

# LC399. Evaluate Division
def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
    graph = defaultdict(dict)
    for (u, v), val in zip(equations, values):  # O(E)
        graph[u][u] = graph[v][v] = 1
        graph[u][v] = val
        graph[v][u] = 1 / val
    for k in graph:  # O(V*E)
        for i in graph[k]:
            for j in graph[k]:
                graph[i][j] = graph[i][k] * graph[k][j] if i != j else 1
    return [graph[u].get(v, -1) for u, v in queries]
# https://leetcode.com/problems/evaluate-division/solutions/3544428/python-elegant-short-floyd-warshall

def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
    alphabet = set(sum(equations, []))  # start with []. return all diff chars in a set
    uf = UnionFind(alphabet)  # O(N+M*lg∗N)
    for (u, v), w in zip(equations, values): uf.union(u, v, w)
    ans = []
    for u, v in queries:
        if u in alphabet and v in alphabet:
            pu, vu = uf.find(u)
            pv, vv = uf.find(v)
            if pu == pv: ans.append(vu / vv)
            else: ans.append(-1)
        else: ans.append(-1)
    return ans
class UnionFind:  ## M union and find operations on N objects takes O(N + M lg* N) time
    def __init__(self, alphabet):  ## weighted union + path compression
        self.parent = {c: c for c in alphabet}
        self.value = {c: 1 for c in alphabet}
        self.rank = {c: 1 for c in alphabet}
    def find(self, u):
        if u != self.parent[u]:
            self.parent[u], val = self.find(self.parent[u])
            self.value[u] *= val
        return self.parent[u], self.value[u]
    def union(self, u, v, w):
        pu, vu = self.find(u)
        pv, vv = self.find(v)
        if pu == pv: return
        if self.rank[pu] > self.rank[pv]: # self.union(v, u, 1/w)
            self.parent[pv] = self.parent[pu]
            self.value[pv] = 1/w * vu / vv
            self.rank[pu] += self.rank[pv]
        else:
            self.parent[pu] = self.parent[pv]
            self.value[pu] = w * vv / vu
            self.rank[pv] += self.rank[pu]

# LC2307. Check for Contradictions in Equations
def checkContradictions(self, equations: List[List[str]], values: List[float]) -> bool:
    PRECISION = 10 ** -5  # O(n) time and space
    def find(nmr):
        root[nmr] = root.get(nmr, (nmr, 1))
        if root[nmr][0] != nmr:
            dnr1, q1 = root[nmr]
            dnr2, q2 = find(dnr1)
            root[nmr] = (dnr2, q1 * q2)
        return root[nmr]
    root = {}
    for equation, q in zip(equations, values):
        nmr1, nmr2 = equation
        dnr1, q1 = find(nmr1)
        dnr2, q2 = find(nmr2)
        if dnr1 == dnr2:
            if abs(q1 / q2 - q) >= PRECISION: return True
        else: root[dnr2] = (dnr1, q1 / (q * q2))
    return False
# https://leetcode.com/problems/check-for-contradictions-in-equations/?envType=company&envId=amazon&favoriteSlug=amazon-three-months


# LC1579. Remove Max Number of Edges to Keep Graph Fully Traversable




# LC323. Number of Connected Components in an Undirected Graph
def countComponents(self, n, edges):
    graph = defaultdict(set) #{i: set() for i in range(n)}
    for v1, v2 in edges:
        graph[v1].add(v2)
        graph[v2].add(v1)
    seen = set()
    def bfs(node):  # get seen populated
        queue = [node]
        for n in queue:
            for nei in graph[n]:
                if nei not in seen:
                    seen.add(nei)
                    queue.append(nei)
    count = 0
    for i in range(n):
        if i not in seen:
            bfs(i)
            count += 1
    return count

# LC1136. Parallel Courses
def minimumSemesters(self, N: int, relations: List[List[int]]) -> int:
    g = collections.defaultdict(set)  # O(V + E)
    g_reversed = collections.defaultdict(set)  # to peer off
    for c in relations:
        g[c[0]].add(c[1])
        g_reversed[c[1]].add(c[0])
    queue = [(1, i) for i in range(1, N+1) if not g_reversed[i]]  # leaves
    max_level, seen = 0, []
    while queue:
        level, v1 = queue.pop(0)
        seen.append(v1)
        max_level = max(level, max_level)
        for v2 in g[v1]:
            g_reversed[v2].remove(v1)
            if not g_reversed[v2]: queue.append((level+1, v2))  # new leaves
    return max_level if len(seen) == N else -1

# LC1192. Critical Connections in a Network
def criticalConnections(self, n: int, connections: List[List[int]]) -> List[List[int]]:  # O(V+E)
    network = [[] for _ in range(n)]
    for a, b in connections:
        network[a].append(b)
        network[b].append(a)
    disc, low = [-1]*n, [-1]*n  # discovery time and low link
    ret = []
    def tarjan(prev, node, time): # DFS on low
        # base case, we already visited this node, so don't need to touch it again.
        if disc[node] != -1: return disc[node]
        disc[node] = low[node] = time
        for x in network[node]:
            if x != prev:  # so we don't go back to parent/prev
                time += 1
                newLow = tarjan(node, x, time)
                low[node] = min(low[node], newLow)
                if low[x] > disc[node]: ret.append([node, x])  # find bridge, x has no circle back to node
        return low[node]
    tarjan(0, 0, 0)
    return ret

# LC1319. Number of Operations to Make Network Connected
def makeConnected(self, n: int, connections: List[List[int]]) -> int:  # O(m) m = len(conns)
    if len(connections) < n - 1: return -1
    G = [set() for i in range(n)]
    for i, j in connections:  # space could be n^2, for fully connected net
        G[i].add(j)
        G[j].add(i)
    seen = [0] * n
    def dfs(i):
        if seen[i]: return 0
        seen[i] = 1
        for j in G[i]: dfs(j)
        return 1
    # the number of connected networks - 1 is what we need to do to connect them
    return sum(dfs(i) for i in range(n)) - 1

# LC1059. All Paths from Source Lead to Destination # BBG
def leadsToDestination(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
    g = defaultdict(set) # O(V)
    for [x,y] in edges: g[x].add(y)
    visited = defaultdict(int)
    def dfs(node):
        if visited[node] == 1: return True
        elif visited[node] == -1: return False
        elif len(g[node]) == 0: return node == destination
        else:
            visited[node] = -1 # not reach to dest
            for child in g[node]:
                if not dfs(child): return False
            visited[node] = 1 # reach dest
            return True
    return dfs(source)

# LC797. All Paths From Source to Target
# To return all solutions, we need to dfs with path  # BBG
def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:  # O(n * 2^n)
    results, target = [], len(graph) - 1
    def backtrack(currNode, path):  # we need all paths, so backtrack on path.
        if currNode == target:
            results.append(list(path))  # new path
            return
        for nextNode in graph[currNode]:  # neighbours
            path.append(nextNode)
            backtrack(nextNode, path)
            path.pop()  # backout
    backtrack(0, [0])  # 0 is starting point, [0] is current path
    return results

def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
    target, res = len(graph) - 1, []
    def dfs(node, path):
        if node == target: res.append(path)
        else:
            for nei in graph[node]: dfs(nei, path + [nei])  # O(2^n)
    dfs(0, [0])
    return res


# Cycle Detection
# LC684. Redundant Connection - undirected graph
def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
    graph = defaultdict(set)
    def dfs(source, target): # detect cycle
        if source not in seen:
            seen.add(source)
            if source == target: return True
            return any(dfs(nei, target) for nei in graph[source])
    for u, v in edges:
        seen = set()
        if u in graph and v in graph and dfs(u, v): return u, v
        graph[u].add(v)
        graph[v].add(u)

# LC685. Redundant Connection II - Directed graph
def findRedundantDirectedConnection(self, edges):  # [[2,3],[3,1],[3,4],[4,2]]
    parents = {}
    def find(u):  # union find
        if p[u] != u: p[u] = find(p[u])
        return p[u]
    def detect_cycle(edge):  # go from u to v (forms a cycle) along parents
        u, v = edge
        while u != v and u in parents: u = parents[u]
        return u == v
    candidates = []  # stores two edges from the vertex where it has two parents
    for u, v in edges:
        if v not in parents: parents[v] = u
        else:
            candidates.append((parents[v], v))
            candidates.append((u, v))
    if candidates:  # case 2 & case 3 where one vertex has two parents
        return candidates[0] if detect_cycle(candidates[0]) else candidates[1]
    # case 1, we just perform a standard union find, same as redundant-connection
    p = list(range(len(edges)+1)) # cycle
    for edge in edges:
        u, v = map(find, edge)
        if u == v: return edge
        p[u] = p[v]

# LC1129. Shortest Path with Alternating Colors alter colors
def shortestAlternatingPaths(self, n: int, redEdges: List[List[int]], blueEdges: List[List[int]]) -> List[int]:
    conns = defaultdict(list)
    for a, b in redEdges: conns[a].append((b, 'red'))
    for a, b in blueEdges: conns[a].append((b, 'blue'))
    res = [math.inf] * n
    queue = deque([(0, 'red', 0), (0, 'blue', 0)])
    visited = set()
    while queue:
        node, color, level = queue.popleft()
        if (node, color) in visited: continue
        visited.add((node, color))
        res[node] = min(res[node], level)
        for next_node, next_color in conns[node]:
            if next_color != color:
                queue.append((next_node, next_color, level + 1))
    return [-1 if x == math.inf else x for x in res]

# LC834. Sum of Distances in Tree
def sumOfDistancesInTree(self, N: int, edges: List[List[int]]) -> List[int]:
    tree = collections.defaultdict(set)  # it's really a graph
    res = [0] * N
    count = [1] * N  # count[i] is the total number of nodes in subtree i, which also includes the node i itself
    for i, j in edges:
        tree[i].add(j)
        tree[j].add(i)

    def dfs(root, pre):
        for i in tree[root]:
            if i != pre:
                dfs(i, root)
                count[root] += count[i]
                res[root] += res[i] + count[i]

    def dfs2(root, pre):
        for i in tree[root]:
            if i != pre:
                res[i] = res[root] - count[i] + N - count[i]
                dfs2(i, root)
    dfs(0, -1)
    dfs2(0, -1)
    return res

# Merge Directed graph nodes if there is only 1 parent, and that parent has 1 child.
def merge(adj_map: dict):  # parent -> children, such 'A' -> ['B', 'C']
    def get_parents(am: dict):
        res = defaultdict(set)
        for n, c in am.items():
            for m in c: res[c].add(m)
        return res

    parents = get_parents(adj_map)

    def merge_child(node):
        children = adj_map[node]
        if len(children) == 1 and len(parents[children[0]]) == 1:
            adj_map[node + children[0]] = adj_map[children[0]]
            for c in adj_map[children[0]]:
                parents[c].remove(children[0])
                parents[c].add(node + children[0])

            del adj_map[node]
            del adj_map[children[0]]
            del parents[children[0]]

            merge_child(node + children[0])

    keys = adj_map.keys()
    for node in keys:
        merge_child(node)

# A -> B -> C -> D merge to ABCD
# A ->        -> D
#      B -> C
# E ->        -> F
# merges to
# A ->    -> D
#      BC
# E ->    -> F
