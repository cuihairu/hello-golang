### 基数排序（Radix Sort）

基数排序是一种非比较排序算法，按位（或字符）把数据分组，用稳定的排序算法（如计数排序）从低位到高位逐位排，排完最高位整体就有序了。时间复杂度为 $O(n \cdot k)$，其中 $n$ 是待排序的元素个数，$k$ 是最大位数或字符数。数据量大而基数小的场景（如数字）用它合适。

#### 1. 基数排序的基本概念

基数排序的基本思想是：
1. **确定排序位数**: 找出数据中最长的位数或字符数。
2. **从最低位到最高位进行排序**: 按照从低到高的顺序，对每一位进行排序。可以使用稳定的排序算法（如计数排序）来实现。

#### 2. 基数排序的算法步骤

1. **确定排序位数**: 找到待排序数据中最长的位数或字符数。
2. **按位进行排序**: 从最低有效位（LSD，Least Significant Digit）开始，对每一位进行排序，直到最高有效位（MSD，Most Significant Digit）。
3. **使用稳定的排序算法**: 对每一位使用稳定的排序算法，如计数排序，来确保相同位的元素保持原有的相对位置。

#### 3. 基数排序的时间复杂度和空间复杂度

- **时间复杂度**: 最好、最坏、平均都是 $O(n \cdot k)$，不随输入数据的分布变化。
- **空间复杂度**: $O(n + k)$，需要额外的空间来存储排序结果和计数数组。

#### 4. 基数排序的代码示例

```go
package main

import "fmt"

// getMax 获取数组中的最大值
func getMax(arr []int) int {
    max := arr[0]
    for _, v := range arr {
        if v > max {
            max = v
        }
    }
    return max
}

// countingSort 对数组按照某个位数进行计数排序
func countingSort(arr []int, exp int) {
    n := len(arr)
    output := make([]int, n) // 输出数组
    count := make([]int, 10) // 计数数组

    // 统计每个数字出现的次数
    for i := 0; i < n; i++ {
        index := (arr[i] / exp) % 10
        count[index]++
    }

    // 累加计数数组
    for i := 1; i < 10; i++ {
        count[i] += count[i-1]
    }

    // 按位排序
    for i := n - 1; i >= 0; i-- {
        index := (arr[i] / exp) % 10
        output[count[index]-1] = arr[i]
        count[index]--
    }

    // 将排序结果复制到原数组
    for i := 0; i < n; i++ {
        arr[i] = output[i]
    }
}

// RadixSort 对整数切片进行基数排序
func RadixSort(arr []int) {
    max := getMax(arr)

    // 从最低位到最高位进行排序
    for exp := 1; max/exp > 0; exp *= 10 {
        countingSort(arr, exp)
    }
}

func main() {
    arr := []int{170, 45, 75, 90, 802, 24, 2, 66}
    fmt.Println("Original array:", arr)
    RadixSort(arr)
    fmt.Println("Sorted array:", arr)
}
```

#### 5. 基数排序的优缺点

基数排序不比较元素大小，$k$ 位的数就排 $k$ 轮，而且每一轮用的都是稳定排序，相同值的元素保持原有相对位置；整数范围有限时表现尤其好。代价有两处：一是空间，计数数组加输出数组要 $O(n + k)$；二是数据类型，它只对整数或字符有效，浮点数这类排不了。实现上也要比简单排序多处理逐位的逻辑。

### 总结

基数排序按位分组、逐位用计数排序，$n$ 个元素 $k$ 位就是 $O(n \cdot k)$，输入怎么分布都不变。稳定和轮数固定这两个特点让它适合整数、字符串这类数据；换来的是 $O(n + k)$ 的额外空间，以及排不了浮点数的限制。