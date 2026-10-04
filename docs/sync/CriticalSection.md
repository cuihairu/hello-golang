### 临界区（Critical Section）

临界区是指在多线程或多进程环境中，访问和修改共享资源的代码块。为了避免数据不一致和竞态条件，必须保证在同一时间只有一个线程或进程执行临界区的代码。通常通过同步机制（如互斥锁）来保护临界区。

### Go中的临界区示例

在Go语言中，可以使用互斥锁（`sync.Mutex`）来保护临界区，确保在同一时间只有一个Goroutine可以访问和修改共享资源。看一个计数器的例子：

#### 临界区的例子

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
		mu.Lock()   // 进入临界区
		counter++
		mu.Unlock() // 离开临界区
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

在这个例子中，`increment`函数中对`counter`的访问就是临界区。通过在访问共享资源前使用`mu.Lock()`加锁，确保只有一个Goroutine可以进入临界区。访问完成后，使用`mu.Unlock()`解锁，以允许其他Goroutine进入临界区。

#### 代码解释

1. **定义互斥锁**：
    ```go
    var mu sync.Mutex
    ```

2. **进入临界区**：
    ```go
    mu.Lock()   // 进入临界区
    counter++
    mu.Unlock() // 离开临界区
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

在访问共享资源的代码块（即临界区）前后加锁，同一时刻就只有一个线程或Goroutine在临界区里，数据不一致和竞态条件由此避免。