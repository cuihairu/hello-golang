# 跳表

跳表（Skip List）是在有序链表基础上增加多层索引的动态数据结构。底层是一条包含全部元素的有序链表，上层是对下层的"抽样"，查找时自上而下、自左向右地缩小范围，平均时间复杂度 $O(\log n)$。Redis 的有序集合（ZSet）底层就用到了跳表。

### 结构特点

1. **多层链表**: 每个节点被提升到第 `i` 层的概率为 $1/2$（可调），层数由随机数决定。
2. **有序性**: 同一条链上的节点按 `key` 升序排列。
3. **概率平衡**: 不需要旋转等再平衡操作，用随机化期望上保证性能。

### 算法步骤

1. **查找**: 从最高层开始，若后继节点 `key` 小于目标则右移，否则下降一层，直到第 0 层定位目标。
2. **插入**: 先按查找过程记录每层的"前驱节点"，随机生成新节点的层数，再逐层把新节点接入。
3. **删除**: 定位目标后，把它从每一层的链表中摘除；若顶层变空则降低表高。

### 代码示例（Go语言实现）

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

// SkipList 跳表
type SkipList struct {
	head  *skipNode
	level int
	rng   *rand.Rand
}

// NewSkipList 创建跳表
func NewSkipList() *SkipList {
	return &SkipList{
		head:  &skipNode{next: make([]*skipNode, maxLevel)},
		level: 1,
		rng:   rand.New(rand.NewSource(1)),
	}
}

// randomLevel 随机生成节点层数，每次以 1/2 概率上升一层
func (s *SkipList) randomLevel() int {
	lvl := 1
	for lvl < maxLevel && s.rng.Intn(2) == 0 {
		lvl++
	}
	return lvl
}

// Search 查找 key
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

// Insert 插入或更新键值对
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
		next.val = val // 已存在则更新
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

// Delete 删除 key
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

	s.Insert(3, 99) // 更新
	v, _ := s.Search(3)
	fmt.Println("after update, 3 =", v)

	fmt.Println("delete 2:", s.Delete(2))
	_, ok := s.Search(2)
	fmt.Println("2 exists:", ok)
}
```

运行输出：

```text
1:10 2:20 3:30 4:40 5:50 
after update, 3 = 99
delete 2: true
2 exists: false
```

### 复杂度分析

- **查找/插入/删除**: 平均 $O(\log n)$，最坏 $O(n)$（概率极低）。
- **空间**: 期望 $O(n)$（每层期望节点数折半）。

### 总结

跳表用"空间 + 随机化"换取了接近平衡树的性能，实现却简单得多，且天然支持有序遍历与范围查询，是链表与平衡树之间的经典折中方案。
