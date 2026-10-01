**分配排序（Distribution Sort）**

分配排序（Distribution Sort）是一类排序算法的统称，这些算法通过将元素分配到不同的桶或分区中，再对这些分区进行排序来实现整体排序。常见的分配排序包括桶排序（Bucket Sort）、基数排序（Radix Sort）和计数排序（Counting Sort）。

### 1. 算法概述

分配排序的核心思想是将输入数据根据某种规则分配到不同的桶或分区中，然后对每个桶或分区分别排序，最后合并所有桶或分区得到有序数据。

### 2. 常见的分配排序算法

#### 2.1 桶排序（Bucket Sort）

桶排序通过将数据分布到多个桶中，然后对每个桶分别排序，最后合并所有桶中的数据。适用于数据分布较均匀的情况。

**算法步骤**：
1. 初始化若干个空桶。
2. 遍历输入数据，将每个元素分配到对应的桶中。
3. 对每个非空桶中的数据进行排序。
4. 按顺序合并所有桶中的数据。

**时间复杂度**：
- 平均时间复杂度：$O(n + k + n \log(n/k))$，其中 $k$ 是桶的数量。
- 最坏时间复杂度：$O(n^2)$（当所有元素都分配到同一个桶中）。

**空间复杂度**：$O(n + k)$。

**代码示例（Go 语言实现）**：

```go
package main

import (
	"fmt"
	"sort"
)

func bucketSort(arr []int) {
	if len(arr) == 0 {
		return
	}

	// 找到最大值和最小值
	maxVal, minVal := arr[0], arr[0]
	for _, v := range arr {
		if v > maxVal {
			maxVal = v
		}
		if v < minVal {
			minVal = v
		}
	}

	// 桶的数量
	bucketCount := len(arr)
	buckets := make([][]int, bucketCount)

	// 数据分配到桶中
	for _, v := range arr {
		index := (v - minVal) * (bucketCount - 1) / (maxVal - minVal)
		buckets[index] = append(buckets[index], v)
	}

	// 对每个桶中的数据进行排序
	result := arr[:0]
	for _, bucket := range buckets {
		sort.Ints(bucket)
		result = append(result, bucket...)
	}
}

func main() {
	arr := []int{42, 32, 33, 52, 37, 47, 51}
	fmt.Println("Original array:", arr)
	bucketSort(arr)
	fmt.Println("Sorted array:", arr)
}
```

#### 2.2 基数排序（Radix Sort）

基数排序通过逐位比较元素的每一位（从最低位到最高位或从最高位到最低位），逐次分配到桶中，最终实现排序。适用于整数或固定长度字符串的排序。

**算法步骤**：
1. 设定一个基数（例如 10）。
2. 从最低位开始，按照每一位将数据分配到桶中。
3. 将桶中数据按顺序合并。
4. 依次处理更高位，直到所有位都处理完毕。

**时间复杂度**：$O(d \cdot (n + b))$，其中 $d$ 是位数，$b$ 是基数。

**空间复杂度**：$O(n + b)$。

**代码示例（Go 语言实现）**：

```go
package main

import (
	"fmt"
)

func countingSortByDigit(arr []int, exp int) {
	n := len(arr)
	output := make([]int, n)
	count := make([]int, 10)

	// 统计每个桶中的元素个数
	for i := 0; i < n; i++ {
		index := (arr[i] / exp) % 10
		count[index]++
	}

	// 计算每个桶的位置
	for i := 1; i < 10; i++ {
		count[i] += count[i-1]
	}

	// 构建输出数组
	for i := n - 1; i >= 0; i-- {
		index := (arr[i] / exp) % 10
		output[count[index]-1] = arr[i]
		count[index]--
	}

	// 复制输出数组到原数组
	copy(arr, output)
}

func radixSort(arr []int) {
	if len(arr) == 0 {
		return
	}

	// 找到最大值
	maxVal := arr[0]
	for _, v := range arr {
		if v > maxVal {
			maxVal = v
		}
	}

	// 从最低位开始排序
	for exp := 1; maxVal/exp > 0; exp *= 10 {
		countingSortByDigit(arr, exp)
	}
}

func main() {
	arr := []int{170, 45, 75, 90, 802, 24, 2, 66}
	fmt.Println("Original array:", arr)
	radixSort(arr)
	fmt.Println("Sorted array:", arr)
}
```

#### 2.3 计数排序（Counting Sort）

计数排序通过统计每个元素的出现次数，然后按顺序输出，从而实现排序。适用于元素范围较小的情况。

**算法步骤**：
1. 找到最大值和最小值，计算元素范围。
2. 初始化计数数组，统计每个元素的出现次数。
3. 计算累积计数。
4. 将元素按累积计数分配到输出数组中。

**时间复杂度**：\(O(n + k)\)，其中 \(k\) 是元素范围。

**空间复杂度**：\(O(n + k)\)。

**代码示例（Go 语言实现）**：

```go
package main

import (
	"fmt"
)

func countingSort(arr []int) {
	if len(arr) == 0 {
		return
	}

	// 找到最大值和最小值
	maxVal, minVal := arr[0], arr[0]
	for _, v := range arr {
		if v > maxVal {
			maxVal = v
		}
		if v < minVal {
			minVal = v
		}
	}

	// 初始化计数数组
	countRange := maxVal - minVal + 1
	count := make([]int, countRange)

	// 统计每个元素的出现次数
	for _, v := range arr {
		count[v-minVal]++
	}

	// 构建输出数组
	output := arr[:0]
	for i, c := range count {
		for c > 0 {
			output = append(output, i+minVal)
			c--
		}
	}
}

func main() {
	arr := []int{4, 2, 2, 8, 3, 3, 1}
	fmt.Println("Original array:", arr)
	countingSort(arr)
	fmt.Println("Sorted array:", arr)
}
```

### 3. 总结

分配排序通过将元素分配到不同的桶或分区中，然后对每个分区分别排序，再合并所有分区来实现整体排序。桶排序、基数排序和计数排序是三种常见的分配排序算法，各有其适用场景和特点。在选择排序算法时，需要根据数据的特性和应用场景来决定。