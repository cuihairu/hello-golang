## 猴子排序（Bogosort）

猴子排序（Bogosort）的思路很简单：随机打乱数组，直到碰巧有序为止。它没有实用价值，一般只作为教学里的反面示例。

### 算法步骤

1. **检查数组是否有序**：遍历数组，检查数组是否按非降序排列。
2. **随机打乱数组**：如果数组未排序，则随机打乱数组。
3. **重复步骤1和2**：直到数组有序。

### 代码示例（Go语言实现）

```go
package main

import (
	"fmt"
	"math/rand"
	"time"
)

// 检查数组是否有序
func isSorted(arr []int) bool {
	for i := 0; i < len(arr)-1; i++ {
		if arr[i] > arr[i+1] {
			return false
		}
	}
	return true
}

// 随机打乱数组
func shuffle(arr []int) {
	rand.Seed(time.Now().UnixNano())
	for i := range arr {
		j := rand.Intn(i + 1)
		arr[i], arr[j] = arr[j], arr[i]
	}
}

// 猴子排序算法
func bogosort(arr []int) {
	for !isSorted(arr) {
		shuffle(arr)
	}
}

func main() {
	arr := []int{3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5}
	fmt.Println("Original array:", arr)
	bogosort(arr)
	fmt.Println("Sorted array:", arr)
}
```

### 复杂度分析

- **时间复杂度**:
  - 平均情况: $O((n+1)!)$
  - 最坏情况: 无穷大（在最坏的情况下，可能永远无法完成排序）

- **空间复杂度**: $O(1)$ （只需常数级别的额外空间）

### 稳定性

猴子排序是稳定的，因为在最终找到有序排列之前，相等的元素不会改变相对顺序。

### 总结

猴子排序的平均时间复杂度是 $O((n+1)!)$，只在元素个数很少的数组上碰运气才有机会跑完，元素一多基本等不到结果。实际工程里不要用它排任何真实数据。