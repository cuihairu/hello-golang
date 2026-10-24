# Algorithms section keep/drop list

There are only two criteria: **strongly related to Go development topics** (typical use of goroutines, channels, interfaces, and generics inside data structures), or **high-frequency and practical** (fundamentals such as sorting, searching, binary trees, heaps, and graph traversal). Anything meeting neither gets deleted.

Result: **103 pages currently exist, 47 kept, 56 deleted.** Deleted pages are removed from SUMMARY, the sidebar, and disk together — no remnants left behind. Kept pages get their implementations and complexity notes completed (see "Completion log" at the end).

## Kept (47 pages)

| Page | Criterion |
|---|---|
| arrary/array.md | Array section index (currently in the misspelled arrary/ directory; moved to array/Array.md in this cleanup) |
| array/CircularBuffer.md | Circular buffer, a structure commonly used for producer-consumer patterns |
| array/DoubleEndedQueue.md | Double-ended queue, a complete implementation of 10 operations |
| array/DynamicArray.md | Go slice semantics (growth / shared underlying array) |
| array/MultidimensionalArray.md | Multidimensional arrays and slices |
| array/PriorityQueue.md | Priority queue, with Go's built-in container/heap |
| array/SparseArray.md | Sparse array, a common space-saving technique |
| hash/Hash.md | Hash table concepts and Go's map |
| list/DynamicArray.md | Hand-written dynamic array, using growth and slices |
| list/HashLinkedList.md | Hash + linked list combination, the basis for an LRU implementation |
| list/Queue.md | Queue implemented with a linked list, complementary to the queue section |
| list/SinglyLinkedList.md | Singly linked list fundamentals |
| list/SkipList.md | Skip list, the underlying structure of Redis zset |
| list/Stack.md | Stack implemented with a linked list, complementary to the stack section |
| list/list.md | Linked list section index |
| queue/Queue.md | Circular queue implementation |
| sort/BubbleSort.md | Basic comparison sort, the starting point for teaching |
| sort/BucketSort.md | A representative non-comparison sort, $O(n)$ on uniform distributions |
| sort/CocktailSort.md | Bidirectional bubble sort, a common improvement over bubble sort |
| sort/CountingSort.md | A representative non-comparison sort, $O(n+k)$ |
| sort/HeapSort.md | A heap application, linked with the heap section |
| sort/InsertionSort.md | Basic comparison sort, $O(n)$ on nearly sorted data |
| sort/MergeSort.md | A representative divide-and-conquer sort, stable $O(n\log n)$ |
| sort/QuickSort.md | Fastest comparison sort on average, pivot and partition ideas |
| sort/RadixSort.md | A representative non-comparison sort, digit-by-digit processing |
| sort/SelectionSort.md | Basic comparison sort |
| sort/ShellSort.md | Shell sort, an interval improvement over insertion sort, illustrates pre-sorting |
| sort/Sort.md | Sort section index and complexity comparison table |
| sort/StableSort.md | The stability concept and multi-field sorting |
| sort/TimSort.md | Industrial-grade stable sort (Python/Java standard libraries), a merge + insertion combination |
| stack/Stack.md | Slice-based stack + bracket-matching example |
| tree/AVLTree.md | A representative balanced tree, rotation operations |
| tree/B+Tree.md | The mainstream structure for database indexes |
| tree/BTree.md | Disk / database index structure |
| tree/BinaryHeap.md | Array implementation of a binary heap and heap construction |
| tree/BinarySearchTree.md | Search tree fundamentals, $O(\log n)$ lookup |
| tree/BinaryTree.md | Binary tree and traversal fundamentals |
| tree/CompleteBinaryTree.md | The complete binary tree is the structural prerequisite for a heap |
| tree/FenwickTree.md | Binary indexed tree, a lightweight implementation for range statistics |
| tree/FullBinaryTree.md | Definition and properties of the full binary tree |
| tree/Heap.md | The heap concept and generic operations |
| tree/HuffmanTree.md | Foundation of compression coding, linked with the compression section |
| tree/MinimumSpanningTree.md | Fundamental graph-algorithm building block (Kruskal/Prim) |
| tree/PrefixTree.md | Trie, prefix matching is high-frequency and practical |
| tree/RedBlackTree.md | The underlying structure of map and the standard library, a frequent interview topic |
| tree/SegmentTree.md | Fundamental building block for range query / update |
| tree/Tree.md | Tree section index |

## Deleted (56 pages)

