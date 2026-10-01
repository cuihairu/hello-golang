## 图书馆排序（Library Sort）

图书馆排序（Library Sort）是一种排序算法，得名于其操作类似于将新书插入到已经排序的书架上的过程。它是在插入排序的基础上进行改进，通过在数组中留出空位（gap）来减少插入过程中移动元素的次数，从而提高效率。

### 算法步骤

1. **初始化**: 创建一个比原始数组大的数组，并在数组中留出空位（gap）。
2. **插入**: 遍历原始数组，将每个元素插入到新数组的适当位置，如果遇到空位，则直接插入，否则移动元素直到找到空位。
3. **重分配空位**: 在插入过程中，如果空位不足，重新分配空位，扩展数组并重新插入元素。
4. **清理**: 完成所有插入操作后，移除空位，得到排序后的数组。

### 代码示例（Go语言实现）

```go
package main

import (
	"fmt"
	"math"
)

// 插入元素到有空位的数组
func insertWithGaps(arr []int, n int, gaps int) []int {
	newArr := make([]int, 2*n)
	for i := range newArr {
		newArr[i] = math.MaxInt64
	}

	for i := 0; i < n; i++ {
		pos := i + gaps*(i+1)
		newArr[pos] = arr[i]
	}

	return newArr
}

// 插入元素并保持数组有序
func insertElement(arr []int, gaps int, elem int) []int {
	i := 0
	for ; i < len(arr); i++ {
		if arr[i] == math.MaxInt64 || arr[i] > elem {
			break
		}
	}

	j := len(arr) - 1
	for ; j > i; j-- {
		arr[j] = arr[j-1]
	}
	arr[i] = elem

	return arr
}

// 移除空位，得到排序后的数组
func removeGaps(arr []int) []int {
	result := []int{}
	for _, val := range arr {
		if val != math.MaxInt64 {
			result = append(result, val)
		}
	}
	return result
}

// 图书馆排序算法
func librarySort(arr []int) []int {
	n := len(arr)
	if n <= 1 {
		return arr
	}

	gaps := int(math.Ceil(math.Log2(float64(n))))
	newArr := insertWithGaps(arr, n, gaps)

	for i := 1; i < n; i++ {
		newArr = insertElement(newArr, gaps, arr[i])
	}

	return removeGaps(newArr)
}

func main() {
	arr := []int{38, 27, 43, 3, 9, 82, 10}
	fmt.Println("Original array:", arr)
	sortedArr := librarySort(arr)
	fmt.Println("Sorted array:", sortedArr)
}
```

### 复杂度分析

- **时间复杂度**:
  - 最坏情况: $O(n \log n)$
  - 平均情况: $O(n \log n)$
  - 最好情况: $O(n)$

- **空间复杂度**: $O(n \log n)$

### 稳定性

图书馆排序是稳定的，因为在插入过程中相等的元素不会改变相对顺序。

### 总结

图书馆排序通过在数组中预留空位来减少插入操作中移动元素的次数，从而提高插入排序的效率。其时间复杂度与归并排序和快速排序相当，但在实际应用中可能不如这些常用的排序算法。尽管如此，图书馆排序在某些特定场景下，如需要稳定排序且初始数组近乎有序时，可能会表现得更好。