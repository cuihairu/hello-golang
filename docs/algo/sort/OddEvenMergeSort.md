### 奇偶奇归并排序（Odd-Even Merge Sort）

**奇偶奇归并排序**（Odd-Even Merge Sort, OEMS）是一种并行排序算法。它把排序写成固定的"比较-交换"网络，每一轮的比较位置与数据无关，同一轮里相距 `r` 的比较可以同时执行。

### 算法概述

奇偶奇归并排序的核心思想是把排序过程表达成一个固定的"比较-交换"网络（sorting network）：

1. **递归划分**: 把序列从中间对半分成两半，分别递归排序，使左右两半各自有序。
2. **奇偶归并**: 对已排序的两半，先递归地归并其中的偶数下标子序列和奇数下标子序列，再用一轮固定位置的比较-交换把两者交织成整体有序。
3. **补齐长度**: 经典网络只对长度为 2 的幂的序列成立，一般长度需要先用哨兵值补齐到 2 的幂，排序后再去掉哨兵。

### 算法步骤

1. **初始化**:
   - 若序列长度不是 2 的幂，先在末尾补足够多的最大值哨兵，把长度补齐到 2 的幂。

2. **递归排序**:
   - `oddEvenMergeSort` 把区间 `[lo, hi]` 从中点分成两半，先递归排序左半部分和右半部分。

3. **奇偶归并**:
   - `oddEvenMerge` 以步长 `r` 处理区间：递归地按步长 `2r` 归并偶数下标子序列和奇数下标子序列，最后对 `(i, i+r)` 这些固定位置执行比较-交换，使两半合并为整体有序。

4. **还原结果**:
   - 排序完成后去掉末尾的哨兵，即得到原数组的有序序列。

### 代码示例（Go语言实现）

```go
package main

import (
    "fmt"
)

// compareExchange 比较交换：保证 arr[i] <= arr[j]
func compareExchange(arr []int, i, j int) {
    if arr[i] > arr[j] {
        arr[i], arr[j] = arr[j], arr[i]
    }
}

// oddEvenMerge 用奇偶归并的方式合并 arr[lo..hi]（闭区间），
// 前提是 arr[lo..mid] 与 arr[mid+1..hi] 各自有序，且 hi-lo+1 是 2 的幂
func oddEvenMerge(arr []int, lo, hi, r int) {
    step := r * 2
    if step < hi-lo {
        oddEvenMerge(arr, lo, hi, step)   // 归并偶数下标子序列
        oddEvenMerge(arr, lo+r, hi, step) // 归并奇数下标子序列
        for i := lo + r; i <= hi-r; i += step {
            compareExchange(arr, i, i+r)
        }
    } else {
        compareExchange(arr, lo, lo+r)
    }
}

// 奇偶归并排序函数，对 arr[lo..hi]（闭区间）排序，要求区间长度为 2 的幂
func oddEvenMergeSort(arr []int, lo, hi int) {
    if hi-lo >= 1 {
        mid := lo + (hi-lo)/2
        oddEvenMergeSort(arr, lo, mid)
        oddEvenMergeSort(arr, mid+1, hi)
        oddEvenMerge(arr, lo, hi, 1)
    }
}

// 主排序函数：任意长度先用最大值哨兵补齐到 2 的幂，排序后取回前 n 个元素
func oddEvenMergeSortWrapper(arr []int) []int {
    n := len(arr)
    if n < 2 {
        return arr
    }
    size := 1
    for size < n {
        size *= 2
    }
    padded := make([]int, size)
    copy(padded, arr)
    for i := n; i < size; i++ {
        padded[i] = int(^uint(0) >> 1) // MaxInt 哨兵
    }
    oddEvenMergeSort(padded, 0, size-1)
    copy(arr, padded[:n])
    return arr
}

func main() {
    arr := []int{38, 27, 43, 3, 9, 82, 10}
    fmt.Println("Original array:", arr)
    oddEvenMergeSortWrapper(arr)
    fmt.Println("Sorted array:", arr)
}
```

### 复杂度分析

- **时间复杂度**:
  - 最坏情况: $O(n \log^2 n)$ （归并排序的时间复杂度乘以合并操作的复杂度）
  - 平均情况: $O(n \log^2 n)$
  - 最好情况: $O(n \log^2 n)$

- **空间复杂度**: $O(n)$ （示例实现为把长度补齐到 2 的幂而复制了一份切片；比较交换网络本身可以原地执行）

### 稳定性

奇偶奇归并排序是不稳定的：归并网络中的比较-交换发生在相距 `r` 的两个元素之间，相等元素可能被交换而改变相对顺序。它的另一个特点是整个网络与数据的初始内容无关（数据无关性），每一轮的比较位置固定，因此非常适合硬件实现和并行执行。

### 总结

奇偶奇归并排序的比较序列固定、与输入无关，这是它能并行执行、也能做成硬件电路的原因。代价是不稳定，比较次数 $O(n \log^2 n)$ 略多于最优的比较排序，单线程下不如归并排序；优势在规则的网格结构带来的并行度。