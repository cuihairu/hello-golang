### 稳定排序

稳定排序算法是一类保持相等元素相对顺序不变的排序算法。换句话说，如果两个元素在排序前是相等的，那么在排序后，它们的相对顺序也应保持不变。稳定排序对于那些需要保留排序稳定性的应用场景特别重要，比如对多重排序字段的排序。

### 常见稳定排序算法

1. **冒泡排序（Bubble Sort）**
   - **时间复杂度**:
     - 最坏情况: $O(n^2)$
     - 平均情况: $O(n^2)$
     - 最好情况: $O(n)$ （当数组已排序时）
   - **空间复杂度**: $O(1)$
   - **稳定性**: 稳定

2. **插入排序（Insertion Sort）**
   - **时间复杂度**:
     - 最坏情况: $O(n^2)$
     - 平均情况: $O(n^2)$
     - 最好情况: $O(n)$ （当数组已排序时）
   - **空间复杂度**: $O(1)$
   - **稳定性**: 稳定

3. **归并排序（Merge Sort）**
   - **时间复杂度**:
     - 最坏情况: $O(n \log n)$
     - 平均情况: $O(n \log n)$
     - 最好情况: $O(n \log n)$
   - **空间复杂度**: $O(n)$
   - **稳定性**: 稳定

4. **计数排序（Counting Sort）**
   - **时间复杂度**:
     - 最坏情况: $O(n + k)$ 其中 $k$ 是范围内的最大值
   - **空间复杂度**: $O(k)$
   - **稳定性**: 稳定

5. **基数排序（Radix Sort）**
   - **时间复杂度**:
     - 最坏情况: $O(n \cdot k)$ 其中 $k$ 是基数的位数
   - **空间复杂度**: $O(n + k)$
   - **稳定性**: 稳定

6. **冒泡排序（Bubble Sort）**
   - **时间复杂度**:
     - 最坏情况: $O(n^2)$
     - 平均情况: $O(n^2)$
     - 最好情况: $O(n)$ （当数组已排序时）
   - **空间复杂度**: $O(1)$
   - **稳定性**: 稳定

### 稳定排序算法的选择

- **适用场景**:
  - 当你需要对多个字段进行排序时，稳定排序能够保持先前字段排序的结果。
  - 需要处理的数据集较小或者对空间复杂度要求不高时，可以考虑使用归并排序。

- **优缺点**:
  - **优点**: 稳定排序算法保留了相等元素的相对顺序，这对于某些应用场景是非常重要的。
  - **缺点**: 有些稳定排序算法（如归并排序）可能在时间和空间复杂度上不如不稳定的排序算法（如快速排序和堆排序）。

### 代码示例（Go语言）

以下是几种稳定排序算法的 Go 实现示例：

#### 插入排序

```go
package main

import "fmt"

func insertionSort(arr []int) {
	for i := 1; i < len(arr); i++ {
		key := arr[i]
		j := i - 1
		for j >= 0 && arr[j] > key {
			arr[j+1] = arr[j]
			j--
		}
		arr[j+1] = key
	}
}

func main() {
	arr := []int{12, 11, 13, 5, 6}
	insertionSort(arr)
	fmt.Println("Sorted array:", arr)
}
```

#### 归并排序

```go
package main

import "fmt"

func mergeSort(arr []int) []int {
	if len(arr) <= 1 {
		return arr
	}

	mid := len(arr) / 2
	left := mergeSort(arr[:mid])
	right := mergeSort(arr[mid:])

	return merge(left, right)
}

func merge(left, right []int) []int {
	result := []int{}
	i, j := 0, 0
	for i < len(left) && j < len(right) {
		if left[i] <= right[j] {
			result = append(result, left[i])
			i++
		} else {
			result = append(result, right[j])
			j++
		}
	}
	for i < len(left) {
		result = append(result, left[i])
		i++
	}
	for j < len(right) {
		result = append(result, right[j])
		j++
	}
	return result
}

func main() {
	arr := []int{12, 11, 13, 5, 6}
	sorted := mergeSort(arr)
	fmt.Println("Sorted array:", sorted)
}
```

稳定排序在处理实际应用中的数据时非常重要，尤其是在需要保留排序稳定性的情况下。