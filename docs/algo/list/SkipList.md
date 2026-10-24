# Skip List

A skip list is a dynamic data structure built on an ordered linked list by adding multiple layers of index. The bottom layer is an ordered linked list containing every element; each upper layer is a "sample" of the layer below it. Search narrows down top-down and left-to-right, with an average time complexity of $O(\log n)$. Redis's sorted set (ZSet) uses a skip list underneath.

### Structural characteristics

1. **Multiple linked layers**: each node is promoted to level `i` with probability $1/2$ (tunable); the number of levels is determined by a random number.
2. **Ordering**: nodes on the same chain are arranged in ascending order by `key`.
3. **Probabilistic balance**: no rebalancing operations such as rotations are needed; performance is guaranteed in the expected sense by randomization.

### Algorithm steps

1. **Search**: start at the highest level; if the successor node's `key` is less than the target, move right, otherwise drop down a level, continuing until level 0 locates the target.
2. **Insert**: first record each layer's "predecessor node" while performing the search, generate the new node's level randomly, then splice the new node into each layer.
3. **Delete**: after locating the target, unlink it from the chain at every level; if the top level becomes empty, lower the list's height.

### Code example (implemented in Go)

```go
package main

import (
	"fmt"
	"math/rand"
)

const maxLevel = 16

type skipNode struct {
	key  int
	val  int
	next []*skipNode
}

// SkipList skip list
type SkipList struct {
	head  *skipNode
	level int
	rng   *rand.Rand
}

// NewSkipList create a skip list
func NewSkipList() *SkipList {
	return &SkipList{
		head:  &skipNode{next: make([]*skipNode, maxLevel)},
		level: 1,
		rng:   rand.New(rand.NewSource(1)),
	}
}

// randomLevel randomly generate the node's level, rising one level with probability 1/2 each time
func (s *SkipList) randomLevel() int {
	lvl := 1
	for lvl < maxLevel && s.rng.Intn(2) == 0 {
		lvl++
	}
	return lvl
}

// Search look up key
func (s *SkipList) Search(key int) (int, bool) {
	cur := s.head
	for i := s.level - 1; i >= 0; i-- {
		for cur.next[i] != nil && cur.next[i].key < key {
			cur = cur.next[i]
		}
	}
	cur = cur.next[0]
	if cur != nil && cur.key == key {
		return cur.val, true
	}
	return 0, false
}

// Insert insert or update a key-value pair
func (s *SkipList) Insert(key, val int) {
	update := make([]*skipNode, maxLevel)
	cur := s.head
	for i := s.level - 1; i >= 0; i-- {
		for cur.next[i] != nil && cur.next[i].key < key {
			cur = cur.next[i]
		}
		update[i] = cur
	}
	if next := cur.next[0]; next != nil && next.key == key {
		next.val = val // already exists, so update
		return
	}
	lvl := s.randomLevel()
	if lvl > s.level {
		for i := s.level; i < lvl; i++ {
			update[i] = s.head
		}
		s.level = lvl
	}
	node := &skipNode{key: key, val: val, next: make([]*skipNode, lvl)}
	for i := 0; i < lvl; i++ {
		node.next[i] = update[i].next[i]
		update[i].next[i] = node
	}
}

// Delete delete key
func (s *SkipList) Delete(key int) bool {
	update := make([]*skipNode, maxLevel)
	cur := s.head
	for i := s.level - 1; i >= 0; i-- {
		for cur.next[i] != nil && cur.next[i].key < key {
			cur = cur.next[i]
		}
		update[i] = cur
	}
	target := cur.next[0]
	if target == nil || target.key != key {
		return false
	}
	for i := 0; i < s.level && update[i].next[i] == target; i++ {
		update[i].next[i] = target.next[i]
	}
	for s.level > 1 && s.head.next[s.level-1] == nil {
		s.level--
	}
	return true
}

func main() {
	s := NewSkipList()
	for i := 1; i <= 5; i++ {
		s.Insert(i, i*10)
	}
	for i := 1; i <= 5; i++ {
		v, _ := s.Search(i)
		fmt.Printf("%d:%d ", i, v)
	}
	fmt.Println()

	s.Insert(3, 99) // update
	v, _ := s.Search(3)
	fmt.Println("after update, 3 =", v)

	fmt.Println("delete 2:", s.Delete(2))
	_, ok := s.Search(2)
	fmt.Println("2 exists:", ok)
}
```

Output:

```text
1:10 2:20 3:30 4:40 5:50 
after update, 3 = 99
delete 2: true
2 exists: false
```

### Complexity analysis

- **Search / insert / delete**: average $O(\log n)$, worst case $O(n)$ (extremely unlikely).
- **Space**: expected $O(n)$ (the expected number of nodes halves at each level).

### Summary

A skip list uses "space plus randomization" to buy performance close to that of a balanced tree, with a far simpler implementation. It also naturally supports ordered traversal and range queries, making it a classic middle ground between a linked list and a balanced tree.

## References

- [Skip list · Wikipedia](https://en.wikipedia.org/wiki/Skip_list)

## Sibling pages

- [SinglyLinkedList](/algo/list/SinglyLinkedList.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [DynamicArray](/algo/list/DynamicArray.md)
- [HashLinkedList](/algo/list/HashLinkedList.md)
- [Queue](/algo/list/Queue.md)
- [SinglyLinkedList](/algo/list/SinglyLinkedList.md)
- [Stack](/algo/list/Stack.md)
- [list](/algo/list/list.md)
- [glossary](/glossary.md)
