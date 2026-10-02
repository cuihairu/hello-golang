# 哈希链表

哈希链表是哈希表与双向链表的结合体：哈希表负责 $O(1)$ 定位节点，双向链表负责维护节点的访问顺序。典型的应用是 LRU 缓存（Least Recently Used）：`map` 记录 key 到链表节点的映射，链表按"最近使用"从头部到尾部排列，容量满时直接淘汰尾部节点。

### 结构定义

1. **map**: `key -> *entry`，实现 $O(1)$ 查找。
2. **双向链表**: 带 `prev/next` 的节点串联，头部是最近使用的元素，尾部是最久未用的元素。
3. **伪头/伪尾哨兵**: 简化边界条件，避免对头尾节点特判。

### 算法步骤

1. **Get**: 哈希表查到节点后，把节点移到链表头部。
2. **Put（已存在）**: 更新值并把节点移到头部。
3. **Put（新 key）**: 若容量已满，删除尾部节点并从哈希表移除；再把新节点插入头部。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// entry 双向链表节点
type entry struct {
	key, value int
	prev, next *entry
}

// LRUCache 哈希链表实现的 LRU 缓存
type LRUCache struct {
	cap  int
	m    map[int]*entry
	head *entry // 伪头哨兵，之后是最近使用的
	tail *entry // 伪尾哨兵，之前是最久未用的
}

// NewLRUCache 创建容量为 capacity 的 LRU 缓存
func NewLRUCache(capacity int) *LRUCache {
	h, t := &entry{}, &entry{}
	h.next, t.prev = t, h
	return &LRUCache{cap: capacity, m: make(map[int]*entry), head: h, tail: t}
}

// remove 把节点从链表中摘除
func (c *LRUCache) remove(e *entry) {
	e.prev.next = e.next
	e.next.prev = e.prev
}

// moveToHead 把节点移到头部（表示最近使用）
func (c *LRUCache) moveToHead(e *entry) {
	c.remove(e)
	e.next = c.head.next
	e.prev = c.head
	c.head.next.prev = e
	c.head.next = e
}

// Get 查询 key
func (c *LRUCache) Get(key int) (int, bool) {
	e, ok := c.m[key]
	if !ok {
		return 0, false
	}
	c.moveToHead(e)
	return e.value, true
}

// Put 写入键值对
func (c *LRUCache) Put(key, value int) {
	if e, ok := c.m[key]; ok {
		e.value = value
		c.moveToHead(e)
		return
	}
	if len(c.m) >= c.cap {
		last := c.tail.prev // 最久未用
		c.remove(last)
		delete(c.m, last.key)
	}
	e := &entry{key: key, value: value}
	c.m[key] = e
	e.next = c.head.next
	e.prev = c.head
	c.head.next.prev = e
	c.head.next = e
}

// keysOldestFirst 按最久未用到最近使用返回所有 key
func (c *LRUCache) keysOldestFirst() []int {
	var keys []int
	for e := c.tail.prev; e != c.head; e = e.prev {
		keys = append(keys, e.key)
	}
	return keys
}

func main() {
	c := NewLRUCache(2)
	c.Put(1, 1)
	c.Put(2, 2)
	fmt.Println("order:", c.keysOldestFirst()) // [1 2]

	if v, ok := c.Get(1); ok {
		fmt.Println("get 1:", v) // 访问 1 后 1 变为最近使用
	}
	c.Put(3, 3) // 容量满，淘汰最久未用的 2
	_, ok := c.Get(2)
	fmt.Println("2 exists:", ok)
	fmt.Println("order:", c.keysOldestFirst()) // [1 3]
}
```

运行输出：

```text
order: [1 2]
get 1: 1
2 exists: false
order: [1 3]
```

### 复杂度分析

- **Get / Put**: $O(1)$，哈希定位 + 固定次数的指针修改。
- **空间**: $O(capacity)$。

### 应用场景

- LRU 缓存、数据库缓冲池。
- 需要同时"按 key 快速查找"和"按访问顺序淘汰"的场景。

### 总结

哈希链表的精髓是两种结构互补：哈希表解决了链表查找慢的问题，双向链表解决了哈希表无法维护顺序的问题，两者合在一起就能在 $O(1)$ 时间内完成 LRU 的全部操作。
