# Compact question tuples: (id, text, category, subcategory, difficulty, companies, frequency, tags, round_type, hint)
_G1 = ["Google","Meta"]
_G2 = ["Google","Meta","Amazon"]
_G3 = ["Google","Meta","Amazon","Microsoft","Uber","LinkedIn"]
_ALL = ["Google","Meta","Amazon","Microsoft","Uber","LinkedIn","Adobe","Razorpay","PhonePe","TCS","Infosys","Wipro"]
_SVC = ["TCS","Infosys","Wipro","Cognizant","Accenture","HCL","Tech Mahindra","Capgemini"]

CODING_QUESTIONS = [
  # --- ARRAYS ---
  ("c001","Two Sum","coding","arrays","Easy",_ALL,95,"hash-map,arrays","Coding Round","Store complement in hash map. O(n) time."),
  ("c002","Three Sum","coding","arrays","Medium",_G2+["Uber","Airbnb","LinkedIn"],85,"two-pointers,sorting","Coding Round","Sort + two pointers for each element. O(n²)."),
  ("c003","Maximum Subarray (Kadane's Algorithm)","coding","arrays","Medium",_ALL[:8],82,"dp,kadane","Coding Round","Track curr_sum and max_sum; reset curr_sum when negative."),
  ("c004","Product of Array Except Self","coding","arrays","Medium",_G2+["LinkedIn","Uber","Airbnb","Atlassian"],80,"prefix-suffix","Coding Round","Prefix products left-to-right, multiply suffix right-to-left. No division."),
  ("c005","Trapping Rain Water","coding","arrays","Hard",_G2+["Uber","Microsoft"],78,"two-pointers,stack","Coding Round","Two pointers, track left_max/right_max. Add water at each step."),
  ("c006","Container With Most Water","coding","arrays","Medium",_G1+["Amazon","Atlassian","Airbnb"],75,"two-pointers,greedy","Coding Round","Move the shorter pointer inward each step."),
  ("c007","Find Minimum in Rotated Sorted Array","coding","arrays","Medium",_G1+["Uber","LinkedIn","Microsoft","Razorpay"],74,"binary-search","Coding Round","Binary search: compare mid with right to determine rotation side."),
  ("c008","Search in Rotated Sorted Array","coding","arrays","Medium",_G1+["Uber","LinkedIn","Amazon","CRED"],73,"binary-search","Coding Round","Find sorted half, check if target is in it, recurse."),
  ("c009","Best Time to Buy and Sell Stock","coding","arrays","Easy",_ALL[:7]+["PayPal"],82,"greedy","Coding Round","Track min price seen; compute max profit at each step."),
  ("c010","Merge Intervals","coding","arrays","Medium",_G2+["LinkedIn","Uber","Airbnb","Atlassian","Adobe"],79,"sorting,intervals","Coding Round","Sort by start; merge if next.start <= curr.end."),
  ("c011","Subarray Sum Equals K","coding","arrays","Medium",_G1+["Uber","Amazon","Razorpay","PhonePe"],74,"prefix-sum,hash-map","Coding Round","prefix[j]-prefix[i]=k; store prefix sum counts in map."),
  ("c012","Sliding Window Maximum","coding","arrays","Hard",_G1+["Uber","Amazon"],68,"sliding-window,deque","Coding Round","Monotonic deque: keep indices in decreasing order of value."),
  ("c013","Median of Two Sorted Arrays","coding","arrays","Hard",_G1+["Databricks","Snowflake"],72,"binary-search,divide-conquer","Coding Round","Binary search on smaller array for correct partition. O(log min(m,n))."),
  ("c014","Find the Duplicate Number","coding","arrays","Medium",_G1+["Amazon","CRED","Razorpay"],60,"floyd-cycle","Coding Round","Floyd's cycle detection treating values as next pointers."),
  ("c015","Majority Element","coding","arrays","Easy",["Amazon","Google"]+_SVC[:3],72,"boyer-moore","Coding Round","Boyer-Moore voting: cancel out non-majority elements."),
  ("c016","Jump Game","coding","arrays","Medium",["Amazon","Google","Uber","Meta"],65,"greedy","Coding Round","Track max reachable index; return false if index exceeds it."),
  ("c017","Spiral Matrix","coding","arrays","Medium",["Microsoft","Apple","Google","Amazon","Adobe"],63,"matrix,simulation","Coding Round","Four boundary pointers (top/bottom/left/right), shrink after each pass."),
  ("c018","Next Permutation","coding","arrays","Medium",["Google","Amazon","Microsoft","Uber"],62,"arrays,math","Coding Round","Find rightmost ascending pair; swap with next greater; reverse suffix."),
  ("c019","First Missing Positive","coding","arrays","Hard",["Google","Stripe","Amazon"],58,"in-place-hashing","Coding Round","Place each num n at index n-1 (if 1<=n<=len). Answer is first mismatch."),
  ("c020","Rotate Array","coding","arrays","Medium",["Microsoft","Amazon"]+_SVC[:3],65,"reversal-algorithm","Coding Round","Reverse all, reverse first k, reverse rest. O(n) O(1)."),
  # --- STRINGS ---
  ("c021","Longest Substring Without Repeating Chars","coding","strings","Medium",_ALL[:8]+["CRED","Swiggy"],88,"sliding-window,hash-set","Coding Round","Sliding window with set; move left when duplicate found."),
  ("c022","Minimum Window Substring","coding","strings","Hard",_G1+["Uber","LinkedIn","Airbnb"],74,"sliding-window,frequency-map","Coding Round","Two freq maps; expand right, contract left when all chars covered."),
  ("c023","Group Anagrams","coding","strings","Medium",["Amazon","Google","Meta","Uber","Microsoft","Atlassian"],78,"hash-map,sorting","Coding Round","Group by sorted-string key. O(n·k log k)."),
  ("c024","Valid Palindrome","coding","strings","Easy",["Meta","Google","Amazon","Microsoft"]+_SVC[:3],78,"two-pointers","Coding Round","Two pointers; skip non-alphanumeric characters."),
  ("c025","Longest Palindromic Substring","coding","strings","Medium",["Amazon","Microsoft","Google","Meta","Oracle"],75,"expand-center","Coding Round","Expand around center for each char and each pair. O(n²)."),
  ("c026","Valid Parentheses","coding","strings","Easy",_ALL[:7]+["CRED"],82,"stack","Coding Round","Push open brackets; pop and match for closing."),
  ("c027","Word Break","coding","strings","Medium",["Google","Amazon","Uber","Meta","LinkedIn"],72,"dp,trie","Coding Round","dp[i]=true if s[0..i-1] can be segmented. Check all valid word endings."),
  ("c028","Palindromic Substrings Count","coding","strings","Medium",["Google","Amazon","LinkedIn"],65,"expand-center","Coding Round","Expand around each center; count every palindrome found."),
  ("c029","String to Integer (atoi)","coding","strings","Medium",["Amazon","Microsoft","Google"]+_SVC[:2],68,"parsing","Coding Round","Handle whitespace, sign, overflow, non-digit termination."),
  ("c030","Encode and Decode Strings","coding","strings","Medium",["Google","Uber","Airbnb","LinkedIn"],62,"design,encoding","Coding Round","Length-prefix: '4#word'. Unambiguous even with special chars."),
  # --- TREES ---
  ("c031","Binary Tree Inorder Traversal (Iterative)","coding","trees","Easy",_ALL[:6]+_SVC[:2],78,"stack,dfs","Coding Round","Stack: go left as far as possible, process, go right."),
  ("c032","Maximum Depth of Binary Tree","coding","trees","Easy",["Meta","Google","Amazon","Microsoft"]+_SVC[:3],80,"dfs,recursion","Coding Round","1 + max(depth(left), depth(right))."),
  ("c033","Validate Binary Search Tree","coding","trees","Medium",_G2+["Microsoft","Uber","Razorpay"],82,"dfs,bounds","Coding Round","Pass (min_val, max_val) bounds through recursion."),
  ("c034","Lowest Common Ancestor","coding","trees","Medium",_G2+["LinkedIn","Uber","Swiggy"],83,"dfs,bst","Coding Round","If both < node go left; both > node go right; else current is LCA."),
  ("c035","Binary Tree Level Order Traversal","coding","trees","Medium",_G2+["Microsoft","Adobe","Atlassian","Razorpay"],82,"bfs,queue","Coding Round","BFS with queue; track level size to separate levels."),
  ("c036","Binary Tree Maximum Path Sum","coding","trees","Hard",_G1+["Amazon","Uber","LinkedIn"],75,"dfs,postorder","Coding Round","DFS returns max single-branch gain; update global with left+node+right."),
  ("c037","Serialize and Deserialize Binary Tree","coding","trees","Hard",_G1+["Uber","Amazon","LinkedIn"],78,"bfs,design","Coding Round","BFS with null markers; split on delimiter for deserialization."),
  ("c038","Diameter of Binary Tree","coding","trees","Easy",["Meta","Google","Amazon","Zomato","Swiggy"],72,"dfs,height","Coding Round","DFS tracking height; diameter = height(left)+height(right) at each node."),
  ("c039","Kth Smallest in BST","coding","trees","Medium",["Amazon","Airbnb","LinkedIn","Google"],68,"inorder,bst","Coding Round","Inorder traversal (sorted for BST); return kth element."),
  ("c040","Construct BT from Preorder and Inorder","coding","trees","Hard",_G1+["Amazon","Microsoft"],70,"recursion,hash-map","Coding Round","Root=preorder[0]; split inorder by root; recurse on halves."),
  # --- GRAPHS ---
  ("c041","Number of Islands","coding","graphs","Medium",_ALL[:8]+["CRED","Swiggy"],92,"dfs,bfs,union-find","DSA Round","DFS/BFS marking visited cells. Count DFS initiations."),
  ("c042","Course Schedule (Cycle Detection)","coding","graphs","Medium",["Google","Airbnb","Uber","Amazon","LinkedIn","Atlassian"],82,"topological-sort,dfs","DSA Round","DFS with 3 states: unvisited/visiting/visited. Visiting again = cycle."),
  ("c043","Course Schedule II","coding","graphs","Medium",_G1+["Uber","LinkedIn","Amazon","Meta"],76,"topological-sort,bfs,kahn","DSA Round","Kahn's algorithm: BFS with in-degree tracking."),
  ("c044","Clone Graph","coding","graphs","Medium",["Amazon","Google","Meta","Microsoft"],72,"dfs,hash-map","DSA Round","DFS + map from original to clone; recursively clone neighbors."),
  ("c045","Word Ladder","coding","graphs","Hard",["Amazon","Google","Meta","Uber"],72,"bfs,string","DSA Round","BFS; at each step try all single-char transformations. Return level count."),
  ("c046","Network Delay Time (Dijkstra)","coding","graphs","Medium",["Google","Uber","Amazon","LinkedIn","Databricks"],72,"dijkstra,heap","DSA Round","Min-heap; relax edges; return max dist to all nodes."),
  ("c047","Alien Dictionary","coding","graphs","Hard",_G1+["Airbnb","Uber"],68,"topological-sort,graph","DSA Round","Build char-order graph from adjacent word pairs; topo sort."),
  ("c048","Detect Cycle in Directed Graph","coding","graphs","Medium",["Amazon","Google","Uber","PhonePe","Razorpay"],74,"dfs,cycle","DSA Round","DFS with visited + rec-stack. Node in rec-stack = cycle."),
  ("c049","Pacific Atlantic Water Flow","coding","graphs","Medium",_G1+["Uber","Meta"],66,"dfs,reverse","DSA Round","Reverse DFS from each ocean; return intersection of reachable cells."),
  ("c050","Minimum Spanning Tree","coding","graphs","Medium",["Google","Uber","Databricks","Snowflake"],65,"kruskal,union-find,prim","DSA Round","Kruskal: sort edges, add if no cycle. Prim: min-heap greedy expansion."),
  # --- DP ---
  ("c051","Coin Change","coding","dp","Medium",_G2+["Uber","Microsoft","Razorpay","Swiggy"],86,"bottom-up-dp","Coding Round","dp[i]=min coins for amount i. For each coin: dp[c..amount]."),
  ("c052","Longest Common Subsequence","coding","dp","Medium",["Google","Amazon","Microsoft","Meta","Databricks"],80,"2d-dp","Coding Round","dp[i][j]: match=1+dp[i-1][j-1]; else max(dp[i-1][j],dp[i][j-1])."),
  ("c053","House Robber","coding","dp","Medium",["Google","Airbnb","Amazon","LinkedIn","Meta"],76,"dp","Coding Round","dp[i]=max(dp[i-1], dp[i-2]+nums[i]). O(1) space with two vars."),
  ("c054","Longest Increasing Subsequence","coding","dp","Medium",_G2+["Microsoft","LinkedIn","Uber"],74,"dp,binary-search,patience","Coding Round","O(n log n): maintain tails array; binary search for position."),
  ("c055","Edit Distance","coding","dp","Hard",_G1+["Amazon","Uber","LinkedIn"],70,"2d-dp","Coding Round","Match: dp[i-1][j-1]. Mismatch: 1+min(replace,delete,insert)."),
  ("c056","Decode Ways","coding","dp","Medium",["Meta","Amazon","Google","Microsoft","LinkedIn"],74,"dp","Coding Round","dp[i]: ways for s[0..i-1]. Consider 1-digit and valid 2-digit."),
  ("c057","Unique Paths","coding","dp","Medium",_G1+["Amazon","Uber","Atlassian"],70,"dp,combinatorics","Coding Round","dp[i][j]=dp[i-1][j]+dp[i][j-1]. Or C(m+n-2,m-1)."),
  ("c058","Partition Equal Subset Sum","coding","dp","Medium",["Amazon","Google","Meta","Uber","Razorpay"],68,"0-1-knapsack","Coding Round","Check if subset sums to total/2. 1D DP boolean array."),
  ("c059","Maximum Product Subarray","coding","dp","Medium",["Amazon","Google","Meta","Uber"],72,"dp","Coding Round","Track both max and min at each pos (negative can flip max/min)."),
  ("c060","Target Sum","coding","dp","Medium",["Google","Amazon","Meta"],65,"dp,dfs","Coding Round","DFS with memoization or subset sum DP: count subsets with sum=(target+total)/2."),
  # --- HEAP ---
  ("c061","Merge K Sorted Lists","coding","heap","Hard",_G2+["Uber","Microsoft","LinkedIn"],82,"heap,merge","Coding Round","Min-heap of (val, list_idx, node). Poll min, push next from same list."),
  ("c062","Find Median from Data Stream","coding","heap","Hard",_G1+["Amazon","Uber","LinkedIn"],76,"two-heaps","Coding Round","Max-heap (lower half) + min-heap (upper half). Keep sizes balanced."),
  ("c063","Top K Frequent Elements","coding","heap","Medium",["Amazon","Google","Uber","Meta","Atlassian","Razorpay"],80,"heap,bucket-sort","Coding Round","Min-heap of size k or bucket-sort by frequency. Bucket is O(n)."),
  ("c064","K Closest Points to Origin","coding","heap","Medium",["Amazon","Uber","Google","Meta","Swiggy","Zomato"],76,"heap,quickselect","Coding Round","Max-heap of size k. Or QuickSelect for O(n) average."),
  ("c065","Meeting Rooms II","coding","heap","Medium",["Google","Airbnb","Uber","LinkedIn","Microsoft","Razorpay"],82,"heap,greedy,intervals","Coding Round","Sort by start; min-heap of end times. Reuse room if start>=heap.min."),
  ("c066","Task Scheduler","coding","heap","Medium",_G1+["Uber","Amazon"],68,"heap,greedy","Coding Round","Greedy: schedule most frequent first. Max-heap + cooldown queue."),
  # --- BACKTRACKING ---
  ("c067","Subsets","coding","backtracking","Medium",_G2+["Microsoft","Atlassian","Razorpay"],78,"backtracking,bit-manipulation","Coding Round","Include/exclude at each index. Or 2^n bitmask approach."),
  ("c068","Permutations","coding","backtracking","Medium",_G2+["Microsoft","Uber"],80,"backtracking,swap","Coding Round","Swap-at-index or visited-array backtracking approach."),
  ("c069","Combination Sum","coding","backtracking","Medium",_G2+["LinkedIn","Uber"],78,"backtracking","Coding Round","Allow reuse; prune when sum exceeds target."),
  ("c070","Word Search","coding","backtracking","Medium",["Amazon","Microsoft","Google","Meta"],72,"dfs,backtracking,matrix","Coding Round","DFS from each cell; mark visited, restore after backtrack."),
  ("c071","N-Queens","coding","backtracking","Hard",_G1+["Amazon"],68,"backtracking,constraint","Coding Round","Place row by row; sets for cols, diag1 (r-c), diag2 (r+c)."),
  # --- DESIGN / DATA STRUCTURES ---
  ("c072","LRU Cache","coding","design","Medium",_G2+["Uber","LinkedIn","Microsoft","Razorpay","CRED"],88,"hash-map,doubly-linked-list","Machine Coding","HashMap + doubly linked list. Move accessed node to front. O(1) ops."),
  ("c073","LFU Cache","coding","design","Hard",_G1+["Amazon","Uber","LinkedIn"],72,"hash-map,design","Machine Coding","2 maps: key→(val,freq), freq→DLL. Track min_freq for O(1) eviction."),
  ("c074","Implement Trie (Prefix Tree)","coding","design","Medium",_G2+["Uber","LinkedIn","Razorpay"],78,"trie","Machine Coding","Node with children[26] + is_end. Insert/Search/StartsWith all O(L)."),
  ("c075","Design Hit Counter","coding","design","Medium",["Google","Uber","LinkedIn","Stripe"],68,"circular-buffer,sliding-window","Machine Coding","Circular array of 300 slots (seconds). Each slot: (timestamp, count)."),
  # --- BINARY SEARCH ---
  ("c076","Kth Largest Element","coding","binary_search","Medium",_G2+["Uber","Microsoft","LinkedIn"],82,"quickselect,heap","Coding Round","QuickSelect O(n) avg, or min-heap of size k O(n log k)."),
  ("c077","Find Peak Element","coding","binary_search","Medium",_G1+["Uber","LinkedIn"],70,"binary-search","Coding Round","If mid<mid+1 peak is right; if mid<mid-1 peak is left."),
  ("c078","Capacity to Ship in D Days","coding","binary_search","Medium",["Amazon","Google","LinkedIn"],66,"binary-search,greedy","Coding Round","Binary search on capacity; greedy O(n) feasibility check."),
  ("c079","Split Array Largest Sum","coding","binary_search","Hard",_G1+["LinkedIn"],62,"binary-search,greedy","Coding Round","Binary search on answer; greedy to count minimum partitions."),
  ("c080","Kth Smallest in Matrix","coding","binary_search","Medium",["Google","Amazon","Uber"],65,"binary-search,heap","Coding Round","Binary search on value range; count elements <= mid in O(n)."),
]

QUESTIONS = [{
    "id":q[0],"text":q[1],"category":q[2],"subcategory":q[3],
    "difficulty":q[4],"companies":q[5],"frequency":q[6],
    "tags":q[7].split(","),"round_type":q[8],"answer_hint":q[9]
} for q in CODING_QUESTIONS]
