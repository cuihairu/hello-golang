# 八叉树

八叉树（Octree）是四叉树的三维版本：每个节点负责一个立方体区域，点数超过容量时把立方体沿三个坐标轴对半切开，分成 8 个子立方体。它是三维点云、体素建模、碰撞检测等场景的标准空间索引。

### 结构定义

1. **区域**: 轴对齐的立方体（这里用一般的包围盒表示），由两个对角点确定。
2. **8 个孩子**: 按 x、y、z 三个维度的前后各切成两半，共 $2^3 = 8$ 个子区域。
3. **容量**: 叶子最多容纳的点数，超出即细分。

### 算法步骤

1. **插入**: 不在区域内则拒绝；叶子未满直接存；满则细分为 8 个孩子并把存量点重新分发。
2. **区域查询**: 节点包围盒与查询盒不相交则整支剪掉；否则检查自身点并递归 8 个孩子。
3. 三维相交判断与二维完全同构：三个维度分别判"分离"即可。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// Point3 三维点
type Point3 struct{ X, Y, Z int }

// Box3 轴对齐包围盒
type Box3 struct {
	Min, Max Point3 // Max 为开区间上界
}

func (b Box3) contains(p Point3) bool {
	return p.X >= b.Min.X && p.X < b.Max.X &&
		p.Y >= b.Min.Y && p.Y < b.Max.Y &&
		p.Z >= b.Min.Z && p.Z < b.Max.Z
}

// intersects 判断两个包围盒是否相交
func intersects(a, b Box3) bool {
	return !(a.Min.X >= b.Max.X || b.Min.X >= a.Max.X ||
		a.Min.Y >= b.Max.Y || b.Min.Y >= a.Max.Y ||
		a.Min.Z >= b.Max.Z || b.Min.Z >= a.Max.Z)
}

// OctNode 八叉树节点
type OctNode struct {
	boundary Box3
	capacity int
	points   []Point3
	children [8]*OctNode
	divided  bool
}

// NewOctree 创建覆盖 region 的八叉树
func NewOctree(region Box3, capacity int) *OctNode {
	return &OctNode{boundary: region, capacity: capacity}
}

// subdivide 沿三个轴对半切分
func (n *OctNode) subdivide() {
	b := n.boundary
	mx := (b.Min.X + b.Max.X) / 2
	my := (b.Min.Y + b.Max.Y) / 2
	mz := (b.Min.Z + b.Max.Z) / 2
	xs := [2]Box3{{b.Min, Point3{mx, b.Max.Y, b.Max.Z}}, {Point3{mx, b.Min.Y, b.Min.Z}, b.Max}}
	ys := [2][2]int{{b.Min.Y, my}, {my, b.Max.Y}}
	zs := [2][2]int{{b.Min.Z, mz}, {mz, b.Max.Z}}
	i := 0
	for xi, xr := range xs {
		_ = xi
		for _, yr := range ys {
			for _, zr := range zs {
				child := &OctNode{
					boundary: Box3{
						Min: Point3{xr.Min.X, yr[0], zr[0]},
						Max: Point3{xr.Max.X, yr[1], zr[1]},
					},
					capacity: n.capacity,
				}
				n.children[i] = child
				i++
			}
		}
	}
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
func (n *OctNode) Insert(p Point3) bool {
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

// QueryRange 收集包围盒 r 内的所有点
func (n *OctNode) QueryRange(r Box3, out *[]Point3) {
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
	tree := NewOctree(Box3{Point3{0, 0, 0}, Point3{8, 8, 8}}, 2)
	points := []Point3{
		{1, 1, 1}, {2, 2, 2}, {6, 6, 6}, {7, 1, 3}, {3, 7, 5},
	}
	for _, p := range points {
		tree.Insert(p)
	}

	var out []Point3
	tree.QueryRange(Box3{Point3{0, 0, 0}, Point3{4, 4, 4}}, &out)
	fmt.Println("查询 [0,4)^3:", out)

	out = nil
	tree.QueryRange(Box3{Point3{4, 0, 0}, Point3{8, 8, 8}}, &out)
	fmt.Println("查询 [4,8)^3:", out)
}
```

运行输出：

```text
查询 [0,4)^3: [{1 1 1} {2 2 2}]
查询 [4,8)^3: [{7 1 3} {6 6 6}]
```

### 复杂度分析

- **插入**: 平均 $O(\log n)$；点分布极端时退化。
- **区域查询**: $O(\log n + k)$，$k$ 为命中数。
- **空间**: $O(n)$ 量级（由容量与细分深度共同决定）。

### 应用场景

- 3D 点云与体素数据的范围检索。
- 游戏引擎的碰撞检测宽相位、LOD 层次细节管理。

### 总结

八叉树把四叉树的"平面四分"推广到"三维八分"，实现上的差别只是多了一个维度的切分与相交判断。理解了"容量触发细分 + 包围盒剪枝"这套机制，就能在任意维度构造对应的空间索引。
