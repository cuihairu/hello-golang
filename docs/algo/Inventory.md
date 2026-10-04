# 算法篇去留清单

判据只有两条:**与 Go 语言学习主线强相关**(goroutine/channel/接口/泛型在数据结构里的典型运用),或**高频实用**(排序/查找/二叉树/堆/图遍历这类基础件)。两条都不占的,删。

结果:**现存 103 页,保留 47,删除 56**。删除篇目从 SUMMARY、侧边栏与磁盘一并清掉,不留残骸;保留篇目补齐实现与复杂度说明(见文末「补全记录」)。

## 保留(47 篇)

| 页面 | 判据 |
|---|---|
| arrary/array.md | 数组篇索引(现状在拼错目录 arrary/,随本次清理改到 array/Array.md) |
| array/CircularBuffer.md | 环形缓冲区,生产者-消费者常用结构 |
| array/DoubleEndedQueue.md | 双端队列,10 个操作的完整实现 |
| array/DynamicArray.md | Go 切片语义(扩容/共享底层数组) |
| array/MultidimensionalArray.md | 多维数组与切片 |
| array/PriorityQueue.md | 优先队列,Go 自带 container/heap |
| array/SparseArray.md | 稀疏数组,节省空间的常见手法 |
| hash/Hash.md | 哈希表概念与 Go map |
| list/DynamicArray.md | 手写动态数组,扩容与切片运用 |
| list/HashLinkedList.md | 哈希+链表组合,LRU 的实现基础 |
| list/Queue.md | 链表实现的队列,与 queue 篇互补 |
| list/SinglyLinkedList.md | 单链表基础 |
| list/SkipList.md | 跳表,Redis zset 底层结构 |
| list/Stack.md | 链表实现的栈,与 stack 篇互补 |
| list/list.md | 链表篇索引 |
| queue/Queue.md | 环形队列实现 |
| sort/BubbleSort.md | 基础比较排序,教学起点 |
| sort/BucketSort.md | 非比较排序代表,均匀分布 $O(n)$ |
| sort/CocktailSort.md | 双向冒泡,冒泡的常见改进 |
| sort/CountingSort.md | 非比较排序代表,$O(n+k)$ |
| sort/HeapSort.md | 堆的应用,与堆篇联动 |
| sort/InsertionSort.md | 基础比较排序,有序数据 $O(n)$ |
| sort/MergeSort.md | 分治代表,稳定 $O(n\log n)$ |
| sort/QuickSort.md | 平均最快的比较排序,主元/分区思想 |
| sort/RadixSort.md | 非比较排序代表,按位处理 |
| sort/SelectionSort.md | 基础比较排序 |
| sort/ShellSort.md | 希尔排序,插入排序的间隔改进,理解预排序 |
| sort/Sort.md | 排序篇索引与复杂度对比表 |
| sort/StableSort.md | 稳定性概念与多字段排序 |
| sort/TimSort.md | 工业级稳定排序(Python/Java 标准库),归并+插入的组合 |
| stack/Stack.md | 切片实现的栈+括号匹配示例 |
| tree/AVLTree.md | 平衡树代表,旋转操作 |
| tree/B+Tree.md | 数据库索引的主流结构 |
| tree/BTree.md | 磁盘/数据库索引结构 |
| tree/BinaryHeap.md | 二叉堆的数组实现与建堆 |
| tree/BinarySearchTree.md | 查找树基础,$O(\log n)$ 查找 |
| tree/BinaryTree.md | 二叉树与遍历基础 |
| tree/CompleteBinaryTree.md | 完全二叉树是堆的结构前提 |
| tree/FenwickTree.md | 树状数组,区间统计的轻量实现 |
| tree/FullBinaryTree.md | 满二叉树定义与性质 |
| tree/Heap.md | 堆的概念与通用操作 |
| tree/HuffmanTree.md | 压缩编码基础,与压缩篇联动 |
| tree/MinimumSpanningTree.md | 图算法基础件(Kruskal/Prim) |
| tree/PrefixTree.md | Trie,前缀匹配高频实用 |
| tree/RedBlackTree.md | map 与标准库的底层结构,高频面试 |
| tree/SegmentTree.md | 区间查询/更新基础件 |
| tree/Tree.md | 树篇索引 |

## 删除(56 篇)

