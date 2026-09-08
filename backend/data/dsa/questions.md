# Data Structures & Algorithms (DSA) Interview Questions

## Easy

### Q1: What is Big-O notation, and what do time complexity and space complexity represent?
**Answer:** Big-O notation is a mathematical formalism used to describe the asymptotic upper bound of an algorithm's resource requirements as the input size $N$ grows toward infinity. Time complexity quantifies the number of basic computational steps an algorithm performs, whereas space complexity measures the amount of auxiliary memory or working storage required beyond the input itself. By focusing on asymptotic growth rather than clock-time seconds, Big-O allows engineers to compare algorithmic efficiency independently of machine hardware, programming languages, or compiler optimizations. Standard complexities range from $O(1)$ (constant time) to logarithmic $O(\log N)$, linear $O(N)$, log-linear $O(N \log N)$, quadratic $O(N^2)$, and exponential $O(2^N)$.
**Key Points:**
- Asymptotic upper bound characterizing algorithmic scaling as $N \to \infty$.
- Time complexity measures operation count; space complexity measures auxiliary memory usage.
- Hardware-independent and language-agnostic benchmarking framework.
- Primary complexity classes: $O(1) < O(\log N) < O(N) < O(N \log N) < O(N^2) < O(2^N)$.
**Evaluation Criteria:** Candidate should define Big-O as an asymptotic upper bound, clearly differentiate time from auxiliary space complexity, and correctly order standard efficiency classes.

### Q2: What are the fundamental differences between an Array and a Singly Linked List regarding memory layout and access performance?
**Answer:** An array stores elements in a contiguous block of physical memory, allowing instant $O(1)$ random access to any element by computing a memory address offset from the base pointer using its index. However, inserting or deleting elements at arbitrary positions in an array requires shifting subsequent elements, incurring $O(N)$ time complexity. A linked list stores elements (nodes) non-contiguously in memory, where each node contains data and a pointer to the next node, requiring $O(N)$ sequential traversal to access an element by index. However, inserting or deleting a node when a pointer is already available is an $O(1)$ pointer update. Furthermore, linked lists incur memory overhead per element due to storing pointer references and suffer from CPU cache misses.
**Key Points:**
- Memory layout: Contiguous memory (array) vs. heap-allocated nodes with pointers (linked list).
- Random access: $O(1)$ for arrays; $O(N)$ sequential traversal for linked lists.
- Insertion/Deletion: $O(N)$ for arrays (shifting elements); $O(1)$ for linked lists (when node pointer is held).
- Hardware efficiency: Arrays maximize CPU cache locality; linked lists suffer frequent cache misses.
**Evaluation Criteria:** Candidate should contrast contiguous vs. non-contiguous memory, explain index address arithmetic vs. pointer traversal, and discuss cache locality implications.

### Q3: How does a Stack operate, and what are its primary operations, time complexities, and typical use cases?
**Answer:** A stack is a linear data structure that adheres strictly to the Last-In, First-Out (LIFO) principle, where the last element added is the first one removed. Its primary operations are `push` (inserting an element onto the top), `pop` (removing and returning the top element), and `peek` or `top` (inspecting the top element without removing it), all of which execute in $O(1)$ constant time. Stacks can be implemented using either dynamic arrays or linked lists. Common use cases include function call call-stack management in runtime environments, expression evaluation and syntax parsing (e.g., matching parentheses), undo/redo history in software applications, and Depth-First Search (DFS) graph traversals.
**Key Points:**
- Last-In, First-Out (LIFO) operational discipline.
- Core operations: `push()`, `pop()`, `peek()`, and `isEmpty()`, all running in $O(1)$ time.
- Space complexity: $O(N)$ to store $N$ elements.
- Practical use cases: Call stack management, backtracking, balanced parenthesis validation, expression evaluation.
**Evaluation Criteria:** Look for understanding of the LIFO principle, constant time bounds for all operations, and standard real-world applications like matching parentheses or runtime call stacks.

### Q4: How does a Queue operate, and how does a circular queue prevent array drift?
**Answer:** A queue is a linear data structure that operates according to the First-In, First-Out (FIFO) principle, where elements are inserted at the back (rear/tail) via `enqueue` and removed from the front (head) via `dequeue`, both operating in $O(1)$ time. In a naive array-based queue, dequeueing elements increments the front pointer, causing unused empty memory to accumulate at the beginning of the array while the rear quickly reaches the array's capacity—a problem known as array drift. A circular queue resolves this by treating the array as a contiguous ring using modulo arithmetic: `rear = (rear + 1) % capacity` and `front = (front + 1) % capacity`. This allows newly enqueued items to wrap around and reuse vacant space at the beginning of the array, preventing unnecessary reallocations.
**Key Points:**
- First-In, First-Out (FIFO) operational order.
- Core operations: `enqueue()` at rear, `dequeue()` at front, both $O(1)$ time.
- Array drift: Front pointer advances rightward, leaving wasted unclaimable array cells.
- Circular Queue solution: Modulo arithmetic `(index + 1) % capacity` wraps pointers around to reuse memory.
**Evaluation Criteria:** Candidate should define FIFO, explain the problem of memory waste in naive array queues, and clearly demonstrate how circular queues wrap indices using modulo arithmetic.

