# 红黑树

红黑树（Red-Black Tree）是一种自平衡二叉搜索树，通过给节点染色（红/黑）并施加五条性质，把树高限制在 $O(\log n)$。它比 AVL 树放松了平衡要求，插入删除的旋转更少，因此被广泛用于语言标准库（Java 的 TreeMap、C++ 的 std::map、Linux 内核的调度器等）。

### 五条性质

1. 每个节点是红色或黑色。
2. 根节点是黑色。
3. 每个叶子（NIL 哨兵）是黑色。
4. 红色节点的两个孩子都是黑色（不存在连续红节点）。
5. 任一节点到其每个 NIL 子叶的路径都含相同数目的黑节点（黑高一致）。

性质 1-5 共同保证：最长路径不超过最短路径的两倍，树高 $O(\log n)$。

### 插入修复思路

新节点先染成红色（避免破坏性质 5），再根据"父亲与叔叔"的颜色调整：

1. **叔叔红**: 父、叔染黑，祖父染红，把问题上移。
2. **叔叔黑（三角形）**: 先旋转把情形化为直线。
3. **叔叔黑（直线）**: 父染黑、祖父染红，对祖父做一次相反方向的旋转。
最后把根染黑。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

type color int

const (
	red color = iota
	black
)

// RBNode 红黑树节点，NIL 哨兵的 Color 恒为 black
type RBNode struct {
	Key    int
	Color  color
	Left   *RBNode
	Right  *RBNode
	Parent *RBNode // 根的 Parent 为 nil
}

// RedBlackTree 红黑树，nil 为黑色 NIL 哨兵
type RedBlackTree struct {
	nil  *RBNode
	root *RBNode
}

// NewRedBlackTree 创建空树
func NewRedBlackTree() *RedBlackTree {
	t := &RedBlackTree{}
	t.nil = &RBNode{Color: black}
	t.root = t.nil
	return t
}

// leftRotate 左旋
func (t *RedBlackTree) leftRotate(x *RBNode) {
	y := x.Right
	x.Right = y.Left
	if y.Left != t.nil {
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

// rightRotate 右旋
func (t *RedBlackTree) rightRotate(x *RBNode) {
	y := x.Left
	x.Left = y.Right
	if y.Right != t.nil {
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

// Insert 插入 key（重复键忽略）
func (t *RedBlackTree) Insert(key int) {
	var y *RBNode
	x := t.root
	for x != t.nil {
		y = x
		switch {
		case key < x.Key:
			x = x.Left
		case key > x.Key:
			x = x.Right
		default:
			return
		}
	}
	z := &RBNode{Key: key, Color: red, Left: t.nil, Right: t.nil}
	if y == nil { // 空树
		t.root = z
	} else {
		z.Parent = y
		if key < y.Key {
			y.Left = z
		} else {
			y.Right = z
		}
	}
	t.insertFixup(z)
}

// insertFixup 插入后恢复红黑性质
func (t *RedBlackTree) insertFixup(z *RBNode) {
	for z.Parent != nil && z.Parent.Color == red {
		if z.Parent == z.Parent.Parent.Left {
			uncle := z.Parent.Parent.Right
			if uncle.Color == red { // 情形 1：叔叔红
				z.Parent.Color = black
				uncle.Color = black
				z.Parent.Parent.Color = red
				z = z.Parent.Parent
			} else {
				if z == z.Parent.Right { // 情形 2：化为直线
					z = z.Parent
					t.leftRotate(z)
				}
				// 情形 3：旋转祖父
				z.Parent.Color = black
				z.Parent.Parent.Color = red
				t.rightRotate(z.Parent.Parent)
			}
		} else { // 镜像情形
			uncle := z.Parent.Parent.Left
			if uncle.Color == red {
				z.Parent.Color = black
				uncle.Color = black
				z.Parent.Parent.Color = red
				z = z.Parent.Parent
			} else {
				if z == z.Parent.Left {
					z = z.Parent
					t.rightRotate(z)
				}
				z.Parent.Color = black
				z.Parent.Parent.Color = red
				t.leftRotate(z.Parent.Parent)
			}
		}
	}
	t.root.Color = black
}

// InOrder 中序遍历
func (t *RedBlackTree) InOrder() []int {
	var out []int
	var walk func(n *RBNode)
	walk = func(n *RBNode) {
		if n == t.nil {
			return
		}
		walk(n.Left)
		out = append(out, n.Key)
		walk(n.Right)
	}
	walk(t.root)
	return out
}

// validate 校验五条性质中可程序化验证的部分
func (t *RedBlackTree) validate() string {
	if t.root.Color != black {
		return "根不是黑色"
	}
	keys := t.InOrder()
	for i := 1; i < len(keys); i++ {
		if keys[i-1] >= keys[i] {
			return "中序遍历不有序"
		}
	}
	// 每条路径黑节点数一致，且无连续红节点
	var check func(n *RBNode, redParent bool) (int, bool)
	check = func(n *RBNode, redParent bool) (int, bool) {
		if n == t.nil {
			return 1, true // NIL 哨兵是黑色，计 1
		}
		if n.Color == red && redParent {
			return 0, false // 连续红
		}
		lb, lok := check(n.Left, n.Color == red)
		rb, rok := check(n.Right, n.Color == red)
		if !lok || !rok || lb != rb {
			return 0, false
		}
		if n.Color == black {
			return lb + 1, true // 黑节点计入黑高
		}
		return lb, true // 红节点不计入
	}
	if _, ok := check(t.root, false); !ok {
		return "黑高不一致或存在连续红节点"
	}
	return "合法"
}

func main() {
	t := NewRedBlackTree()
	for _, k := range []int{10, 20, 30, 15, 25, 40, 50, 60, 55} {
		t.Insert(k)
	}
	fmt.Println("中序遍历:", t.InOrder())
	fmt.Println("校验:", t.validate())
}
```

运行输出：

```text
中序遍历: [10 15 20 25 30 40 50 55 60]
校验: 合法
```

### 复杂度分析

- **查找/插入/删除**: $O(\log n)$。
- **空间**: $O(n)$，额外颜色与父指针字段。
- 与 AVL 相比：查找略慢（允许更松的平衡），插入删除更快（旋转更少）。

### 总结

红黑树用染色规则代替严格的身高差，把"不会退化成链表"这件事变成了五条可验证的性质。插入修复的三种情形（叔叔红、三角形、直线）看似琐碎，实则每一步都在同时维护有序性与黑高平衡。
