# 伸展树

伸展树（Splay Tree）是一种"自我调整"的二叉搜索树：每次访问（查找、插入、删除）后都通过一系列旋转把目标节点转到根的位置。它不需要为节点额外记录颜色或高度，访问过的节点"沉到根部"，最近热点数据就在树顶，均摊时间复杂度为 $O(\log n)$。

### 伸展操作（Splay）

设被访问的节点为 `x`，按以下规则不断旋转直到 `x` 成为根：

1. **zig（单旋）**: `x` 的父亲就是根——对父亲做一次左旋或右旋。
2. **zig-zig（同侧双旋）**: `x` 是左孩子的左孩子（或右孩子的右孩子）——先旋转父节点，再旋转祖父节点。
3. **zig-zag（异侧双旋）**: `x` 是左孩子的右孩子（或右孩子的左孩子）——先旋转父节点把 `x` 顶到原父位置，再旋转祖父节点。

### 算法步骤（三种操作）

1. **查找**: 沿 BST 路径找到 `x`，对 `x` 执行 splay，使其成为根。
2. **插入**: 按 BST 顺序找到空位挂上新节点，再对新节点 splay。
3. **删除**: 先把目标 splay 到根；若无左子树则右子树直接接任；否则把左子树的最大值 splay 到根，再把它与目标的右子树拼接。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// SplayNode 伸展树节点
type SplayNode struct {
	Key    int
	Left   *SplayNode
	Right  *SplayNode
	Parent *SplayNode
}

// SplayTree 伸展树
type SplayTree struct {
	root *SplayNode
}

// rotateLeft 左旋
func (t *SplayTree) rotateLeft(x *SplayNode) {
	y := x.Right
	x.Right = y.Left
	if y.Left != nil {
		y.Left.Parent = x
	}
	y.Parent = x.Parent
	if x.Parent == nil {
		t.root = y
	} else if x == x.Parent.Left {
		x.Parent.Left = y
	} else {
		x.Parent.Right = y
	}
	y.Left = x
	x.Parent = y
}

// rotateRight 右旋
func (t *SplayTree) rotateRight(x *SplayNode) {
	y := x.Left
	x.Left = y.Right
	if y.Right != nil {
		y.Right.Parent = x
	}
	y.Parent = x.Parent
	if x.Parent == nil {
		t.root = y
	} else if x == x.Parent.Right {
		x.Parent.Right = y
	} else {
		x.Parent.Left = y
	}
	y.Right = x
	x.Parent = y
}

// splay 把 x 旋转到根
func (t *SplayTree) splay(x *SplayNode) {
	for x.Parent != nil {
		p := x.Parent
		g := p.Parent
		if g == nil { // zig
			if x == p.Left {
				t.rotateRight(p)
			} else {
				t.rotateLeft(p)
			}
			continue
		}
		// 先旋转父节点，把 x 抬到父的位置
		if x == p.Left {
			t.rotateRight(p)
		} else {
			t.rotateLeft(p)
		}
		// 再旋转祖父节点（zig-zig 与 zig-zag 统一为同一方向）
		if x == g.Left {
			t.rotateRight(g)
		} else {
			t.rotateLeft(g)
		}
	}
}

// Find 查找 key，命中后伸展到根
func (t *SplayTree) Find(key int) bool {
	x := t.root
	for x != nil {
		if key == x.Key {
			t.splay(x)
			return true
		} else if key < x.Key {
			x = x.Left
		} else {
			x = x.Right
		}
	}
	return false
}

// Insert 插入 key
func (t *SplayTree) Insert(key int) {
	var parent *SplayNode
	x := t.root
	for x != nil {
		parent = x
		if key < x.Key {
			x = x.Left
		} else if key > x.Key {
			x = x.Right
		} else {
			t.splay(x)
			return
		}
	}
	n := &SplayNode{Key: key, Parent: parent}
	if parent == nil {
		t.root = n
	} else if key < parent.Key {
		parent.Left = n
	} else {
		parent.Right = n
	}
	t.splay(n)
}

// Delete 删除 key
func (t *SplayTree) Delete(key int) bool {
	n := t.root
	for n != nil {
		if key == n.Key {
			break
		} else if key < n.Key {
			n = n.Left
		} else {
			n = n.Right
		}
	}
	if n == nil {
		return false
	}
	t.splay(n) // n 现在是根
	if n.Left == nil {
		t.root = n.Right
		if n.Right != nil {
			n.Right.Parent = nil
		}
		return true
	}
	// 找左子树的最大值，伸展到根
	m := n.Left
	for m.Right != nil {
		m = m.Right
	}
	t.splay(m)
	// m 是新根，m.Right 即原根 n，n.Left 已在伸展中并入 m
	m.Right = n.Right
	if n.Right != nil {
		n.Right.Parent = m
	}
	return true
}

// InOrder 中序遍历
func (t *SplayTree) InOrder() []int {
	var out []int
	var walk func(n *SplayNode)
	walk = func(n *SplayNode) {
		if n == nil {
			return
		}
		walk(n.Left)
		out = append(out, n.Key)
		walk(n.Right)
	}
	walk(t.root)
	return out
}

func main() {
	t := &SplayTree{}
	for _, k := range []int{10, 20, 30, 15, 25, 5} {
		t.Insert(k)
	}
	fmt.Println("中序遍历:", t.InOrder())

	fmt.Println("find 25:", t.Find(25))
	fmt.Println("find 99:", t.Find(99))
	// 伸展后被访问的节点成为根
	fmt.Println("根节点:", t.root.Key)

	fmt.Println("delete 20:", t.Delete(20))
	fmt.Println("中序遍历:", t.InOrder())
}
```

运行输出：

```text
中序遍历: [5 10 15 20 25 30]
find 25: true
find 99: false
根节点: 25
delete 20: true
中序遍历: [5 10 15 25 30]
```

### 复杂度分析

- **查找/插入/删除**: 单次最坏 $O(n)$，但可以证明**均摊** $O(\log n)$（势能法）。
- **空间**: $O(n)$，每个节点额外一个父指针。
- **局部性**: 最近访问的节点集中在根附近，对缓存与"热点访问"友好。

### 总结

伸展树把"被访问的东西变热"直接编码成了树的形状：不引入任何辅助信息，仅靠旋转就能维持均摊对数性能。它适合访问模式倾斜的场景，也是自调整数据结构的代表作。
