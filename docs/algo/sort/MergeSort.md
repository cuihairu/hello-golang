### 归并排序（Merge Sort）

归并排序是一种基于分治法的排序算法，它将一个大问题分解成多个小问题，递归地解决这些小问题，然后将结果合并成最终的有序序列。它的时间复杂度是 $O(n \log n)$，而且是稳定排序。

#### 1. 归并排序的基本概念

归并排序的过程可以分为两个主要步骤：

1. **分解**:
   - 将待排序的数组分成两半，递归地对这两半进行排序，直到每个子数组只包含一个元素。

2. **合并**:
   - 将已排序的子数组合并成一个有序的数组。合并操作将两个有序的子数组合并成一个新的有序子数组。

#### 2. 归并排序的算法步骤

1. **分解**:
   - 如果数组的长度大于 1，将其分成两个大致相等的部分。
   - 递归地对这两个部分进行归并排序。

2. **合并**:
   - 创建一个新数组来存储合并的结果。
   - 使用两个指针分别遍历两个已排序的子数组，将较小的元素插入到新数组中。
   - 当一个子数组遍历完后，将另一个子数组中剩余的元素直接复制到新数组中。

3. **返回结果**:
   - 返回合并后的有序数组。

#### 3. 归并排序的时间复杂度和空间复杂度

- **时间复杂度**:
  - **最坏情况**: $O(n \log n)$，在分解和合并阶段的时间复杂度都是 $O(\log n)$ 和 $O(n)$ 的乘积。
  - **最佳情况**: $O(n \log n)$，无论输入数据如何，时间复杂度都是 $O(n \log n)$。
  - **平均情况**: $O(n \log n)$，对随机排序的数组进行排序时，平均时间复杂度为 $O(n \log n)$。

- **空间复杂度**: $O(n)$，需要额外的存储空间来存储合并的结果。

#### 4. 归并排序的代码示例

以下是使用 Go 语言实现的归并排序算法：

```go
package main

import "fmt"

// Merge 函数将两个已排序的切片合并为一个有序切片
func Merge(left, right []int) []int {
    result := []int{}
    i, j := 0, 0

    // 合并两个有序切片
    for i < len(left) && j < len(right) {
        if left[i] < right[j] {
            result = append(result, left[i])
            i++
        } else {
            result = append(result, right[j])
            j++
        }
    }

    // 将剩余的元素添加到结果切片
    for i < len(left) {
        result = append(result, left[i])
        i++
    }
    for j < len(right) {
        result = append(result, right[j])
        j++
    }

    return result
}

// MergeSort 对整数切片进行归并排序
func MergeSort(arr []int) []int {
    if len(arr) <= 1 {
        return arr
    }

    mid := len(arr) / 2
    left := MergeSort(arr[:mid])
    right := MergeSort(arr[mid:])
    return Merge(left, right)
}

func main() {
    arr := []int{64, 34, 25, 12, 22, 11, 90}
    fmt.Println("Original array:", arr)
    sortedArray := MergeSort(arr)
    fmt.Println("Sorted array:", sortedArray)
}
```

#### 5. 归并排序的优缺点

**优点**:
- **稳定排序**: 归并排序是稳定排序算法，相同值的元素保持相对位置不变。
- **时间复杂度**: 时间复杂度为 $O(n \log n)$，对大规模数据的排序表现良好。
- **适用性广**: 可以用于链表排序以及其他数据结构的排序。

**缺点**:
- **空间复杂度**: 需要额外的存储空间来存储合并的结果，空间复杂度为 $O(n)$。
- **非原地排序**: 由于需要额外的空间，归并排序不适合空间受限的环境。

### 总结

归并排序把数组分解成更小的子数组递归排序，再合并回一个有序数组。代价是 $O(n)$ 的额外空间，换来的是稳定不受输入影响的 $O(n \log n)$，适合大规模数据以及需要保持元素相对位置的场景。