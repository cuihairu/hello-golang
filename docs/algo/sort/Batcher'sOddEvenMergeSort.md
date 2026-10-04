# Batcher 奇偶归并排序

Batcher 奇偶归并排序（Batcher's Odd–Even Merge Sort）是由 Kenneth E. Batcher 提出的比较交换网络排序算法。它把整个排序过程分解为一系列固定的比较-交换步骤，每个比较的位置都与输入数据无关，因此可以并行执行，也是硬件排序网络的常用结构。

### 算法概述

1. **递归划分**: 把长度为 2 的幂的序列从中间对半分，分别递归排序，使左右两半各自有序。
2. **奇偶归并**: 对已排序的两半，先递归地归并其中的偶数下标子序列与奇数下标子序列，再对固定位置的元素对 `(i, i+r)` 做比较-交换，使两半交织成整体有序。
3. **补齐长度**: 经典网络只对 2 的幂长度成立，一般长度先用最大值哨兵补齐到 2 的幂，排序后再去掉哨兵。

### 算法步骤

1. **初始化**: 若 `n` 不是 2 的幂，构造长度为 `size`（大于等于 `n` 的最小 2 的幂）的数组，前 `n` 位放原元素，其余放 `MaxInt` 哨兵。
2. **递归排序**: `oddEvenMergeSort(lo, hi)` 把区间从中点分开，先递归排序左半，再递归排序右半。
3. **奇偶归并**: `oddEvenMerge(lo, hi, r)` 若 `2r < hi-lo`，递归归并偶数子序列 `oddEvenMerge(lo, hi, 2r)` 与奇数子序列 `oddEvenMerge(lo+r, hi, 2r)`，然后比较 `(i, i+r)`；否则直接比较 `(lo, lo+r)`。
4. **还原**: 排序完成后丢弃哨兵，得到原数组的有序序列。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// compareExchange 比较交换：保证 arr[i] <= arr[j]
func compareExchange(arr []int, i, j int) {
	if arr[i] > arr[j] {
		arr[i], arr[j] = arr[j], arr[i]
	}
}

// oddEvenMerge 合并 arr[lo..hi]（闭区间），
// 前提是 arr[lo..mid] 与 arr[mid+1..hi] 各自有序，且 hi-lo+1 是 2 的幂
func oddEvenMerge(arr []int, lo, hi, r int) {
	step := r * 2
	if step < hi-lo {
		oddEvenMerge(arr, lo, hi, step)   // 归并偶数下标子序列
		oddEvenMerge(arr, lo+r, hi, step) // 归并奇数下标子序列
		for i := lo + r; i <= hi-r; i += step {
			compareExchange(arr, i, i+r)
		}
	} else {
		compareExchange(arr, lo, lo+r)
	}
}

// oddEvenMergeSort 对 arr[lo..hi]（闭区间）排序，要求区间长度为 2 的幂
func oddEvenMergeSort(arr []int, lo, hi int) {
	if hi-lo >= 1 {
		mid := lo + (hi-lo)/2
		oddEvenMergeSort(arr, lo, mid)
		oddEvenMergeSort(arr, mid+1, hi)
		oddEvenMerge(arr, lo, hi, 1)
	}
}

// batcherSort 对任意长度切片排序：补齐到 2 的幂后排序，再取回前 n 个元素
func batcherSort(arr []int) []int {
	n := len(arr)
	if n < 2 {
		return arr
	}
	size := 1
	for size < n {
		size *= 2
	}
	padded := make([]int, size)
	copy(padded, arr)
	for i := n; i < size; i++ {
		padded[i] = int(^uint(0) >> 1) // MaxInt 哨兵
	}
	oddEvenMergeSort(padded, 0, size-1)
	copy(arr, padded[:n])
	return arr
}

func main() {
	arr := []int{38, 27, 43, 3, 9, 82, 10}
	fmt.Println("Original array:", arr)
	batcherSort(arr)
	fmt.Println("Sorted array:", arr)

	// 2 的幂长度的典型用例
	a2 := []int{5, 2, 9, 1, 7, 3, 8, 6}
	batcherSort(a2)
	fmt.Println("Sorted array:", a2)
}
```

运行输出：

```text
Original array: [38 27 43 3 9 82 10]
Sorted array: [3 9 10 27 38 43 82]
Sorted array: [1 2 3 5 6 7 8 9]
```

### 复杂度分析

- **时间复杂度**: $O(n \log^2 n)$ 次比较（比归并排序的 $O(n \log n)$ 多出一个 $\log$ 因子）。
- **空间复杂度**: $O(n)$，示例实现需要一份补齐后的副本；比较交换网络本身可以原地执行。
- **并行性**: 所有可同时进行的比较-交换构成一个"层"，$\log^2 n$ 层天然适合并行流水线。

### 稳定性

奇偶归并网络不是稳定排序：比较-交换发生在相距 `r` 的两个元素之间，相等元素可能被交换而改变相对顺序。它换来的是数据无关的比较序列，便于硬件实现。

### 总结

Batcher 奇偶归并排序用固定模式的比较交换网络换来了数据无关的比较序列，可以并行执行，是排序网络与硬件排序的经典结构。虽然比较次数比最优的 $O(n \log n)$ 多一个对数因子，但在并行与硬件场景中仍被广泛使用。
