# Red-Black Tree

A red-black tree is a self-balancing binary search tree that keeps the tree height at $O(\log n)$ by coloring nodes (red/black) and imposing five properties. It relaxes the balance requirement compared with an AVL tree, so insert and delete use fewer rotations; this is why it is widely used in language standard libraries (Java's TreeMap, C++'s std::map, the Linux kernel scheduler, and others).

### The Five Properties

1. Every node is red or black.
2. The root is black.
3. Every leaf (NIL sentinel) is black.
4. Both children of a red node are black (no consecutive red nodes).
5. Every path from any node to each of its NIL leaves contains the same number of black nodes (consistent black height).

Properties 1-5 together guarantee: the longest path is no more than twice the shortest, so the tree height is $O(\log n)$.

### Insertion Fixup Idea

A new node is first colored red (to avoid breaking property 5), then adjusted based on the colors of its "parent and uncle":

1. **Uncle red**: color the parent and uncle black, color the grandparent red, and move the problem up.
2. **Uncle black (triangle)**: first rotate to turn the case into a straight line.
3. **Uncle black (straight line)**: color the parent black and the grandparent red, then perform one rotation in the opposite direction on the grandparent.
Finally color the root black.

### Code Example (Go Implementation)

```go
package main

import "fmt"

type color int

const (
	red color = iota
	black
)

// RBNode red-black tree node; the NIL sentinel's Color is always black
type RBNode struct {
	Key    int
	Color  color
	Left   *RBNode
	Right  *RBNode
	Parent *RBNode // the root's Parent is nil
}

// RedBlackTree red-black tree; nil is the black NIL sentinel
type RedBlackTree struct {
	nil  *RBNode
	root *RBNode
}

// NewRedBlackTree creates an empty tree
func NewRedBlackTree() *RedBlackTree {
	t := &RedBlackTree{}
	t.nil = &RBNode{Color: black}
	t.root = t.nil
	return t
}

// leftRotate left rotation
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

// rightRotate right rotation
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

// Insert inserts key (duplicate keys are ignored)
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
	if y == nil { // empty tree
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

// insertFixup restores the red-black properties after insertion
func (t *RedBlackTree) insertFixup(z *RBNode) {
	for z.Parent != nil && z.Parent.Color == red {
		if z.Parent == z.Parent.Parent.Left {
			uncle := z.Parent.Parent.Right
			if uncle.Color == red { // case 1: red uncle
				z.Parent.Color = black
				uncle.Color = black
				z.Parent.Parent.Color = red
				z = z.Parent.Parent
			} else {
				if z == z.Parent.Right { // case 2: turn into a straight line
					z = z.Parent
					t.leftRotate(z)
				}
				// case 3: rotate the grandparent
				z.Parent.Color = black
				z.Parent.Parent.Color = red
				t.rightRotate(z.Parent.Parent)
			}
		} else { // mirror cases
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

// InOrder in-order traversal
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

// validate checks the programmatically verifiable parts of the five properties
func (t *RedBlackTree) validate() string {
	if t.root.Color != black {
		return "root is not black"
	}
	keys := t.InOrder()
	for i := 1; i < len(keys); i++ {
		if keys[i-1] >= keys[i] {
			return "in-order traversal is not sorted"
		}
	}
	// the number of black nodes is the same on every path, and there are no consecutive red nodes
	var check func(n *RBNode, redParent bool) (int, bool)
	check = func(n *RBNode, redParent bool) (int, bool) {
		if n == t.nil {
			return 1, true // NIL sentinel is black, counts as 1
		}
		if n.Color == red && redParent {
			return 0, false // consecutive red
		}
		lb, lok := check(n.Left, n.Color == red)
		rb, rok := check(n.Right, n.Color == red)
		if !lok || !rok || lb != rb {
			return 0, false
		}
		if n.Color == black {
			return lb + 1, true // black node counts toward black height
		}
		return lb, true // red node does not count
	}
	if _, ok := check(t.root, false); !ok {
		return "inconsistent black height or consecutive red nodes present"
	}
	return "valid"
}

func main() {
	t := NewRedBlackTree()
	for _, k := range []int{10, 20, 30, 15, 25, 40, 50, 60, 55} {
		t.Insert(k)
	}
	fmt.Println("In-order traversal:", t.InOrder())
	fmt.Println("Validation:", t.validate())
}
```

Output:

```text
In-order traversal: [10 15 20 25 30 40 50 55 60]
Validation: valid
```

### Complexity Analysis

- **Search / Insert / Delete**: $O(\log n)$.
- **Space**: $O(n)$, plus the extra color and parent pointer fields.
- Compared with AVL: search is slightly slower (it allows a looser balance), insert and delete are faster (fewer rotations).

### Summary

A red-black tree replaces a strict height difference with a coloring rule, turning "it won't degenerate into a linked list" into five checkable properties. The three cases of insertion fixup (red uncle, triangle, straight line) may look tedious, but every step maintains both the ordering and the black height balance at the same time.

## References

- [Red-Black Tree · Wikipedia](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree)

<!-- BACKLINKS-AUTO -->
## Related pages

- [AVLTree](/algo/tree/AVLTree.md)
- [B+Tree](/algo/tree/B+Tree.md)
- [BTree](/algo/tree/BTree.md)
- [BinaryHeap](/algo/tree/BinaryHeap.md)
- [BinarySearchTree](/algo/tree/BinarySearchTree.md)
- [BinaryTree](/algo/tree/BinaryTree.md)
- [CompleteBinaryTree](/algo/tree/CompleteBinaryTree.md)
- [FenwickTree](/algo/tree/FenwickTree.md)
- [FullBinaryTree](/algo/tree/FullBinaryTree.md)
- [HuffmanTree](/algo/tree/HuffmanTree.md)
- [PrefixTree](/algo/tree/PrefixTree.md)
- [SegmentTree](/algo/tree/SegmentTree.md)
- [Tree](/algo/tree/Tree.md)
- [glossary](/glossary.md)
