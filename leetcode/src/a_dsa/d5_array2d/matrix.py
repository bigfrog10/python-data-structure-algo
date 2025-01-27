from typing import List
import itertools

# LC407. Trapping Rain Water II
def trapRainWater(self, heights: List[List[int]]) -> int:
    if not heights: return 0
    n, m = len(heights), len(heights[0])  # O(nmlog(nm))
    heap, visited = [], set()
    for i in range(n): # put all boundary cells into heap
        for j in [0, m-1]: # only 2 columns
            heap.append((heights[i][j], i, j))
            visited.add((i, j))
    for j in range(1, m-1):
        for i in [0, n-1]: # only 2 rows
            heap.append((heights[i][j], i, j))
            visited.add((i, j))
    heapq.heapify(heap)
    vmax = ret = 0
    while heap:
        h, i, j = heapq.heappop(heap)
        vmax = max(vmax, h)  # later cells are bigger than this
        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            x, y = i + dx, j + dy
            if 0 <= x < n and 0 <= y < m and (x, y) not in visited:
                nh = heights[x][y]
                ret += max(0, vmax - nh)
                heapq.heappush(heap, (nh, x, y))
                visited.add((x, y))
    return ret

# LC1572. Matrix Diagonal Sum
def diagonalSum(self, mat: List[List[int]]) -> int:
    n = len(mat)
    ans = idx = 0
    for row in mat:
        ans += row[idx] + row[~idx]
        idx += 1
    if n % 2 == 1: ans -= mat[n // 2][n // 2]
    return ans

# LC1886. Determine Whether Matrix Can Be Obtained By Rotation matrix rotation
def findRotation(self, mat: List[List[int]], target: List[List[int]]) -> bool:
    for _ in range(4): # 4 possible directions
        if mat == target: return True
        mat = [list(x) for x in zip(*mat[::-1])]
    return False

# LC48. Rotate Image
def rotate(self, A):
    A[:] = zip(*A[::-1])
def rotate(self, matrix: List[List[int]]) -> None:  # O(n^2)
    n = len(matrix)
    for i in range(n//2): matrix[i], matrix[~i] = matrix[~i], matrix[i]
    for i,j in itertools.combinations(range(n), 2):  # flip around diagonal
        matrix[j][i], matrix[i][j] = matrix[i][j], matrix[j][i]
def rotate(self, matrix: List[List[int]]) -> None:  # right clockwise by 90 degrees
    n = len(matrix[0])
    for i in range(n // 2 + n % 2):
        for j in range(n // 2):
            tmp = matrix[n - 1 - j][i]
            matrix[n - 1 - j][i] = matrix[n - 1 - i][n - j - 1]
            matrix[n - 1 - i][n - j - 1] = matrix[j][n - 1 - i]
            matrix[j][n - 1 - i] = matrix[i][j]
            matrix[i][j] = tmp
def transpose(self, matrix):  # flip along diagonal
    return zip(*matrix)
def reflect(self, matrix):  # flip from left to right
    return [matrix[i][::-1] for i in range(len(matrix))]

# LC867. Transpose Matrix
def transpose(self, matrix: List[List[int]]) -> List[List[int]]:  # O(mn)
    return zip(*matrix)
def transpose(self, A: List[List[int]]) -> List[List[int]] :
    R, C = len(A), len(A[0])
    ans = [[None] * R for _ in range(C)]
    for r, row in enumerate(A):
        for c, val in enumerate(row):
            ans[c][r] = val
    return ans

# LC149. Max Points on a Line
def maxPoints(self, points: List[List[int]]) -> int:  # O(n^2)
    points.sort()
    slope, res = defaultdict(int), 0
    for i, (x1, y1) in enumerate(points):
        slope.clear()
        for x2, y2 in points[i + 1:]:
            dx, dy = x2 - x1, y2 - y1  # this is where we need sort
            g = gcd(dx, dy)
            m = (dx // g, dy // g)
            slope[m] += 1
            res = max(res, slope[m])
    return res + 1  # plus the 1st point

# LC632. Smallest Range Covering Elements from K Lists small range small k list range k list small
def smallestRange(self, nums: List[List[int]]) -> List[int]:  # O(nlogk) time, O(k) space, n total # of elements
    pq = [(row[0], i, 0) for i, row in enumerate(nums)] # push 1st element from each list
    heapq.heapify(pq) # (value, row, column)  n = len(nums)
    ans = -inf, inf
    right = max(row[0] for row in nums)
    while pq:
        left, i, j = heapq.heappop(pq)  # min value
        if right - left < ans[1] - ans[0]: ans = left, right # track ans
        if j + 1 == len(nums[i]): return ans # the min row reached end
        v = nums[i][j+1] # replace minimal value with next one in same list
        right = max(right, v)
        heapq.heappush(pq, (v, i, j+1))

# LC498. Diagonal Traverse
def findDiagonalOrder(self, matrix):  # O(mn) time, O(1) space
    if not matrix: return []
    m, n = len(matrix), len(matrix[0])
    ret = []
    row = col = 0
    for _ in range(m * n):
        ret.append(matrix[row][col])
        if (row + col) % 2 == 0:  # start from row, move up
            if col == n - 1: row += 1  # hit right, move down
            elif row == 0: col += 1  # hit top, move right
            else:  # the order of if-else check is significant
                row -= 1
                col += 1
        else:  # start from col, move down
            if row == m - 1: col += 1  # hit bottom, move right
            elif col == 0: row += 1  # hit left, move down
            else:
                row += 1
                col -= 1
    return ret

# LC1428. Leftmost Column with at Least a One - sorted 01 matrix leftmost one leftmost 1
def leftMostColumnWithOne(self, binaryMatrix: 'BinaryMatrix') -> int:  # O(n + m), diagonal
    rows, cols = binaryMatrix.dimensions()
    row, col = 0, cols - 1  # upper right corner
    while row < rows and col >= 0:
        if binaryMatrix.get(row, col) == 0: row += 1  # move down
        else: col -= 1  # move left
    # If we never left the last column, it must have been all 0's.
    return col + 1 if col != cols - 1 else -1

# LC766. Toeplitz Matrix
def isToeplitzMatrix(self, matrix):  # O(mn) runtime, O(1) space, has follow ups
    return all(r == 0 or c == 0 or matrix[r-1][c-1] == val
               for r, row in enumerate(matrix)
               for c, val in enumerate(row))
def isToeplitzMatrix(self, m):
    return all(r1[:-1] == r2[1:] for r1,r2 in zip(m, m[1:]))

# LC1424. Diagonal Traverse II
def findDiagonalOrder(self, nums: List[List[int]]) -> List[int]:
    res = defaultdict(list)
    for i, r in enumerate(nums):
        for j, a in enumerate(r): res[i + j].append(a)
    return [a for r in res.values() for a in reversed(r)]

# LC311. Sparse Matrix Multiplication
def multiply(self, A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    if not A or not A[0] or not B or not B[0]: return [[]]  # O(m⋅k⋅n) time and O(mn) space
    def get_none_zero(A):
        n, m, res = len(A), len(A[0]), []
        for i, j in itertools.product(range(n), range(m)):
            if A[i][j] != 0: res.append((i, j, A[i][j]))  # we should model sparse matrix like this
        return res  # this list should use smaller space than the matrix
    sparse_A, sparse_B = get_none_zero(A), get_none_zero(B)
    n, m, k = len(A), len(A[0]), len(B[0])
    C = [[0] * k for _ in range(n)]
    for i, j, val_A in sparse_A:
        for x, y, val_B in sparse_B:
            if j == x: C[i][y] += val_A * val_B
    return C
def multiply(self, mat1: List[List[int]], mat2: List[List[int]]) -> List[List[int]]:
    ans = [[0] * len(mat2[0]) for _ in range(len(mat1))]
    for ri, row in enumerate(mat1):
        for ci, cell in enumerate(row):
            if cell:
                for k, c1 in enumerate(mat2[ci]):
                    ans[ri][k] += cell * c1
    return ans

# LC378. Kth Smallest Element in a Sorted Matrix
def kthSmallest(self, matrix: List[List[int]], k: int) -> int:  # O(klogk) time and O(k) space
    m, n = len(matrix), len(matrix[0])  # For general, the matrix need not be a square
    minHeap = []  # val, r, c
    for r in range(min(k, m)):  # x = min(k, m), space O(x), time O(x + klogx)
        heappush(minHeap, (matrix[r][0], r, 0))  # need location to get next cell
    ans = -1  # any dummy value
    for i in range(k):
        ans, r, c = heappop(minHeap)  # find min pointer and move it
        if c+1 < n: heappush(minHeap, (matrix[r][c + 1], r, c + 1))
    return ans  # find kth smallest in m sorted lists
def kthSmallest(self, matrix, k):
    m, n = len(matrix), len(matrix[0])  # For general, the matrix need not be a square
    def countLessOrEqual(x):
        cnt = 0
        c = n - 1  # start with the rightmost column
        for r in range(m):
            while c >= 0 and matrix[r][c] > x: c -= 1  # decrease column until matrix[r][c] <= x
            cnt += (c + 1)
        return cnt
    left, right = matrix[0][0], matrix[-1][-1]
    ans = -1
    while left <= right:
        mid = (left + right) // 2
        if countLessOrEqual(mid) >= k:
            ans = mid
            right = mid - 1  # try to looking for a smaller value in the left side
        else:
            left = mid + 1  # try to looking for a bigger value in the right side
    return ans

# LC2033. Minimum Operations to Make a Uni-Value Grid - uni value, univalue
def minOperations(self, grid: List[List[int]], x: int) -> int:
    vals = list(itertools.chain(*grid))  # flatting matrix to array - [[2,4],[6,8]] ->  [2,4,6,8]
    if len(set(val % x for val in vals)) > 1: return -1  # if we have 2 diff residues, can't do it.
    median = heapq.nlargest((len(vals)+1) // 2, vals)[-1]  # O(N) possible via "quick select", return 6 for 8, 6
    return sum(abs(val - median)//x for val in vals)

# LC1861. Rotating the Box - stones, obstacles
def rotateTheBox(self, box: List[List[str]]) -> List[List[str]]:
    for row in box:
        bottom = len(row) - 1            # initialize with the last position in row
        for j in range(len(row))[::-1]:  # iterate from the end of the row
            if row[j] == "*":            # we cannot move stones behind obstacles,
                bottom = j - 1           # so update move position to the first before obstacle
            elif row[j] == "#":          # if stone, move it to the "move_position"
                row[bottom], row[j] = row[j], row[bottom]
                bottom -= 1
    return zip(*box[::-1])               # rotate array, or list(...)

# LC1878. Get Biggest Three Rhombus Sums in a Grid
def getBiggestThree(self, grid):  # O(C), C number of cells
    m, n, heap = len(grid), len(grid[0]), []

    def update(heap, num):
        if num not in heap:
            heappush(heap, num)
            if len(heap) > 3: heappop(heap)
        return heap

    for num in chain(*grid): update(heap, num)

    @lru_cache(None)
    def dp(i, j, dr):
        if not 0 <= i < n or not 0 <= j < m: return 0
        return dp(i-1, j+dr, dr) + grid[j][i]

    for q in range(1, (1 + min(m, n))//2):  # q is center to point length in the square case
        for i in range(q, n - q):
            for j in range(q, m - q):
                p1 = dp(i + q, j, -1) - dp(i, j - q, -1)  # upper right edge without upper point
                p2 = dp(i - 1, j + q - 1, -1) - dp(i - q - 1, j - 1, -1)  # lower left edge without lower point
                p3 = dp(i, j - q, 1) - dp(i - q, j, 1)  # upper left edge without left point
                p4 = dp(i + q - 1, j + 1, 1) - dp(i - 1, j + q + 1, 1)  # lower right edge without right point
                update(heap, p1 + p2 + p3 + p4)

    return sorted(heap)[::-1]

# LC764. Largest Plus Sign  axis-aligned  axis aligned
def orderOfLargestPlusSign(self, n: int, mines: List[List[int]]) -> int:  # O(n^2)
    grid = [[n] * n for _ in range(n)]  # max plus size for plus sign centered at (i,j)
    for x, y in mines: grid[x][y] = 0
    for i in range(n):
        l, r, u, d = 0, 0, 0, 0  # how far can reach in each direction
        for j in range(n):
            # set counters
            l = l + 1 if grid[i][j] != 0 else 0
            r = r + 1 if grid[i][n-j-1] != 0 else 0
            u = u + 1 if grid[j][i] != 0 else 0
            d = d + 1 if grid[n-j-1][i] != 0 else 0

            grid[i][j] = min(grid[i][j], l)
            grid[i][n-j-1] = min(grid[i][n-j-1], r)
            grid[j][i] = min(grid[j][i], u)
            grid[n-j-1][i] = min(grid[n-j-1][i], d)
    return max(map(max, grid))
# https://leetcode.com/problems/largest-plus-sign/solutions/4204626/764-memory-beats-91-40-solution-with-step-by-step-explanation/?envType=company&envId=facebook&favoriteSlug=facebook-three-months

# LC74. Search a 2D Matrix - matrix binary search elem in matrix, matrix bs, search 2d matrix search matrix
def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:  # O(log(mn))
    if not matrix: return False
    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1 # binary search
    while left <= right:
        pivot_idx = (left + right) // 2
        pivot_element = matrix[pivot_idx // n][pivot_idx % n]
        if target == pivot_element: return True
        elif target < pivot_element: right = pivot_idx - 1
        else: left = pivot_idx + 1
    return False

# LC1074. Number of Submatrices That Sum to Target - area sum to target
def numSubmatrixSumTarget(self, A, target):
    m, n = len(A), len(A[0])
    for row in A:
        for i in range(n - 1):
            row[i + 1] += row[i]  # sum up each row
    res = 0
    for i in range(n):  # loop 2 columns
        for j in range(i, n):  # O(mnn) runtime and O(m) space
            c = collections.defaultdict(int)
            cur, c[0] = 0, 1
            for k in range(m):  # 560. Subarray Sum Equals K, 1D case
                cur += A[k][j] - (A[k][i - 1] if i > 0 else 0)
                res += c[cur - target]
                c[cur] += 1
    return res



# LC542. 01 Matrix - distance to near 0  binary matrix
def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:  # O(rc)
    m, n = len(mat), len(mat[0])
    for r in range(m):
        for c in range(n):
            if mat[r][c] > 0:  # reuse top and left
                top = mat[r - 1][c] if r > 0 else math.inf
                left = mat[r][c - 1] if c > 0 else math.inf
                mat[r][c] = 1 + min(top, left)
    for r in range(m - 1, -1, -1):
        for c in range(n - 1, -1, -1):
            if mat[r][c] > 0:
                bottom = mat[r + 1][c] if r < m - 1 else math.inf
                right = mat[r][c + 1] if c < n - 1 else math.inf
                mat[r][c] = min(mat[r][c], bottom + 1, right + 1)
    return mat
# https://leetcode.com/problems/01-matrix/solutions/5676804/simple-solution-with-diagrams-in-video-javascript-c-java-python/?envType=company&envId=apple&favoriteSlug=apple-more-than-six-months

# LC73. Set Matrix Zeroes
def setZeroes(self, matrix):
    m, n = len(matrix), len(matrix[0])
    firstRowHasZero = not all(matrix[0])  # First row has zero?
    # first column's zero is marked by c[0][0]
    for i in range(1, m):  # Use first row/column as marker, scan the matrix
        for j in range(n):
            if matrix[i][j] == 0: matrix[0][j] = matrix[i][0] = 0
    for i in range(1, m): # Set the zeros
        for j in range(n - 1, -1, -1):
            if matrix[i][0] == 0 or matrix[0][j] == 0: matrix[i][j] = 0
    # Set the zeros for the first row
    if firstRowHasZero: matrix[0] = [0] * n

# LC661. Image Smoother
def imageSmoother(self, img: List[List[int]]) -> List[List[int]]:  # O(mn)
    m, n = len(img), len(img[0])
    res = copy.deepcopy(img)
    for x in range(m):
        for y in range(n):
            neighbors = [img[_x][_y] for _x in (x-1, x, x+1) for _y in (y-1, y, y+1)
                                     if 0 <= _x < m and 0 <= _y < n]
            res[x][y] = sum(neighbors) // len(neighbors)
    return res



# LC1329. Sort the Matrix Diagonally
def diagonalSort(self, mat: List[List[int]]) -> List[List[int]]:
    n, m = len(mat), len(mat[0])
    d = collections.defaultdict(list)
    for i in range(n):
        for j in range(m): d[i - j].append(mat[i][j])
    for k in d: d[k].sort(reverse=1)
    for i in range(n):
        for j in range(m): mat[i][j] = d[i - j].pop()
    return mat

# LC1901. Find a Peak Element II  2d matrix
def findPeakGrid(self, mat: List[List[int]]) -> List[int]:  # O(mlogn)
    top, bottom = 0, len(mat)-1
    while bottom > top:  # find row max
        mid = (top + bottom) // 2
        if max(mat[mid]) > max(mat[mid+1]): bottom = mid
        else: top = mid+1
    return [bottom, mat[bottom].index(max(mat[bottom]))]
def findPeakGrid(self, mat: List[List[int]]) -> List[int]:  # O(m + n)
    m, n = len(mat), len(mat[0])
    def quad_search(s0, e0, s1, e1):
        m0, m1 = (s0 + e0) // 2, (s1 + e1) // 2
        i, j = m0, m1
        for jj in range(s1, e1):  # find max along middle lines
            if mat[m0][jj] > mat[m0][j]: j = jj
        for ii in range(s0, e0):
            if mat[ii][m1] > mat[i][j]: i, j = ii, m1
        cur = mat[i][j]  # compare with 4 sides
        up = mat[i-1][j] if i > 0 else -1
        down = mat[i+1][j] if i < m - 1 else -1
        left = mat[i][j-1] if j > 0 else -1
        right = mat[i][j+1] if j < n - 1 else - 1
        if cur > up and cur > down and cur > left and cur > right:
            return i, j
        if i < m0 or (i == m0 and cur < up): e0 = m0  # move interval boundaries
        else: s0 = m0 + 1
        if j < m1 or (j == m1 and cur < left): e1 = m1
        else: s1 = m1 + 1
        return quad_search(s0, e0, s1, e1)  # drill down
    return quad_search(0, m, 0, n)



# LC221. Maximal Square  max square
def maximalSquare(self, matrix: List[List[str]]) -> int: # DP
    if not matrix: return 0
    rows, cols = len(matrix), len(matrix[0])
    # DP(i, j) is the largest side of all squares ended at (i, j)
    dp = collections.defaultdict(int)  # O(mn)
    max_len = 0  # track this
    for i, j in itertools.product(range(rows), range(cols)):
        if matrix[i][j] == '1':
            dp[i+1, j+1] = 1 + min([dp[i+1, j], dp[i, j+1], dp[i, j]])  # weakest link
            max_len = max(max_len, dp[i+1, j+1])
    return max_len ** 2
# https://leetcode.com/problems/maximal-square/?envType=company&envId=apple&favoriteSlug=apple-six-months

# LC240. Search a 2D Matrix II - zigzag search 2d matrix
def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
    if not matrix: return False
    h, w = len(matrix), len(matrix[0])
    row, col = h - 1, 0
    while row >= 0 and col < w:
        if target == matrix[row][col]: return True
        elif target < matrix[row][col]:  row -= 1
        else: col += 1
    return False

# LC1351. Count Negative Numbers in a Sorted Matrix - zigzag
def countNegatives(self, grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])  # O(m + n)
    r, c, cnt = m - 1, 0, 0
    while r >= 0 and c < n:
        if grid[r][c] < 0:
            cnt += n - c
            r -= 1
        else: c += 1
    return cnt

# LC1314. Matrix Block Sum
def matrixBlockSum(self, mat: List[List[int]], K: int) -> List[List[int]]:
    m, n = len(mat), len(mat[0])
    rangeSum = [[0] * (n + 1) for _ in range(m + 1)] # 0 row and col are dummy
    for i in range(m):
        for j in range(n):
            rangeSum[i + 1][j + 1] = rangeSum[i + 1][j] + rangeSum[i][j + 1] - rangeSum[i][j] + mat[i][j]
    ans = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            r1, c1, r2, c2 = max(0, i - K), max(0, j - K), min(m, i + K + 1), min(n, j + K + 1)
            ans[i][j] = rangeSum[r2][c2] - rangeSum[r1][c2] - rangeSum[r2][c1] + rangeSum[r1][c1]
    return ans

# LC1274. Number of Ships in a Rectangle
def countShips(self, sea, P, Q):  # P - topRight, Q - bottomLeft
    res = 0
    if P.x >= Q.x and P.y >= Q.y and sea.hasShips(P, Q):
        if P.x == Q.x and P.y == Q.y: return 1
        mx, my = (P.x + Q.x) // 2, (P.y + Q.y) // 2
        # upper right
        res += self.countShips(sea, P, Point(mx + 1, my + 1))
        # upper left
        res += self.countShips(sea, Point(mx, P.y), Point(Q.x, my + 1))
        # lower left
        res += self.countShips(sea, Point(mx, my), Q)
        # lower right
        res += self.countShips(sea, Point(P.x, my), Point(mx + 1, Q.y))
    return res

# LC54. Spiral Matrix, top100 - return elems in spiral
def spiralOrder(self, matrix: List[List[int]]) -> List[int]:  # O(mn)
    m, n = len(matrix), len(matrix[0])
    step = 1 # Start off going right/down vs left/up
    i, j = 0, -1
    output = []
    while min(m,n) > 0:
        for _ in range(n): # move horizontally
            j += step
            output.append(matrix[i][j])
        m -= 1
        for _ in range(m): # move vertically
            i += step
            output.append(matrix[i][j])
        n -= 1
        step *= -1 # flip dir
    return output
def spiralOrder(self, matrix):  # O(mn) time
    res = []
    while matrix:
        res.extend(matrix.pop(0))
        # zip rows to columns, flattern each column, reverse order
        matrix = [*zip(*matrix)][::-1]
    return res
# [[1,2,3],[4,5,6],[7,8,9]] ->  [(6, 9), (5, 8), (4, 7)] ->  [(8, 7), (5, 4)] -> [(4,), (5,)] -> [(5,)]
def spiralOrder(self, matrix):  # O(mn) time, O(1) space
    result = []
    while matrix:
        if matrix[0]: result += matrix.pop(0)  # pop 1st row
        if matrix and matrix[0]:  # pop last element
            for row in matrix: result.append(row.pop())
        if matrix:  # pop last row
            result += matrix.pop()[::-1]
        if matrix and matrix[0]:  # pop 1st cell in each row reverse
            for row in matrix[::-1]: result.append(row.pop(0))
    return result

# LC59. Spiral Matrix II  generate
def generateMatrix(self, n: int) -> List[List[int]]:  # same logic as spiral matrix
    step = 1 # Start off going right/down vs left/up
    i, j = 0, -1
    k = 1
    res = [[0 for _ in range(n)] for _ in range(n)]
    m = n
    while n > 0:
        for _ in range(n): # move horizontally
            j += step
            res[i][j] = k
            k += 1
        m -= 1
        for _ in range(m): # move vertically
            i += step
            res[i][j] = k
            k += 1
        n -= 1
        step *= -1 # flip dir
    return res

# LC885. Spiral Matrix III
def spiralMatrixIII(self, R, C, r0, c0):
    i, j = r0, c0
    res = [[r0, c0]]
    step_size = sign = 1
    while len(res) < R*C:
        for _ in range(step_size):
            j += sign # follow row
            if 0 <= i < R and 0 <= j < C: res.append([i, j])
        for _ in range(step_size):
            i += sign # follow column
            if 0 <= i < R and 0 <= j < C: res.append([i, j])
        step_size += 1
        sign *= -1
    return res

















