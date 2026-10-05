### 互斥锁（Mutual Lock）

互斥锁（mutual exclusion lock）是保证互斥访问的具体实现。在 Go 语言中对应 `sync.Mutex`，它只有两个方法：

- `Lock()`：获取锁。如果锁已被持有，调用方阻塞，直到锁可用。
- `Unlock()`：释放锁。释放一把未被持有的锁会直接 panic（`sync: unlock of unlocked mutex`）。

除阻塞式的 `Lock` 之外，Go 1.18 起还提供了非阻塞的 `TryLock()`：尝试获取锁，成功返回 `true`，锁被占用则立即返回 `false`，不会等待。

### 基本用法

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
		mu.Lock()
		counter++
		mu.Unlock()
	}
}

func main() {
	var wg sync.WaitGroup

	for i := 0; i < 10; i++ {
		wg.Add(1)
		go increment(&wg)
	}

	wg.Wait()
	fmt.Println("Final Counter:", counter)
}
```

### 用 TryLock 实现非阻塞获取

某些场景下，拿不到锁时更适合先去做别的事情，而不是干等。这时可以用 `TryLock`：

```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	var mu sync.Mutex

	mu.Lock() // 先持有锁，模拟锁被占用

	if mu.TryLock() {
		fmt.Println("获取到锁")
		mu.Unlock()
	} else {
		fmt.Println("锁被占用，先去做别的事")
	}

	mu.Unlock()
}
```

输出：

```
锁被占用，先去做别的事
```

### 使用规范

1. **加锁与解锁必须成对出现**：重复 `Unlock` 或解锁未加锁的锁都会 panic。分支多的函数建议写法固定为：

   ```go
   var mu sync.Mutex

   mu.Lock()
   defer mu.Unlock()
   ```

2. **不要重复加锁**：`sync.Mutex` 不可重入，同一个 Goroutine 两次 `Lock()` 会永久阻塞。

3. **不要拷贝锁**：互斥锁通过内部状态实现互斥，按值拷贝后各副本互不相干。锁应作为指针在函数间传递，包含锁的结构体也不要按值传递。下面的代码会被 `go vet` 检查出来：

   ```go
   type Counter struct {
       mu sync.Mutex
       n  int
   }

   // 错误：按值接收者会拷贝锁
   // func (c Counter) BadInc() { c.mu.Lock(); c.n++; c.mu.Unlock() }

   // 正确：使用指针接收者
   func (c *Counter) Inc() {
       c.mu.Lock()
       defer c.mu.Unlock()
       c.n++
   }
   ```

4. **保持锁的持有时间尽量短**：临界区只放必要的共享数据访问，I/O、耗时计算应移到锁外。

### 小结

`sync.Mutex` 是 Go 中实现互斥的基础工具：`Lock`/`Unlock` 成对使用，配合 `defer` 保证释放；拿不到锁就继续执行的场景用 `TryLock`；同时注意锁不可重入、不可拷贝这两条语言层面的约定，能避开互斥锁相关的常见 bug。
