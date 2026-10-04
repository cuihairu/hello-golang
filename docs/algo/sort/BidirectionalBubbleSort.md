## 双向冒泡排序（Cocktail Shaker Sort）

双向冒泡排序（Cocktail Shaker Sort），也称为鸡尾酒排序，是冒泡排序的一种改进版本。它的主要区别在于排序过程是双向的，每一趟排序包括从左到右和从右到左两个方向。这样可以在一定程度上减少排序的趟数。

### 算法步骤

1. 从左到右进行一次冒泡排序，将最大的元素移到数组末尾。
2. 从右到左进行一次冒泡排序，将最小的元素移到数组开头。
3. 重复以上过程，直到整个数组有序。

### 代码示例（Go语言实现）

```go
package main

import (
	"fmt"
)

func cocktailShakerSort(arr []int) {
	n := len(arr)
	for {
		swapped := false
		
		// 从左到右冒泡
		for i := 0; i < n-1; i++ {
			if arr[i] > arr[i+1] {
				arr[i], arr[i+1] = arr[i+1], arr[i]
				swapped = true
			}
		}

		// 如果没有交换，说明已经有序
		if !swapped {
			break
		}

		swapped = false

		// 从右到左冒泡
		for i := n - 1; i > 0; i-- {
			if arr[i] < arr[i-1] {
				arr[i], arr[i-1] = arr[i-1], arr[i]
				swapped = true
			}
		}

		// 如果没有交换，说明已经有序
		if !swapped {
			break
		}
	}
}

func main() {
	arr := []int{5, 1, 4, 2, 8, 0, 2}
	fmt.Println("Original array:", arr)
	cocktailShakerSort(arr)
	fmt.Println("Sorted array:", arr)
}
```

### 复杂度分析

- **时间复杂度**:
  - 最坏情况: $O(n^2)$
  - 平均情况: $O(n^2)$
  - 最好情况: $O(n)$（当数组已经有序时）

- **空间复杂度**: $O(1)$

### 稳定性
双向冒泡排序是稳定的排序算法，因为相等的元素不会被交换顺序。

### 总结

每趟排序同时从两头往中间冒泡，最大和最小元素各走一端，排序趟数比普通冒泡少。在某些情况下它比普通冒泡更高效，尤其是对近乎有序的数组。