## 图书馆排序（Library Sort）

图书馆排序（Library Sort）是一种排序算法，得名于其操作类似于将新书插入到已经排序的书架上的过程。它是在插入排序的基础上进行改进，通过在数组中留出空位（gap）来减少插入过程中移动元素的次数，从而提高效率。

### 算法步骤

1. **初始化**: 创建一个比原始数组大的数组，并在数组中留出空位（gap）。
2. **插入**: 遍历原始数组，将每个元素插入到新数组的适当位置，如果遇到空位，则直接插入，否则移动元素直到找到空位。
3. **预留空位**: 新数组长度取元素个数的 2 倍，保证插入过程中始终有空位可用，无需扩容。
4. **清理**: 完成所有插入操作后，移除空位，得到排序后的数组。

### 代码示例（Go语言实现）

```go
package main

import (
	"fmt"
	"math"
)

// gapMark 表示新数组中的空位（gap）
const gapMark = math.MaxInt

// 图书馆排序算法
func librarySort(arr []int) []int {
	n := len(arr)
	if n <= 1 {
		return arr
	}

	// 1. 初始化：新数组容量约为元素个数的 2 倍，全部置为空位
	newArr := make([]int, 2*n)
	for i := range newArr {
		newArr[i] = gapMark
	}
	// 第一个元素放在中间，前后都留有空位
	newArr[n] = arr[0]

	// 2. 依次插入剩余元素
	for i := 1; i < n; i++ {
		insertWithGap(newArr, arr[i])
	}

	// 3. 清理：移除空位，得到排序结果
	return removeGaps(newArr, n)
}

// insertWithGap 在带空位的有序数组中插入 elem，保持有序
func insertWithGap(arr []int, elem int) {
	// 定位：找到第一个值 >= elem 的真实元素下标 p
	p := lowerBound(arr, elem)

	if p == len(arr) { // elem 比所有元素都大，直接放到最后一个元素之后
		e := len(arr) - 1
		for arr[e] == gapMark {
			e--
		}
		arr[e+1] = elem
		return
	}

	// 从 p 向右找最近的空位 g，把 [p, g-1] 整体右移一格，腾出位置放入 elem
	g := p
	for arr[g] != gapMark {
		g++
	}
	copy(arr[p+1:g+1], arr[p:g])
	arr[p] = elem
}

// lowerBound 在带空位的数组中查找第一个值 >= elem 的真实元素下标
func lowerBound(arr []int, elem int) int {
	lo, hi := 0, len(arr)-1
	res := len(arr)
	for lo <= hi {
		mid := (lo + hi) / 2
		if arr[mid] == gapMark {
			// mid 落在空位上：向左找最近的真实元素来判断方向
			l := mid
			for l >= lo && arr[l] == gapMark {
				l--
			}
			if l < lo {
				// [lo, mid] 全是空位，插入点只可能在右半区
				lo = mid + 1
			} else if arr[l] >= elem {
				hi = l
			} else {
				lo = mid + 1
			}
		} else if arr[mid] >= elem {
			res = mid
			hi = mid - 1
		} else {
			lo = mid + 1
		}
	}
	return res
}

// 移除空位，得到排序后的数组
func removeGaps(arr []int, n int) []int {
	result := make([]int, 0, n)
	for _, val := range arr {
		if val != gapMark {
			result = append(result, val)
		}
	}
	return result
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