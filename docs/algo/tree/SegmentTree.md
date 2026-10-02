# 线段树

线段树（Segment Tree）是一棵把数组区间递归二分的二叉树：根节点表示整个数组，每个内部节点把区间从中间分开，叶子节点表示单个元素。每个节点存储该区间的某种聚合信息（求和、最值等），从而把"区间查询 + 区间/单点更新"都做到 $O(\log n)$。

### 结构特点

1. **区间二分**: 每个节点对应区间 `[l, r]`，左孩子 `[l, mid]`，右孩子 `[mid+1, r]`。
2. **数组存储**: 节点按堆的方式编号（根为 1，孩子为 `2*node` 与 `2*node+1`），开 $4n$ 空间即可容纳。
3. **信息上浮**: 子节点更新后，父节点重新由两个孩子聚合得到。

### 算法步骤（区间求和）

1. **构建**: 递归到叶子存原值，回溯时 `tree[node] = tree[left] + tree[right]`。
2. **点更新**: 沿路径下行到叶子改值，回溯更新沿途节点。
3. **区间查询**: 若当前节点区间被完全包含直接返回；否则分情况递归左右，合并结果。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// SegmentTree 线段树（区间求和，单点更新）
type SegmentTree struct {
	n    int
	tree []int
}

// NewSegmentTree 由数组构建线段树
func NewSegmentTree(arr []int) *SegmentTree {
	st := &SegmentTree{n: len(arr), tree: make([]int, 4*len(arr))}
	var build func(node, l, r int)
	build = func(node, l, r int) {
		if l == r {
			st.tree[node] = arr[l]
			return
		}
		mid := (l + r) / 2
		build(node*2, l, mid)
		build(node*2+1, mid+1, r)
		st.tree[node] = st.tree[node*2] + st.tree[node*2+1]
	}
	build(1, 0, len(arr)-1)
	return st
}

// Update 把下标 i 的值改为 val
func (st *SegmentTree) Update(i, val int) {
	var rec func(node, l, r int)
	rec = func(node, l, r int) {
		if l == r {
			st.tree[node] = val
			return
		}
		mid := (l + r) / 2
		if i <= mid {
			rec(node*2, l, mid)
		} else {
			rec(node*2+1, mid+1, r)
		}
		st.tree[node] = st.tree[node*2] + st.tree[node*2+1]
	}
	rec(1, 0, st.n-1)
}

// Query 求区间和 [ql, qr]
func (st *SegmentTree) Query(ql, qr int) int {
	var rec func(node, l, r int) int
	rec = func(node, l, r int) int {
		if ql <= l && r <= qr {
			return st.tree[node]
		}
		mid := (l + r) / 2
		sum := 0
		if ql <= mid {
			sum += rec(node*2, l, mid)
		}
		if qr > mid {
			sum += rec(node*2+1, mid+1, r)
		}
		return sum
	}
	return rec(1, 0, st.n-1)
}

func main() {
	arr := []int{1, 3, 5, 7, 9}
	st := NewSegmentTree(arr)

	fmt.Println("区间和[1..3]:", st.Query(1, 3)) // 3+5+7 = 15
	st.Update(2, 10)                           // a[2] = 10
	fmt.Println("更新后[1..3]:", st.Query(1, 3)) // 3+10+7 = 20
	fmt.Println("全数组和:", st.Query(0, 4))      // 1+3+10+7+9 = 30
}
```

运行输出：

```text
区间和[1..3]: 15
更新后[1..3]: 20
全数组和: 30
```

### 复杂度分析

- **构建**: $O(n)$，底层节点共 $n$ 个、上层各占一半，总和 $2n-1$。
- **点更新/区间查询**: $O(\log n)$，每次只走一条或两条分支。
- **空间**: $O(4n)$。
- 加上懒标记（lazy propagation）后，区间更新同样可以做到 $O(\log n)$，见"隐式线段树"一章的打标示范。

### 应用场景

- 区间求和/最值/异或等可合并信息的查询。
- 扫描线求矩形面积并、区间染色、区间历史最值等变体。

### 总结

线段树把"数组"变成"可递归二分的结构"，凡是满足结合律的区间信息都可以挂在节点上。它的模板比树状数组长，但能覆盖区间更新、多信息维护等更复杂的场景。
