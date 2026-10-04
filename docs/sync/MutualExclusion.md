### 互斥（Mutual Exclusion）

互斥是并发编程中最基本的同步要求：在任一时刻，最多只允许一个线程（Goroutine）进入访问共享资源的临界区。它解决的核心问题是，多个执行流同时对同一份数据进行读写时，操作的交错会导致数据损坏和竞态条件。

互斥通常通过锁机制实现：

- **进入临界区前加锁**：如果锁已被其他线程持有，当前线程阻塞等待。
- **离开临界区后解锁**：释放锁，让等待的线程有机会进入。

### Go 中的互斥

在 Go 语言中，互斥由标准库 `sync` 包的 `sync.Mutex` 提供。`Mutex` 内部通过原子操作和运行时信号量实现：加锁失败时 Goroutine 会被挂起，而不是像自旋锁那样占用 CPU 空转。

```go
package main

import (
	"fmt"
	"sync"
)

var (
	counter int
	mu      sync.Mutex
)

func increment(wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 0; i < 1000; i++ {
		mu.Lock() // 进入临界区前加锁
		counter++
		mu.Unlock() // 离开临界区后解锁
	}
}

func main() {
	var wg sync.WaitGroup

	for i := 0; i < 10; i++ {
		wg.Add(1)
		go increment(&wg)
	}

	wg.Wait()
	fmt.Println("Final Counter:", counter) // 总是 10000
}
```

如果没有 `mu.Lock()` / `mu.Unlock()`，10 个 Goroutine 并发执行 `counter++` 就会产生竞态条件，最终结果通常小于 10000；加上互斥锁之后，每次运行的结果都恒定为 10000。

### 使用注意事项

1. **临界区要尽量小**：只在真正访问共享数据的代码段持锁，不要把耗时的计算或 I/O 放进临界区，否则会显著降低并发度。
2. **保证锁一定会被释放**：对于包含分支、提前返回的代码，建议在加锁后立即用 `defer mu.Unlock()` 释放，避免某条路径忘记解锁导致死锁。
3. **`sync.Mutex` 不可重入**：同一个 Goroutine 在持有锁的情况下再次调用 `Lock()` 会永远阻塞（死锁）。这一点与 Java 的 `synchronized`、C++ 的 `std::recursive_mutex` 等可重入锁不同，需要通过拆分函数或调整加锁范围来避免。
4. **锁不要按值拷贝**：`sync.Mutex` 使用后不应被复制，否则两份副本的状态会彼此独立，失去互斥作用。`go vet` 的 copylocks 检查可以发现这类问题。
5. **加锁顺序要一致**：需要同时持有多个锁时，所有 Goroutine 按相同顺序加锁，避免互相等待形成死锁。

### 小结

互斥保证同一时刻只有一个执行流访问共享资源，是消除竞态条件最直接的手段。Go 的 `sync.Mutex` 是现成的互斥锁，配合 `defer` 解锁、保持临界区精简、避免重入和锁拷贝，就可以写出并发安全的代码。