| Page | Reason |
|---|---|
| list/CircularBuffer.md | A circular buffer is an array structure; array/CircularBuffer is kept, so this one is deleted (a misplaced duplicate under the linked list section) |
| list/DoubleEndedQueue.md | Duplicates array/DoubleEndedQueue (this page has 6 operations, the array version has 10 and is more complete) |
| list/StaticLinkedList.md | Static linked list (cursor-based implementation), leftover textbook material with no use case in Go |
| sort/Batcher'sOddEvenMergeSort.md | Sorting network; the same algorithm as OddEvenMergeSort in two pages, niche |
| sort/BeadSort.md | Bead sort, a toy algorithm that depends on parallel-hardware assumptions |
| sort/BidirectionalBubbleSort.md | i.e. cocktail sort, duplicates CocktailSort (this page itself calls itself an alias) |
| sort/BinaryInsertionSort.md | Real but niche, a small improvement over insertion sort with limited teaching value |
| sort/BitmapSort.md | Niche / duplicate |
| sort/BitwiseSort.md | The content is the digit-wise version of radix sort, duplicates RadixSort, and the code does not even compile |
| sort/BogoSort.md | A joke algorithm, average $O((n+1)!)$, no practical value |
| sort/BozoSort.md | A joke algorithm |
| sort/BridgeSort.md | A non-standard algorithm; the original text itself says "not a standard sorting algorithm" |
| sort/CatalanSort.md | Sorts by mapping onto Catalan numbers, a theoretical toy; the original text itself says it is uncommon |
| sort/CombSort.md | Real but niche, an interval improvement over bubble sort (overlaps with Shell's idea) |
| sort/CycleSort.md | Real but niche; its only selling point is the fewest moves |
| sort/DistributionSort.md | An umbrella concept page for distribution sorts, duplicates the bucket / radix / counting pages |
| sort/DualPivotQuickSort.md | Dual-pivot quicksort, the internal implementation in Java's standard library; weakly related to Go's main line |
| sort/FlashSort.md | Real but niche, histogram flash sort |
| sort/GnomeSort.md | Real but niche, equivalent to insertion sort |
| sort/GroupSort.md | A non-standard algorithm; the original text itself says "not a standard algorithm name" |
| sort/IntervalTreeSort.md | Non-standard naming |
| sort/LayeredQuickSort.md | A home-grown variant, block sort + merge |
| sort/LibrarySort.md | Real but niche, library sort |
| sort/MonkeySort.md | A joke algorithm, same category as BogoSort |
| sort/OddEvenMergeSort.md | Sorting network, the Batcher algorithm, niche (duplicates another page; both are deleted) |
| sort/OddEvenSort.md | Odd-even sort, no advantage under sequential execution |
| sort/OrderTreeSort.md | i.e. TreeSort (BST insertion + in-order traversal), duplicate and non-standard naming |
| sort/PancakeSort.md | Pancake sort, a reversal puzzle, niche |
| sort/ParabolicSort.md | The original text itself says it is "not common"; not a real algorithm |
| sort/ParallelHeapSort.md | Parallel heap sort, showing off |
| sort/PigeonholeSort.md | Equivalent to counting sort, already covered by the counting sort page |
| sort/RebuildSort.md | The original text itself calls it "a hypothetical algorithm" — fictional |
| sort/RippleSort.md | Non-standard naming, niche |
| sort/SleepSort.md | Sleep sort, a joke algorithm (relies on goroutine sleep timing, unreliable) |
| sort/SmoothSort.md | Real but niche, an adaptive heap sort; it is even registered twice in SUMMARY |
| sort/StoogeSort.md | A negative teaching example, slower than bubble sort |
| sort/StrandSort.md | Misnamed in SUMMARY as "bare radix sort"; the real name is Strand sort, niche |
| sort/TreeSort.md | BST sort; the tree section already covers BST, niche |
| tree/BalancedBinaryTree.md | The balanced binary tree concept, duplicates AVLTree |
| tree/BinarySearchHeap.md | A non-standard structure (no such name found) |
| tree/CartesianTree.md | Cartesian tree, niche |
| tree/DynamicTree.md | Dynamic tree (LCT), competition-oriented, niche |
| tree/ExpressionTree.md | Expression tree, compiler-oriented, niche |
| tree/FibonacciHeap.md | Fibonacci heap, high theoretical value but almost never used in engineering |
| tree/ImplicitSegmentTree.md | A variant of the segment tree; SegmentTree already covers it |
| tree/K-DimensionalTree.md | K-D tree, spatial partitioning, niche |
| tree/LinkTree.md | Link/Cut Tree, competition-oriented, niche |
| tree/MaximumSpanningTree.md | The mirror of Kruskal (descending order), replaceable in one sentence; a standalone page is redundant |
| tree/Octree.md | Octree, spatial partitioning, niche |
| tree/Quadtree.md | Quadtree, spatial partitioning, niche |
| tree/RangeTree.md | Range tree, niche (range queries are already covered by the segment tree / binary indexed tree) |
| tree/SplayTree.md | Splay tree, niche |
| tree/SuffixArray.md | Suffix array, an advanced string topic, niche |
| tree/SuffixTree.md | Suffix tree, an advanced string topic, niche |
| tree/Treap.md | Tree heap, a randomized balanced-tree implementation; AVL / red-black already represent balanced trees |
| tree/TreeHeap.md | i.e. the split/merge implementation of Treap, duplicates the Treap page; both are deleted |

## Sections without pages

The six sections in SUMMARY — graph, search, divide and conquer, backtracking, dynamic programming, and greedy — are dead links (no pages). They do not belong to the "existing algorithms inventory", so they are not written up this time; among them, graph traversal is one of the basic building blocks named in the criteria, so a standalone page is recommended later (adjacency-list BFS/DFS).

## Completion log (kept pages)

Acceptance bar for kept pages: every code block passes `go build` + `go run` on its own, with a runnable example and a complexity explanation. The inventory verified 47 pages and 49 code blocks, all of which passed. Two examples that did not compile were fixed along the way: `hash/Hash`'s value-retrieval demo declared an unused variable, so it was changed to the comma-ok idiom; `sort/HeapSort` merged a function fragment split across two blocks into a single block. Five pages missing a complexity explanation got one added: `array/DoubleEndedQueue`, `array/DynamicArray`, `array/MultidimensionalArray`, `array/PriorityQueue`, and `tree/BinaryTree`.

## Sibling pages

- [Graph](/algo/Graph.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Graph](/algo/Graph.md)
- [Queue](/algo/queue/Queue.md)
- [Stack](/algo/stack/Stack.md)
