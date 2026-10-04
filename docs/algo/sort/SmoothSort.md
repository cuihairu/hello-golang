**平滑排序（Smoothsort）**

平滑排序（Smoothsort）是一种比较排序算法，由 Edsger Dijkstra 在 1981 年提出。它是堆排序的变体：最坏情况同样是 $O(n \log n)$，但遇到已经部分有序的数据时更快，许多情况下耗时低于普通堆排序。名字里的 smooth（平滑）指的就是这种随有序程度变化的耗时曲线。

### 1. 算法概念

普通堆排序不管数据长什么样都做满一遍堆化，平滑排序则让堆操作的次数跟数据的有序程度挂钩：越接近有序，要做的调整越少，最好情形能到 $O(n)$。

### 2. 算法步骤

1. **构建平滑堆**:
   - 初始化一个空的平滑堆，并将元素逐个插入堆中。

2. **堆化和调整**:
   - 通过堆化操作确保堆的结构，维护堆的性质。
   - 在插入新元素时，调整堆结构，保证平滑堆的性质。

3. **排序**:
   - 使用堆排序的基本方法进行排序，通过反复调整堆结构，提取最大元素，并将其放到数组的末尾。

### 3. 时间复杂度和空间复杂度

- **时间复杂度**:
  - **最坏情况**: $O(n \log n)$，在最坏情况下，平滑排序的时间复杂度与堆排序相同。
  - **最佳情况**: $O(n)$，在特定情况下，平滑排序可以达到线性时间复杂度。
  - **平均情况**: $O(n \log n)$，平滑排序在大多数情况下提供良好的平均性能。

- **空间复杂度**:
  - $O(1)$，平滑排序是原地排序，不需要额外的空间来存储临时数据。

### 4. 代码示例

```go
package main

import "fmt"

// 平滑堆结构体
type SmoothHeap struct {
    arr []int
    size int
}

// 插入到平滑堆中
func (sh *SmoothHeap) insert(value int) {
    sh.arr = append(sh.arr, value)
    sh.size++
    sh.heapifyUp(sh.size - 1)
}

// 堆化向上
func (sh *SmoothHeap) heapifyUp(index int) {
    parent := (index - 1) / 2
    for index > 0 && sh.arr[index] > sh.arr[parent] {
        sh.arr[index], sh.arr[parent] = sh.arr[parent], sh.arr[index]
        index = parent
        parent = (index - 1) / 2
    }
}

// 构建平滑堆
func buildSmoothHeap(arr []int) *SmoothHeap {
    sh := &SmoothHeap{}
    for _, value := range arr {
        sh.insert(value)
    }
    return sh
}

// 堆化向下
func (sh *SmoothHeap) heapifyDown(index int) {
    left := 2*index + 1
    right := 2*index + 2
    largest := index

    if left < sh.size && sh.arr[left] > sh.arr[largest] {
        largest = left
    }
    if right < sh.size && sh.arr[right] > sh.arr[largest] {
        largest = right
    }
    if largest != index {
        sh.arr[index], sh.arr[largest] = sh.arr[largest], sh.arr[index]
        sh.heapifyDown(largest)
    }
}

// 提取最大值
func (sh *SmoothHeap) extractMax() int {
    if sh.size == 0 {
        panic("Heap is empty")
    }
    max := sh.arr[0]
    sh.arr[0] = sh.arr[sh.size-1]
    sh.size--
    sh.arr = sh.arr[:sh.size]
    sh.heapifyDown(0)
    return max
}

// 平滑排序
func smoothSort(arr []int) []int {
    sh := buildSmoothHeap(arr)
    for i := len(arr) - 1; i >= 0; i-- {
        arr[i] = sh.extractMax()
    }
    return arr
}

func main() {
    arr := []int{8, 3, 5, 1, 7, 6, 4, 2}
    fmt.Println("Original array:", arr)
    sorted := smoothSort(arr)
    fmt.Println("Sorted array:", sorted)
}
```

### 5. 优缺点

平滑排序保住了堆排序的底线——最坏 $O(n \log n)$、原地 $O(1)$ 空间——同时在数据部分有序时更快。要付出的是实现成本：相比堆排序，它的堆结构维护细节多得多。

### 总结

平滑排序是堆排序在部分有序数据上的改良版：最坏 $O(n \log n)$，最好 $O(n)$，空间 $O(1)$。数据越接近有序，它相对普通堆排序省下的时间越多；数据完全随机时，两者差别不大。