### Q5: How does a Hash Map work under the hood to achieve $O(1)$ average-time lookup, insertion, and deletion?
**Answer:** A Hash Map stores key-value pairs in an underlying bucket array by passing the key through a hash function that computes a large integer hash code. This hash code is converted into a valid array index using the modulo operator (`index = hash(key) % array_length`). When keys hash to the same bucket index—a collision—the map resolves it using collision resolution strategies such as Separate Chaining (storing colliding entries in a linked list or red-black tree at that bucket) or Open Addressing (probing alternative empty slots). When the number of stored elements exceeds a predefined Load Factor threshold (typically 0.75), the map dynamically rehashes: it allocates an array twice the size and re-indexes all keys, amortizing average lookup, insertion, and deletion to $O(1)$ time.
**Key Points:**
- Hash function maps keys to numerical indices via `hash(key) % capacity`.
- Collision resolution via Separate Chaining (linked lists / balanced trees) or Open Addressing (linear/quadratic probing).
- Average time complexity: $O(1)$ for search, insert, and delete; worst-case $O(N)$ when collisions degenerate.
- Dynamic resizing: Doubles array size and rehashes entries when Load Factor threshold is crossed.
**Evaluation Criteria:** Candidate must detail the pipeline (key $\to$ hash $\to$ index), explain collision resolution, and discuss dynamic resizing based on the load factor.

### Q6: What is Binary Search, what is its prerequisite, and why is its time complexity $O(\log N)$?
**Answer:** Binary Search is an efficient searching algorithm that finds the position of a target value within a sorted collection by repeatedly dividing the search space in half. Its strict prerequisite is that the input array must already be sorted (or possess monotonic properties). At each step, the algorithm compares the target value to the element at the midpoint of the current search interval; if they match, the search concludes; if the target is smaller, the search continues in the left half; if larger, it continues in the right half. Because the size of the remaining search space is cut in half on every iteration ($N, N/2, N/4, \dots, 1$), the maximum number of comparisons required is $\log_2 N$, yielding an $O(\log N)$ time complexity.
**Key Points:**
- Prerequisite: Collection must be sorted or monotonically ordered.
- Divide and conquer: Cuts the candidate search range in half on each step.
- Time complexity: $O(\log N)$ logarithmic time; space complexity $O(1)$ iterative.
- Prevents integer overflow: Midpoint calculation should use `mid = low + (high - low) / 2`.
**Evaluation Criteria:** Candidate should state the sorted precondition, explain the halving mechanism, derive $O(\log N)$, and mention integer overflow safety in midpoint calculation.

### Q7: Compare Bubble Sort and Insertion Sort in terms of algorithmic mechanics, best-case, and worst-case time complexities.
**Answer:** Bubble Sort repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order, causing the largest unsorted element to "bubble up" to its correct position at the end of the array on each pass. Insertion Sort builds the final sorted array one item at a time by taking the next unsorted element and scanning backwards through the sorted portion to shift larger elements right and insert the item into its proper position. Both algorithms have a worst-case and average-case time complexity of $O(N^2)$ with $O(1)$ auxiliary space. However, on nearly-sorted data, Insertion Sort runs in $O(N)$ linear time with minimal comparisons and data movement, making it substantially faster in practice than Bubble Sort and widely used as the base case in hybrid algorithms like Timsort.
**Key Points:**
- Bubble Sort: Swaps adjacent out-of-order pairs; bubbles max element to the end per pass.
- Insertion Sort: Inserts current element into its correct position within an already sorted prefix.
- Both have $O(N^2)$ worst-case and average-case time complexity and $O(1)$ auxiliary space.
- Best-case on pre-sorted data: Both achieve $O(N)$, but Insertion Sort performs fewer operations.
**Evaluation Criteria:** Look for clear mechanics of both algorithms, space/time bounds, and recognition of Insertion Sort's practical utility in hybrid sorting algorithms (e.g., Timsort).

### Q8: What is a Binary Tree, and how do Pre-order, In-order, and Post-order depth-first traversals differ?
**Answer:** A Binary Tree is a hierarchical data structure where each node has at most two children, referred to as the left child and the right child. Depth-First Search (DFS) traversals systematically visit every node in the tree recursively, differentiated by when the parent node is processed relative to its children. In **Pre-order Traversal** (`Root -> Left -> Right`), the root node is processed first, which is useful for serializing or cloning tree hierarchies. In **In-order Traversal** (`Left -> Root -> Right`), the left subtree is visited, followed by the root, and then the right subtree; for a Binary Search Tree (BST), this visits all keys in sorted ascending order. In **Post-order Traversal** (`Left -> Right -> Root`), children are processed before their parent, making it ideal for bottom-up operations like deleting a tree or calculating subtree heights.
**Key Points:**
- Node structure: Data, `left` pointer, `right` pointer.
- Pre-order (`Root, Left, Right`): Ideal for tree copying and prefix serialization.
- In-order (`Left, Root, Right`): Traverses Binary Search Trees (BST) in sorted ascending order.
- Post-order (`Left, Right, Root`): Ideal for bottom-up evaluations, tree freeing, and height calculations.
**Evaluation Criteria:** Candidate should state the exact visitation sequence for all three traversals and associate each traversal with a practical application (e.g., in-order for sorted BST output).

