# 二叉堆

二叉堆（Binary Heap）是完全二叉树与堆序性质的直接产物：因为是完全二叉树，它可以原封不动地放进数组，父子关系只用下标计算——下标 `i` 的父节点是 `(i-1)/2`，孩子是 `2i+1` 与 `2i+2`。本篇用最大堆演示建堆与堆排序。

### 数组表示

1. **父节点**: `(i-1)/2`。
2. **左孩子**: `2i+1`，**右孩子**: `2i+2`。
3. **叶子节点**: 下标从 $\lfloor n/2 \rfloor$ 到 $n-1$，它们没有孩子，无需下沉。

### 算法步骤（堆排序）

1. **建堆**: 从最后一个非叶节点 $\lfloor n/2 \rfloor - 1$ 开始倒序对每个节点执行下沉，自底向上得到最大堆，耗时 $O(n)$。
2. **排序**: 堆顶（最大值）与末尾元素交换，堆规模减一，对新的堆顶下沉；重复 $n-1$ 次。
3. 结果数组即为升序序列。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// siftDown 在 arr[0..n) 内把下标 i 的元素下沉到正确位置
func siftDown(arr []int, n, i int) {
	for {
		left, right := 2*i+1, 2*i+2
		largest := i
		if left < n && arr[left] > arr[largest] {
			largest = left
		}
		if right < n && arr[right] > arr[largest] {
			largest = right
		}
		if largest == i {
			return
		}
		arr[i], arr[largest] = arr[largest], arr[i]
		i = largest
	}
}

// heapSort 原地堆排序（升序）
func heapSort(arr []int) {
	n := len(arr)
	// 自底向上建最大堆，O(n)
	for i := n/2 - 1; i >= 0; i-- {
		siftDown(arr, n, i)
	}
	// 每次把堆顶最大值换到末尾，再修复堆
	for end := n - 1; end > 0; end-- {
		arr[0], arr[end] = arr[end], arr[0]
		siftDown(arr, end, 0)
	}
}

func main() {
	arr := []int{9, 4, 7, 1, 8, 2, 6}
	fmt.Println("Original array:", arr)
	heapSort(arr)
	fmt.Println("Sorted array:", arr)

	empty := []int{}
	heapSort(empty)
	fmt.Println("Empty array:", empty)
}
```

运行输出：

```text
Original array: [9 4 7 1 8 2 6]
Sorted array: [1 2 4 6 7 8 9]
Empty array: []
```

### 复杂度分析

- **建堆**: $O(n)$。第 $h$ 层最多 $n/2^{h+1}$ 个节点，各下沉 $h$ 层，求和 $\sum h \cdot n/2^{h+1} = O(n)$。
- **排序**: $O(n \log n)$，$n-1$ 次交换各伴随一次 $O(\log n)$ 下沉。
- **空间**: $O(1)$，原地排序；**不稳定**（长距离交换会打乱相等元素的次序）。

### 总结

二叉堆展示了"结构 + 下标"的威力：完全二叉树的形态让所有指针都变成了算术，堆排序因此可以原地完成。它的不稳定与较差的缓存局部性是相比快排的短板，但 $O(n)$ 建堆与 $O(\log n)$ 的动态极值维护仍不可替代。
