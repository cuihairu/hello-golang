# 树状数组

树状数组（Fenwick Tree，二叉索引树）用一个紧凑的数组维护前缀和，支持**单点更新**与**区间查询**，两个操作都是 $O(\log n)$。它由 Peter Fenwick 于 1994 年提出，代码量远小于线段树，是前缀和问题的首选实现。

### 核心思想

1. **lowbit**: `lowbit(x) = x & -x`，取二进制最低位的 1，例如 `lowbit(6) = 2`。
2. **树状结构**: 下标 `i` 的元素负责管理区间 `(i - lowbit(i), i]` 上的和，"树"的父节点是 `i + lowbit(i)`。
3. **下标约定**: 元素下标从 1 开始（0 号下标无 lowbit），代码中用 `i+1` 映射原数组。

### 算法步骤

1. **Update(i, delta)**: 从 `i` 开始，`i += lowbit(i)` 逐级向上，把 delta 加到所有管辖该位置的节点。
2. **Query(i)**: 从 `i` 开始，`i -= lowbit(i)` 逐级向下求和，得到前缀和 `a[1..i]`。
3. **区间和 [l, r]**: `Query(r) - Query(l-1)`。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// FenwickTree 树状数组
type FenwickTree struct {
	n   int
	bit []int
}

// NewFenwickTree 创建可容纳 n 个元素的树状数组
func NewFenwickTree(n int) *FenwickTree {
	return &FenwickTree{n: n, bit: make([]int, n+1)}
}

// lowbit 取最低位的 1
func lowbit(x int) int { return x & -x }

// Update 把下标 i（从 1 开始）的元素增加 delta
func (f *FenwickTree) Update(i, delta int) {
	for i <= f.n {
		f.bit[i] += delta
		i += lowbit(i)
	}
}

// Query 求前缀和 [1, i]
func (f *FenwickTree) Query(i int) int {
	sum := 0
	for i > 0 {
		sum += f.bit[i]
		i -= lowbit(i)
	}
	return sum
}

// RangeQuery 求区间和 [l, r]（下标从 1 开始）
func (f *FenwickTree) RangeQuery(l, r int) int {
	return f.Query(r) - f.Query(l-1)
}

func main() {
	arr := []int{1, 3, 5, 7, 9, 11}
	f := NewFenwickTree(len(arr))
	for i, v := range arr {
		f.Update(i+1, v)
	}

	fmt.Println("前缀和[1..3]:", f.Query(3))         // 1+3+5 = 9
	fmt.Println("区间和[2..5]:", f.RangeQuery(2, 5)) // 3+5+7+9 = 24

	f.Update(3, 2) // 第 3 个元素 +2
	fmt.Println("更新后区间和[2..5]:", f.RangeQuery(2, 5))
	fmt.Println("全数组和:", f.Query(len(arr)))
}
```

运行输出：

```text
前缀和[1..3]: 9
区间和[2..5]: 24
更新后区间和[2..5]: 26
全数组和: 38
```

### 复杂度分析

- **单点更新**: $O(\log n)$，最多沿树走上 $\log n$ 层。
- **前缀/区间查询**: $O(\log n)$。
- **空间**: $O(n)$，只有一个长度为 $n+1$ 的数组。
- **限制**: 只能处理"单点更新 + 前缀查询"的区间和；区间更新需要差分转单点 + 前缀查询，或改用线段树。

### 应用场景

- 求逆序对、求区间第 k 小（配合值域离散化）。
- 二维前缀和（二维树状数组）、树上问题的 DFS 序维护。

### 总结

树状数组把"前缀和的增量"与"下标的二进制结构"绑定在一起，用 `lowbit` 完成了线段树 $O(\log n)$ 的全部核心功能，代码却只有十来行。它是小规模区间统计问题中性价比最高的数据结构。
