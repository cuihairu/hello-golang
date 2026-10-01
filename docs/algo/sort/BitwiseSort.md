比特位排序（Bitwise Sort）是一种利用位操作进行排序的方法，特别适用于整数排序。比特位排序有几种不同的实现方式，最常见的有基数排序（Radix Sort）和二进制快速排序（Binary Quick Sort）。下面我们详细讲解这两种排序方法。

### 基数排序（Radix Sort）

基数排序是非比较排序的一种，通过逐位（或逐字符）处理数字（或字符串）来排序。它可以是 LSD（Least Significant Digit）从低位到高位处理，也可以是 MSD（Most Significant Digit）从高位到低位处理。我们将介绍 LSD 基数排序。

#### 基数排序的步骤

1. **确定排序的位数**：找到最大元素，确定需要处理的位数。
2. **逐位处理**：从最低有效位（LSD）到最高有效位（MSD），对每一位进行计数排序。

#### 基数排序的实现

假设我们要排序一组非负整数，且每个整数最多有 `d` 位。

```go
package main

import "fmt"

// 获取数组中最大元素的位数
func getMax(arr []int) int {
    max := arr[0]
    for _, num := range arr {
        if num > max {
            max = num
        }
    }
    return max
}

// 计数排序，按位进行
func countSort(arr []int, exp int) {
    n := len(arr)
    output := make([]int, n)
    count := make([]int, 10) // 十进制，范围为0-9

    // 统计每个桶中的元素数量
    for i := 0; i < n; i++ {
        index := (arr[i] / exp) % 10
        count[index]++
    }

    // 变换 count，使其包含位置信息
    for i := 1; i < 10; i++ {
        count[i] += count[i-1]
    }

    // 构建输出数组
    for i := n - 1; i >= 0; i-- {
        index := (arr[i] / exp) % 10
        output[count[index]-1] = arr[i]
        count[index]--
    }

    // 将输出数组复制回原数组
    for i := 0; i < n; i++ {
        arr[i] = output[i]
    }
}

// 基数排序
func radixSort(arr []int) {
    max := getMax(arr)
    // 按照每个位进行排序
    for exp := 1; max/exp > 0; exp *= 10 {
        countSort(arr, exp)
    }
}

func main() {
    arr := []int{170, 45, 75, 90, 802, 24, 2, 66}
    fmt.Println("原始数组：", arr)
    radixSort(arr)
    fmt.Println("排序后数组：", arr)
}
```

### 二进制快速排序（Binary Quick Sort）

二进制快速排序是基于快速排序的思想，通过逐位比较来分割数组。它适用于排序整数数组。

#### 二进制快速排序的步骤

1. **选择位**：选择当前要比较的比特位。
2. **划分数组**：根据当前位的值，将数组分成两部分，一部分为当前位为 0 的元素，另一部分为当前位为 1 的元素。
3. **递归排序**：对两部分分别进行排序，直到所有位都处理完毕。

#### 二进制快速排序的实现

```go
package main

import "fmt"

// 二进制快速排序的递归函数
func binaryQuickSort(arr []int, left, right, bit int) {
    if left >= right || bit < 0 {
        return
    }

    // 划分数组
    i, j := left, right
    for i <= j {
        for i <= right && (arr[i]&(1<<bit)) == 0 {
            i++
        }
        for j >= left && (arr[j]&(1<<bit)) != 0 {
            j--
        }
        if i <= j {
            arr[i], arr[j] = arr[j], arr[i]
            i++
            j--
        }
    }

    // 递归排序
    binaryQuickSort(arr, left, j, bit-1)
    binaryQuickSort(arr, i, right, bit-1)
}

// 二进制快速排序主函数
func binarySort(arr []int) {
    if len(arr) == 0 {
        return
    }
    maxBit := 31 // 假设32位整数
    binaryQuickSort(arr, 0, len(arr)-1, maxBit)
}

func main() {
    arr := []int{170, 45, 75, 90, 802, 24, 2, 66}
    fmt.Println("原始数组：", arr)
    binarySort(arr)
    fmt.Println("排序后数组：", arr)
}
```

### 总结

- **基数排序（Radix Sort）**：适用于长度较短的整数或字符串的排序。其时间复杂度为 $O(n \times k)$，其中 $n$ 是待排序的元素个数，$k$ 是元素的位数（或字符数）。
- **二进制快速排序（Binary Quick Sort）**：适用于整数的排序，基于快速排序的思想，利用位操作进行划分。其时间复杂度与快速排序类似，为 $O(n \log n)$。

这两种排序方法都利用了位操作的特性，在特定情况下可以显著提高排序效率。