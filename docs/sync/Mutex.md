### 互斥锁（Mutex）

互斥锁是一种同步机制，用于在多线程或多进程环境中确保共享资源在同一时间只能被一个线程或进程访问。通过互斥锁，可以避免竞争条件（Race Conditions），确保数据的一致性和正确性。

### Go中的互斥锁

在Go语言中，互斥锁由标准库`sync`包提供。常用的类型是`sync.Mutex`，它有两个主要方法：

- `Lock()`: 加锁，如果锁已经被持有，调用此方法的Goroutine会阻塞，直到锁被释放。
- `Unlock()`: 解锁，释放锁，使其他阻塞的Goroutine可以获得锁。

#### 互斥锁的例子

下面是一个简单的例子，展示如何在Go中使用互斥锁来保护共享资源。

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

通过使用互斥锁，可以确保在同一时间只有一个Goroutine访问共享资源，从而避免竞争条件和数据不一致的问题。在Go语言中，使用`sync.Mutex`提供的`Lock`和`Unlock`方法，可以方便地实现对临界区的保护。