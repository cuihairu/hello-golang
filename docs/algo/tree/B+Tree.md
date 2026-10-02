# B+树

B+树是 B树的变体，也是数据库索引的事实标准：**所有数据都存放在叶子层**，内部节点只存放用于导航的分隔键；同时叶子节点用指针串成一条**有序链表**，使范围扫描变得极其高效。MySQL InnoDB 的主键索引就是一棵 B+树。

### 与 B树的区别

1. **数据只在叶子**: 内部节点只是"路标"，同样大小的节点能容纳更多路标，树更矮。
2. **叶子成链**: 找到范围起点后沿 `next` 指针顺序扫描即可，无需回到上层。
3. **每次查询都到叶子**: 无论命中与否，查找路径长度一致。

### 实现要点

本篇采用**批量装载**方式建树：叶子按容量切分并串成链，上一层以"右孩子最小键"为分隔键逐层向上收敛，直到只剩一个根。这是构建 B+树最快、也最不易出错的方式，适合一次性灌入大量有序数据。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// bpNode B+树节点：内部节点用 keys+children，叶子用 keys+vals+next
type bpNode struct {
	leaf     bool
	keys     []int
	children []*bpNode
	vals     []string
	next     *bpNode
}

// leftmostKey 找到子树最左侧叶子的第一个键（即该子树的最小键）
func leftmostKey(n *bpNode) int {
	for !n.leaf {
		n = n.children[0]
	}
	return n.keys[0]
}

// buildBPlusTree 批量装载：keys 需升序，maxKeys 为每节点最大关键字数
func buildBPlusTree(keys []int, vals []string, maxKeys int) *bpNode {
	// 1. 切分叶子层并串链
	var leaves []*bpNode
	for i := 0; i < len(keys); i += maxKeys {
		j := i + maxKeys
		if j > len(keys) {
			j = len(keys)
		}
		leaves = append(leaves, &bpNode{
			leaf: true,
			keys: append([]int(nil), keys[i:j]...),
			vals: append([]string(nil), vals[i:j]...),
		})
	}
	for i := 0; i+1 < len(leaves); i++ {
		leaves[i].next = leaves[i+1]
	}
	// 2. 自底向上构建内部层
	level := leaves
	for len(level) > 1 {
		var next []*bpNode
		for i := 0; i < len(level); i += maxKeys {
			j := i + maxKeys
			if j > len(level) {
				j = len(level)
			}
			group := level[i:j]
			node := &bpNode{children: group}
			for _, c := range group[1:] {
				// 分隔键 = 右子树中的最小键（该子树最左叶子的首键）
				node.keys = append(node.keys, leftmostKey(c))
			}
			next = append(next, node)
		}
		level = next
	}
	if len(level) == 0 {
		return nil
	}
	return level[0]
}

// Search 查找 key 对应的值
func Search(root *bpNode, key int) (string, bool) {
	n := root
	for n != nil && !n.leaf {
		i := 0
		for i < len(n.keys) && key >= n.keys[i] {
			i++
		}
		n = n.children[i]
	}
	if n == nil {
		return "", false
	}
	for i, k := range n.keys {
		if k == key {
			return n.vals[i], true
		}
	}
	return "", false
}

// RangeQuery 返回 key 在 [lo, hi] 内的所有值（沿叶子链扫描）
func RangeQuery(root *bpNode, lo, hi int) []string {
	n := root
	for n != nil && !n.leaf {
		i := 0
		for i < len(n.keys) && lo >= n.keys[i] {
			i++
		}
		n = n.children[i]
	}
	var out []string
	for n != nil {
		for i, k := range n.keys {
			if k > hi {
				return out
			}
			if k >= lo {
				out = append(out, n.vals[i])
			}
		}
		n = n.next
	}
	return out
}

func main() {
	keys := []int{1, 3, 5, 7, 9, 11, 13, 15, 17, 19}
	vals := make([]string, len(keys))
	for i, k := range keys {
		vals[i] = fmt.Sprintf("row-%02d", k)
	}
	root := buildBPlusTree(keys, vals, 4)

	if v, ok := Search(root, 11); ok {
		fmt.Println("查找 11:", v)
	}
	_, ok := Search(root, 12)
	fmt.Println("查找 12:", ok)

	fmt.Println("范围 [5,13]:", RangeQuery(root, 5, 13))
	fmt.Println("范围 [14,19]:", RangeQuery(root, 14, 19))
	fmt.Println("范围 [0,100]:", len(RangeQuery(root, 0, 100)), "条")
}
```

运行输出：

```text
查找 11: row-11
查找 12: false
范围 [5,13]: [row-05 row-07 row-09 row-11 row-13]
范围 [14,19]: [row-15 row-17 row-19]
范围 [0,100]: 10 条
```

### 复杂度分析

- **查找/范围起点定位**: $O(\log_m n)$ 层导航（$m$ 为节点容量）。
- **范围查询**: $O(\log_m n + k)$，$k$ 为命中条数——沿叶子链顺序读取。
- **批量装载**: $O(n)$。
- **空间**: $O(n)$。

### 应用场景

- 数据库主键/二级索引、文件系统（如 ext4 的 HTree）。
- 任何需要"点查 + 范围扫"兼备的有序存储。

### 总结

B+树用"数据下沉到叶子 + 叶子成链"的改造，让范围查询从"逐层回溯"变成"顺序扫描"，这正是它击败 B树成为数据库标准索引的根本原因。
