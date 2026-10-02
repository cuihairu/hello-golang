# K-D 树

K-D 树（K-Dimensional Tree，k 维树）是组织 k 维空间点的二叉树：每一层沿一个坐标轴把点集按中位数切成两半，轴按深度轮流取（二维时第 0 层按 x、第 1 层按 y 循环）。它把"平面/空间中的最近邻、范围统计"做到平均 $O(\log n)$，是计算几何里最常用的索引之一。

### 结构定义

1. **节点**: 保存一个点 `p`、划分轴 `axis` 与左右子树。
2. **划分规则**: 深度为偶数层按 x 坐标划分，奇数层按 y 坐标划分（k 维时 `axis = depth % k`）。
3. **左小右大**: 左子树所有点在划分轴上的坐标都不大于节点，右子树都大于节点。

### 算法步骤

1. **建树**: 每层按当前轴对点排序，取中位数做根，左右两半递归。复杂度 $O(n \log^2 n)$。
2. **最近邻查询**: 先递归包含目标点的一侧；若"目标点到分割面的垂直距离平方"小于当前最优距离，另一侧也可能有更近的点，需要一并递归，否则剪枝。
3. **范围统计**: 节点的划分坐标小于区间下界则只搜右子树，大于区间上界则只搜左子树，否则两边都搜，顺便统计落在矩形内的点。

### 代码示例（Go语言实现）

```go
package main

import (
	"fmt"
	"sort"
)

// Point 二维点
type Point struct{ X, Y int }

// kdNode K-D 树节点：偶数层按 x 划分，奇数层按 y 划分
type kdNode struct {
	p     Point
	left  *kdNode
	right *kdNode
	axis  int
}

// buildKD 用中位数法建树
func buildKD(pts []Point, depth int) *kdNode {
	if len(pts) == 0 {
		return nil
	}
	axis := depth % 2
	sort.Slice(pts, func(i, j int) bool {
		if axis == 0 {
			return pts[i].X < pts[j].X
		}
		return pts[i].Y < pts[j].Y
	})
	mid := len(pts) / 2
	return &kdNode{
		p:     pts[mid],
		axis:  axis,
		left:  buildKD(pts[:mid], depth+1),
		right: buildKD(pts[mid+1:], depth+1),
	}
}

func dist2(a, b Point) int {
	dx, dy := a.X-b.X, a.Y-b.Y
	return dx*dx + dy*dy
}

// nearest 最近邻查询：返回最近点与距离平方
func nearest(n *kdNode, target Point) (Point, int) {
	if n == nil {
		return Point{}, 1 << 60
	}
	best, bestD := n.p, dist2(n.p, target)
	// 目标点在划分面的哪一侧，先搜那一侧
	var near, far *kdNode
	if (n.axis == 0 && target.X < n.p.X) || (n.axis == 1 && target.Y < n.p.Y) {
		near, far = n.left, n.right
	} else {
		near, far = n.right, n.left
	}
	if p, d := nearest(near, target); d < bestD {
		best, bestD = p, d
	}
	// 分割面另一侧可能更近：垂距平方小于当前最优距离才需要搜
	diff := target.X - n.p.X
	if n.axis == 1 {
		diff = target.Y - n.p.Y
	}
	if diff*diff < bestD {
		if p, d := nearest(far, target); d < bestD {
			best, bestD = p, d
		}
	}
	return best, bestD
}

// rangeCount 统计矩形 [x1,x2] x [y1,y2] 内的点数
func rangeCount(n *kdNode, x1, x2, y1, y2 int) int {
	if n == nil {
		return 0
	}
	cnt := 0
	if n.p.X >= x1 && n.p.X <= x2 && n.p.Y >= y1 && n.p.Y <= y2 {
		cnt++
	}
	lo, hi := x1, x2
	if n.axis == 1 {
		lo, hi = y1, y2
	}
	v := n.p.X
	if n.axis == 1 {
		v = n.p.Y
	}
	if lo <= v {
		cnt += rangeCount(n.left, x1, x2, y1, y2)
	}
	if hi >= v {
		cnt += rangeCount(n.right, x1, x2, y1, y2)
	}
	return cnt
}

func main() {
	points := []Point{
		{2, 3}, {5, 4}, {9, 6}, {4, 7}, {8, 1}, {7, 2},
	}
	root := buildKD(append([]Point(nil), points...), 0)

	target := Point{9, 2}
	p, d := nearest(root, target)
	fmt.Printf("离 %v 最近的点是 %v，距离平方 %d\n", target, p, d)

	fmt.Println("矩形 [4,9]x[1,6] 内点数:", rangeCount(root, 4, 9, 1, 6))
}
```

运行输出：

```text
离 {9 2} 最近的点是 {8 1}，距离平方 2
矩形 [4,9]x[1,6] 内点数: 4
```

### 复杂度分析

- **建树**: $O(n \log^2 n)$（每层排序），可优化到 $O(n \log n)$。
- **最近邻 / 范围查询**: 平均 $O(\log n)$，最坏 $O(n)$（点分布退化时）。
- **空间**: $O(n)$。

### 应用场景

- 地图"找最近的加油站"、推荐系统中的近邻检索。
- 图形学中的范围查询与碰撞候选集筛选。

### 总结

K-D 树的核心是"按轴轮流切分 + 用分割面距离剪枝"。它与四叉树互补：四叉树按空间均匀四分，K-D 树按数据分布取中位数切分，后者对倾斜数据更友好。查询代码里唯一容易写错的是另一侧的剪枝条件——必须用垂距与当前最优距离比较，而不是简单跳过。
