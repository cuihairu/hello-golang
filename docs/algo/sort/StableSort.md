### 稳定排序

稳定排序算法保持相等元素的相对顺序不变：两个元素排序前相等，排序后先后关系也不变。多字段排序依赖这一点——先按次要字段排一次，再用稳定算法按主要字段排，次要字段的顺序才留得住。

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

### 稳定排序算法的选择

- **适用场景**:
  - 当你需要对多个字段进行排序时，稳定排序能够保持先前字段排序的结果。
  - 需要处理的数据集较小或者对空间复杂度要求不高时，可以考虑使用归并排序。

- **优缺点**:
  - **优点**: 保留相等元素的相对顺序，多字段排序必须用到这一点。
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

规模小、实现简单，插入排序就够用；数据量大且对空间不敏感时选归并排序。