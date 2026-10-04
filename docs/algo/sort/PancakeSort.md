### 潘卡克排序（Pancake Sort）

潘卡克排序（Pancake Sort）得名于翻煎饼的类比：每一步只允许翻转数组的前 `k` 个元素，靠这个操作把乱序数组排好。这个算法不常见，主要出现在教学和算法竞赛中。

### 算法概述

核心操作是翻转前 `k` 个元素。排序过程就是用一系列这样的翻转，把当前未排序部分的最大值逐步送到位。

### 算法步骤

1. **找到最大值**: 在当前未排序部分找到最大值。
2. **将最大值翻转到数组开头**: 如果最大值不在数组开头，将其翻转到开头。
3. **将最大值翻转到正确位置**: 然后将最大值翻转到其最终位置（即当前未排序部分的末尾）。
4. **重复**: 对剩余未排序部分重复上述操作，直到所有元素排序完毕。

### 代码示例（Go语言实现）

以下是潘卡克排序的 Go 语言实现示例：

```go
package main

import "fmt"

// 翻转数组的前 k 个元素
func flip(arr []int, k int) {
    for i, j := 0, k-1; i < j; i, j = i+1, j-1 {
        arr[i], arr[j] = arr[j], arr[i]
    }
}

// 找到最大值的索引
func findMaxIndex(arr []int, n int) int {
    maxIndex := 0
    for i := 1; i < n; i++ {
        if arr[i] > arr[maxIndex] {
            maxIndex = i
        }
    }
    return maxIndex
}

// 潘卡克排序
func pancakeSort(arr []int) {
    n := len(arr)
    for size := n; size > 1; size-- {
        // 找到最大值的索引
        maxIndex := findMaxIndex(arr, size)

        // 将最大值翻转到开头
        if maxIndex != size-1 {
            if maxIndex != 0 {
                flip(arr, maxIndex+1)
            }
            flip(arr, size)
        }
    }
}

func main() {
    arr := []int{3, 6, 1, 5, 2, 4}
    pancakeSort(arr)
    fmt.Println("Sorted array:", arr)
}
```

### 复杂度分析

- **时间复杂度**:
  - 最坏情况: $O(n^2)$
  - 平均情况: $O(n^2)$
  - 最好情况: $O(n^2)$

- **空间复杂度**: $O(1)$ （原地排序，不需要额外的空间）

### 稳定性

潘卡克排序不是稳定的排序算法。由于翻转操作的性质，相等元素的相对位置可能会改变。

### 总结

潘卡克排序只用「翻转前 k 个元素」一种操作完成排序，最好、平均和最坏情况都是 $O(n^2)$，不适合大规模数据，常见于教学和竞赛题。