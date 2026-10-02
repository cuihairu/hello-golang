# 动态树

动态树（Dynamic Tree）问题研究的是：树的结构在变化（加边、删边、改点权）的同时，还要随时回答"某条路径上的信息"。Link/Cut Tree 一章实现了纯连通性版本，这里在其骨架上加入点权 `val` 与子树最大值 `mx`，让每次 `access` 打通路径时顺便把路径聚合值维护到 splay 树根上，从而支持路径最大点权查询。

### 结构定义

1. **节点**: 在 LCT 节点基础上增加 `val`（点权）与 `mx`（所在 splay 子树的最大点权）。
2. **pushup**: `x.mx = max(x.val, 左孩子.mx, 右孩子.mx)`，与普通 splay 维护区间信息完全一致。
3. **路径定位**: `makeRoot(a)` + `access(b)` + `splay(b)` 之后，a 到 b 的路径恰好是 b 所在 splay 树的全部节点，路径最大值就是 `b.mx`。

### 算法步骤

1. **建树**: 每个节点初始化 `val = mx = 自身点权`，用 `Link` 逐条加边。
2. **改点权**: 先 `splay(x)` 把 x 转到辅助树根，修改 `val` 后 `pushup` 即可，不影响其他路径。
3. **路径查询**: 若两点不连通返回 -1；否则 `split` 后读 `b.mx`。
4. **加边/删边**: 与 LCT 完全一致，删除边时注意 `pushup` 修复聚合值。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// node 动态树节点：val 为点权，mx 维护所在 splay 子树的最大点权
type node struct {
	ch  [2]*node
	fa  *node
	rev bool
	val int
	mx  int
	id  int
}

type DynTree struct {
	vs []*node
}

func NewDynTree(vals []int) *DynTree {
	d := &DynTree{vs: make([]*node, len(vals))}
	for i, v := range vals {
		d.vs[i] = &node{val: v, mx: v, id: i}
	}
	return d
}

func isRoot(x *node) bool {
	return x.fa == nil || (x.fa.ch[0] != x && x.fa.ch[1] != x)
}

// pushup 用孩子信息更新 x.mx
func pushup(x *node) {
	x.mx = x.val
	for _, c := range x.ch {
		if c != nil && c.mx > x.mx {
			x.mx = c.mx
		}
	}
}

func pushdown(x *node) {
	if x.rev {
		x.ch[0], x.ch[1] = x.ch[1], x.ch[0]
		if x.ch[0] != nil {
			x.ch[0].rev = !x.ch[0].rev
		}
		if x.ch[1] != nil {
			x.ch[1].rev = !x.ch[1].rev
		}
		x.rev = false
	}
}

func rotate(x *node) {
	p := x.fa
	g := p.fa
	if !isRoot(p) {
		if g.ch[0] == p {
			g.ch[0] = x
		} else {
			g.ch[1] = x
		}
	}
	x.fa = g
	dir := 0
	if p.ch[1] == x {
		dir = 1
	}
	p.ch[dir] = x.ch[dir^1]
	if x.ch[dir^1] != nil {
		x.ch[dir^1].fa = p
	}
	x.ch[dir^1] = p
	p.fa = x
	pushup(p)
	pushup(x)
}

func splay(x *node) {
	var stk []*node
	for y := x; ; y = y.fa {
		stk = append(stk, y)
		if isRoot(y) {
			break
		}
	}
	for i := len(stk) - 1; i >= 0; i-- {
		pushdown(stk[i])
	}
	for !isRoot(x) {
		p := x.fa
		g := p.fa
		if !isRoot(p) {
			if (g.ch[0] == p) == (p.ch[0] == x) {
				rotate(p)
			} else {
				rotate(x)
			}
		}
		rotate(x)
	}
}

func access(x *node) {
	for y := (*node)(nil); x != nil; y, x = x, x.fa {
		splay(x)
		x.ch[1] = y
		pushup(x)
	}
}

func makeRoot(x *node) {
	access(x)
	splay(x)
	x.rev = !x.rev
}

func (d *DynTree) findRoot(x *node) *node {
	access(x)
	splay(x)
	for {
		pushdown(x)
		if x.ch[0] == nil {
			break
		}
		x = x.ch[0]
	}
	splay(x)
	return x
}

// Link 加入一条边（已连通时返回 false）
func (d *DynTree) Link(a, b int) bool {
	x, y := d.vs[a], d.vs[b]
	makeRoot(x)
	if d.findRoot(y) == x {
		return false
	}
	x.fa = y
	return true
}

// Cut 删除一条边（不存在时返回 false）
func (d *DynTree) Cut(a, b int) bool {
	x, y := d.vs[a], d.vs[b]
	if d.findRoot(x) != d.findRoot(y) {
		return false
	}
	makeRoot(x)
	access(y)
	splay(y)
	if y.ch[0] == x && x.ch[1] == nil {
		y.ch[0] = nil
		x.fa = nil
		pushup(y)
		return true
	}
	return false
}

// Update 修改点权
func (d *DynTree) Update(a, v int) {
	x := d.vs[a]
	splay(x)
	x.val = v
	pushup(x)
}

// split 把 a 到 b 的路径聚合一处（此后 b.mx 即路径最大点权）
func (d *DynTree) split(a, b int) {
	x, y := d.vs[a], d.vs[b]
	makeRoot(x)
	access(y)
	splay(y)
}

// PathMax 路径最大点权；不连通时返回 -1
func (d *DynTree) PathMax(a, b int) int {
	if d.findRoot(d.vs[a]) != d.findRoot(d.vs[b]) {
		return -1
	}
	d.split(a, b)
	return d.vs[b].mx
}

func main() {
	// 树: 0-1 0-2 2-3，点权依次为 2, 3, 7, 5
	vals := []int{2, 3, 7, 5}
	d := NewDynTree(vals)
	d.Link(0, 1)
	d.Link(0, 2)
	d.Link(2, 3)

	fmt.Println("0 到 3 路径最大点权:", d.PathMax(0, 3))
	fmt.Println("1 到 3 路径最大点权:", d.PathMax(1, 3))
	d.Update(2, 1)
	fmt.Println("把 2 的点权改为 1 后, 0 到 3 路径最大点权:", d.PathMax(0, 3))
	fmt.Println("把 2 的点权改为 1 后, 1 到 3 路径最大点权:", d.PathMax(1, 3))
	d.Cut(0, 2)
	fmt.Println("Cut(0,2) 后 0 到 3 路径最大点权:", d.PathMax(0, 3))
}
```

运行输出：

```text
0 到 3 路径最大点权: 7
1 到 3 路径最大点权: 7
把 2 的点权改为 1 后, 0 到 3 路径最大点权: 5
把 2 的点权改为 1 后, 1 到 3 路径最大点权: 5
Cut(0,2) 后 0 到 3 路径最大点权: -1
```

### 复杂度分析

- **Link / Cut / Update / PathMax**: 均摊 $O(\log n)$。
- **空间**: $O(n)$。

### 应用场景

- 网络流量建模：边容量变化时查询两点间瓶颈（把"边权下放点权"即可查路径最小/最大边）。
- 动态维护树链信息：路径和、路径最值、路径异或和等都只需替换 `pushup` 的合并式。

### 总结

动态树是 LCT 的直接推广：结构层（access/splay/link/cut）一行不改，只在节点上挂聚合域并让每次旋转、拼接后 `pushup`。把"路径最大"换成"路径和"或"路径最小"，配合懒标记还能支持路径整体加减，这正是它常出现在竞赛题与网络流优化里的原因。验证这类结构最有效的手段是拿朴素邻接表 + DFS 的暴力实现对拍。
