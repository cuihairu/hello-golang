# 最小生成树

最小生成树（Minimum Spanning Tree, MST）在连通无向带权图中选出一棵包含全部 $n$ 个顶点的树，使边权之和最小。Kruskal 算法按"边权从小到大、不成环就选"的贪心策略构造它，配合并查集判环，时间复杂度 $O(E \log E)$。

### Kruskal 算法步骤

1. 把所有边按权值升序排序。
2. 依次考察每条边 `(u, v)`：若 `u` 与 `v` 尚不连通（并查集中根不同），选入生成树并合并两个集合；否则丢弃（会成环）。
3. 选满 $n-1$ 条边或边用完为止。选中的边构成最小生成树。

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
		d.parent[x] = d.parent[d.parent[x]] // 路径压缩
		x = d.parent[x]
	}
	return x
}

// Union 合并两个集合，已在同一集合时返回 false
func (d *DSU) Union(a, b int) bool {
	ra, rb := d.Find(a), d.Find(b)
	if ra == rb {
		return false
	}
	d.parent[ra] = rb
	return true
}

// kruskal 求最小生成树，返回选中的边与总权值
func kruskal(n int, edges []Edge) ([]Edge, int) {
	sorted := append([]Edge(nil), edges...)
	sort.Slice(sorted, func(i, j int) bool { return sorted[i].w < sorted[j].w })

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
	mst, total := kruskal(4, edges)
	fmt.Println("最小生成树的边:")
	for _, e := range mst {
		fmt.Printf("  %d - %d (w=%d)\n", e.u, e.v, e.w)
	}
	fmt.Println("总权值:", total)
}
```

运行输出：

```text
最小生成树的边:
  0 - 2 (w=1)
  2 - 1 (w=2)
  1 - 3 (w=5)
总权值: 8
```

### 复杂度分析

- **排序**: $O(E \log E)$，主导整个算法。
- **并查集操作**: 均摊近似 $O(1)$（路径压缩 + 按秩合并）。
- **空间**: $O(V + E)$。

### 应用场景

- 网络布线、电网、管道铺设等"连通全部节点、总代价最小"的问题。
- 聚类分析（删掉最长的几条边得到簇）、近似算法的基础结构。

### 总结

最小生成树的贪心正确性由"切割性质"保证：任何时刻，横跨已选/未选两个集合的最小边一定属于某棵最小生成树。Kruskal 的实现大半在并查集：判环靠 `Union` 返回 `false`，选边靠它把两个集合合并，选满 $n-1$ 条边就停。
