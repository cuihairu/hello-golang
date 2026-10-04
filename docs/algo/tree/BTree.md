# B树

B树（B-Tree）是一种多路平衡搜索树，专为磁盘等块状存储设计：每个节点可以存放多个关键字和多个子指针，一次读入一整个节点就完成多路比较，从而大幅减少 I/O 次数。数据库索引（如 MySQL InnoDB）就是 B 树家族的典型应用。

### 结构约束（最小度 t）

1. 每个节点最多 $2t-1$ 个关键字、$2t$ 个孩子。
2. 除根外每个节点至少 $t-1$ 个关键字、$t$ 个孩子。
3. 关键字在节点内升序，父节点关键字把子树的关键字范围分隔开。
4. 所有叶子在同一层——B 树是"从叶子往上半满"生长的，插入时通过**节点分裂**保持平衡。

### 算法步骤（插入）

1. **插入非满节点**: 按 key 下行定位；叶节点直接插入并保持有序；内部节点则选择合适的子树继续下行。
2. **提前分裂**: 下行途中遇到"满节点"（$2t-1$ 个关键字）立即分裂：中间关键字上移给父节点，左右两半成为两个新孩子，再选择一半继续插入。
3. **根分裂**: 根满时新建一个只含原根的根，分裂后树高加一——这正是 B 树"向上生长"保持所有叶子同层的方式。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// BTreeNode B 树节点
type BTreeNode struct {
	keys     []int        // 关键字，升序
	children []*BTreeNode // 子指针，长度为 len(keys)+1；叶节点为空
	leaf     bool
}

// BTree 最小度 t 的 B 树，节点最多 2t-1 个关键字
type BTree struct {
	root *BTreeNode
	t    int
}

// NewBTree 创建空 B 树
func NewBTree(t int) *BTree {
	return &BTree{root: &BTreeNode{leaf: true}, t: t}
}

// Search 查找 key 是否存在
func (bt *BTree) Search(key int) bool {
	n := bt.root
	for {
		i := 0
		for i < len(n.keys) && key > n.keys[i] {
			i++
		}
		if i < len(n.keys) && key == n.keys[i] {
			return true
		}
		if n.leaf {
			return false
		}
		n = n.children[i]
	}
}

// splitChild 把 x 的第 i 个满孩子分裂成两个
func (bt *BTree) splitChild(x *BTreeNode, i int) {
	t := bt.t
	y := x.children[i]
	z := &BTreeNode{leaf: y.leaf}
	mid := y.keys[t-1]
	z.keys = append(z.keys, y.keys[t:]...)
	y.keys = y.keys[:t-1]
	if !y.leaf {
		z.children = append(z.children, y.children[t:]...)
		y.children = y.children[:t]
	}
	x.children = append(x.children, nil)
	copy(x.children[i+2:], x.children[i+1:])
	x.children[i+1] = z
	x.keys = append(x.keys, 0)
	copy(x.keys[i+1:], x.keys[i:])
	x.keys[i] = mid
}

// Insert 插入 key
func (bt *BTree) Insert(key int) {
	if len(bt.root.keys) == 2*bt.t-1 {
		s := &BTreeNode{leaf: false, children: []*BTreeNode{bt.root}}
		bt.root = s
		bt.splitChild(s, 0)
		bt.insertNonFull(s, key)
	} else {
		bt.insertNonFull(bt.root, key)
	}
}

func (bt *BTree) insertNonFull(x *BTreeNode, key int) {
	i := len(x.keys) - 1
	if x.leaf {
		x.keys = append(x.keys, 0)
		for i >= 0 && key < x.keys[i] {
			x.keys[i+1] = x.keys[i]
			i--
		}
		x.keys[i+1] = key
		return
	}
	for i >= 0 && key < x.keys[i] {
		i--
	}
	i++
	if len(x.children[i].keys) == 2*bt.t-1 {
		bt.splitChild(x, i)
		if key > x.keys[i] {
			i++
		}
	}
	bt.insertNonFull(x.children[i], key)
}

// Traverse 中序遍历，得到升序序列
func (bt *BTree) Traverse() []int {
	var out []int
	var walk func(n *BTreeNode)
	walk = func(n *BTreeNode) {
		for i := 0; i < len(n.keys); i++ {
			if !n.leaf {
				walk(n.children[i])
			}
			out = append(out, n.keys[i])
		}
		if !n.leaf {
			walk(n.children[len(n.keys)])
		}
	}
	walk(bt.root)
	return out
}

func main() {
	bt := NewBTree(3)
	for _, k := range []int{10, 20, 5, 6, 12, 30, 7, 17, 3, 25} {
		bt.Insert(k)
	}
	fmt.Println("中序遍历:", bt.Traverse())
	fmt.Println("查找 12:", bt.Search(12))
	fmt.Println("查找 15:", bt.Search(15))
}
```

运行输出：

```text
中序遍历: [3 5 6 7 10 12 17 20 25 30]
查找 12: true
查找 15: false
```

### 复杂度分析

设关键字总数为 $n$、最小度为 $t$，树高 $h \le \log_t \frac{n+1}{2}$：

- **查找/插入**: $O(\log_t n)$ 次节点访问；节点内为有序数组定位 $O(t)$。
- **空间**: $O(n)$。
- **I/O 优势**: 树高远小于二叉树，例如 $t=100$ 时百万级数据树高只有约 3 层。

### 总结

B树把"一个节点装很多关键字"和"所有叶子同层"结合起来，用提前分裂换来从不退化的平衡形态。插入时的分裂与上移，也是 B+树、B*树共用的机制。
