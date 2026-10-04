### 互斥锁（Mutex）

互斥锁是同步机制：同一时刻只放一个线程进入临界区，用来挡住竞争条件（Race Conditions）。

### Go中的互斥锁

在Go语言中，互斥锁由标准库`sync`包提供。常用的类型是`sync.Mutex`，它有两个主要方法：

- `Lock()`: 加锁，如果锁已经被持有，调用此方法的Goroutine会阻塞，直到锁被释放。
- `Unlock()`: 解锁，释放锁，使其他阻塞的Goroutine可以获得锁。

#### 互斥锁的例子

下面这个例子用 `sync.Mutex` 保护一个 `counter`：

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
		mu.Lock()   // 加锁，进入临界区
		counter++
		mu.Unlock() // 解锁，离开临界区
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

#### 代码解释

1. **定义互斥锁和共享变量**：
    ```go
    var (
        counter int
        mu      sync.Mutex
    )
    ```

2. **使用互斥锁保护临界区**：
    ```go
    func increment(wg *sync.WaitGroup) {
        defer wg.Done()
        for i := 0; i < 1000; i++ {
            mu.Lock()   // 加锁，进入临界区
            counter++
            mu.Unlock() // 解锁，离开临界区
        }
    }
    ```

3. **主函数**：
    ```go
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

在主函数中，启动了10个Goroutine，每个Goroutine执行`increment`函数，这些函数并发地增加`counter`的值。由于`counter`的访问被互斥锁保护，所以在所有Goroutine执行完毕后，`counter`的最终值总是正确的，即`10 * 1000 = 10000`。

### 小结

`sync.Mutex` 的 `Lock`/`Unlock` 把临界区夹住，锁被占着时，别的 goroutine 会阻塞在 `Lock` 上。上例 10 个 goroutine 各加 1000 次，`counter` 最终是 10000；去掉 `Lock`/`Unlock`，结果就不一定是这个数了。