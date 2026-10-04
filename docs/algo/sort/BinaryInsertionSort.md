### 二叉插入排序（Binary Insertion Sort）

二叉插入排序（Binary Insertion Sort）用二分查找代替逐个比较来定位插入位置，找到位置这一步从 $O(n)$ 降到 $O(\log n)$。但元素该移动还得移动，整体时间复杂度仍是 $O(n^2)$，比标准插入排序省的只是比较次数。

### 算法步骤

1. **遍历数组**: 从第二个元素开始，逐个遍历数组中的元素。
2. **二分查找**: 对于当前元素，使用二分查找算法在已排序部分中找到它的插入位置。
3. **插入元素**: 将当前元素插入到正确的位置，同时将大于当前元素的元素向右移动。
4. **继续**: 重复上述步骤直到遍历完整个数组。

### 代码示例（Go语言实现）

```go
package main

import (
	"fmt"
)

// 二分查找插入位置
func binarySearch(arr []int, target int, low int, high int) int {
	for low <= high {
		mid := low + (high-low)/2
		if arr[mid] == target {
			return mid
		} else if arr[mid] < target {
			low = mid + 1
		} else {
			high = mid - 1
		}
	}
	return low
}

// 二叉插入排序函数
func binaryInsertionSort(arr []int) {
	n := len(arr)
	for i := 1; i < n; i++ {
		key := arr[i]
		j := i - 1

		// 使用二分查找确定插入位置
		insertPos := binarySearch(arr, key, 0, j)

		// 移动元素，为插入新的元素腾出空间
		for k := j; k >= insertPos; k-- {
			arr[k+1] = arr[k]
		}
		arr[insertPos] = key
	}
}

func main() {
	arr := []int{64, 34, 25, 12, 22, 11, 90}
	binaryInsertionSort(arr)
	fmt.Println("Sorted array:", arr)
}
```

### 复杂度分析

- **时间复杂度**:
  - 最坏情况: $O(n^2)$ （虽然二分查找降低了查找时间，但插入操作需要移动元素）
  - 平均情况: $O(n^2)$
  - 最好情况: $O(n \log n)$ （当数组已接近排序时）

- **空间复杂度**: $O(1)$ （原地排序，不需要额外的空间）

### 稳定性

上面示例中的二叉插入排序是不稳定的：`binarySearch` 在遇到相等的元素时会直接返回该位置，新元素被插到相等元素的前面，相等元素的相对顺序可能被改变。若需要稳定排序，应让二分查找返回"第一个大于 `target` 的位置"（即相等的元素都排在前面）。

### 总结

二叉插入排序把定位插入位置的比较次数从 $O(n)$ 降到 $O(\log n)$，移动元素的次数则和普通插入排序一样，所以整体仍是 $O(n^2)$。元素个数不多时，它比逐个比较的插入排序更快；数据量一上去，$O(n^2)$ 的移动量就成了瓶颈。