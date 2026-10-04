# 哈希表

哈希表（Hash Table）是根据键（key）直接访问值（value）的数据结构。它通过哈希函数把键映射到桶数组的下标，理想情况下查找、插入、删除的平均时间复杂度都是 $O(1)$。

### 核心概念

1. **哈希函数**: 把任意键转换为桶数组下标，如 `index = hash(key) % bucketCount`。
2. **冲突**: 不同键被映射到同一个下标。常见解决方法：
   - **链地址法**: 每个桶挂一条链表，冲突元素追加到链表上。
   - **开放寻址法**: 冲突时按探测序列寻找下一个空桶（线性探测、平方探测等）。
3. **负载因子**: 元素个数 / 桶数量，负载因子过高时需要扩容（rehash）。

### Go 内置的 map

Go 的 `map` 就是一个哈希表，底层使用桶数组 + 链地址式的溢出桶，并自动扩容：

```go
m := make(map[string]int)
m["go"] = 1
if v, ok := m["go"]; ok { // v=1, ok=true
	fmt.Println(v, ok)
}
delete(m, "go")
```

### 代码示例（手写链地址法哈希表）

```go
package main

import "fmt"

// entry 键值对节点
type entry struct {
	key   string
	value int
	next  *entry
}

// HashTable 链地址法哈希表
type HashTable struct {
	buckets []*entry
	size    int
}

// NewHashTable 创建指定桶数量的哈希表
func NewHashTable(n int) *HashTable {
	return &HashTable{buckets: make([]*entry, n)}
}

// indexOf 计算键所在的桶下标
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

// Put 插入或更新键值对
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

// Get 查找键对应的值
func (h *HashTable) Get(key string) (int, bool) {
	for e := h.buckets[h.indexOf(key)]; e != nil; e = e.next {
		if e.key == key {
			return e.value, true
		}
	}
	return 0, false
}

// Delete 删除键
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
	h.Put("go", 2024) // 更新
	fmt.Println("go =", func() int { v, _ := h.Get("go"); return v }())
	fmt.Println("size =", h.size)

	fmt.Println("delete c:", h.Delete("c"))
	_, ok := h.Get("c")
	fmt.Println("c exists:", ok)
}
```

### 复杂度分析

设元素个数为 $n$，桶数量为 $m$，负载因子 $\alpha = n/m$：

- **查找/插入/删除**: 平均 $O(1)$（假设哈希均匀），最坏 $O(n)$（所有键落入同一桶）。
- **空间**: $O(n + m)$。

### 总结

哈希表用空间换时间，通过哈希函数实现"一步定位"。工程上通常直接使用 Go 内置的 `map`；理解冲突处理与扩容机制有助于写出更高效的哈希相关代码。
