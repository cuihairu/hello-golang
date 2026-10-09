Go 语言的 `goroutine` 是一种轻量级的线程实现，由运行时调度，写并发程序不用自己管线程。本节讲它的基本用法、优缺点和使用注意事项。

### 1. 基本用法

`goroutine` 是通过关键字 `go` 启动的，它会在后台运行一个函数或方法，并与其他 `goroutine` 并发执行。使用 `goroutine` 很简单，只需在函数调用前加上 `go` 关键字即可。

#### 示例代码

```go
package main

import (
    "fmt"
    "time"
)

func sayHello() {
    for i := 0; i < 5; i++ {
        fmt.Println("Hello")
        time.Sleep(time.Second)
    }
}

func sayGoodbye() {
    for i := 0; i < 5; i++ {
        fmt.Println("Goodbye")
        time.Sleep(time.Second)
    }
}

func main() {
    go sayHello() // 启动一个 goroutine
    go sayGoodbye() // 启动另一个 goroutine

    // 等待一段时间，让 goroutines 完成执行
    time.Sleep(6 * time.Second)
}
```

### 2. 优缺点

#### 优点

1. **轻量**：单个 `goroutine` 占用的内存比线程少，创建和销毁的开销也小得多。
2. **调度由运行时负责**：调度器把大量 `goroutine` 复用到少量操作系统线程上，数量随程序需要自动增减。
3. **写法简单**：函数调用前加 `go` 就启动，不需要显式管理线程的创建和销毁。

#### 缺点

1. **内存占用**：单个占用虽少，数量一多仍然消耗大量内存。
2. **调试复杂**：并发程序的调试比单线程复杂得多，竞态条件、死锁都难定位和修复。
3. **调度延迟**：高负载下，调度和上下文切换会引入延迟。

### 3. 使用注意事项

1. **确保退出**：`goroutine` 不再需要时要能退出，否则会一直占着资源，造成内存泄漏。
2. **避免数据竞争**：共享数据用 `sync.Mutex` 或 `sync.RWMutex` 之类的同步机制保护。
3. **优先用 `channel` 通信**：同步和数据传递都走 `channel`，比直接共享数据更容易保证安全。
4. **设置超时**：涉及 I/O 操作或外部资源时设置超时，避免 `goroutine` 长时间阻塞，导致程序无法正常退出。
5. **处理错误**：`goroutine` 里的错误不影响主流程，但仍要有人处理；可以用 `select` 和 `channel` 把错误传出来。

### 4. 可能遇到的问题

1. **死锁**：`channel` 等同步机制用不当会死锁，要保证每个 `channel` 都有对应的发送和接收方。
2. **资源泄漏**：`goroutine` 一直运行不退出就会泄漏，靠超时和取消机制兜住。
3. **竞态条件**：共享资源没有同步保护就会出现，用 `go test -race` 检测。
4. **调度问题**：高负载下调度和上下文切换会拖慢程序，用性能分析工具定位。

### 5. 栈与调度

goroutine 的栈初始很小（约 2KB），按需增长，上限量级是 1GB，绝大多数程序用不满，这是它比操作系统线程轻的主要原因。运行时调度器把大量 goroutine 复用到少量线程上，映射关系对使用者透明。

有一个必须记住的行为：主 goroutine 退出时，其余 goroutine 会被立即终止，不管它们跑没跑完。所以启动后台 goroutine 后，主 goroutine 要等它们，用通道或 `sync.WaitGroup` 都能实现。

### 6. 用通道等待 goroutine

```go
package main

import "fmt"

func worker(done chan bool) {
    fmt.Println("Working...")
    done <- true
}

func main() {
    done := make(chan bool, 1)
    go worker(done)
    <-done
    fmt.Println("Done")
}
```

主 goroutine 停在 `<-done`，直到 worker 发来完成信号。

### 7. 并行计算与网络服务

把数据切开，每段一个 goroutine 算，再用通道把结果汇总：

```go
package main

import (
    "fmt"
    "sync"
)

func sum(array []int, result chan<- int, wg *sync.WaitGroup) {
    defer wg.Done()
    total := 0
    for _, v := range array {
        total += v
    }
    result <- total
}

func main() {
    array := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    result := make(chan int, 2)
    var wg sync.WaitGroup

    wg.Add(2)
    go sum(array[:len(array)/2], result, &wg)
    go sum(array[len(array)/2:], result, &wg)
    wg.Wait()
    close(result)

    total := 0
    for r := range result {
        total += r
    }
    fmt.Println("Total:", total)
}
```

网络服务里 goroutine 同样是默认形态：`net/http` 服务器对每个请求都起一个独立的 goroutine 跑 handler，业务代码不用自己管并发接待。

### 8. 绑定到操作系统线程

`runtime.LockOSThread` 把当前 goroutine 绑在它正在跑的线程上，`UnlockOSThread` 解绑：

```go
package main

import (
    "fmt"
    "runtime"
)

func main() {
    done := make(chan struct{})
    go func() {
        runtime.LockOSThread()
        defer runtime.UnlockOSThread()
        // 绑定后这个 goroutine 不会迁移到其他线程，
        // 需要独占线程的资源（如 GUI 线程）在这里操作
        fmt.Println("locked to one OS thread")
        close(done)
    }()
    <-done
}
```

绑定和解绑必须发生在同一个 goroutine 里，所以这两行一般写在需要独占线程的那个 goroutine 内部。

### 9. 控制数量与让出调度

goroutine 虽轻，数量失控照样吃内存和调度开销。要限流就用池：固定几个 worker 从通道领任务。

```go
package main

import (
    "fmt"
    "sync"
)

func worker(id int, jobs <-chan int, wg *sync.WaitGroup) {
    defer wg.Done()
    for j := range jobs {
        fmt.Printf("Worker %d: job %d\n", id, j)
    }
}

func main() {
    const numJobs = 5
    jobs := make(chan int, numJobs)
    var wg sync.WaitGroup

    for w := 1; w <= 3; w++ {
        wg.Add(1)
        go worker(w, jobs, &wg)
    }

    for j := 1; j <= numJobs; j++ {
        jobs <- j
    }
    close(jobs)

    wg.Wait()
    fmt.Println("All jobs completed.")
}
```

`runtime.Gosched` 让当前 goroutine 主动让出 CPU 时间片给别的 goroutine；`runtime.Goexit` 终止当前 goroutine，终止前会先跑完它的 defer。

### 10. 和其他语言的协程比

Python 的协程靠 `async` 和 `await` 加事件循环，主要服务 I/O 密集场景，CPU 密集任务不会自动并发；Lua 的协程要手动切换；C++20 的协程（`co_await`、`co_yield`）把调度和资源管理留给开发者；C# 的 `async`/`await` 服务于异步 I/O；Kotlin 的协程支持结构化并发，形态上与 goroutine 最接近。goroutine 的差异点在运行时：栈管理、调度、阻塞时的切换都由运行时兜住，使用者只管 `go` 一个函数。

### 总结

`goroutine` 让并发程序的写法接近普通函数调用，同步靠 `channel` 和 `sync` 包配合。用好它的关键是让每个 `goroutine` 都能退出、共享数据有同步保护，出问题时用 `go test -race` 和性能分析工具排查。