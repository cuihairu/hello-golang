# Hash table

A hash table is a data structure that accesses a value directly by its key. It maps each key to a bucket-array index through a hash function, so that lookup, insertion, and deletion all average $O(1)$ in the ideal case.

### Core concepts

1. **Hash function**: turns any key into a bucket-array index, e.g. `index = hash(key) % bucketCount`.
2. **Collision**: different keys map to the same index. Common resolutions:
   - **Separate chaining**: each bucket holds a linked list; colliding elements are appended to the list.
   - **Open addressing**: on collision, follow a probe sequence to find the next empty bucket (linear probing, quadratic probing, etc.).
3. **Load factor**: elements / buckets. When the load factor gets too high, the table must grow (rehash).

### Go's built-in map

Go's `map` is a hash table: it uses a bucket array plus chained overflow buckets, and grows automatically.

```go
m := make(map[string]int)
m["go"] = 1
if v, ok := m["go"]; ok { // v=1, ok=true
	fmt.Println(v, ok)
}
delete(m, "go")
```

### Code example (hand-written hash table with separate chaining)

```go
package main

import "fmt"

// entry is a key-value node
type entry struct {
	key   string
	value int
	next  *entry
}

// HashTable is a hash table using separate chaining
type HashTable struct {
	buckets []*entry
	size    int
}

// NewHashTable creates a hash table with the given number of buckets
func NewHashTable(n int) *HashTable {
	return &HashTable{buckets: make([]*entry, n)}
}

// indexOf computes the bucket index for a key
func (h *HashTable) indexOf(key string) int {
	sum := 0
	for i := 0; i < len(key); i++ {
		sum = sum*31 + int(key[i])
	}
	if sum < 0 {
		sum = -sum
	}
	return sum % len(h.buckets)
}

// Put inserts or updates a key-value pair
func (h *HashTable) Put(key string, value int) {
	idx := h.indexOf(key)
	for e := h.buckets[idx]; e != nil; e = e.next {
		if e.key == key {
			e.value = value
			return
		}
	}
	h.buckets[idx] = &entry{key: key, value: value, next: h.buckets[idx]}
	h.size++
}

// Get looks up the value for a key
func (h *HashTable) Get(key string) (int, bool) {
	for e := h.buckets[h.indexOf(key)]; e != nil; e = e.next {
		if e.key == key {
			return e.value, true
		}
	}
	return 0, false
}

// Delete removes a key
func (h *HashTable) Delete(key string) bool {
	idx := h.indexOf(key)
	var prev *entry
	for e := h.buckets[idx]; e != nil; prev, e = e, e.next {
		if e.key == key {
			if prev == nil {
				h.buckets[idx] = e.next
			} else {
				prev.next = e.next
			}
			h.size--
			return true
		}
	}
	return false
}

func main() {
	h := NewHashTable(8)
	h.Put("go", 2009)
	h.Put("c", 1972)
	h.Put("python", 1991)

	if v, ok := h.Get("go"); ok {
		fmt.Println("go =", v)
	}
	h.Put("go", 2024) // update
	fmt.Println("go =", func() int { v, _ := h.Get("go"); return v }())
	fmt.Println("size =", h.size)

	fmt.Println("delete c:", h.Delete("c"))
	_, ok := h.Get("c")
	fmt.Println("c exists:", ok)
}
```

### Complexity analysis

Let $n$ be the number of elements, $m$ the number of buckets, and the load factor $\alpha = n/m$:

- **Lookup / insertion / deletion**: average $O(1)$ (assuming a uniform hash), worst case $O(n)$ (all keys land in the same bucket).
- **Space**: $O(n + m)$.

### Summary

A hash table trades space for time, using a hash function to "land in one step." In practice you usually use Go's built-in `map` directly; understanding collision handling and growth helps you write more efficient hash-related code.

## References

- [Hash function · Wikipedia](https://en.wikipedia.org/wiki/Hash_function)
- [Hash table · Wikipedia](https://en.wikipedia.org/wiki/Hash_table)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
