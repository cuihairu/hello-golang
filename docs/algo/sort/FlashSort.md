**闪排序（Flashsort）**

闪排序（Flashsort）是一种分布式排序算法，适用于数据分布较均匀的情况。它的基本思想是通过将数据分布到预定义的桶中，然后对每个桶分别排序，从而达到全局有序的效果。闪排序在特定情况下可以达到线性时间复杂度。

### 1. 算法概念

闪排序的核心思想是将数据分配到若干个类别中，每个类别对应一个桶，桶中的数据局部排序后，再将所有桶合并。

### 2. 算法步骤

1. **类别划分**：确定数据的最大值和最小值，然后将数据分配到预定义的类别中。
2. **分配数据**：遍历数据，根据类别划分规则将数据分配到相应的桶中。
3. **局部排序**：对每个桶中的数据进行局部排序（例如，使用插入排序）。
4. **合并桶**：将所有桶中的数据合并，得到最终的有序数组。

### 3. 时间复杂度和空间复杂度

- **时间复杂度**：
  - 最优情况：$O(n)$，在数据均匀分布且分类合理的情况下，闪排序可以达到线性时间复杂度。
  - 最坏情况：$O(n^2)$，在数据分布极不均匀时，时间复杂度退化为平方级。

- **空间复杂度**：
  - $O(n)$，需要额外的空间来存储桶和类别信息。

### 4. 代码示例

```go
package main

import "fmt"

// 闪排序函数
func flashSort(arr []int) {
	n := len(arr)
	if n <= 1 {
		return
	}

	// 找到最小值和最大值
	minVal, maxIdx := arr[0], 0
	for i := 1; i < n; i++ {
		if arr[i] < minVal {
			minVal = arr[i]
		}
		if arr[i] > arr[maxIdx] {
			maxIdx = i
		}
	}
	if minVal == arr[maxIdx] { // 所有元素相等，无需排序
		return
	}

	// 计算类别数量
	m := int(0.43 * float64(n))
	if m < 2 {
		m = 2
	}

	// 初始化类别计数数组
	L := make([]int, m)
	c := float64(m-1) / float64(arr[maxIdx]-minVal)

	// 统计每个类别的数量
	for i := 0; i < n; i++ {
		k := int(c * float64(arr[i]-minVal))
		L[k]++
	}

	// 累计类别计数，L[k] 变为第 k 类的右边界（不包含）
	for i := 1; i < m; i++ {
		L[i] += L[i-1]
	}

	// 把最大值换到数组开头，作为置换循环的起点
	arr[maxIdx], arr[0] = arr[0], arr[maxIdx]

	// 循环置换：把每个元素移动到它所属类别的边界位置上
	count := 0
	j := 0
	k := m - 1
	for count < n-1 {
		for j > L[k]-1 { // 找到尚未就位的位置 j
			k--
		}
		flash := arr[j] // 取出该位置元素，送回它所属的类别
		for j != L[k] {
			k = int(c * float64(flash-minVal))
			arr[L[k]-1], flash = flash, arr[L[k]-1]
			L[k]--
			count++
		}
	}

	// 各类别内部已基本有序，最后做一次插入排序收尾
	insertionSort(arr)
}

// 插入排序函数
func insertionSort(arr []int) {
	n := len(arr)
	for i := 1; i < n; i++ {
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
	arr := []int{24, 8, 42, 75, 29, 77, 38, 57}
	fmt.Println("Original array:", arr)
	flashSort(arr)
	fmt.Println("Sorted array:", arr)
}
```

### 5. 优缺点

数据分布均匀、类别划分合理时，闪排序能做到 $O(n)$，这是它对大规模数据的吸引力所在。反过来，数据一旦分布极不均匀就退化到 $O(n^2)$，加上要维护桶和类别计数数组、还要写置换循环，实现比插入排序这类简单算法复杂不少。

### 总结

闪排序先按值域把数据分进若干类别，类别内基本有序后再用插入排序收尾。分布均匀时是 $O(n)$，最坏 $O(n^2)$，额外空间 $O(n)$。选不选它，取决于手上数据的分布是否够均匀。