# 最大生成树

最大生成树（Maximum Spanning Tree）与最小生成树镜像：在连通无向带权图中选一棵包含全部顶点的树，使**边权之和最大**。算法与 Kruskal 完全一致，唯一区别是边按权值**降序**排序——贪心方向反转。

### Kruskal 变体步骤

1. 把所有边按权值**降序**排序。
2. 依次考察每条边：两端不连通就选入生成树，否则丢弃。
3. 选满 $n-1$ 条边为止，得到最大生成树。

等价做法：把所有权值取相反数后求最小生成树，再把结果权值取回。

### 代码示例（Go语言实现）

```go
package main

import (
	"fmt"
	"sort"
)

// Edge 无向带权边
type Edge struct {
	u, v, w int
}

// DSU 并查集（带路径压缩）
type DSU struct {
	parent []int
}

func NewDSU(n int) *DSU {
	p := make([]int, n)
	for i := range p {
		p[i] = i
	}
	return &DSU{parent: p}
}

func (d *DSU) Find(x int) int {
	for d.parent[x] != x {
		d.parent[x] = d.parent[d.parent[x]]
		x = d.parent[x]
	}
	return x
}

func (d *DSU) Union(a, b int) bool {
	ra, rb := d.Find(a), d.Find(b)
	if ra == rb {
		return false
	}
	d.parent[ra] = rb
	return true
}

// kruskalMax 求最大生成树：只把排序方向改为降序
func kruskalMax(n int, edges []Edge) ([]Edge, int) {
	sorted := append([]Edge(nil), edges...)
	sort.Slice(sorted, func(i, j int) bool { return sorted[i].w > sorted[j].w })

	dsu := NewDSU(n)
	var mst []Edge
	total := 0
	for _, e := range sorted {
		if dsu.Union(e.u, e.v) {
			mst = append(mst, e)
			total += e.w
			if len(mst) == n-1 {
				break
			}
		}
	}
	return mst, total
}

func main() {
	edges := []Edge{
		{0, 1, 4}, {0, 2, 1}, {2, 1, 2}, {1, 3, 5}, {2, 3, 8},
	}
	mst, total := kruskalMax(4, edges)
	fmt.Println("最大生成树的边:")
	for _, e := range mst {
		fmt.Printf("  %d - %d (w=%d)\n", e.u, e.v, e.w)
	}
	fmt.Println("总权值:", total)
}
```

运行输出：

```text
最大生成树的边:
  2 - 3 (w=8)
  1 - 3 (w=5)
  0 - 1 (w=4)
总权值: 17
```

### 复杂度分析

- **时间**: $O(E \log E)$，与 Kruskal 相同（排序主导）。
- **空间**: $O(V + E)$。

### 应用场景

- 网络中"优先利用高带宽链路"的骨干网设计。
- 图像分割（最小损失割）、 bottleneck 型问题（最大瓶颈路）。

### 总结

最大生成树说明贪心框架的普适性：排序方向决定了求"最小"还是"最大"，判环与合并逻辑完全复用。它与最小生成树共享同一条理论根基——切割性质只是把"最小边"换成了"最大边"。
