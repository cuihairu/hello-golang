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

### 总结

`goroutine` 让并发程序的写法接近普通函数调用，同步靠 `channel` 和 `sync` 包配合。用好它的关键是让每个 `goroutine` 都能退出、共享数据有同步保护，出问题时用 `go test -race` 和性能分析工具排查。