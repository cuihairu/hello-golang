`sync.WaitGroup` 是 Go 语言标准库中 `sync` 包提供的一个同步原语，用于等待一组 goroutine 完成。它通过计数器机制来协调多个 goroutine 的执行，使得主程序或其他 goroutine 能够在所有的 goroutine 完成其任务后再继续执行。以下是对 `sync.WaitGroup` 的详细讲解，包括其基本用法、工作原理以及使用示例。

### 1. 基本用法

#### 1.1 常用方法

- **`Add(int)`**: 增加等待的计数器的值。每调用一次 `Add` 方法，计数器的值就会增加。
- **`Done()`**: 减少等待的计数器的值。当一个 goroutine 完成任务时，它调用 `Done` 方法来通知 `WaitGroup`。
- **`Wait()`**: 阻塞当前 goroutine，直到计数器的值变为零，即所有 goroutine 都调用了 `Done`。

#### 1.2 示例代码

以下是一个使用 `sync.WaitGroup` 的基本示例：

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

func main() {
    var wg sync.WaitGroup

    // 启动多个 goroutine
    for i := 1; i <= 3; i++ {
        wg.Add(1) // 增加计数器
        go func(n int) {
            defer wg.Done() // 在 goroutine 完成时减少计数器
            fmt.Printf("Goroutine %d is starting\n", n)
            time.Sleep(time.Second * 2) // 模拟工作
            fmt.Printf("Goroutine %d is done\n", n)
        }(i)
    }

    wg.Wait() // 阻塞主 goroutine，直到所有 goroutine 完成
    fmt.Println("All goroutines are done")
}
```

### 2. 工作原理

`sync.WaitGroup` 的内部实现基于计数器和条件变量。以下是 `WaitGroup` 的工作原理：

#### 2.1 计数器

- `sync.WaitGroup` 使用一个计数器来跟踪当前正在等待的 goroutine 数量。`Add` 方法增加计数器，`Done` 方法减少计数器，`Wait` 方法会阻塞直到计数器变为零。

#### 2.2 条件变量

- 内部使用了条件变量（`sync.Cond`）来实现阻塞和通知机制。当计数器不为零时，调用 `Wait` 方法的 goroutine 会被阻塞；当计数器减少到零时，条件变量会被通知，从而解除阻塞。

### 3. 注意事项和常见问题

#### 3.1 确保调用 `Done` 的次数与 `Add` 相匹配

每个调用 `Add` 的 goroutine 都应该对应一个 `Done` 调用，否则 `Wait` 将会永久阻塞。

#### 3.2 避免在 `WaitGroup` 计数器为负时调用 `Wait`

如果在 `WaitGroup` 计数器已经减为负值时调用 `Wait`，会导致程序挂起。确保所有的 `Add` 和 `Done` 调用都匹配。

#### 3.3 不要在 `Wait` 之前调用 `Add`

`Add` 方法必须在调用 `Wait` 之前调用。否则，如果 `Wait` 被调用时计数器已经为零，`Wait` 会立即返回，这可能会导致不正确的行为。

### 4. 高级用法和注意事项

#### 4.1 使用 `sync.WaitGroup` 和 `context`

在一些复杂的场景中，可能需要结合 `sync.WaitGroup` 和 `context.Context` 来管理 goroutine 的生命周期和取消操作。

```go
package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

func main() {
    var wg sync.WaitGroup
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    for i := 1; i <= 3; i++ {
        wg.Add(1)
        go func(n int) {
            defer wg.Done()
            select {
            case <-ctx.Done():
                fmt.Printf("Goroutine %d is canceled\n", n)
                return
            case <-time.After(time.Second * 2):
                fmt.Printf("Goroutine %d is done\n", n)
            }
        }(i)
    }

    // Simulate work in main goroutine
    time.Sleep(time.Second)
    cancel() // Cancel all goroutines

    wg.Wait() // Wait for all goroutines to finish
    fmt.Println("All goroutines are done")
}
```

在这个示例中，使用 `context` 来控制 `goroutine` 的取消，这可以与 `sync.WaitGroup` 结合使用来处理复杂的同步问题。

### 总结

`sync.WaitGroup` 是 Go 语言中用于同步等待多个 goroutine 完成的强大工具。它通过简单的计数器和条件变量机制，实现了高效的 goroutine 协调。正确使用 `sync.WaitGroup` 可以有效地管理并发任务，避免常见的同步问题。