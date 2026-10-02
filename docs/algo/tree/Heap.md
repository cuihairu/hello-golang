# 堆

堆（Heap）是一棵完全二叉树，同时满足堆序性质：最小堆中每个节点都小于等于它的孩子，最大堆中每个节点都大于等于它的孩子。因此堆顶永远是全堆最小（大）的元素，插入、删除、取堆顶都是 $O(\log n)$，堆是优先队列的标准实现。

### 核心性质

1. **结构性**: 完全二叉树，可用数组紧凑存储，无空洞。
2. **堆序性**: 只约束"父与子"的大小关系，兄弟之间无序、左右子树之间无序。
3. **基本操作**:
   - **Push**: 追加到末尾后**上浮**（与父节点比较交换）。
   - **Pop**: 取出堆顶，末尾元素补到堆顶后**下沉**（与较小/较大的孩子交换）。
   - **Peek**: 直接读堆顶，$O(1)$。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// MinHeap 最小堆
type MinHeap struct {
	data []int
}

// Push 入堆并上浮
func (h *MinHeap) Push(v int) {
	h.data = append(h.data, v)
	h.up(len(h.data) - 1)
}

// Pop 弹出堆顶（最小值）
func (h *MinHeap) Pop() (int, bool) {
	if len(h.data) == 0 {
		return 0, false
	}
	top := h.data[0]
	last := len(h.data) - 1
	h.data[0] = h.data[last]
	h.data = h.data[:last]
	if last > 0 {
		h.down(0)
	}
	return top, true
}

// Peek 查看堆顶
func (h *MinHeap) Peek() (int, bool) {
	if len(h.data) == 0 {
		return 0, false
	}
	return h.data[0], true
}

// Len 堆中元素个数
func (h *MinHeap) Len() int { return len(h.data) }

// up 让下标 i 的元素上浮
func (h *MinHeap) up(i int) {
	for i > 0 {
		parent := (i - 1) / 2
		if h.data[i] >= h.data[parent] {
			break
		}
		h.data[i], h.data[parent] = h.data[parent], h.data[i]
		i = parent
	}
}

// down 让下标 i 的元素下沉
func (h *MinHeap) down(i int) {
	n := len(h.data)
	for {
		left, right := 2*i+1, 2*i+2
		smallest := i
		if left < n && h.data[left] < h.data[smallest] {
			smallest = left
		}
		if right < n && h.data[right] < h.data[smallest] {
			smallest = right
		}
		if smallest == i {
			return
		}
		h.data[i], h.data[smallest] = h.data[smallest], h.data[i]
		i = smallest
	}
}

func main() {
	h := &MinHeap{}
	for _, v := range []int{5, 3, 8, 1, 9} {
		h.Push(v)
	}
	if v, ok := h.Peek(); ok {
		fmt.Println("peek:", v)
	}
	for h.Len() > 0 {
		v, _ := h.Pop()
		fmt.Println("pop:", v)
	}
}
```

运行输出：

```text
peek: 1
pop: 1
pop: 3
pop: 5
pop: 8
pop: 9
```

### 复杂度分析

- **Push / Pop**: $O(\log n)$，路径长度即树高。
- **Peek**: $O(1)$。
- **建堆（自底向下沉）**: $O(n)$，优于逐个 Push 的 $O(n \log n)$。
- **空间**: $O(n)$。

### 应用场景

- 优先队列、任务调度（Go 标准库提供 `container/heap`）。
- 堆排序、Top-K 问题、多路归并、Dijkstra 最短路。

### 总结

堆用"完全二叉树 + 父子有序"两组约束换来了快速的极值访问，是介于"完全无序的数组"与"完全有序的 BST"之间的折中。掌握上浮与下沉两个基本动作，就掌握了堆的全部操作。
