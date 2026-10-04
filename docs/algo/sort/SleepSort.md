## 睡眠排序（Sleep Sort）

睡眠排序（Sleep Sort）是一种靠玩梗出名的排序算法，不实用。它的基本思想是：对数组中的每个元素创建一个线程（或模拟线程），线程睡眠的时长与元素值成正比，醒来时输出该元素。于是元素按值从小到大依次输出。

排序结果依赖系统的时间延迟和线程调度，因此它只能算理论成立，实际排序任务不会用它。

### 算法步骤

1. **创建一个线程**：对数组中的每个元素，创建一个线程（或模拟线程）。
2. **线程休眠**：每个线程休眠一段时间，时间长度与元素值成正比。
3. **线程输出**：线程在醒来时输出该元素值。
4. **元素按顺序输出**：最终，线程按顺序输出所有元素。

### 代码示例（Go语言实现）

```go
package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

// 睡眠排序算法
func sleepSort(arr []int) {
	var wg sync.WaitGroup
	for _, num := range arr {
		wg.Add(1)
		go func(n int) {
			defer wg.Done()
			// 模拟睡眠时间与元素值成正比
			time.Sleep(time.Duration(n) * time.Millisecond)
			fmt.Println(n)
		}(num)
	}
	wg.Wait()
}

func main() {
	// 随机生成一些值作为示例
	rand.Seed(time.Now().UnixNano())
	arr := []int{3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5}
	fmt.Println("Sorting array using sleep sort:")
	sleepSort(arr)
}
```

### 复杂度分析

- **时间复杂度**:
  - 最坏情况: $O(n \cdot T_{\text{max}})$ 其中 $T_{\text{max}}$ 是数组中最大元素的值，表明算法的运行时间受到最大元素值的影响。

- **空间复杂度**: $O(n)$ （主要是由于需要为每个元素创建一个线程）

### 稳定性

睡眠排序是稳定的，因为线程输出的顺序与元素值的大小关系一致。

### 总结

睡眠排序依赖线程调度和时间延迟来完成排序。时间复杂度随最大元素值增长，且不同系统的调度策略不同，输出顺序也不保证一致，所以它只能用来演示思路，不能承担实际的排序任务。