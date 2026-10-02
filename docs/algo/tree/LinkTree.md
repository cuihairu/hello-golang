# Link/Cut Tree

Link/Cut Tree（LCT，链接/剖分树）是维护"动态森林"的数据结构：在树形结构本身不断变化（加边 `Link`、删边 `Cut`）的前提下，支持连通性判断、路径查询等操作，单次均摊 $O(\log n)$。它的本质是把森林映射成一堆 splay 树：每棵 splay 树存原树的一条"偏爱路径"，splay 树之间用单向的 path-parent 指针相连。

### 结构定义

1. **辅助树**: 每个原树节点对应一个 splay 树节点，中序遍历顺序等于原树中该路径从上到下的顺序。
2. **偏爱路径**: `access(x)` 之后，根到 x 的路径被打通到同一棵 splay 树里。
3. **path-parent**: splay 树根的 `fa` 指向原树中这条路径顶端节点的父节点，但它不算真正的孩子指针——判断"是否为 splay 树根"时必须排除它。

### 算法步骤

1. **access(x)**: 不断把当前 splay 树的右孩子断开、接上上一段路径，自底向上打通根到 x 的偏爱路径。
2. **makeRoot(x)**: `access(x)` 后给整棵辅助树打翻转标记，使 x 成为原树的根。
3. **Link(a, b)**: `makeRoot(a)`，若 `findRoot(b) != a` 则令 `a.fa = b`（挂上 path-parent）。
4. **Cut(a, b)**: `makeRoot(a)` 后 `access(b)` 并 splay，若 a 恰好是 b 的左孩子且 a 没有右子树（说明 a、b 相邻），断开即可。
5. **findRoot(x)**: `access(x)` 后一路向左走并下传翻转标记，最左节点就是树根。
6. **Connected(a, b)**: 比较 `findRoot(a)` 与 `findRoot(b)` 是否为同一节点。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// node LCT 辅助树节点（splay 树节点）
type node struct {
	ch  [2]*node
	fa  *node
	rev bool
	id  int
}

// LCT 维护一片森林：link/cut/connected
type LCT struct {
	vs []*node
}

func NewLCT(n int) *LCT {
	l := &LCT{vs: make([]*node, n)}
	for i := range l.vs {
		l.vs[i] = &node{id: i}
	}
	return l
}

// isRoot x 是否为其所在 splay 树的根（path-parent 不算孩子）
func isRoot(x *node) bool {
	return x.fa == nil || (x.fa.ch[0] != x && x.fa.ch[1] != x)
}

// pushdown 下传翻转标记：交换左右子树
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

// rotate splay 树旋转，注意先挂到祖父上再旋转
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
}

// splay 把 x 转到其所在 splay 树的根（先下传沿途翻转标记）
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

// access 打通根到 x 的偏爱路径
func access(x *node) {
	for y := (*node)(nil); x != nil; y, x = x, x.fa {
		splay(x)
		x.ch[1] = y
	}
}

// makeRoot 把 x 设为其所在树的根
func makeRoot(x *node) {
	access(x)
	splay(x)
	x.rev = !x.rev
}

// findRoot x 所在树的根
func findRoot(x *node) *node {
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

// Connected 判断 a、b 是否连通
func (l *LCT) Connected(a, b int) bool {
	return findRoot(l.vs[a]) == findRoot(l.vs[b])
}

// Link 连接 a、b 所在两棵树（已连通时返回 false）
func (l *LCT) Link(a, b int) bool {
	x, y := l.vs[a], l.vs[b]
	makeRoot(x)
	if findRoot(y) == x {
		return false
	}
	x.fa = y
	return true
}

// Cut 删除 a、b 之间的边（不存在时返回 false）
func (l *LCT) Cut(a, b int) bool {
	x, y := l.vs[a], l.vs[b]
	if findRoot(x) != findRoot(y) {
		return false
	}
	makeRoot(x)
	access(y)
	splay(y)
	if y.ch[0] == x && x.ch[1] == nil {
		y.ch[0] = nil
		x.fa = nil
		return true
	}
	return false
}

func main() {
	l := NewLCT(6)
	l.Link(0, 1)
	l.Link(1, 2)
	l.Link(3, 4)
	fmt.Println("0 和 2 连通:", l.Connected(0, 2))
	fmt.Println("0 和 4 连通:", l.Connected(0, 4))
	fmt.Println("Cut(1,2):", l.Cut(1, 2))
	fmt.Println("Cut 后 0 和 2 连通:", l.Connected(0, 2))
	fmt.Println("再次 Cut(1,2):", l.Cut(1, 2))
	fmt.Println("Link(2,5):", l.Link(2, 5))
	fmt.Println("0 和 5 连通:", l.Connected(0, 5))
	fmt.Println("Link(1,2):", l.Link(1, 2))
	fmt.Println("重新连上后 0 和 5 连通:", l.Connected(0, 5))
}
```

运行输出：

```text
0 和 2 连通: true
0 和 4 连通: false
Cut(1,2): true
Cut 后 0 和 2 连通: false
再次 Cut(1,2): false
Link(2,5): true
0 和 5 连通: false
Link(1,2): true
重新连上后 0 和 5 连通: true
```

（初始森林是 `0-1-2` 与 `3-4`，节点 5 孤立；`Link(2,5)` 之后 0 与 5 分属 `{0,1}` 和 `{2,5}` 两个连通块，所以仍是 false，直到 `Link(1,2)` 把两个分量接起来。）

### 复杂度分析

- **access / makeRoot / Link / Cut / findRoot / Connected**: 均摊 $O(\log n)$。
- **空间**: $O(n)$。

### 应用场景

- 动态图连通性（不断加边、删边，随时询问两点是否连通）。
- 网络可靠性分析、在线游戏中的动态地图。
- 作为基座扩展出路径点权维护、子树信息维护（见"动态树"一章）。

### 总结

LCT 的理解难点全在"path-parent 不算孩子指针"这一条约定上：它让若干 splay 树保持松散连接，`access` 则负责随时重新划分偏爱路径。写对的关键细节是 splay 前先沿祖先栈下传翻转标记，以及 Cut 时用"左孩子且无右子树"确认两点相邻。掌握了连通性版本之后，给它加上 `val` 与 `pushup` 就是能维护路径信息的完整动态树。
