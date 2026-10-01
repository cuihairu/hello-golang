堆排序（Heap Sort）是一种基于堆数据结构的比较排序算法。堆是一种特殊的完全二叉树，满足以下特性：

- 大顶堆（Max-Heap）：每个节点的值都大于或等于其左右孩子节点的值。
- 小顶堆（Min-Heap）：每个节点的值都小于或等于其左右孩子节点的值。

堆排序通常使用大顶堆来实现升序排序，使用小顶堆来实现降序排序。下面我们详细分析堆排序的原理和实现步骤。

### 堆排序的基本步骤

堆排序的基本步骤包括两个阶段：建堆和排序。

#### 1. 建堆

首先将数组构建成一个大顶堆。构建大顶堆的过程是从最后一个非叶子节点开始，向上逐步调整每个节点，确保每个子树都满足大顶堆的性质。

#### 2. 排序

通过不断移除堆顶元素（最大值），将其与堆的最后一个元素交换，然后对堆进行调整，恢复大顶堆的性质。重复此过程，直到所有元素都已排序。

### 堆排序的实现步骤

1. **构建初始堆**：将无序数组构建成大顶堆。
2. **调整堆**：将堆顶元素与末尾元素交换，减少堆的大小，并对堆顶进行调整，恢复堆的性质。
3. **重复步骤2**：直到堆的大小为1，排序完成。

### 具体实现

下面是堆排序的详细实现过程：

#### 辅助函数

首先定义一些辅助函数：

- `heapify`：调整堆，使其满足大顶堆的性质。
- `buildHeap`：构建初始堆。

```go
// 调整堆，使其满足大顶堆的性质
func heapify(arr []int, n, i int) {
    largest := i       // 初始化 largest 为当前节点
    l := 2*i + 1       // 左子节点索引
    r := 2*i + 2       // 右子节点索引

    // 如果左子节点存在，且大于当前节点
    if l < n && arr[l] > arr[largest] {
        largest = l
    }

    // 如果右子节点存在，且大于当前节点
    if r < n && arr[r] > arr[largest] {
        largest = r
    }

    // 如果 largest 不是当前节点
    if largest != i {
        arr[i], arr[largest] = arr[largest], arr[i]  // 交换
        heapify(arr, n, largest)                     // 递归调整子树
    }
}

// 构建初始大顶堆
func buildHeap(arr []int, n int) {
    // 从最后一个非叶子节点开始调整
    for i := n/2 - 1; i >= 0; i-- {
        heapify(arr, n, i)
    }
}
```

#### 堆排序主函数

然后实现堆排序主函数：

```go
func heapSort(arr []int) {
    n := len(arr)

    // 构建初始大顶堆
    buildHeap(arr, n)

    // 逐步将堆顶元素与末尾元素交换，并调整堆
    for i := n - 1; i > 0; i-- {
        arr[0], arr[i] = arr[i], arr[0]  // 交换堆顶和末尾元素
        heapify(arr, i, 0)               // 调整堆
    }
}
```

### 示例

下面是一个使用堆排序的示例：

```go
package main

import "fmt"

// heapify 函数调整堆
func heapify(arr []int, n, i int) {
    largest := i       // 初始化 largest 为当前节点
    l := 2*i + 1       // 左子节点索引
    r := 2*i + 2       // 右子节点索引

    // 如果左子节点存在，且大于当前节点
    if l < n && arr[l] > arr[largest] {
        largest = l
    }

    // 如果右子节点存在，且大于当前节点
    if r < n && arr[r] > arr[largest] {
        largest = r
    }

    // 如果 largest 不是当前节点
    if largest != i {
        arr[i], arr[largest] = arr[largest], arr[i]  // 交换
        heapify(arr, n, largest)                     // 递归调整子树
    }
}

// buildHeap 函数构建初始大顶堆
func buildHeap(arr []int, n int) {
    // 从最后一个非叶子节点开始调整
    for i := n/2 - 1; i >= 0; i-- {
        heapify(arr, n, i)
    }
}

// heapSort 函数实现堆排序
func heapSort(arr []int) {
    n := len(arr)

    // 构建初始大顶堆
    buildHeap(arr, n)

    // 逐步将堆顶元素与末尾元素交换，并调整堆
    for i := n - 1; i > 0; i-- {
        arr[0], arr[i] = arr[i], arr[0]  // 交换堆顶和末尾元素
        heapify(arr, i, 0)               // 调整堆
    }
}

func main() {
    arr := []int{12, 11, 13, 5, 6, 7}
    fmt.Println("原始数组：", arr)

    heapSort(arr)
    fmt.Println("排序后数组：", arr)
}
```

### 堆排序的时间复杂度和空间复杂度

堆排序的时间复杂度为 $O(n \log n)$，其中 $n$ 是待排序数组的元素个数。具体分析如下：

- 建堆的时间复杂度为 $O(n)$。
- 排序过程中，每次调整堆的时间复杂度为 $O(\log n)$，总共需要进行 $n-1$ 次调整，因此排序部分的时间复杂度为 $O(n \log n)$。

堆排序的空间复杂度为 $O(1)$，因为它只需要常数级别的额外空间来进行元素交换和堆调整操作。

堆排序是一种原地排序算法，它具有较好的时间复杂度表现，并且不依赖于输入数据的分布特性，因此在实际应用中是一种很常用的排序算法。