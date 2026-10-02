# 臭皮匠排序

臭皮匠排序（Stooge Sort）是一个以"愚蠢"著称的递归排序算法：如果首元素大于尾元素，先交换首尾；然后把前 2/3 的部分排序，再把后 2/3 的部分排序，最后再把前 2/3 的部分排一次。名字来自"三个臭皮匠顶个诸葛亮"——它靠反复重排"三人组"来完成排序。

### 算法步骤

1. 若 `arr[lo] > arr[hi]`，交换 `arr[lo]` 与 `arr[hi]`。
2. 若当前区间长度大于 2，令 `t = (hi-lo+1)/3`（向下取整）：
   - 对前 2/3 区间 `[lo, hi-t]` 递归排序；
   - 对后 2/3 区间 `[lo+t, hi]` 递归排序；
   - 再对前 2/3 区间 `[lo, hi-t]` 递归排序。

递归的基本情形是区间长度为 1 或 2，长度为 2 时第 1 步的首尾比较即可保证有序。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// stoogeSort 对 arr[lo..hi]（闭区间）排序
func stoogeSort(arr []int, lo, hi int) {
	if lo >= hi {
		return
	}
	// 若首元素大于尾元素，先交换
	if arr[lo] > arr[hi] {
		arr[lo], arr[hi] = arr[hi], arr[lo]
	}
	if hi-lo+1 > 2 {
		t := (hi - lo + 1) / 3
		stoogeSort(arr, lo, hi-t) // 排序前 2/3
		stoogeSort(arr, lo+t, hi) // 排序后 2/3
		stoogeSort(arr, lo, hi-t) // 再次排序前 2/3
	}
}

func main() {
	arr := []int{3, 1, 4, 1, 5, 9, 2, 6}
	fmt.Println("Original array:", arr)
	stoogeSort(arr, 0, len(arr)-1)
	fmt.Println("Sorted array:", arr)

	empty := []int{}
	stoogeSort(empty, 0, len(empty)-1)
	fmt.Println("Empty array:", empty)
}
```

运行输出：

```text
Original array: [3 1 4 1 5 9 2 6]
Sorted array: [1 1 2 3 4 5 6 9]
Empty array: []
```

### 复杂度分析

设区间长度为 $n$：

- **时间复杂度**:
  - 最坏情况 $O(n^{\log_{1.5} 3}) \approx O(n^{2.708})$，递推式为 $T(n) = 3T(2n/3) + O(1)$。
  - 最好情况 $O(n \log n)$（已经有序时仍要递归，但常数极小）。
- **空间复杂度**: $O(\log n)$，递归栈深度为 $\log_{1.5} n$。
- **稳定性**: 稳定，只在比较后才决定交换，且交换仅发生在首尾位置。

### 总结

臭皮匠排序并不实用——它比冒泡排序还要慢得多——但它的递推式 $T(n)=3T(2n/3)+O(1)$ 是主定理的经典练习，常被用来演示"用最笨的办法也能把问题拆成更小的子问题"。
