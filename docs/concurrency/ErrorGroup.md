`ErrorGroup` 是 Go 的一个同步原语，行为类似 `sync.WaitGroup`，但多了错误汇总：它由 `golang.org/x/sync` 包中的 `errgroup` 提供，在等待一组 goroutine 的同时记下并返回第一个出错的结果。

### 1. 基本功能

`ErrorGroup` 的基本功能包括：

- **等待所有 goroutine 完成**：像 `sync.WaitGroup` 一样，`ErrorGroup` 可以等待一组 goroutine 完成。
- **捕获第一个错误**：在并发任务中，如果任何一个任务返回错误，`ErrorGroup` 会记录这个错误（只保留第一个），并在创建时使用了 `errgroup.WithContext` 的情况下取消关联的 context，让其它任务有机会提前退出。注意 `Wait` 仍然会等待所有 goroutine 结束。
- **返回第一个错误**：`ErrorGroup` 会返回第一个发生的错误，允许调用者处理或报告错误。

### 2. 使用示例

以下是一个使用 `ErrorGroup` 的示例，演示如何启动多个 goroutine，并收集可能发生的错误。

```go
package main

import (
	"context"
	"fmt"
	"time"

	"golang.org/x/sync/errgroup"
)

func main() {
	// 使用 WithContext 创建带取消能力的 ErrorGroup
	g, ctx := errgroup.WithContext(context.Background())

	for i := 1; i <= 3; i++ {
		i := i // Capture loop variable
		g.Go(func() error {
			select {
			case <-ctx.Done(): // 其他任务出错时会触发取消
				fmt.Printf("Goroutine %d canceled\n", i)
				return ctx.Err()
			case <-time.After(time.Second * time.Duration(i)):
			}
			if i == 2 {
				return fmt.Errorf("error from goroutine %d", i)
			}
			fmt.Printf("Goroutine %d completed successfully\n", i)
			return nil
		})
	}

	// Wait 等所有 goroutine 结束后返回第一个非 nil 错误
	if err := g.Wait(); err != nil {
		fmt.Printf("Error occurred: %v\n", err)
	}
}
```

### 3. 工作原理

#### 3.1 `errgroup.Group` 结构

`errgroup.Group` 内部使用 `sync.WaitGroup` 来同步 goroutine 的执行，用 `sync.Once` 保证只记录第一个错误。以下是简化的内部结构（为便于阅读，省略了 `SetLimit` 用到的信号量等细节）：

```go
package errgroup

import "sync"

// Group 表示一组为共同目标工作的 goroutine。
type Group struct {
    cancel func(error) // 创建 Group 时注入的取消函数，为 nil 表示不可取消
    errOnce sync.Once  // 保证只记录第一个错误
    err     error
    wg      sync.WaitGroup
}

// Go starts a new goroutine and adds it to the group.
func (g *Group) Go(f func() error) {
    g.wg.Add(1)
    go func() {
        defer g.wg.Done()
        if err := f(); err != nil {
            g.errOnce.Do(func() {
                g.err = err
                if g.cancel != nil {
                    g.cancel(err)
                }
            })
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

`ErrorGroup` 在发现第一个错误后并不会强制终止其他 goroutine，goroutine 无法被外部直接杀死。如果通过 `errgroup.WithContext` 创建了带取消的 context，它会取消该 context，其他 goroutine 需要自己监听 `ctx.Done()` 并尽快返回；没有监听 context 的 goroutine 会继续执行到结束。此外，`Wait` 一定会等所有 goroutine 结束后才返回。

#### 4.2 并发安全

`errgroup.Group` 使用互斥锁来保护错误变量的访问，确保并发环境下的安全性。尽管如此，使用 `ErrorGroup` 时仍需确保其他共享资源的并发安全。

#### 4.3 `context` 的使用

`ErrorGroup` 可以与 `context.Context` 搭配，出错时取消正在运行的 goroutine。创建时传对 context，goroutine 的生命周期才管得住。

### 总结

`ErrorGroup` 把「等待一组 goroutine」和「汇总第一个错误」合成一步：`Go` 提交任务，`Wait` 返回第一个非 `nil` 错误。配上 `errgroup.WithContext`，第一个出错的任务会取消关联的 context，其余监听 `ctx.Done()` 的任务可以提前退出。比起用 `sync.WaitGroup` 等待、再自己加锁记错误的写法，这套 API 少写不少模板代码。