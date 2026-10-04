### 平行堆排序（Parallel Heap Sort）

平行堆排序（Parallel Heap Sort）是一种利用多线程或多处理器来加速传统堆排序算法的排序方法。传统的堆排序是一种不稳定的内存排序算法，其时间复杂度为 \(O(n \log n)\)。平行堆排序的目标是通过并行化堆的构建和调整操作来提高排序的效率，特别是在处理大规模数据时。

### 算法概述

平行堆排序把传统堆排序里最花时间的两步（建堆和调整）放到多个线程上并行做，目标是缩短大规模数据的实际执行时间，渐进复杂度不变。

### 算法步骤

1. **并行构建堆**:
   - 将数据分成若干个块。
   - 为每个块并行构建局部堆。

2. **合并堆**:
   - 将每个块的局部堆合并成一个全局堆。
   - 使用分治策略来平行化堆的合并操作。

3. **平行排序**:
   - 从全局堆中逐步提取最大元素，并通过平行化的堆调整操作维护堆的性质。

### 代码示例（Go语言实现）

Go 版实现，用 goroutine 并行建堆和调整：

```go
package main

import (
    "fmt"
    "sync"
)

// 堆调整函数：把以 i 为根的子树调整成大顶堆（只会访问 i 的子树）
func heapify(arr []int, n, i int) {
    largest := i
    left := 2*i + 1
    right := 2*i + 2

    if left < n && arr[left] > arr[largest] {
        largest = left
    }

    if right < n && arr[right] > arr[largest] {
        largest = right
    }

    if largest != i {
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
    }
}

// 平行构建堆：自底向上按层并行调整。
// 同一层节点的子树互不重叠，同层并行调整不会产生数据竞争；
// 深层调整完成后浅层才能开始，保证被调整的子树已是合法的堆。
func parallelBuildHeap(arr []int) {
    n := len(arr)
    if n < 2 {
        return
    }

    // 找到最深的"拥有孩子节点"的层号
    level := 0
    for 2*(1<<(level+1)) <= n {
        level++
    }

    var wg sync.WaitGroup
    for ; level >= 0; level-- {
        lo := 1<<level - 1     // 该层第一个节点下标
        hi := 1<<(level+1) - 2 // 该层最后一个节点下标
        if hi > n-1 {
            hi = n - 1
        }
        for i := hi; i >= lo; i-- {
            if i > n/2-1 { // 叶子节点无需调整
                continue
            }
            wg.Add(1)
            go func(i int) {
                defer wg.Done()
                heapify(arr, n, i)
            }(i)
        }
        wg.Wait() // 等待本层全部完成后再调整上一层
    }
}

// 平行排序
func parallelHeapSort(arr []int) {
    parallelBuildHeap(arr)

    for i := len(arr) - 1; i > 0; i-- {
        arr[0], arr[i] = arr[i], arr[0]
        var wg sync.WaitGroup
        wg.Add(1)
        go func() {
            defer wg.Done()
            heapify(arr[:i], i, 0)
        }()
        wg.Wait()
    }
}

func main() {
    arr := []int{3, 6, 1, 5, 2, 4}
    parallelHeapSort(arr)
    fmt.Println("Sorted array:", arr)
}
```

### 复杂度分析

- **时间复杂度**: $O(n \log n)$，最坏、平均、最好一致，与传统堆排序相同；并行化减少的是实际执行时间。
- **空间复杂度**: $O(n)$（额外空间用来存放堆）。

### 稳定性

平行堆排序不是稳定的排序算法。由于堆排序的性质，元素的相对顺序可能会在排序过程中发生变化。

### 总结

平行堆排序的时间复杂度仍是 $O(n \log n)$，并行化改的是实际执行时间。它是不稳定的排序，价值在大规模数据上。