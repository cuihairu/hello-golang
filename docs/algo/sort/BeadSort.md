## 班尼奥排序（BogoSort）

班尼奥排序（BogoSort）也被称为“愚蠢排序”或“猴子排序”，做法是反复随机打乱数组，直到数组恰好变成有序为止。它的平均时间复杂度是 $O((n+1)!)$，实际排序用不上，只作为教学工具演示随机化算法的极限。

### 算法步骤

1. **检查数组是否有序**：遍历数组，检查数组是否按非降序排列。
2. **随机打乱数组**：如果数组未排序，则随机打乱数组的顺序。
3. **重复步骤1和2**：继续执行，直到数组变得有序为止。

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

// 班尼奥排序算法
func bogosort(arr []int) {
	for !isSorted(arr) {
		shuffle(arr)
	}
}

func main() {
	arr := []int{38, 27, 43, 3, 9, 82, 10}
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

班尼奥排序是稳定的，因为在最终找到有序排列之前，相等的元素不会改变相对顺序。

### 总结

班尼奥排序的时间复杂度是阶乘级，平均 $O((n+1)!)$，排序时不会用它。它留着当理论工具，展示排序问题本身的难度；真要排序，选快速排序、归并排序或堆排序。