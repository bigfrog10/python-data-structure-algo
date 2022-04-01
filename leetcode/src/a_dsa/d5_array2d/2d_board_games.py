from collections import deque

# LC1263. Minimum Moves to Move a Box to Their Target Location - move box
def minPushBox(self, grid: List[List[str]]) -> int:  # faster BFS, O((mn)^2)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "T": target = (i,j)
            if grid[i][j] == "B": box = (i,j)
            if grid[i][j] == "S": person = (i,j)
    def empty(x, y): # O(1) verify
        return 0 <= x <len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != '#'
    def reachable(curr, dest, box):  #BFS to check dest is reachable from curr
        que, v = deque([curr]), set()
        while que:
            pos = que.popleft()
            if pos == dest: return True
            for x, y in (pos[0]+1,pos[1]), (pos[0]-1,pos[1]), (pos[0],pos[1]+1), (pos[0],pos[1]-1):
                if empty(x, y) and (x, y) != box and (x, y) not in v:
                    v.add((x,y))
                    que.append((x,y))
        return False
    q, visited = deque([(0, box, person)]), {box + person}
    while q:  # main BFS
        pushes, box, person = q.popleft()
        if box == target: return pushes
        b_coord = [(box[0]+1,box[1]),(box[0]-1,box[1]),(box[0],box[1]+1),(box[0],box[1]-1)]
        p_coord = [(box[0]-1,box[1]),(box[0]+1,box[1]),(box[0],box[1]-1),(box[0],box[1]+1)]
        for new_box, new_person in zip(b_coord,p_coord):
            if empty(*new_box) and new_box + box not in visited:
                if empty(*new_person) and reachable(person, new_person, box):
                    visited.add(new_box+box)
                    q.append((pushes + 1,new_box,box))
    return -1

# LC1197. Minimum Knight Moves
def minKnightMoves(self, x: int, y: int) -> int:  # O(x*y)
    @lru_cache(None)
    def dp(x,y):  # O(x*y) in cache
        if x + y == 0: return 0  # (0, 0)
        elif x + y == 2: return 2  # (1, 1), (0, 2), (2, 0)
        return min(dp(abs(x-1), abs(y-2)), dp(abs(x-2), abs(y-1))) + 1
    return dp(abs(x), abs(y))  # first quardrant due to symmetry

# LC 2056. Number of Valid Move Combinations On Chessboard
def countCombinations(self, pieces, positions):
    D = ((), ((-1,0),(1,0),(0,-1),(0,1)),((-1,-1),(1,-1),(-1,1),(1,1)))
    P = {"rook":1, "bishop":2, "queen":3}
    n = len(pieces)
    M = (1<<8)-1  # 011111111, The kth bit of T[x][y] from right indicates a piece is at (x, y) at time k
    T = [[M] * 9 for _ in range(9)]  # 1 means empty, 0 means occupied
    def dfs(i): # search from ith piece
        if i == n: return 1
        p, (x0, y0) = pieces[i], positions[i]
        cnt = 0
        if T[x0][y0] == M:  # stay at its original position
            t = T[x0][y0]
            T[x0][y0] = 0  # set all bits to 0, (x0, y0) stays here all the time
            cnt += dfs(i+1)
            T[x0][y0] = t  # restore bits
        for dx, dy in D[P[p]&1]+D[P[p]&2]:  # move from its original position
            x, y, b = x0+dx, y0+dy, 1  # b is the time to move
            while 0 < x < 9 and 0 < y < 9 and (T[x][y] >> b & 1):  # rule 1
                T[x][y] ^= 1 << b  # rule 1a, move to (x, y), set bth bit to 0
                if (T[x][y] >> b+1) == (M >> b+1):  # rule 2a, if all future states are free to move
                    t = T[x][y]
                    T[x][y] &= (1 << b) - 1  # rule 2b, keep all future states to 0
                    cnt += dfs(i+1)
                    T[x][y] = t  # restore
                x, y, b = x+dx, y+dy, b+1
            while b > 1: T[(x:=x-dx)][(y:=y-dy)] |= (1 << (b:=b-1)) # restore
        return cnt
    return dfs(0)

