`sync.WaitGroup` 是 Go 语言标准库中 `sync` 包提供的一个同步原语，用于等待一组 goroutine 完成。它靠一个计数器协调多个 goroutine：计数归零，`Wait` 才返回，主程序由此等到所有 goroutine 干完活。

### 1. 基本用法

#### 1.1 常用方法

- **`Add(int)`**: 增加等待的计数器的值。每调用一次 `Add` 方法，计数器的值就会增加。
- **`Done()`**: 减少等待的计数器的值。当一个 goroutine 完成任务时，它调用 `Done` 方法来通知 `WaitGroup`。
- **`Wait()`**: 阻塞当前 goroutine，直到计数器的值变为零，即所有 goroutine 都调用了 `Done`。

#### 1.2 示例代码

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

`sync.WaitGroup` 的内部实现基于计数器和运行时信号量。

#### 2.1 计数器

- `sync.WaitGroup` 使用一个计数器来跟踪当前正在等待的 goroutine 数量。`Add` 方法增加计数器，`Done` 方法减少计数器，`Wait` 方法会阻塞直到计数器变为零。

#### 2.2 信号量

- 内部使用运行时的信号量机制（`runtime_Semacquire` / `runtime_Semrelease`）来实现阻塞和通知。当计数器不为零时，调用 `Wait` 方法的 goroutine 会被挂起；当计数器减少到零时，运行时唤醒所有等待中的 goroutine。

### 3. 注意事项和常见问题

#### 3.1 确保调用 `Done` 的次数与 `Add` 相匹配

每个调用 `Add` 的 goroutine 都应该对应一个 `Done` 调用，否则 `Wait` 将会永久阻塞。

#### 3.2 避免让 `WaitGroup` 计数器为负

如果 `Add` 传入的负数使计数器变为负值，或者 `Done` 的调用次数多于 `Add`，程序会直接 panic（`sync: negative WaitGroup counter`）。确保所有的 `Add` 和 `Done` 调用都匹配。

#### 3.3 在 `Wait` 之前调用 `Add`

`Add` 必须在 `Wait` 之前调用。否则，如果 `Wait` 被调用时计数器还是零，`Wait` 会立即返回，后面的 goroutine 就不会被等待，这可能会导致不正确的行为。最常见的做法是在启动 goroutine 之前统一调用 `wg.Add(n)`，或在每次 `go` 之前调用 `wg.Add(1)`。

#### 3.4 Go 1.21+ 新增的 `Go` 方法

从 Go 1.25 开始，`sync.WaitGroup` 提供了 `Go` 方法，它内部完成计数加一、启动 goroutine 并在任务结束时调用 `Done`，可以简化样板代码：

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    var wg sync.WaitGroup
    for i := 1; i <= 3; i++ {
        wg.Go(func() {
            fmt.Println("task", i)
        })
    }
    wg.Wait()
    fmt.Println("All tasks are done")
}
```

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

### 总结

`sync.WaitGroup` 只有三个方法：`Add` 加计数，`Done` 减计数，计数归零时 `Wait` 返回。用的时候 `Add` 要在 `Wait` 之前，`Add` 和 `Done` 的次数要对齐。对不上，`Wait` 要么永久阻塞，要么直接 panic（`sync: negative WaitGroup counter`）。