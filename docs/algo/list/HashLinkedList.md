# Hash Linked List

A hash linked list is a combination of a hash table and a doubly linked list: the hash table locates nodes in $O(1)$, while the doubly linked list maintains their access order. The classic application is the LRU cache (Least Recently Used): the `map` records the mapping from key to linked list node, the list is ordered from most recently used at the head to least recently used at the tail, and when capacity is full the tail node is simply evicted.

### Structure definition

1. **map**: `key -> *entry`, giving $O(1)$ lookup.
2. **Doubly linked list**: nodes chained with `prev/next`; the head is the most recently used element and the tail is the least recently used.
3. **Dummy head / dummy tail sentinels**: simplify boundary conditions and avoid special-casing the head and tail nodes.

### Algorithm steps

1. **Get**: look up the node in the hash table, then move the node to the head of the list.
2. **Put (key exists)**: update the value and move the node to the head.
3. **Put (new key)**: if capacity is full, delete the tail node and remove it from the hash table; then insert the new node at the head.

### Code example (implemented in Go)

```go
package main

import "fmt"

// entry doubly linked list node
type entry struct {
	key, value int
	prev, next *entry
}

// LRUCache LRU cache implemented with a hash linked list
type LRUCache struct {
	cap  int
	m    map[int]*entry
	head *entry // dummy head sentinel, followed by the most recently used
	tail *entry // dummy tail sentinel, preceded by the least recently used
}

// NewLRUCache create an LRU cache with capacity
func NewLRUCache(capacity int) *LRUCache {
	h, t := &entry{}, &entry{}
	h.next, t.prev = t, h
	return &LRUCache{cap: capacity, m: make(map[int]*entry), head: h, tail: t}
}

// remove unlink a node from the list
func (c *LRUCache) remove(e *entry) {
	e.prev.next = e.next
	e.next.prev = e.prev
}

// moveToHead move a node to the head (marking it as most recently used)
func (c *LRUCache) moveToHead(e *entry) {
	c.remove(e)
	e.next = c.head.next
	e.prev = c.head
	c.head.next.prev = e
	c.head.next = e
}

// Get look up key
func (c *LRUCache) Get(key int) (int, bool) {
	e, ok := c.m[key]
	if !ok {
		return 0, false
	}
	c.moveToHead(e)
	return e.value, true
}

// Put write a key-value pair
func (c *LRUCache) Put(key, value int) {
	if e, ok := c.m[key]; ok {
		e.value = value
		c.moveToHead(e)
		return
	}
	if len(c.m) >= c.cap {
		last := c.tail.prev // least recently used
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

// keysOldestFirst return all keys from least recently used to most recently used
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
		fmt.Println("get 1:", v) // after accessing 1, 1 becomes the most recently used
	}
	c.Put(3, 3) // capacity full, evict 2 which is least recently used
	_, ok := c.Get(2)
	fmt.Println("2 exists:", ok)
	fmt.Println("order:", c.keysOldestFirst()) // [1 3]
}
```

Output:

```text
order: [1 2]
get 1: 1
2 exists: false
order: [1 3]
```

### Complexity analysis

- **Get / Put**: $O(1)$, hash lookup plus a fixed number of pointer changes.
- **Space**: $O(capacity)$.

### Use cases

- LRU caches, database buffer pools.
- Scenarios that need both "fast lookup by key" and "eviction by access order".

### Summary

The essence of the hash linked list is two complementary structures: the hash table solves the linked list's slow lookup, and the doubly linked list solves the hash table's inability to maintain order. Combined, the two can perform every LRU operation in $O(1)$.

## References

- [Linked list · Wikipedia](https://en.wikipedia.org/wiki/Linked_list)
- [Hash table · Wikipedia](https://en.wikipedia.org/wiki/Hash_table)

## Sibling pages

- [SkipList](/algo/list/SkipList.md)
- [DynamicArray](/algo/list/DynamicArray.md)
- [Queue](/algo/list/Queue.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [DynamicArray](/algo/list/DynamicArray.md)
- [Queue](/algo/list/Queue.md)
- [SinglyLinkedList](/algo/list/SinglyLinkedList.md)
- [Stack](/algo/list/Stack.md)
- [list](/algo/list/list.md)