| 页面 | 理由 |
|---|---|
| list/CircularBuffer.md | 环形缓冲区是数组结构,array/CircularBuffer 保留,本篇删(链表篇下的错位重复) |
| list/DoubleEndedQueue.md | 与 array/DoubleEndedQueue 重复(本篇 6 个操作,数组版 10 个更完整) |
| list/StaticLinkedList.md | 静态链表(游标实现),教材遗留内容,Go 里无使用场景 |
| sort/Batcher'sOddEvenMergeSort.md | 排序网络,与 OddEvenMergeSort 同一算法两篇,冷门 |
| sort/BeadSort.md | 珠排序,玩具算法,依赖并行硬件假设 |
| sort/BidirectionalBubbleSort.md | 即鸡尾酒排序,与 CocktailSort 重复(本篇自认别名) |
| sort/BinaryInsertionSort.md | 真实但冷门,插入排序的小改进,教学增量有限 |
| sort/BitmapSort.md | 冷门/重复 |
| sort/BitwiseSort.md | 内容即基数排序的按位版,与 RadixSort 重复,且代码编译不过 |
| sort/BogoSort.md | 玩笑算法,平均 $O((n+1)!)$,无实用价值 |
| sort/BozoSort.md | 玩笑算法 |
| sort/BridgeSort.md | 非标准算法,原文自述「不是标准的排序算法」 |
| sort/CatalanSort.md | 按卡塔兰数映射排序,理论玩具,原文自述不常见 |
| sort/CombSort.md | 真实但冷门,冒泡的间隔改进(与希尔思想重复) |
| sort/CycleSort.md | 真实但冷门,唯一卖点是移动次数最少 |
| sort/DistributionSort.md | 分配排序概念统称页,与桶/基数/计数三篇重复 |
| sort/DualPivotQuickSort.md | 双基快排,Java 标准库内部实现,Go 主线弱相关 |
| sort/FlashSort.md | 真实但冷门,直方图 flash 排序 |
| sort/GnomeSort.md | 真实但冷门,与插入排序等价 |
| sort/GroupSort.md | 非标准算法,原文自述「不是一个标准的算法名称」 |
| sort/IntervalTreeSort.md | 非标准命名 |
| sort/LayeredQuickSort.md | 自造变体,分块排序+归并 |
| sort/LibrarySort.md | 真实但冷门,库排序 |
| sort/MonkeySort.md | 玩笑算法,与 BogoSort 同类 |
| sort/OddEvenMergeSort.md | 排序网络,Batcher 算法,冷门(与另一篇重复,两篇均删) |
| sort/OddEvenSort.md | 奇偶排序,串行下无优势 |
| sort/OrderTreeSort.md | 即 TreeSort(BST 插入+中序),重复且非标准命名 |
| sort/PancakeSort.md | 煎饼排序,翻转技巧题,冷门 |
| sort/ParabolicSort.md | 原文自述「并不常见」,非真实算法 |
| sort/ParallelHeapSort.md | 并行堆排序,炫技 |
| sort/PigeonholeSort.md | 与计数排序等价,计数排序篇已覆盖 |
| sort/RebuildSort.md | 原文自述「假想的算法」——虚构 |
| sort/RippleSort.md | 非标准命名,冷门 |
| sort/SleepSort.md | 睡眠排序,玩笑算法(靠 goroutine 睡眠时序,不可靠) |
| sort/SmoothSort.md | 真实但冷门,自适应堆排序,SUMMARY 里还重复登记了两次 |
| sort/StoogeSort.md | 教学反面示例,比冒泡还慢 |
| sort/StrandSort.md | SUMMARY 误名「裸基数排序」,真实名 Strand sort,冷门 |
| sort/TreeSort.md | BST 排序,树篇已覆盖 BST,冷门 |
| tree/BalancedBinaryTree.md | 平衡二叉树概念,与 AVLTree 重复 |
| tree/BinarySearchHeap.md | 非标准结构(查无此名) |
| tree/CartesianTree.md | 笛卡尔树,冷门 |
| tree/DynamicTree.md | 动态树(LCT),竞赛向,冷门 |
| tree/ExpressionTree.md | 表达式树,编译原理向,冷门 |
| tree/FibonacciHeap.md | 斐波那契堆,理论价值高工程几乎不用 |
| tree/ImplicitSegmentTree.md | 线段树的变体,SegmentTree 已覆盖 |
| tree/K-DimensionalTree.md | K-D 树,空间划分,冷门 |
| tree/LinkTree.md | Link/Cut Tree,竞赛向,冷门 |
| tree/MaximumSpanningTree.md | Kruskal 的镜像(降序),一句话可代,独立成篇冗余 |
| tree/Octree.md | 八叉树,空间划分,冷门 |
| tree/Quadtree.md | 四叉树,空间划分,冷门 |
| tree/RangeTree.md | 区间树,冷门(区间查询已由线段树/树状数组覆盖) |
| tree/SplayTree.md | 伸展树,冷门 |
| tree/SuffixArray.md | 后缀数组,字符串高级专题,冷门 |
| tree/SuffixTree.md | 后缀树,字符串高级专题,冷门 |
| tree/Treap.md | 树堆,平衡树的随机化实现,AVL/红黑树已代表平衡树 |
| tree/TreeHeap.md | 即 Treap 的 split/merge 实现,与 Treap 篇重复,两篇均删 |

## 未成篇章节

SUMMARY 里的图、搜索、分治、回溯、动态规划、贪心六节是空链接(无页面)。它们不属于「现存算法盘点」,本次不补写;其中图遍历属判据点名的基础件,建议后续单独成篇(BFS/DFS 邻接表实现)。

## 补全记录(保留篇)

保留篇的验收标准:每个代码块单独 `go build` + `go run` 通过,含可运行示例与复杂度说明。盘点实测 47 页 49 个代码块全部通过。过程中修了两处编不过的示例:`hash/Hash` 的取值演示声明了未使用的变量,改成 comma-ok 惯用法;`sort/HeapSort` 把拆成两块的函数片段合并为一块。给缺复杂度说明的 5 篇补了复杂度一节:`array/DoubleEndedQueue`、`array/DynamicArray`、`array/MultidimensionalArray`、`array/PriorityQueue`、`tree/BinaryTree`。