# LC935. Knight Dialer
def knightDialer(self, n: int) -> int:
    MOD = 10**9 + 7
    moves = [[4,6],[6,8],[7,9],[4,8],[3,9,0],[],[1,7,0],[2,6],[1,3],[2,4]]
    dp = [1] * 10  # counts for current hop and current digit
    for hops in range(n-1):
        dp2 = [0] * 10
        for node, count in enumerate(dp):  # loop all digits 0-9
            for nei in moves[node]:  # loop all jumps
                dp2[nei] += count
                dp2[nei] %= MOD
        dp = dp2
    return sum(dp) % MOD
import numpy as np
def knightDialer(self, N):  # O(logn)
    mod = 10**9 + 7
    if N == 1: return 10
    M = np.matrix([[0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
                   [0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                   [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                   [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                   [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                   [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                   [0, 0, 1, 0, 1, 0, 0, 0, 0, 0]])
    res, N = 1, N - 1
    while N:
        if N % 2: res = res * M % mod
        M = M * M % mod
        N //= 2
    return int(np.sum(res)) % mod

# LC489. Robot Room Cleaner
def cleanRoom(self, robot):  # O(open cells)
    def go_back():
        robot.turnRight()
        robot.turnRight()  # turn back
        robot.move()
        robot.turnRight()
        robot.turnRight()  # turn to original dir
    def clean_cell(cell, cf):
        visited.add(cell)
        robot.clean()
        for i in range(4):
            new_d = (cf + i) % 4  # e.g., facing right needs to start from 2nd index
            new_cell = (cell[0] + directions[new_d][0], cell[1] + directions[new_d][1])
            if not new_cell in visited and robot.move():
                clean_cell(new_cell, new_d)
                go_back()
            robot.turnRight()  # turn the robot following chosen direction : clockwise
    # going clockwise : 0: 'up', 1: 'right', 2: 'down', 3: 'left'
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    visited = set()
    clean_cell((0, 0), 0)

# LC1559. Detect Cycles in 2D Grid
def containsCycle(self, grid: List[List[str]]) -> bool:  # O(mn)
    m, n = len(grid), len(grid[0])
    visited = set()
    def dfs(node, parent):
        if node in visited: return True
        visited.add(node)
        nx,ny = node
        for cx, cy in [nx+1,ny], [nx-1, ny],[nx,ny+1], [nx,ny-1]:
            if m > cx >= 0 <= cy < n and grid[cx][cy] == grid[nx][ny] and (cx,cy) != parent:
                if dfs((cx, cy), node): return True
        return False
    return any((i,j) not in visited and dfs((i, j), (i, j)) for i, j in product(range(m), range(n)))

# LC419. Battleships in a Board
def countBattleships(self, board: List[List[str]]) -> int:
    total = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'X':
                flag = 1
                if j > 0 and board[i][j-1] == 'X': flag = 0  # ignore double count
                if i > 0 and board[i-1][j] == 'X': flag = 0
                total += flag
    return total

# LC529. Minesweeper
def updateBoard(self, board: List[List[str]], click: List[int]) -> List[List[str]]:
    n, m = len(board), len(board[0])  ## O(mn)
    dirs = ((-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (-1, -1), (1, 1), (1, -1))
    def dfs(i, j):  # don't need visited since we alter values already
        if board[i][j] == 'M': board[i][j] = 'X'  # we should get here, i.e., don't step on mine.
        elif board[i][j] == 'E':
            # neighbour mines
            nm = sum(board[i+dx][j+dy] == 'M' for dx, dy in dirs if 0 <= i+dx < n and 0 <= j+dy < m)
            board[i][j] = str(nm or 'B')
            if not nm: # no mine nearby
                for dx, dy in dirs:
                    if 0 <= i+dx < n and 0 <= j+dy < m: dfs(i + dx, j + dy)
            # the logic with mine nearby is complicated, with this logic missing
            # there could be cells not visited, e.g., a mine at (1, 1).
    dfs(*click)
    return board

# 1293. Shortest Path in a Grid with Obstacles Elimination
def shortestPath(self, grid: List[List[int]], k: int) -> int:  # O(Nk), N is # of cells
    rows, cols = len(grid), len(grid[0])
    if k >= rows + cols - 2: return rows + cols - 2
    state = (0, 0, k)  # (row, col, remaining quota to eliminate obstacles)
    queue, seen = deque([(0, state)]), set([state])  # (steps, state)
    while queue:
        steps, (row, col, k) = queue.popleft()
        if (row, col) == (rows - 1, cols - 1): return steps
        for x, y in (row, col + 1), (row + 1, col), (row, col - 1), (row - 1, col):
            if 0 <= x < rows and 0 <= y < cols:
                nk = k - grid[x][y]
                new_state = x, y, nk
                if nk >= 0 and new_state not in seen:
                    seen.add(new_state)
                    queue.append((steps + 1, new_state))
    return -1
def shortestPath(self, grid: List[List[int]], k: int) -> int:  # best, A*, O(Nklog(Nk))
    m, n = len(grid), len(grid[0])
    state = m-1, n-1, k
    queue, seen = [(m+n-2, 0, state)], {state}  # manhattan distance
    while queue:
        _, steps, (i, j, k) = heapq.heappop(queue)  # _ is for sorting
        if k >= i + j - 1: return steps + i + j  # free walk with no obstacle
        for x, y in (i+1, j), (i-1, j), (i, j+1), (i, j-1):
            if m > x >= 0 <= y < n:
                state = x, y, k - grid[x][y]
                if state not in seen and state[2] >= 0:
                    heapq.heappush(queue, (x+y+steps+1, steps+1, state))
                    seen.add(state)
    return -1

# LC51. N-Queens
def solveNQueens(self, n: int) -> List[List[str]]:
    res, board = [], [] # O(n!)
    cols, diag, off_diag = set(), set(), set()
    def backtrack(i):  # recursion on rows
        if i == n:
            res.append(list(board))
            return
        for j in range(n):
            if j not in cols and j-i not in diag and j+i not in off_diag:
                cols.add(j)  # order is not significant, these 4 steps are independent.
                diag.add(j-i)
                off_diag.add(j+i)
                board.append(j)
                backtrack(i+1)  # recursion
                board.pop()  # backout
                off_diag.remove(j+i)
                diag.remove(j-i)
                cols.remove(j)
    backtrack(0)
    res1 = [['.' * col + 'Q' + '.'*(n - col - 1) for col in board] for board in res]
    return res1

# LC1102. Path With Maximum Minimum Value - minmax search
def maximumMinimumPath(self, A: List[List[int]]) -> int:  # Time: O(MN log MN), space O(MN)
    R, C = len(A), len(A[0])  # Dijkstra
    maxHeap = [(-A[0][0], 0, 0)]
    seen = [[0 for _ in range(C)] for _ in range(R)]
    seen[0][0] = 1
    while maxHeap:  # some low level point touched but not expanded
        val, x, y = heapq.heappop(maxHeap)
        if x == R - 1 and y == C - 1:  return -val
        for dx, dy in (0, 1), (1, 0), (0, -1), (-1, 0):
            nx, ny = x + dx, y + dy
            if 0 <= nx < R and 0 <= ny < C and not seen[nx][ny]:
                seen[nx][ny] = 1
                heapq.heappush(maxHeap, (max(val, -A[nx][ny]), nx, ny))
    return -1

# LC994. Rotting Oranges
def orangesRotting(self, grid: List[List[int]]) -> int:  # O(rows * cols)
    rows, cols = len(grid), len(grid[0])
    rotten, fresh = set(), set()
    for i, j in product(range(rows), range(cols)):
        if grid[i][j] == 2: rotten.add((i, j))
        if grid[i][j] == 1: fresh.add((i, j))
    timer = 0
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    while fresh:  # BFS
        if not rotten: return -1
        rotten = {(i+di, j+dj) for i, j in rotten for di, dj in dirs if (i+di, j+dj) in fresh}
        fresh -= rotten
        timer += 1
    return timer

# LC1034. Coloring A Border
def colorBorder(self, grid: List[List[int]], row: int, col: int, color: int) -> List[List[int]]:
    seen, m, n = set(), len(grid), len(grid[0])
    def dfs(x, y):  # return: is the right component or not
        if (x, y) in seen: return True
        if not (0 <= x < m and 0 <= y < n and grid[x][y] == grid[row][col]): return False
        seen.add((x, y)) # now it's in the same component
        if dfs(x + 1, y) + dfs(x - 1, y) + dfs(x, y + 1) + dfs(x, y - 1) < 4:
            grid[x][y] = color  # this is a border
        return True
    dfs(row, col)
    return grid

# LC723. Candy Crush
def candyCrush(self, board):  # TIME : O(M * N)
    R, C = len(board), len(board[0])
    crushed = False
    for i in range(R):  # mark crushed cells by negative numbers
        for j in range(C):
            if board[i][j] == 0: continue
            v = abs(board[i][j])
            # for vertical crush
            if i < R - 2 and v == abs(board[i+1][j]) == abs(board[i+2][j]):
                board[i][j] = board[i+1][j] = board[i+2][j] = -v # This is the key thought
                crushed = True
            # for horizontal crush
            if j < C - 2 and v == abs(board[i][j+1]) == abs(board[i][j+2]):
                board[i][j] = board[i][j+1] = board[i][j+2] = -v
                crushed = True
    if crushed:
        for j in range(C): # for each column, crush from bottom in code.
            row_idx = R - 1 # but logically crush from top.
            for i in range(R-1, -1, -1):
                if board[i][j] > 0:  # if not crushed, move down
                    board[row_idx][j] = board[i][j]
                    row_idx -= 1
            while row_idx >= 0:  # zero out above
                board[row_idx][j] = 0
                row_idx -= 1
    return self.candyCrush(board) if crushed else board

# LC741. Cherry Pickup
def cherryPickup(self, grid: List[List[int]]) -> int:
    # greedy is not working on separate walkers. Have to consider all walkers as whole state.
    if not grid: return 0
    n, m = len(grid), len(grid[0])
    @lru_cache(None)  # dp
    def dp(r1, c1, c2):
        r2 = r1 + c1 - c2 # go with diagonal levels, so that shortest steps reach this level first
        if r1 < 0 or r2 < 0 or c1 < 0 or c2 < 0 or grid[r1][c1] == -1 or grid[r2][c2] == -1:
            return float('-inf')
        # we ignore r2, c2 since r1, c1 already picks up the cherry here, if any
        if r1 == 0 and c1 == 0: return grid[r1][c1] # baseline
        cherry = grid[r1][c1] + (c1 != c2) * grid[r2][c2]
        total = max(dp(r1, c1-1, c2-1),  # left, left
                    dp(r1, c1-1, c2),    # left, up, r2 = r1 + c1 -1 -c2 = curr r2 - 1
                    dp(r1-1, c1, c2),    # up, up
                    dp(r1-1, c1, c2-1))  # up, left
        return cherry + total
    ret = max(0, dp(n-1, m-1, m-1))
    return ret

# LC490. The Maze - soccer ball
def hasPath(self, maze: List[List[int]], start: List[int], destination: List[int]) -> bool:
    q, visited = deque([start]), set()  # BFS super
    while q:
        i, j = q.popleft()
        if [i, j] == destination: return True
        for di,dj in [-1, 0], [0, -1], [1, 0], [0, 1]:
            ni, nj = i + di, j + dj
            while 0 <= ni < len(maze) and 0 <= nj < len(maze[0]) and maze[ni][nj] == 0:
                ni, nj = ni + di, nj + dj
            ni, nj = ni - di, nj - dj  # need to backout 1 step
            if (ni,nj) not in visited:
                visited.add((ni,nj))
                q.append((ni,nj))
    return False

# LC1926. Nearest Exit from Entrance in Maze
def nearestExit(self, maze: List[List[str]], start: List[int]) -> int:  # O(MN), BFS
    M, N = len(maze), len(maze[0])
    isExit = lambda i, j: not i or i == M - 1 or not j or j == N - 1
    que, seen, level = deque([[*start]]), {tuple(start)}, 0
    while que:
        for _ in range(len(que)):
            i, j = que.popleft()
            if isExit(i, j) and level: return level
            for u, v in [i - 1, j], [i, j + 1], [i + 1, j], [i, j - 1]:
                if M > u >= 0 <= v < N and maze[u][v] == '.' and (u, v) not in seen:
                    que.append([u, v])
                    seen.add((u, v))
        level += 1
    return -1

# LC62. Unique Paths - no blocks
def uniquePaths(self, m: int, n: int) -> int:
    return math.comb(m+n-2, n-1)  # select n-1 from m+n-2
def uniquePaths(self, m, n):
    if not m or not n: return 0
    cur = [1] * n  # first row
    for i in range(1, m):  # previous row + current row, 1st cell is always 1.
        for j in range(1, n): cur[j] += cur[j-1]  # previous cur[j] + current cur[j-1]
    return cur[-1]

# LC63. Unique Paths II - has blocks, from upper left to lower right
def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
    og = obstacleGrid
    n, m = len(og), len(og[0])
    if not m or not n: return 0
    idx = m
    for i, c in enumerate(og[0]):
        if c == 1:
            idx = i
            break
    cur = [1] * idx + [0] * (m - idx)
    for i in range(1, n):
        for j in range(0, m):
            if j == 0: # if previously not blocked, check now
                cur[j] = int(cur[j] != 0 and og[i][j] == 0)
            else:
                if og[i][j] == 1: cur[j] = 0
                else: cur[j] += cur[j-1]  # previous cur[j] + current cur[j-1]
    return cur[-1]

# LC980. Unique Paths III - has blocks, arbitrary start and end
def uniquePathsIII(self, A): # O(3^n)
    m, n, empty = len(A), len(A[0]), 1
    for i in range(m):  # find start x, y and count empty cells
        for j in range(n):
            if A[i][j] == 1: x, y = (i, j) # find start
            elif A[i][j] == 0: empty += 1 # count empty
    self.res = 0
    def dfs(x, y, empty): # DFS on cells and empty cell count
        if not (0 <= x < m and 0 <= y < n and A[x][y] >= 0):
            return # obstacles
        if A[x][y] == 2:
            self.res += empty == 0 # reach goal and touch all
            return
        A[x][y] = -2 # mark visited
        for i, j in (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1):
            dfs(i, j, empty - 1)
        A[x][y] = 0  # backout, since we need check history fills all empty cells
    dfs(x, y, empty)
    return self.res

# LC289. Game of Life
def gameOfLife(self, board: List[List[int]]) -> None: # 1 bit for old, 1 bit for new.
    m, n = len(board), len(board[0])
    for i in range(m): # use 2 bits for this life and future life
        for j in range(n):
            # find neighbours
            nbs = [board[r][c] & 1 for r in range(i-1, i+2) for c in range(j-1, j+2) if 0 <= r < m and 0 <=c < n]
            s = board[i][j]
            lp = sum(nbs) - s  # life support
            if s == 0 and lp == 3:  # LIVE
                board[i][j] = 2 + board[i][j]  # move new life state to 2nd bit. 2 = LIVE << 1
            elif s == 1 and (lp == 2 or lp == 3): board[i][j] = 2 + board[i][j]
            # else: # DEAD, don't need to do anything since 2nd bit is 0 already
    for i in range(m):  # we shift 2nd bit back to 1st bit, move from left to right
        for j in range(n):
            board[i][j] >>= 1

# LC361. Bomb Enemy
def maxKilledEnemies(self, grid):
    maxEnemy = 0
    tgrid = [list(i) for i in zip(*grid)]
    for i in range(len(grid)): # for each row, we duplicate scan for each seg(sep by walls)
        for j in range(len(grid[0])):
            if grid[i][j] == '0':
                maxEnemy = max(maxEnemy,
                               self.countEInRow(j, grid[i]) + self.countEInRow(i, tgrid[j]))
    return maxEnemy
def countEInRow(self, i, row):
    #if len(row) == 1: return 0
    tempE = 0
    for j in range(i+1, len(row)): # move right
        if row[j] == 'E': tempE += 1
        if row[j] == 'W': break
    for j in range(i-1,-1,-1): # move left
        if row[j] == 'E': tempE += 1
        if row[j] == 'W': break
    return tempE

# LC909. Snakes and Ladders
def snakesAndLadders(self, board: List[List[int]]) -> int:
    n = len(board)
    def coord(order):
        q, r = divmod(order-1, n)
        x = n - 1 - q
        y = r if q % 2 == 0 else n-1-r  # even and odd rows
        return x, y
    queue, visited = deque([(1, 0)]), set()  # order, steps
    maxs = n * n
    while queue: # BFS to get min
        x, s = queue.popleft()
        if x == maxs: return s
        if x in visited: continue
        visited.add(x)
        for i in range(6):
            move = x + i + 1
            if move > maxs: continue
            x1, y1 = coord(move)
            if board[x1][y1] != -1: move = board[x1][y1]
            if move not in visited:
                queue.append((move, s+1))
    return -1


