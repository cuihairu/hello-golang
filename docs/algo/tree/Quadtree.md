# 四叉树

四叉树（Quadtree）是把二维平面递归四分的空间索引结构：每个节点负责一个矩形区域，当区域内点数超过容量时把矩形分成西北、东北、西南、东南四个子矩形继续细分。它广泛用于二维空间查询（地图瓦片、碰撞检测、点云筛选）。

### 结构定义

1. **区域（boundary）**: 节点覆盖的矩形，用左上角坐标加宽高表示。
2. **容量（capacity）**: 叶子最多保存的点数，超过即触发细分。
3. **四个孩子**: 每个孩子负责父区域的四分之一，父节点细开后不再直接存点。

### 算法步骤

1. **插入**: 点不在当前区域直接拒绝；叶子未满就存下；满了就细分成四个孩子，把存量点重新分发到孩子。
2. **区域查询**: 若节点区域与查询矩形不相交，整棵子树剪掉；否则先检查节点自身保存的点，再递归四个孩子。
3. 相交判断用坐标比较即可，无需浮点运算。

### 代码示例（Go语言实现）

```go
package main

import (
	"fmt"
	"sort"
)

// Point 二维点
type Point struct{ X, Y int }

// Rect 矩形区域，(X, Y) 为左上角
type Rect struct{ X, Y, W, H int }

func (r Rect) contains(p Point) bool {
	return p.X >= r.X && p.X < r.X+r.W && p.Y >= r.Y && p.Y < r.Y+r.H
}

// intersects 判断两个矩形是否相交
func intersects(a, b Rect) bool {
	return !(a.X >= b.X+b.W || b.X >= a.X+a.W ||
		a.Y >= b.Y+b.H || b.Y >= a.Y+a.H)
}

// QuadNode 四叉树节点
type QuadNode struct {
	boundary Rect
	capacity int
	points   []Point
	children [4]*QuadNode
	divided  bool
}

// NewQuadTree 创建覆盖 region 的四叉树
func NewQuadTree(region Rect, capacity int) *QuadNode {
	return &QuadNode{boundary: region, capacity: capacity}
}

// subdivide 细分成四个子区域，并把存量点下发
func (n *QuadNode) subdivide() {
	b := n.boundary
	hw, hh := b.W/2, b.H/2
	n.children[0] = &QuadNode{boundary: Rect{b.X, b.Y, hw, hh}, capacity: n.capacity}           // 西北
	n.children[1] = &QuadNode{boundary: Rect{b.X + hw, b.Y, b.W - hw, hh}, capacity: n.capacity} // 东北
	n.children[2] = &QuadNode{boundary: Rect{b.X, b.Y + hh, hw, b.H - hh}, capacity: n.capacity} // 西南
	n.children[3] = &QuadNode{boundary: Rect{b.X + hw, b.Y + hh, b.W - hw, b.H - hh}, capacity: n.capacity} // 东南
	for _, p := range n.points {
		for _, c := range n.children {
			if c.Insert(p) {
				break
			}
		}
	}
	n.points = nil
	n.divided = true
}

// Insert 插入点，成功返回 true
func (n *QuadNode) Insert(p Point) bool {
	if !n.boundary.contains(p) {
		return false
	}
	if !n.divided {
		if len(n.points) < n.capacity {
			n.points = append(n.points, p)
			return true
		}
		n.subdivide()
	}
	for _, c := range n.children {
		if c.Insert(p) {
			return true
		}
	}
	return false
}

// QueryRange 收集矩形 r 内的所有点
func (n *QuadNode) QueryRange(r Rect, out *[]Point) {
	if !intersects(n.boundary, r) {
		return
	}
	for _, p := range n.points {
		if r.contains(p) {
			*out = append(*out, p)
		}
	}
	if n.divided {
		for _, c := range n.children {
			c.QueryRange(r, out)
		}
	}
}

func main() {
	tree := NewQuadTree(Rect{0, 0, 16, 16}, 2)
	points := []Point{
		{1, 1}, {2, 3}, {5, 4}, {9, 9}, {12, 2}, {14, 14}, {7, 7},
	}
	for _, p := range points {
		tree.Insert(p)
	}

	var out []Point
	tree.QueryRange(Rect{0, 0, 8, 8}, &out) // 左上 8x8 区域
	sort.Slice(out, func(i, j int) bool {
		if out[i].X != out[j].X {
			return out[i].X < out[j].X
		}
		return out[i].Y < out[j].Y
	})
	fmt.Println("区域 [0,8)x[0,8) 内的点:", out)

	out = nil
	tree.QueryRange(Rect{8, 0, 8, 16}, &out)
	fmt.Println("区域 [8,16)x[0,16) 内的点:", out)
}
```

运行输出：

```text
区域 [0,8)x[0,8) 内的点: [{1 1} {2 3} {5 4} {7 7}]
区域 [8,16)x[0,16) 内的点: [{12 2} {9 9} {14 14}]
```

### 复杂度分析

- **插入**: 平均 $O(\log n)$，最坏 $O(n)$（所有点挤在一个象限里）。
- **区域查询**: $O(\log n + k)$，$k$ 为命中点数（数据均匀时）。
- **空间**: $O(n)$（容量控制下与点数线性相关）。

### 应用场景

- 地图瓦片金字塔（Web Mercator 瓦片即四叉树编号）。
- 2D 游戏 / 图形中的碰撞检测与视锥剔除、稀疏点云索引。

### 总结

四叉树把"二维空间邻近性"翻译成"树的包含关系"，查询时整块子树一起剪掉。它是 k-d 树在均匀网格意义上的姊妹结构，向三维推广就是八叉树。
