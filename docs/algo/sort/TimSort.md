### 蒂姆排序（Timsort）

蒂姆排序（Timsort）由 Tim Peters 在 2002 年为 Python 的排序库设计，先用插入排序把数据切成有序小块，再用归并把这些小块合成整体有序。Python 和 Java 的 `Arrays.sort()` 用的都是它。

#### 1. 蒂姆排序的基本概念

蒂姆排序的做法：
1. **分块（Run）**: 将待排序的数据划分为若干个有序的块（称为 "run"）。
2. **使用插入排序**: 对每个小块（run）内部的数据进行插入排序，确保每个块是有序的。
3. **归并排序**: 使用归并排序将这些有序的块合并成一个整体有序的数据。

#### 2. 蒂姆排序的算法步骤

按代码走一遍，分三步：

1. **分块（Run）**:
   - 把待排序数据分成若干块，块的大小由参数定，通常在 32 到 64 之间。

2. **使用插入排序**:
   - 逐块做插入排序。块小，插入排序正合适，还能吃进数据里已有的顺序。

3. **归并排序**:
   - 使用归并排序将有序的块合并成一个整体有序的数据。归并排序的过程通过一个优先队列（如最小堆）来高效地进行合并操作。

#### 3. 蒂姆排序的时间复杂度和空间复杂度

- **时间复杂度**: 最坏、最佳、平均三种情况都是 $O(n \log n)$，与归并排序一致。

- **空间复杂度**: $O(n)$，归并要额外的临时数组。

#### 4. 蒂姆排序的代码示例

下面是 Go 实现的简化版，块大小取 32：

```go
package main

import (
    "fmt"
    "math"
)

// 插入排序
func insertionSort(arr []int, left, right int) {
    for i := left + 1; i <= right; i++ {
        key := arr[i]
        j := i - 1
        for j >= left && arr[j] > key {
            arr[j+1] = arr[j]
            j--
        }
        arr[j+1] = key
    }
}

// 合并函数
func merge(arr []int, l, m, r int) {
    n1 := m - l + 1
    n2 := r - m

    // 创建临时数组
    L := make([]int, n1)
    R := make([]int, n2)

    // 复制数据到临时数组
    copy(L, arr[l:l+n1])
    copy(R, arr[m+1:m+1+n2])

    // 合并临时数组
    i, j, k := 0, 0, l
    for i < n1 && j < n2 {
        if L[i] <= R[j] {
            arr[k] = L[i]
            i++
        } else {
            arr[k] = R[j]
            j++
        }
        k++
    }

    // 复制剩余元素
    for i < n1 {
        arr[k] = L[i]
        i++
        k++
    }

    for j < n2 {
        arr[k] = R[j]
        j++
        k++
    }
}

// 蒂姆排序
func timSort(arr []int) {
    n := len(arr)
    run := 32 // 小块的大小
    for i := 0; i < n; i += run {
        end := int(math.Min(float64(i+run-1), float64(n-1)))
        insertionSort(arr, i, end)
    }

    size := run
    for size < n {
        for left := 0; left < n; left += 2 * size {
            mid := int(math.Min(float64(left+size-1), float64(n-1)))
            right := int(math.Min(float64(left+2*size-1), float64(n-1)))
            if mid < right {
                merge(arr, left, mid, right)
            }
        }
        size *= 2
    }
}

func main() {
    arr := []int{5, 21, 7, 23, 19, 17}
    fmt.Println("Original array:", arr)
    timSort(arr)
    fmt.Println("Sorted array:", arr)
}
```

#### 5. 蒂姆排序的优缺点

**优点**:
- 稳定排序，相同元素排完后相对位置不变。
- 插入排序吃进局部有序的数据块，块内顺序越好，比较次数越少。

**缺点**:
- 分块、逐块插入、成对归并三段逻辑都要处理，实现比简单排序算法长。
- 归并需要 $O(n)$ 额外空间。

### 总结

蒂姆排序把插入排序和归并拼在一起：块内插入，块间归并，三种时间情况都是 $O(n \log n)$，额外空间 $O(n)$。Python 和 Java 的 `Arrays.sort()` 用的就是它。