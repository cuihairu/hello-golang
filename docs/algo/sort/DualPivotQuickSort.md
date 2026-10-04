**双基快速排序（Dual-Pivot Quicksort）**

双基快速排序（Dual-Pivot Quicksort）是快速排序的变种，由 Vladimir Yaroslavskiy 于 2009 年提出。相比传统的快速排序，它用两个枢轴（pivot）来分割数组，一次分割把数组切成三段。

### 1. 算法概念

双基快速排序的主要思想是使用两个枢轴将数组分成三个部分：

1. **小于第一个枢轴的元素**
2. **介于两个枢轴之间的元素**
3. **大于第二个枢轴的元素**

切成三段之后每段规模更小，递归调用的深度随之减少。

### 2. 算法步骤

步骤如下：

1. **选择两个枢轴**：从数组中选择两个枢轴 $p$ 和 $q$，并确保 $p \leq q$。
2. **分割数组**：将数组分割成三部分：
   - 小于 $p$ 的元素
   - 介于 $p$ 和 $q$ 之间的元素
   - 大于 $q$ 的元素
3. **递归排序**：对分割后的每一部分递归调用双基快速排序。

### 3. 时间复杂度和空间复杂度

- **时间复杂度**：
  - **最坏情况**：$O(n^2)$，枢轴选择不当时退化为平方级。
  - **平均情况**：$O(n \log n)$。
  - **最佳情况**：$O(n \log n)$。

- **空间复杂度**：$O(\log n)$，来自递归调用栈；排序在原数组上进行，不额外存储临时数据。

### 4. 代码示例

Go 实现：

```go
package main

import (
	"fmt"
)

// 双基快速排序的分割函数
func partition(arr []int, low, high int) (int, int) {
	if arr[low] > arr[high] {
		arr[low], arr[high] = arr[high], arr[low]
	}
	p := arr[low]
	q := arr[high]

	lt := low + 1
	gt := high - 1
	i := low + 1

	for i <= gt {
		if arr[i] < p {
			arr[i], arr[lt] = arr[lt], arr[i]
			lt++
		} else if arr[i] > q {
			arr[i], arr[gt] = arr[gt], arr[i]
			gt--
			i--
		}
		i++
	}
	lt--
	gt++

	arr[low], arr[lt] = arr[lt], arr[low]
	arr[high], arr[gt] = arr[gt], arr[high]

	return lt, gt
}

// 双基快速排序的递归函数
func dualPivotQuicksort(arr []int, low, high int) {
	if low < high {
		lp, rp := partition(arr, low, high)
		dualPivotQuicksort(arr, low, lp-1)
		dualPivotQuicksort(arr, lp+1, rp-1)
		dualPivotQuicksort(arr, rp+1, high)
	}
}

// 双基快速排序的主函数
func sort(arr []int) {
	dualPivotQuicksort(arr, 0, len(arr)-1)
}

func main() {
	arr := []int{24, 8, 42, 75, 29, 77, 38, 57}
	fmt.Println("Original array:", arr)
	sort(arr)
	fmt.Println("Sorted array:", arr)
}
```

### 5. 优缺点

**优点**：
- 两个枢轴减少了递归调用的深度，排序更快。
- 原地排序，不额外存储数据，空间复杂度 $O(\log n)$。

**缺点**：
- 实现比传统快速排序复杂。
- 枢轴选得不好时，时间复杂度会退化为 $O(n^2)$。

### 总结

双基快速排序用两个枢轴把数组分成三段，减少了递归调用的深度。它的实现比传统快速排序复杂，但在大多数情况下性能更好。