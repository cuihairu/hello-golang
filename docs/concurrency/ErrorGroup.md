`ErrorGroup` 是 Go 语言中的一个同步原语，提供了类似于 `sync.WaitGroup` 的功能，但专注于错误处理和任务的错误汇总。`ErrorGroup` 由 Google 的 `golang.org/x/sync` 包中的 `errgroup` 包提供。它使得管理并发任务时更方便地处理和汇总错误变得更加简洁。

### 1. 基本功能

`ErrorGroup` 的基本功能包括：

- **等待所有 goroutine 完成**：像 `sync.WaitGroup` 一样，`ErrorGroup` 可以等待一组 goroutine 完成。
- **捕获第一个错误**：在并发任务中，如果任何一个任务返回错误，`ErrorGroup` 会立即捕获这个错误，并停止等待其他任务完成（可选行为）。
- **返回第一个错误**：`ErrorGroup` 会返回第一个发生的错误，允许调用者处理或报告错误。

### 2. 使用示例

以下是一个使用 `ErrorGroup` 的示例，演示如何启动多个 goroutine，并收集可能发生的错误。

```go
package main

import (
    "context"
    "fmt"
    "golang.org/x/sync/errgroup"
    "time"
)

func main() {
    // Create a new ErrorGroup with a context
    var g errgroup.Group
    ctx := context.Background()

    // Start multiple goroutines
    for i := 1; i <= 3; i++ {
        i := i // Capture loop variable
        g.Go(func() error {
            // Simulate work
            time.Sleep(time.Second * time.Duration(i))
            // Simulate an error for demonstration
            if i == 2 {
                return fmt.Errorf("error from goroutine %d", i)
            }
            fmt.Printf("Goroutine %d completed successfully\n", i)
            return nil
        })
    }

    // Wait for all goroutines to complete and check for errors
    if err := g.Wait(); err != nil {
        fmt.Printf("Error occurred: %v\n", err)
    } else {
        fmt.Println("All goroutines completed successfully")
    }
}
```

### 3. 工作原理

#### 3.1 `errgroup.Group` 结构

`errgroup.Group` 内部使用 `sync.WaitGroup` 来同步 goroutine 的执行，使用一个错误变量来记录第一个发生的错误。以下是简化的内部结构：

```go
package errgroup

import (
    "context"
    "sync"
)

// ErrorGroup represents a group of goroutines working on subtasks of a common goal.
type Group struct {
    ctx    context.Context
    cancel context.CancelFunc
    mu     sync.Mutex
    err    error
    wg     sync.WaitGroup
}

// Go starts a new goroutine and adds it to the group.
func (g *Group) Go(f func() error) {
    g.wg.Add(1)
    go func() {
        defer g.wg.Done()
        if err := f(); err != nil {
            g.mu.Lock()
            if g.err == nil {
                g.err = err
                g.cancel()
            }
            g.mu.Unlock()
        }
    }()
}

// Wait waits for all goroutines to finish and returns the first non-nil error encountered.
func (g *Group) Wait() error {
    g.wg.Wait()
    return g.err
}
```

#### 3.2 `Go` 方法

`Go` 方法启动一个新的 goroutine，并将其添加到 `ErrorGroup` 中。它在 goroutine 完成后检查错误，并在发现第一个错误时记录下来，同时取消其他 goroutine 的执行（如果提供了取消函数）。

#### 3.3 `Wait` 方法

`Wait` 方法会等待所有 goroutine 完成，并返回第一个非 `nil` 错误。如果没有错误发生，则返回 `nil`。

### 4. 注意事项和常见问题

#### 4.1 错误处理

`ErrorGroup` 会在发现第一个错误后停止执行其他 goroutine。这是通过上下文的取消来实现的。需要注意的是，其他 goroutine 在上下文被取消后可能会继续执行，但不会报告错误。

#### 4.2 并发安全

`errgroup.Group` 使用互斥锁来保护错误变量的访问，确保并发环境下的安全性。尽管如此，使用 `ErrorGroup` 时仍需确保其他共享资源的并发安全。

#### 4.3 `context` 的使用

`ErrorGroup` 可以与 `context.Context` 一起使用，以便在出现错误时可以取消所有正在运行的 goroutine。确保创建和传递正确的上下文，以便正确处理 goroutine 的生命周期。

### 总结

`ErrorGroup` 是一个高效的并发任务管理工具，特别适合于需要处理错误的场景。它通过 `Go` 方法启动和管理多个 goroutine，通过 `Wait` 方法汇总错误，并允许在任务出现错误时中止其他任务。`ErrorGroup` 的设计使得并发错误处理变得更加简洁和易于使用，是处理并发任务时的有力工具。