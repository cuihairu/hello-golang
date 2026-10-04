### 位图排序（Bitmap Sort）

**位图排序**（Bitmap Sort）用一个布尔数组按值域标记哪些整数出现过，标记完成后再按顺序把 `true` 的位置收集起来，即为有序结果。它只适用于范围有限且已知的整数值。

### 算法概述

1. **确定范围**: 例如待排序的数据是0到1000之间的整数，位图的大小就是1001位。

2. **初始化位图**: 创建一个长度等于数据范围的布尔数组，所有位初始设置为 `false`。

3. **标记数据**: 遍历待排序的数据，将每个数据值在位图中对应的位置标记为 `true`。

4. **生成排序结果**: 再遍历一遍位图，把标记为 `true` 的位置对应的值收集起来。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// 位图排序函数
func bitmapSort(arr []int, maxValue int) []int {
    // 创建位图，长度为maxValue+1，初始化为false
    bitmap := make([]bool, maxValue+1)

    // 标记数据
    for _, value := range arr {
        if value >= 0 && value <= maxValue {
            bitmap[value] = true
        }
    }

    // 生成排序结果
    var sortedArr []int
    for i, present := range bitmap {
        if present {
            sortedArr = append(sortedArr, i)
        }
    }

    return sortedArr
}

func main() {
    arr := []int{3, 7, 1, 8, 5, 3, 0, 9}
    maxValue := 9 // 设定数据范围的最大值
    sortedArr := bitmapSort(arr, maxValue)
    fmt.Println("Sorted array:", sortedArr)
}
```

### 复杂度分析

- **时间复杂度**:
  - **标记数据**: $O(n)$，其中 $n$ 是待排序数据的数量。
  - **生成排序结果**: $O(m)$，其中 $m$ 是数据范围的大小（即位图的大小）。
  - 总体时间复杂度为 $O(n + m)$，其中 $n$ 是待排序数据的数量，$m$ 是数据范围的大小。

- **空间复杂度**: $O(m)$，其中 $m$ 是数据范围的大小，用于存储位图。

### 优缺点

- **优点**:
  - 时间复杂度 $O(n + m)$，实现只有标记和收集两步。
  - 不比较任何两个元素，没有比较排序的 $O(n \log n)$ 开销。

- **缺点**:
  - 空间复杂度与数据范围大小成正比，数据范围非常大时位图会占掉大量内存。
  - 不适用于数据范围非常大的情况（如大数据集或非整数数据）。

### 应用场景

位图排序适用于以下情况：
- 数据值的范围较小且已知，比如 0 到 1000 的整数。
- 数据量大但值域有限的整数排序（它是计数排序的一种变体）。

### 总结

位图排序的时间是 $O(n + m)$、空间是 $O(m)$，这里的 $m$ 是值域大小而不是数据量：0 到 1000 的数据占 1001 个位置，值域拉到几亿就要几亿个位置，所以它只在值域小且已知时划算。