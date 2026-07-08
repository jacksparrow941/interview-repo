"""Full answers for DSA coding questions (c001-c080) from questions_coding.py."""

def A(*s):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in s]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

FULL_ANSWERS_CODING = {

"c001": A(("Approach","Use a hash map to store <code>complement = target - num</code> as you iterate. "
    "If current number exists in map → found the pair."),
  ("Solution","<pre>def twoSum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        if num in seen:\n            return [seen[num], i]\n        seen[target - num] = i</pre>"),
  ("Complexity","Time: O(n) | Space: O(n)"),
  ("Follow-ups",'<div class="followup">• What if the array is sorted? (two pointers, O(1) space)<br>'
    '• What if we need ALL pairs? (collect instead of return first)<br>• 4-Sum approach?</div>')),

"c002": A(("Approach","Sort array. For each element, use two pointers on the rest to find pairs summing to -nums[i]. "
    "Skip duplicates at each level."),
  ("Solution","<pre>def threeSum(nums):\n    nums.sort(); res = []\n    for i in range(len(nums)-2):\n        if i &gt; 0 and nums[i] == nums[i-1]: continue\n        l, r = i+1, len(nums)-1\n        while l &lt; r:\n            s = nums[i]+nums[l]+nums[r]\n            if s == 0: res.append([nums[i],nums[l],nums[r]]); l+=1; r-=1\n            while l &lt; r and nums[l]==nums[l-1]: l+=1\n            while l &lt; r and nums[r]==nums[r+1]: r-=1\n            elif s &lt; 0: l+=1\n            else: r-=1\n    return res</pre>"),
  ("Complexity","Time: O(n²) | Space: O(1) excluding output"),
  ("Follow-ups",'<div class="followup">• How does 4-Sum extend this? (add outer loop, O(n³))<br>'
    '• What is the hash-map approach and why is two-pointer preferred?</div>')),

"c003": A(("Kadane's Algorithm","Track current subarray sum. If it goes negative, reset to 0 (start fresh). "
    "Track global maximum throughout."),
  ("Solution","<pre>def maxSubArray(nums):\n    cur = best = nums[0]\n    for n in nums[1:]:\n        cur = max(n, cur + n)\n        best = max(best, cur)\n    return best</pre>"),
  ("Complexity","Time: O(n) | Space: O(1)"),
  ("Extension","For indices: track start/end/temp_start. For 2D: apply Kadane on column sums for each row pair."),
  ("Follow-ups",'<div class="followup">• What if we need the actual subarray (not just the sum)?<br>'
    '• Maximum product subarray — how is it different? (track both min and max because negatives)</div>')),

"c004": A(("Approach","Prefix product from left, then multiply with suffix product from right in one pass. No division needed."),
  ("Solution","<pre>def productExceptSelf(nums):\n    n = len(nums); res = [1]*n\n    # Left pass\n    prefix = 1\n    for i in range(n):\n        res[i] = prefix; prefix *= nums[i]\n    # Right pass\n    suffix = 1\n    for i in range(n-1,-1,-1):\n        res[i] *= suffix; suffix *= nums[i]\n    return res</pre>"),
  ("Complexity","Time: O(n) | Space: O(1) (output array not counted)"),
  ("Follow-ups",'<div class="followup">• What if zeros are in the array?<br>'
    '• Can you solve with division in O(n) but handle zeros? (count zeros separately)</div>')),

"c005": A(("Approach","Two pointer from both ends. Track left_max and right_max. "
    "Water at index i = min(left_max, right_max) - height[i]. Move the shorter side inward."),
  ("Solution","<pre>def trap(height):\n    l, r = 0, len(height)-1\n    lmax = rmax = water = 0\n    while l &lt; r:\n        if height[l] &lt;= height[r]:\n            if height[l] &gt;= lmax: lmax = height[l]\n            else: water += lmax - height[l]\n            l += 1\n        else:\n            if height[r] &gt;= rmax: rmax = height[r]\n            else: water += rmax - height[r]\n            r -= 1\n    return water</pre>"),
  ("Complexity","Time: O(n) | Space: O(1)"),
  ("Follow-ups",'<div class="followup">• Stack-based approach — how does it differ?<br>'
    '• 3D version of trapping rain water?</div>')),

"c007": A(("Approach","Binary search: if mid &gt;= right, minimum is in left half (including mid is rotation boundary). "
    "Otherwise minimum is in right half (excluding mid)."),
  ("Solution","<pre>def findMin(nums):\n    l, r = 0, len(nums)-1\n    while l &lt; r:\n        mid = (l+r)//2\n        if nums[mid] &gt; nums[r]: l = mid+1\n        else: r = mid\n    return nums[l]</pre>"),
  ("Complexity","Time: O(log n) | Space: O(1)"),
  ("Follow-ups",'<div class="followup">• What if duplicates exist? (need O(n) worst case)<br>'
    '• How does this extend to Search in Rotated Array (c008)?</div>')),

"c009": A(("Approach","One pass. Track running minimum price. At each step, compute profit = price - min_price. Track max profit."),
  ("Solution","<pre>def maxProfit(prices):\n    min_p, profit = float('inf'), 0\n    for p in prices:\n        min_p = min(min_p, p)\n        profit = max(profit, p - min_p)\n    return profit</pre>"),
  ("Complexity","Time: O(n) | Space: O(1)"),
  ("Follow-ups",'<div class="followup">• Best time to buy and sell stock II — unlimited transactions? (sum all positive differences)<br>'
    '• Stock with cooldown? (DP with states)<br>• At most k transactions? (DP)</div>')),

"c010": A(("Approach","Sort by start time. Merge if next interval starts ≤ current end. Extend current end to max of both."),
  ("Solution","<pre>def merge(intervals):\n    intervals.sort(key=lambda x: x[0])\n    res = [intervals[0]]\n    for s, e in intervals[1:]:\n        if s &lt;= res[-1][1]: res[-1][1] = max(res[-1][1], e)\n        else: res.append([s, e])\n    return res</pre>"),
  ("Complexity","Time: O(n log n) | Space: O(n)"),
  ("Follow-ups",'<div class="followup">• Insert interval into sorted list of non-overlapping intervals?<br>'
    '• Meeting rooms — is there any conflict? (sort + check adjacent)<br>'
    '• Minimum meeting rooms needed? (heap tracking end times)</div>')),

"c011": A(("Approach","Prefix sum: if prefixSum[j] - prefixSum[i] = k, then subarray i+1..j sums to k. "
    "Store count of each prefix sum in a hash map."),
  ("Solution","<pre>def subarraySum(nums, k):\n    count = prefix = 0\n    freq = {0: 1}\n    for n in nums:\n        prefix += n\n        count += freq.get(prefix - k, 0)\n        freq[prefix] = freq.get(prefix, 0) + 1\n    return count</pre>"),
  ("Complexity","Time: O(n) | Space: O(n)"),
  ("Follow-ups",'<div class="followup">• What if we need longest subarray with sum k? (store first occurrence of prefix sum)<br>'
    '• Binary subarray with sum? (same technique)<br>'
    '• Product of subarray = k (harder — use division, handle zeros)</div>')),

"c021": A(("Approach","Sliding window with a set. Expand right pointer. If duplicate found, shrink left pointer until duplicate removed."),
  ("Solution","<pre>def lengthOfLongestSubstring(s):\n    seen = {}; l = res = 0\n    for r, c in enumerate(s):\n        if c in seen and seen[c] &gt;= l:\n            l = seen[c] + 1\n        seen[c] = r\n        res = max(res, r - l + 1)\n    return res</pre>"),
  ("Complexity","Time: O(n) | Space: O(min(m,n)) where m = charset size"),
  ("Follow-ups",'<div class="followup">• At most 2 distinct characters? (sliding window with count map)<br>'
    '• At most k distinct characters? (generalize with deque or count map)</div>')),

"c023": A(("Approach","Group strings by sorted-character key. Anagrams share the same sorted string."),
  ("Solution","<pre>from collections import defaultdict\ndef groupAnagrams(strs):\n    groups = defaultdict(list)\n    for s in strs:\n        groups[tuple(sorted(s))].append(s)\n    return list(groups.values())</pre>"),
  ("Optimization","Use tuple of 26-char counts as key instead of sorting: O(n) per string instead of O(k log k)."),
  ("Complexity","Time: O(n·k log k) | Space: O(n·k)"),
  ("Follow-ups",'<div class="followup">• How does the character-count key approach improve time complexity?<br>'
    '• What if we need anagram index grouping?</div>')),

"c026": A(("Approach","Use a stack. Push open brackets. When closing bracket found, check if top of stack is matching open."),
  ("Solution","<pre>def isValid(s):\n    stack = []\n    match = {')':'(', ']':'[', '}':'{'}\n    for c in s:\n        if c in match:\n            if not stack or stack[-1] != match[c]: return False\n            stack.pop()\n        else: stack.append(c)\n    return not stack</pre>"),
  ("Complexity","Time: O(n) | Space: O(n)"),
  ("Follow-ups",'<div class="followup">• Valid parenthesis string with wildcard *? (greedy or DP)<br>'
    '• Minimum additions to make string valid? (unmatched opens + unmatched closes)</div>')),

"c031": A(("Approach","Iterative inorder: use explicit stack. Go left as far as possible, process node, move right."),
  ("Solution","<pre>def inorderTraversal(root):\n    res, stack, cur = [], [], root\n    while cur or stack:\n        while cur:\n            stack.append(cur); cur = cur.left\n        cur = stack.pop()\n        res.append(cur.val)\n        cur = cur.right\n    return res</pre>"),
  ("Complexity","Time: O(n) | Space: O(h) where h = tree height"),
  ("Follow-ups",'<div class="followup">• Morris traversal — O(1) space inorder? (thread right pointers temporarily)<br>'
    '• Iterative preorder and postorder?</div>')),

"c033": A(("Approach","DFS passing valid range (min_val, max_val). Each node must be strictly within its range. "
    "Left subtree: max = current node. Right subtree: min = current node."),
  ("Solution","<pre>def isValidBST(root, lo=float('-inf'), hi=float('inf')):\n    if not root: return True\n    if not (lo &lt; root.val &lt; hi): return False\n    return (isValidBST(root.left, lo, root.val) and\n            isValidBST(root.right, root.val, hi))</pre>"),
  ("Complexity","Time: O(n) | Space: O(h)"),
  ("Follow-ups",'<div class="followup">• What is wrong with comparing only left.val &lt; node.val &lt; right.val?<br>'
    '• Recover BST with two swapped nodes? (inorder + find inversion)</div>')),

"c035": A(("Approach","BFS with queue. Process all nodes at current level before moving to next. "
    "Use level size or sentinel None to track level boundaries."),
  ("Solution","<pre>from collections import deque\ndef levelOrder(root):\n    if not root: return []\n    res, q = [], deque([root])\n    while q:\n        level = []\n        for _ in range(len(q)):\n            node = q.popleft()\n            level.append(node.val)\n            if node.left: q.append(node.left)\n            if node.right: q.append(node.right)\n        res.append(level)\n    return res</pre>"),
  ("Complexity","Time: O(n) | Space: O(w) where w = max width"),
  ("Follow-ups",'<div class="followup">• Zigzag level order? (alternate direction each level)<br>'
    '• Right side view? (take last element of each level)<br>'
    '• Average of each level?</div>')),

"c041": A(("Approach","DFS or BFS. When land cell found, increment count and DFS to mark all connected land as visited."),
  ("Solution","<pre>def numIslands(grid):\n    if not grid: return 0\n    count = 0\n    def dfs(r, c):\n        if r &lt; 0 or r &gt;= len(grid) or c &lt; 0 or c &gt;= len(grid[0]): return\n        if grid[r][c] != '1': return\n        grid[r][c] = '0'  # mark visited\n        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:\n            dfs(r+dr, c+dc)\n    for r in range(len(grid)):\n        for c in range(len(grid[0])):\n            if grid[r][c] == '1':\n                count += 1; dfs(r, c)\n    return count</pre>"),
  ("Union-Find alternative","<code>find</code> with path compression + <code>union</code> by rank. O(α(n)) per operation. Good for streaming updates."),
  ("Complexity","Time: O(m×n) | Space: O(m×n) recursion stack"),
  ("Follow-ups",'<div class="followup">• Max area of island? (count cells in each DFS)<br>'
    '• Number of distinct islands (accounting for shape)? (encode DFS path)<br>'
    '• Surrounded regions (capture)?</div>')),

"c042": A(("Approach","DFS with 3-color marking: WHITE(0)=unvisited, GRAY(1)=in-current-path, BLACK(2)=done. "
    "Cycle detected if GRAY node encountered again."),
  ("Solution","<pre>def canFinish(numCourses, prerequisites):\n    graph = [[] for _ in range(numCourses)]\n    for a, b in prerequisites: graph[b].append(a)\n    color = [0] * numCourses\n    def dfs(v):\n        if color[v] == 1: return False  # cycle\n        if color[v] == 2: return True\n        color[v] = 1\n        if not all(dfs(u) for u in graph[v]): return False\n        color[v] = 2; return True\n    return all(dfs(v) for v in range(numCourses))</pre>"),
  ("Complexity","Time: O(V+E) | Space: O(V+E)"),
  ("Follow-ups",'<div class="followup">• Return actual order (Course Schedule II)? Kahn\'s BFS topo sort.<br>'
    '• Detect cycle in undirected graph? (parent tracking instead of 3-color)</div>')),

"c046": A(("Dijkstra's Algorithm","Min-heap (priority queue) for greedy shortest path. Relax all edges from current shortest node."),
  ("Solution","<pre>import heapq\ndef networkDelayTime(times, n, k):\n    graph = defaultdict(list)\n    for u,v,w in times: graph[u].append((v,w))\n    dist = {k: 0}\n    heap = [(0, k)]\n    while heap:\n        d, u = heapq.heappop(heap)\n        if d &gt; dist.get(u, float('inf')): continue\n        for v, w in graph[u]:\n            nd = d + w\n            if nd &lt; dist.get(v, float('inf')):\n                dist[v] = nd; heapq.heappush(heap, (nd,v))\n    return max(dist.values()) if len(dist)==n else -1</pre>"),
  ("Complexity","Time: O((V+E) log V) | Space: O(V+E)"),
  ("Follow-ups",'<div class="followup">• When does Dijkstra fail? (negative edge weights — use Bellman-Ford)<br>'
    '• All-pairs shortest path? (Floyd-Warshall O(V³))<br>'
    '• Negative cycle detection? (Bellman-Ford: after V-1 iterations, try once more)</div>')),

"c051": A(("Approach","Sort intervals by end time (greedy). A meeting can be held if its start ≥ end of last selected meeting."),
  ("Solution","<pre>def eraseOverlapIntervals(intervals):\n    intervals.sort(key=lambda x: x[1])\n    count = 0; end = float('-inf')\n    for s, e in intervals:\n        if s &gt;= end: end = e\n        else: count += 1\n    return count</pre>"),
  ("Complexity","Time: O(n log n) | Space: O(1)"),
  ("Follow-ups",'<div class="followup">• Meeting rooms minimum count? (heap of end times)<br>'
    '• Maximum non-overlapping intervals? (n - eraseOverlapIntervals result)</div>')),

"c061": A(("Approach","DP. For each coin, update dp[amount] for all amounts from coin to target. "
    "Classic unbounded knapsack."),
  ("Solution","<pre>def coinChange(coins, amount):\n    dp = [float('inf')] * (amount+1)\n    dp[0] = 0\n    for coin in coins:\n        for x in range(coin, amount+1):\n            dp[x] = min(dp[x], dp[x-coin]+1)\n    return dp[amount] if dp[amount] != float('inf') else -1</pre>"),
  ("Complexity","Time: O(n×amount) | Space: O(amount)"),
  ("Follow-ups",'<div class="followup">• Coin change II — number of ways? (same DP, add instead of min)<br>'
    '• What if coin denominations are not integers?</div>')),

"c065": A(("Approach","DP with memoization. <code>dp[i][j]</code> = LCS length of s1[i:] and s2[j:]. "
    "If chars match: 1 + dp[i+1][j+1]. Else max(dp[i+1][j], dp[i][j+1])."),
  ("Solution","<pre>def longestCommonSubsequence(text1, text2):\n    m, n = len(text1), len(text2)\n    dp = [[0]*(n+1) for _ in range(m+1)]\n    for i in range(m-1,-1,-1):\n        for j in range(n-1,-1,-1):\n            if text1[i]==text2[j]:\n                dp[i][j] = 1 + dp[i+1][j+1]\n            else:\n                dp[i][j] = max(dp[i+1][j], dp[i][j+1])\n    return dp[0][0]</pre>"),
  ("Complexity","Time: O(m×n) | Space: O(m×n), optimizable to O(min(m,n))"),
  ("Follow-ups",'<div class="followup">• Shortest common supersequence? (m+n - LCS)<br>'
    '• Edit distance (Levenshtein)? (similar DP with insert/delete/replace)<br>'
    '• LCS of 3 strings?</div>')),
}