### Q9: What is the Two-Pointer technique, and in what array/string problems is it most effective?
**Answer:** The Two-Pointer technique involves initializing two index pointers that iterate through an array or string either toward each other from opposite ends (opposite-direction pointers) or in the same direction at differing speeds (fast and slow pointers). It is exceptionally effective for reducing brute-force $O(N^2)$ nested-loop algorithms down to $O(N)$ linear time by capitalizing on sorted array properties or monotonic relationships. Common applications of opposite-direction pointers include solving the classic Two-Sum problem on sorted arrays, checking for palindromes, and reversing strings in-place. Fast-and-slow pointers (Floyd's algorithm) are commonly used for finding the midpoint of a linked list, detecting cycles, or removing duplicate values in-place from sorted arrays.
**Key Points:**
- Reduces nested-loop $O(N^2)$ searches down to $O(N)$ linear time.
- Opposite-direction pointers: Start at opposite ends (`left = 0, right = n-1`) and move toward center.
- Fast and slow pointers: Advance at different velocities (e.g., slow moves 1 step, fast moves 2 steps).
- Common use cases: Two-Sum on sorted inputs, palindrome validation, linked list cycle detection, in-place deduplication.
**Evaluation Criteria:** Candidate should describe both opposite-direction and fast-and-slow pointer patterns, and explain how exploiting sorted/monotonic order eliminates redundant comparisons.

### Q10: What is recursion, what constitutes a valid base case, and what causes a Call Stack Overflow?
**Answer:** Recursion is a programming technique where a function solves a problem by calling smaller, self-similar instances of itself until it reaches a terminating condition. A valid base case is a specific, non-recursive condition that immediately returns a concrete result without making further recursive calls, preventing infinite loops. Every recursive call pushes a new stack frame onto the system call stack, storing local variables, parameters, and return addresses. A Stack Overflow error occurs when recursion continues too deeply without hitting a base case, exhausting the fixed memory allocated to the thread call stack.
**Key Points:**
- Function calling itself on smaller subproblems until a termination condition is reached.
- Base Case: Essential halting condition returning a direct value without recursion.
- Call stack frames: Each invocation allocates memory for parameters and return addresses.
- Stack Overflow: Memory exhaustion resulting from missing/unreachable base cases or excessive recursion depth.
**Evaluation Criteria:** Candidate must explain the subproblem reduction mechanism, identify the role of the base case, and trace stack overflow directly to memory frame accumulation.

---

## Medium

### Q1: How does Floyd's Cycle Detection Algorithm (Tortoise and Hare) detect cycles in a Linked List in $O(N)$ time and $O(1)$ space?
**Answer:** Floyd's Cycle Detection Algorithm uses two pointers that traverse a linked list at different speeds: a slow pointer (the tortoise) that advances one node per step, and a fast pointer (the hare) that advances two nodes per step. If the linked list is acyclic, the fast pointer will eventually reach the `null` terminus, confirming there is no cycle. If a cycle exists, both pointers will eventually enter the loop; with each iteration inside the cycle, the relative distance between the fast pointer and the slow pointer decreases by one node, guaranteeing that the fast pointer will lap and collide with the slow pointer inside the cycle. Because the fast pointer travels at most $2N$ steps and requires no auxiliary data storage, the algorithm runs in $O(N)$ time with $O(1)$ space complexity, vastly outperforming a hash set approach.
**Key Points:**
- Slow pointer advances 1 step; fast pointer advances 2 steps.
- Termination: Fast pointer reaches `null` $\to$ acyclic list.
- Collision: Fast pointer laps slow pointer (`slow == fast`) $\to$ cycle confirmed.
- Space and Time: $O(N)$ time complexity and $O(1)$ auxiliary memory (zero hashing overhead).
**Evaluation Criteria:** Look for a clear mathematical explanation of relative closing distance within the loop and a contrast with the $O(N)$ space hash table approach.

### Q2: How do Hash Tables resolve hash collisions using Separate Chaining versus Open Addressing, and what are their trade-offs?
**Answer:** In Separate Chaining, each bucket in the hash table points to an auxiliary data structure (typically a linked list, which upgrades to a balanced red-black tree when chain lengths exceed a threshold, as in Java 8+). Colliding keys are simply appended to the bucket's chain; its load factor can safely exceed 1.0, but it suffers from pointer memory overhead and cache misses. In Open Addressing, all key-value pairs reside directly within the array itself; when a collision occurs, the algorithm systematically probes alternative empty slots using Linear Probing ($i + 1$), Quadratic Probing ($i + c_1 k + c_2 k^2$), or Double Hashing ($h_1(k) + i \cdot h_2(k)$). Open Addressing provides superior CPU cache locality and eliminates pointer overhead, but its load factor must remain strictly below 0.7 to avoid severe clustering performance degradation, and deletions require complex tombstone markers.
**Key Points:**
- Separate Chaining: Linked lists/balanced trees per bucket; tolerates high load factors; pointer overhead.
- Open Addressing: Stores elements in-table; probes alternative slots via linear/quadratic/double hashing.
- Clustering: Primary and secondary clustering can degrade Open Addressing lookups to $O(N)$.
- Deletion complexity: Open Addressing requires "tombstone" soft deletions to prevent broken probe chains.
**Evaluation Criteria:** Candidate should contrast in-table storage vs. auxiliary chains, explain the clustering phenomenon in open addressing, and explain tombstone handling during deletion.

### Q3: Contrast Quick Sort and Merge Sort regarding algorithmic paradigm, stability, auxiliary space, and worst-case time complexity.
**Answer:** Both algorithms follow the Divide and Conquer paradigm, but they partition and combine subproblems differently. Merge Sort recursively divides an array into equal halves until single elements remain, and then merges the sorted halves together; it is inherently stable, guarantees $O(N \log N)$ time in all cases (best, average, and worst), but requires $O(N)$ auxiliary space for merge buffers. Quick Sort chooses a pivot element and partitions the array in-place so that elements smaller than the pivot precede it and larger elements follow it, before recursively sorting partitions. Quick Sort runs in $O(N \log N)$ average time with $O(\log N)$ auxiliary stack space, but its worst-case degrades to $O(N^2)$ on poorly chosen pivots (e.g., already sorted inputs with naive pivot selection) and it is unstable in its in-place variant.
**Key Points:**
- Merge Sort: Guarantees $O(N \log N)$ in all cases; stable; requires $O(N)$ auxiliary memory.
- Quick Sort: $O(N \log N)$ average, $O(N^2)$ worst-case; unstable in-place; requires $O(\log N)$ stack space.
- In-place partitioning: Quick Sort sorts in-place; Merge Sort requires buffer copying.
- Practical preference: Quick Sort has smaller constant factors and better cache locality for arrays; Merge Sort excels for linked lists and external sorting.
**Evaluation Criteria:** Candidate must contrast stability, space overhead ($O(N)$ vs. $O(\log N)$), worst-case degradation scenarios, and cache performance.

### Q4: What defines a valid Binary Search Tree (BST), and how do you correctly validate one algorithmically?
**Answer:** A Binary Search Tree (BST) is a binary tree where every node satisfies the strict ordering property: all node keys in its left subtree must be strictly less than the node's key, and all node keys in its right subtree must be strictly greater than the node's key. A common algorithmic pitfall is simply checking that a node's left child is smaller and right child is larger, which fails because a node deep in the left subtree could violate an ancestor's bound. Correct validation requires either a recursive traversal that passes down valid open interval bounds `(min_val, max_val)` that narrow on every recursive descent, or an in-order traversal that verifies that visited node values are strictly monotonically increasing. Both correct approaches validate the tree in $O(N)$ time with $O(H)$ stack space.
**Key Points:**
- Definition: All nodes in left subtree $< \text{root} <$ all nodes in right subtree (strictly).
- Common pitfall: Only validating immediate parent-child relationships rather than whole subtrees.
- Range-bound validation: Recursively passing narrowing valid intervals `(min_allowed, max_allowed)`.
- In-order traversal validation: Confirming that an in-order traversal yields strictly ascending values.
**Evaluation Criteria:** Candidate should identify why local checks fail, explain the global bounding interval algorithm, and cite the equivalent in-order monotonicity property.

### Q5: Compare Breadth-First Search (BFS) and Depth-First Search (DFS) on graphs regarding implementation, traversal path, and optimal use cases.
**Answer:** Breadth-First Search (BFS) explores a graph level-by-level, visiting all immediate neighbors of a node before moving to nodes at the next depth level, implemented iteratively using a Queue (FIFO). Depth-First Search (DFS) explores as deep as possible along each branch before backtracking, implemented using recursion or an explicit Stack (LIFO). For unweighted graphs, BFS is guaranteed to find the shortest path between a source and destination, making it optimal for social network degree-of-separation queries or web crawlers. DFS is optimal for exhaustive exploration, cycle detection, finding connected components, topological sorting, and solving maze/pathfinding puzzles with backtracking. Both algorithms visit all vertices and edges in $O(V + E)$ time and require $O(V)$ space for tracking visited nodes.
**Key Points:**
- Data structure: BFS uses a Queue (FIFO); DFS uses a Stack (LIFO) or recursion.
- Traversal pattern: BFS radiates outwards radially; DFS plunges deep along branches before backtracking.
- Shortest path: BFS guarantees shortest path on unweighted graphs; DFS does not.
- Time and Space: Both run in $O(V + E)$ time and require $O(V)$ space for tracking visited states.
**Evaluation Criteria:** Candidate should contrast queue vs. stack mechanics, explain BFS shortest path guarantees on unweighted graphs, and outline specific use cases for each.

### Q6: What is a Monotonic Stack, and how does it solve problems like "Next Greater Element" in $O(N)$ linear time?
**Answer:** A Monotonic Stack is a stack data structure that enforces a strict monotonic invariant on its elements—maintaining elements in either strictly non-decreasing or strictly non-increasing order. When processing an array, incoming elements are compared to the stack top; while the invariant is violated, elements are popped from the stack and processed before the new element is pushed. For the "Next Greater Element" problem, maintaining a monotonic decreasing stack allows the incoming larger element to serve as the immediate "next greater element" for all smaller values currently sitting on the stack top. Because every element is pushed onto the stack exactly once and popped at most once, the algorithm executes in amortized $O(N)$ linear time, replacing a naive $O(N^2)$ brute-force search.
**Key Points:**
- Enforces strict monotonic ordering (always ascending or always descending).
- Incoming elements trigger popping of violating elements; popped items record their answer.
- Amortized analysis: Each element is pushed once and popped at most once $\to O(N)$ total time.
- Applications: Next Greater Element, Daily Temperatures, Largest Rectangle in Histogram, Trapping Rain Water.
**Evaluation Criteria:** Candidate must explain the invariant preservation mechanism, prove amortized $O(N)$ complexity through push/pop counting, and cite standard algorithmic applications.

### Q7: Explain the Sliding Window technique and how it optimizes contiguous subarray problems from $O(N^2)$ to $O(N)$ time.
**Answer:** The Sliding Window technique maintains a dynamic or fixed-size subset of contiguous elements within an array or string using two boundary pointers (`left` and `right`). Instead of recalculating properties of every possible subarray from scratch using nested loops ($O(N^2)$), the window expands by advancing the `right` pointer to include new elements and shrinks by advancing the `left` pointer to discard expired elements. When the window condition is violated (e.g., window contains too many distinct characters or sum exceeds target), the `left` pointer advances until the invariant is restored. Because each pointer traverses the array from index $0$ to $N$ at most once, the total operations are bounded by $2N$, achieving $O(N)$ linear time with $O(K)$ auxiliary space.
**Key Points:**
- Maintains a contiguous range `[left, right]` across an array or string.
- Incremental updates: Add element at `right`, subtract element at `left`.
- Expands window to search for solutions; contracts window to restore constraints.
- Replaces $O(N^2)$ brute-force recalculations with amortized $O(N)$ linear scans.
**Evaluation Criteria:** Candidate should explain incremental state updates, dynamic expansion/contraction mechanics, and prove linear amortized time complexity.

### Q8: What is a Binary Heap (Priority Queue), and what are the time complexities of insertion, extraction, and building a heap?
**Answer:** A Binary Heap is a complete binary tree stored compactly inside an array without pointer overhead, where every parent node satisfies the heap property: in a Min-Heap, the parent's key is less than or equal to its children; in a Max-Heap, it is greater than or equal to its children. For any node at index $i$, its left child is at $2i + 1$, right child at $2i + 2$, and parent at $\lfloor (i - 1) / 2 \rfloor$. Insertion places the new element at the end of the array and performs "bubble-up" (sift-up) in $O(\log N)$ time. Extracting the minimum/maximum swaps the root with the last leaf, removes it, and performs "bubble-down" (sift-down) in $O(\log N)$ time. Building a heap from an arbitrary array of $N$ elements using bottom-up heapification (`buildHeap`) runs in mathematically surprising $O(N)$ linear time, rather than $O(N \log N)$, because the majority of nodes reside near the leaves where sift-down paths are short.
**Key Points:**
- Complete binary tree mapped directly to contiguous array indices.
- Min-Heap invariant: $\text{Parent} \le \text{Children}$; Max-Heap: $\text{Parent} \ge \text{Children}$.
- Complexities: Peek $O(1)$, Insert $O(\log N)$, Extract Min/Max $O(\log N)$.
- `buildHeap` algorithm runs in $O(N)$ linear time through bottom-up sift-down operations.
**Evaluation Criteria:** Candidate must explain array index mapping, sift-up and sift-down mechanics, and articulate why building a heap takes $O(N)$ linear time rather than $O(N \log N)$.

### Q9: What is Dynamic Programming, and how does Top-Down Memoization differ from Bottom-Up Tabulation?
**Answer:** Dynamic Programming (DP) is an algorithmic optimization technique used to solve complex problems by breaking them down into overlapping subproblems that exhibit optimal substructure. Top-Down Memoization maintains the natural recursive structure of the problem, checking a cache (hash map or table) before executing any computation; if the subproblem has already been solved, it returns the stored result immediately, pruning redundant branches. Bottom-Up Tabulation eliminates recursion entirely, solving the smallest base subproblems first and iteratively filling an array or table in topological dependency order until reaching the target state. Memoization is often easier to write and only computes states that are strictly needed, but incurs call-stack overhead; Tabulation avoids recursion, prevents stack overflows, and often allows space optimization by discarding obsolete historical states.
**Key Points:**
- Prerequisites: Overlapping subproblems and optimal substructure.
- Top-Down (Memoization): Recursive exploration + cache lookups; computes only visited states.
- Bottom-Up (Tabulation): Iterative loop solving subproblems from base cases upward.
- Trade-offs: Recursion stack overhead vs. cache locality and iterative space-saving optimizations.
**Evaluation Criteria:** Candidate should define the two prerequisite properties of DP and compare memoization with tabulation regarding memory, execution flow, and space optimization potential.

### Q10: What is a Greedy Algorithm, what is the Greedy Choice Property, and when does Greedy succeed where Dynamic Programming is needed?
**Answer:** A Greedy Algorithm builds up a solution piece-by-piece, always choosing the immediate next option that offers the highest local benefit or optimal choice at that specific moment, without ever reconsidering past choices. For a greedy approach to yield a globally optimal solution, the problem must exhibit both Optimal Substructure and the **Greedy Choice Property**—meaning a globally optimal solution can be reached by making locally optimal choices without backtracking. The classic comparison is Knapsack: the **Fractional Knapsack** problem satisfies the greedy choice property (sorting items by value-per-weight density and greedily taking highest density fractions yields the optimal solution). The **0/1 Knapsack** problem fails the greedy choice property because taking a locally high-density item can prevent packing a combination of items that yield higher total value, requiring Dynamic Programming to explore combinations exhaustively.
**Key Points:**
- Makes locally optimal decisions at each step with zero backtracking.
- Greedy Choice Property: Local optimal choices lead directly to global optimum.
- Fractional Knapsack: Greedy succeeds by sorting by value-to-weight ratio.
- 0/1 Knapsack: Greedy fails; requires Dynamic Programming ($O(N \times W)$).
**Evaluation Criteria:** Candidate must precisely define the Greedy Choice Property, contrast greedy decisions with DP state exploration, and use the Fractional vs. 0/1 Knapsack comparison to illustrate failure modes.

---

## Hard

### Q1: How do you design and implement a Least Recently Used (LRU) Cache supporting $O(1)$ time complexity for both `get` and `put` operations?
**Answer:** An LRU Cache requires fast key lookup, rapid item removal, and ordered tracking of access recency. To achieve $O(1)$ performance for both `get` and `put`, the cache is implemented by combining a Hash Map with a Doubly Linked List. The Hash Map maps keys directly to pointers/references of nodes in the doubly linked list, enabling $O(1)$ key lookups. The Doubly Linked List maintains the recency ordering: recently accessed or inserted nodes are moved to the head, while the least recently used node resides at the tail. Utilizing dummy head and dummy tail sentinel nodes eliminates null-pointer edge cases during insertion and deletion. When capacity is exceeded during a `put`, the node immediately preceding the dummy tail is severed in $O(1)$ time and its key is purged from the hash map.
**Key Points:**
- Data structures: Hash Map (for $O(1)$ key lookup) + Doubly Linked List (for $O(1)$ reordering).
- Hash map values store direct node memory references.
- Sentinel nodes (dummy head and dummy tail) eliminate boundary condition edge cases.
- `get(key)`: Fetches node via map, moves node to head, returns value in $O(1)$.
- `put(key, val)`: Updates/inserts node at head; if over capacity, evicts tail node and deletes map entry in $O(1)$.
**Evaluation Criteria:** Look for understanding of combining both data structures, explanation of sentinel nodes, step-by-step eviction mechanics, and proof of strict $O(1)$ time bounds.

### Q2: How does Dijkstra's Algorithm work with a Min-Heap, and why does it fundamentally fail in graphs with negative edge weights?
**Answer:** Dijkstra's Algorithm finds the shortest path from a single source node to all other nodes in a directed or undirected graph with non-negative edge weights. It maintains a distance array initialized to infinity and uses a Min-Heap (priority queue) storing `(distance, vertex)` pairs. At each step, it extracts the unvisited vertex with the minimum tentative distance, marks it as finalized (visited), and relaxes all outgoing edges: if `dist[u] + weight(u, v) < dist[v]`, it updates `dist[v]` and pushes the new pair into the heap, running in $O((V + E) \log V)$ time. It fundamentally fails with negative edge weights because Dijkstra operates on a greedy assumption: once a node is finalized and popped from the priority queue, its shortest distance is assumed to be permanently settled and is never revisited. A negative edge encountered later could provide a shorter path to an already-finalized vertex, violating the invariant and returning incorrect distances.
**Key Points:**
- Greedy Single-Source Shortest Path using Min-Heap and edge relaxation.
- Time complexity: $O((V + E) \log V)$ with a binary heap.
- Invariant: Once a vertex is popped from the min-heap, its shortest path is permanently locked.
- Negative edge failure: A negative weight edge encountered later can invalidate the greedy finality assumption.
- Alternative: Bellman-Ford must be used when negative edge weights exist.
**Evaluation Criteria:** Candidate should detail edge relaxation mechanics, prove the $O((V+E)\log V)$ complexity, and clearly articulate why greedy finality breaks down in the presence of negative edges.

### Q3: Explain Topological Sorting in Directed Acyclic Graphs (DAGs) using Kahn's Algorithm (BFS) and DFS, and how cycle detection is incorporated.
**Answer:** A Topological Sort of a DAG is a linear ordering of vertices such that for every directed edge $u \to v$, vertex $u$ comes before vertex $v$. **Kahn's Algorithm (BFS)** tracks the in-degree (count of incoming edges) of every vertex; all vertices with an in-degree of 0 are added to a queue. As vertices are dequeued and added to the topological list, the in-degrees of their neighbors are decremented; if a neighbor's in-degree drops to 0, it is enqueued. If the total number of processed vertices is less than $V$, the graph contains at least one cycle. **DFS Topological Sort** runs DFS while tracking recursion stack states (unvisited, visiting, visited); visited nodes are prepended to a linked list upon finishing their recursive exploration. A cycle is detected in DFS if an edge leads to a node currently marked as "visiting" (a back-edge).
**Key Points:**
- Valid only on Directed Acyclic Graphs (DAGs); linear dependency ordering.
- Kahn's Algorithm (BFS): In-degree tracking; queue nodes with in-degree 0; decrement neighbor degrees.
- Kahn's Cycle Detection: If processed nodes $< V$, a cycle exists.
- DFS Approach: Post-order traversal pushed to stack/list; 3-state coloring detects back-edges (cycles).
- Time and Space: $O(V + E)$ time and $O(V)$ auxiliary space.
**Evaluation Criteria:** Candidate should explain in-degree mechanics in Kahn's algorithm, 3-state cycle detection in DFS (back-edges), and state time/space bounds.

### Q4: How do Disjoint Set Union (DSU / Union-Find) data structures achieve near-constant $O(\alpha(N))$ time using Path Compression and Union by Rank?
**Answer:** Disjoint Set Union (DSU) maintains a partition of elements into disjoint, non-overlapping sets, supporting two primary operations: `find(x)` (identifying the representative root of $x$'s set) and `union(x, y)` (merging the sets containing $x$ and $y$). Without optimization, trees can degenerate into linear chains yielding $O(N)$ operations. **Path Compression** flattens the tree during `find(x)` by setting the parent of every traversed node directly to the root, making subsequent lookups instant. **Union by Rank (or Size)** always attaches the shorter tree beneath the root of the taller tree during `union()`, preventing tree depth from growing unnecessarily. Together, these two optimizations bound the amortized time complexity per operation to $O(\alpha(N))$, where $\alpha$ is the Inverse Ackermann Function. Because $\alpha(N) < 5$ for all realistic values of $N$ in the observable universe, operations run in virtually constant time.
**Key Points:**
- Manages dynamic connectivity and equivalence classes.
- Path Compression: Recursively updates parent pointers directly to the root during `find()`.
- Union by Rank/Size: Attaches shallower trees under deeper trees to minimize maximum tree height.
- Amortized Complexity: $O(\alpha(N))$ per operation, where $\alpha$ is the extremely slow-growing Inverse Ackermann function.
- Applications: Kruskal's Minimum Spanning Tree, dynamic graph connectivity, cycle detection in undirected graphs.
**Evaluation Criteria:** Look for understanding of both optimizations (path compression and union by rank), the Inverse Ackermann function bound, and application to Kruskal's algorithm.

### Q5: Compare the Bellman-Ford algorithm with the Floyd-Warshall algorithm regarding problem scope, algorithmic mechanics, and time complexity.
**Answer:** Bellman-Ford solves the Single-Source Shortest Path problem on graphs that may contain negative edge weights, operating by relaxing all $E$ edges in the graph $V - 1$ times, yielding a time complexity of $O(V \cdot E)$. A subsequent $V$-th pass checks if any edge can still be relaxed; if so, a negative weight cycle exists. Floyd-Warshall solves the All-Pairs Shortest Path problem on dense graphs using Dynamic Programming, computing the shortest distances between every pair of vertices $(i, j)$ across $O(V^3)$ time and $O(V^2)$ space. It iterates through all possible intermediate vertices $k$, updating `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`. While Bellman-Ford is suited for single-source queries on sparse graphs and negative cycle detection, Floyd-Warshall is suited for dense graphs needing global path matrices.
**Key Points:**
- Bellman-Ford: Single-Source Shortest Path; $O(V \cdot E)$ time; detects negative weight cycles on $V$-th pass.
- Floyd-Warshall: All-Pairs Shortest Path; $O(V^3)$ time, $O(V^2)$ matrix memory.
- Floyd-Warshall DP recurrence: `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`.
- Negative cycles in Floyd-Warshall: Detected if any diagonal element `dist[i][i] < 0`.
**Evaluation Criteria:** Candidate should contrast single-source vs. all-pairs scope, explain the $V-1$ relaxation mechanics of Bellman-Ford, and write/explain the 3-loop DP relation of Floyd-Warshall.

### Q6: How do self-balancing trees (AVL vs. Red-Black Trees) maintain $O(\log N)$ operational bounds, and how do their balancing strictness trade-offs differ?
**Answer:** Unbalanced Binary Search Trees can degenerate into linear linked lists with $O(N)$ operations on sorted inputs; self-balancing trees prevent this by executing tree rotations during insertion and deletion to maintain a bounded height. **AVL Trees** enforce strict balance: the balance factor (height difference between left and right subtrees) for any node must be in $\{-1, 0, +1\}$; violations trigger Single (LL, RR) or Double (LR, RL) rotations. **Red-Black Trees** enforce looser balance using color properties: the root is black, red nodes cannot have red children, and every path from root to leaf must contain the same number of black nodes. Because AVL trees are more strictly balanced, their maximum height is smaller ($\approx 1.44 \log_2 N$) than Red-Black trees ($\approx 2 \log_2 N$), making AVL trees faster for read-heavy workloads. However, Red-Black trees require fewer rotations during mutations, making them superior for write-heavy workloads and the standard choice in system libraries (e.g., C++ `std::map`, Java `TreeMap`).
**Key Points:**
- Prevents tree degeneration using tree rotations (LL, RR, LR, RL).
- AVL Trees: Strict balance factor ($|\text{height}_L - \text{height}_R| \le 1$); faster lookups.
- Red-Black Trees: Balanced via coloring rules; maximum height $\le 2 \log_2(N+1)$; faster insertions/deletions.
- Workload selection: AVL for read-heavy lookups; Red-Black for high-frequency insert/delete environments.
**Evaluation Criteria:** Candidate should explain tree rotation mechanics, contrast balance strictness criteria, and explain why Red-Black trees are preferred for general-purpose standard libraries.

### Q7: How do you solve the 0/1 Knapsack problem using Dynamic Programming, and how do you optimize auxiliary space from $O(N \times W)$ to $O(W)$?
**Answer:** In the 0/1 Knapsack problem, we are given $N$ items with weights and values, and a maximum capacity $W$. The 2D DP state $dp[i][w]$ represents the maximum value achievable considering the first $i$ items with capacity $w$. The recurrence relation is: if $wt[i-1] > w$, then $dp[i][w] = dp[i-1][w]$; otherwise, $dp[i][w] = \max(dp[i-1][w], val[i-1] + dp[i-1][w - wt[i-1]])$, taking $O(N \times W)$ time and space. Notice that computing row $i$ depends exclusively on values from the immediately preceding row $i-1$. We can compress the table into a 1D array $dp[w]$ of size $W+1$ by iterating the capacity $w$ in **reverse** order from $W$ down to $wt[i-1]$. Iterating backwards ensures that $dp[w - wt[i-1]]$ still holds the value from the previous item iteration rather than being overwritten by the current item, preventing the item from being selected multiple times.
**Key Points:**
- State: $dp[i][w]$ is maximum value with $i$ items and capacity $w$.
- Recurrence: $\max(\text{exclude item}, \text{include item if weight permits})$.
- 2D Complexity: $O(N \cdot W)$ time and $O(N \cdot W)$ space (pseudo-polynomial).
- Space optimization to $O(W)$: Single 1D array traversed in reverse ($W \to wt[i]$) to prevent item reuse.
**Evaluation Criteria:** Candidate must write the recurrence relation, explain pseudo-polynomial complexity, and explain why reverse iteration is strictly necessary for 1D space compression.

### Q8: Explain the Trie (Prefix Tree) data structure, its node representation, and why it is superior to Hash Tables for prefix queries and autocomplete.
**Answer:** A Trie is a tree-like data structure used for storing and retrieving strings over an alphabet where keys are not stored directly in nodes; instead, each node contains an array or hash map of child pointers corresponding to characters, and a boolean flag `isEndOfWord`. Words sharing common prefixes share the same initial branch paths from the root. Inserting and searching for a word of length $L$ runs in $O(L)$ time, completely independent of the total number of words $N$ stored in the Trie. While a Hash Table can look up exact string matches in $O(L)$ time, it cannot efficiently perform prefix queries like "find all words starting with 'car'", which requires an $O(N \cdot L)$ scan of the entire hash table. In contrast, a Trie locates the prefix node in $O(L)$ time and performs a subtree DFS to retrieve all autocomplete matches instantly, with lexicographical sorting for free.
**Key Points:**
- Node contains child pointer mapping (size of alphabet) and `isEndOfWord` boolean.
- Search and insert run in $O(L)$ time, where $L$ is word length (independent of corpus size $N$).
- Prefix search / Autocomplete: Locates prefix node in $O(L)$ and explores subtree; Hash Tables must scan all $N$ keys.
- Common prefix compression saves memory for dense dictionaries with shared prefixes.
**Evaluation Criteria:** Candidate should detail Trie node architecture, explain why lookup depends only on string length $L$, and contrast prefix query capabilities against Hash Tables.

### Q9: How does the Knuth-Morris-Pratt (KMP) substring search algorithm achieve $O(N + M)$ time complexity, and how does the Longest Prefix Suffix (LPS) array operate?
**Answer:** The naive substring search compares a pattern of length $M$ against a text of length $N$, resetting the text pointer backwards upon a mismatch and degrading to $O(N \times M)$ worst-case time. The KMP algorithm eliminates text backtracking entirely, running in $O(N + M)$ time by preprocessing the pattern into a Longest Prefix Suffix (LPS) array (also known as the $\pi$ table) in $O(M)$ time. The value `LPS[i]` stores the length of the longest proper prefix of `pattern[0...i]` that is also a suffix of `pattern[0...i]`. When a mismatch occurs at `pattern[j]` against `text[i]`, the text pointer $i$ never retreats; instead, KMP uses `LPS[j-1]` to slide the pattern forward to the next viable alignment that matches the characters already examined. This guarantees that every character in the text is inspected at most twice, yielding linear $O(N + M)$ execution.
**Key Points:**
- Eliminates backward backtracking in the main text pointer during string matching.
- LPS (Longest Prefix Suffix) array precomputed in $O(M)$ time on the pattern.
- `LPS[i]` defines length of longest proper prefix matching a suffix in `pattern[0...i]`.
- Upon mismatch: Text pointer $i$ advances forward; pattern index shifts via $j = LPS[j-1]$.
- Total time complexity: $O(N + M)$ with $O(M)$ auxiliary memory.
**Evaluation Criteria:** Candidate must define the LPS proper prefix/suffix concept, explain why the text pointer never backtracks, and state the linear runtime bound.

### Q10: How do you solve NP-hard combinatorial problems like the Traveling Salesperson Problem (TSP) using Bitmask Dynamic Programming in $O(N^2 \cdot 2^N)$ time?
**Answer:** The Traveling Salesperson Problem seeks the minimum cost Hamiltonian cycle visiting all $N$ cities exactly once and returning to origin; a brute-force search evaluates $(N-1)!$ permutations, which becomes intractable for $N > 12$. Bitmask Dynamic Programming optimizes this by representing the subset of visited cities as an integer bitmask of length $N$, where the $i$-th bit is $1$ if city $i$ has been visited and $0$ otherwise. The state is defined as $dp(mask, u)$, representing the minimum cost to visit all remaining cities given that the subset of already visited cities is $mask$ and the salesperson is currently at city $u$. The recurrence transition is $dp(mask, u) = \min_{v \notin mask} \{ \text{cost}(u, v) + dp(mask \mid (1 \ll v), v) \}$. There are $2^N$ unique subsets and $N$ choices for the current city, resulting in $N \cdot 2^N$ total states, each with $N$ transitions, bringing the total time complexity to $O(N^2 \cdot 2^N)$ with $O(N \cdot 2^N)$ space.
**Key Points:**
- State representation: Integer bitmask of length $N$ encodes the set of visited vertices compactly.
- DP State: $dp(mask, u)$ = minimum cost to complete tour having visited $mask$ ending at vertex $u$.
- Bitwise manipulation: Checking visitation `mask & (1 << v)` and setting visited `mask | (1 << v)`.
- Complexity: Reduces brute force $O(N!)$ down to $O(N^2 \cdot 2^N)$ time and $O(N \cdot 2^N)$ space.
**Evaluation Criteria:** Candidate should explain how bitmasks encode combinatorial subsets, write out the state definition and recurrence relation, and derive the $O(N^2 \cdot 2^N)$ complexity.
