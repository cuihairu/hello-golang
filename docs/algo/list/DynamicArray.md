# 动态数组

动态数组（Dynamic Array）在定长数组的基础上增加了"自动扩容"能力：容量不足时申请一块更大的内存并把旧元素拷贝过去，从而支持无限追加。Go 的切片（slice）底层正是这种结构。

### 结构定义

1. **data**: 底层数组，容量为 `cap`。
2. **size**: 当前元素个数，`size <= cap`。
3. **扩容策略**: 容量不足时新容量取旧容量的 2 倍，均摊后每次 `Append` 为 $O(1)$。

### 算法步骤

1. **Append**: 若 `size == cap` 先按 2 倍扩容，再在 `size` 处写入。
2. **Insert(i)**: 若满先扩容，再把 `[i, size)` 整体右移一位，写入新元素。
3. **Remove(i)**: 把 `[i+1, size)` 整体左移一位，元素变少时可以缩容以节省内存。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// DynamicArray 可自动扩容的动态数组
type DynamicArray struct {
	data []int
	size int
}

// NewDynamicArray 创建指定初始容量的动态数组
func NewDynamicArray(capacity int) *DynamicArray {
	if capacity < 1 {
		capacity = 1
	}
	return &DynamicArray{data: make([]int, capacity)}
}

// Append 追加元素，容量不足时按 2 倍扩容
func (a *DynamicArray) Append(v int) {
	if a.size == len(a.data) {
		a.resize(a.size * 2)
	}
	a.data[a.size] = v
	a.size++
}

// Insert 在下标 i 处插入 v
func (a *DynamicArray) Insert(i, v int) bool {
	if i < 0 || i > a.size {
		return false
	}
	if a.size == len(a.data) {
		a.resize(a.size * 2)
	}
	copy(a.data[i+1:a.size+1], a.data[i:a.size])
	a.data[i] = v
	a.size++
	return true
}

// Remove 删除下标 i 处的元素
func (a *DynamicArray) Remove(i int) (int, bool) {
	if i < 0 || i >= a.size {
		return 0, false
	}
	v := a.data[i]
	copy(a.data[i:a.size-1], a.data[i+1:a.size])
	a.size--
	a.data[a.size] = 0
	// 元素少于容量的 1/4 时缩容一半
	if a.size > 0 && a.size <= len(a.data)/4 {
		a.resize(len(a.data) / 2)
	}
	return v, true
}

// resize 迁移到容量为 newCap 的新数组
func (a *DynamicArray) resize(newCap int) {
	newData := make([]int, newCap)
	copy(newData, a.data[:a.size])
	a.data = newData
}

// Len 当前元素个数
func (a *DynamicArray) Len() int { return a.size }

func main() {
	a := NewDynamicArray(2)
	for i := 1; i <= 6; i++ {
		a.Append(i * 10)
	}
	fmt.Println("len:", a.Len(), "cap:", len(a.data))

	a.Insert(2, 55)
	fmt.Println("after insert:", a.data[:a.size])

	v, ok := a.Remove(0)
	fmt.Println("removed:", v, ok)
	fmt.Println("after remove:", a.data[:a.size])
}
```

运行输出：

```text
len: 6 cap: 8
after insert: [10 20 55 30 40 50 60]
removed: 10 true
after remove: [20 55 30 40 50 60]
```

### 复杂度分析

- **尾部追加**: 均摊 $O(1)$（扩容的总代价摊到每次追加上）。
- **中间插入/删除**: $O(n)$，需要移动元素。
- **按下标访问**: $O(1)$。

### 总结

动态数组保留了数组的随机访问能力，同时通过倍增扩容实现"看似无限"的追加。理解它就理解了 Go 切片 `len/cap` 的由来，以及为什么频繁 `append` 时预分配容量能减少拷贝。
