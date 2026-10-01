在 Go 语言中，`context` 包是用于在并发编程中传递和管理上下文信息的一个重要工具。`context` 可以用于处理超时、取消操作以及传递请求级别的数据。与并发同步相关的使用场景包括：

1. **控制 goroutine 的生命周期**：使用 `context` 可以在多个 goroutine 之间传递取消信号，从而控制它们的生命周期。
2. **超时控制**：通过 `context` 可以设定超时时间，确保操作在规定时间内完成。
3. **传递请求范围的数据**：可以在多个 goroutine 之间共享请求范围的数据，如认证信息或跟踪 ID。

### 1. 基本概念

#### 1.1 `context` 的类型

- **`context.Context`**: 基本的上下文接口，提供了取消、超时和传递数据的功能。
- **`context.Background()`**: 返回一个根上下文，通常用于程序的顶层，作为其他上下文的父上下文。
- **`context.TODO()`**: 用于表示尚未确定上下文的情况。

#### 1.2 上下文的取消

上下文可以通过 `context.WithCancel` 创建一个可以取消的上下文。取消信号会传递给所有基于该上下文创建的 goroutine。

```go
package main

import (
	"context"
	"fmt"
	"time"
)

func worker(ctx context.Context, id int) {
	for {
		select {
		case <-ctx.Done():
			fmt.Printf("Worker %d stopped\n", id)
			return
		default:
			// 模拟工作
			time.Sleep(time.Millisecond * 100)
			fmt.Printf("Worker %d working\n", id)
		}
	}
}

func main() {
	ctx, cancel := context.WithCancel(context.Background())

	for i := 1; i <= 3; i++ {
		go worker(ctx, i)
	}

	time.Sleep(time.Second)
	cancel() // 发送取消信号，停止所有 worker

	// 等待所有 worker 完成
	time.Sleep(time.Second)
	fmt.Println("All workers stopped")
}
```

### 2. 超时控制

通过 `context.WithTimeout` 或 `context.WithDeadline` 可以为上下文设置超时时间。当超时发生时，上下文会自动被取消。

```go
package main

import (
	"context"
	"fmt"
	"time"
)

func worker(ctx context.Context, id int) {
	select {
	case <-ctx.Done():
		fmt.Printf("Worker %d stopped due to timeout\n", id)
		return
	case <-time.After(time.Second):
		fmt.Printf("Worker %d completed\n", id)
	}
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), time.Millisecond*500)
	defer cancel()

	for i := 1; i <= 3; i++ {
		go worker(ctx, i)
	}

	// 等待所有 worker 完成或超时
	time.Sleep(time.Second)
	fmt.Println("All workers stopped")
}
```

### 3. 传递请求范围的数据

可以使用 `context.WithValue` 将数据传递到上下文中。在多个 goroutine 中，可以通过上下文获取这些数据。

```go
package main

import (
	"context"
	"fmt"
	"time"
)

func worker(ctx context.Context, id int) {
	if val := ctx.Value("request_id"); val != nil {
		fmt.Printf("Worker %d processing request %s\n", id, val)
	} else {
		fmt.Printf("Worker %d no request ID\n", id)
	}

	time.Sleep(time.Millisecond * 100)
}

func main() {
	ctx := context.WithValue(context.Background(), "request_id", "12345")

	for i := 1; i <= 3; i++ {
		go worker(ctx, i)
	}

	time.Sleep(time.Second)
	fmt.Println("All workers done")
}
```

### 4. 与其他同步原语的结合

`context` 可以与其他同步原语（如 `sync.WaitGroup`、`sync.Mutex` 等）结合使用，以实现更复杂的同步和控制。

```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

func worker(ctx context.Context, id int, wg *sync.WaitGroup) {
	defer wg.Done()

	select {
	case <-ctx.Done():
		fmt.Printf("Worker %d stopped\n", id)
	case <-time.After(time.Second):
		fmt.Printf("Worker %d completed\n", id)
	}
}

func main() {
	var wg sync.WaitGroup
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*2)
	defer cancel()

	for i := 1; i <= 5; i++ {
		wg.Add(1)
		go worker(ctx, i, &wg)
	}

	wg.Wait()
	fmt.Println("All workers finished")
}
```

### 总结

`context` 在 Go 的并发编程中提供了一种灵活的机制，用于控制 goroutine 的生命周期、超时控制以及数据传递。通过与其他同步原语结合使用，`context` 可以有效地管理并发操作，确保程序的鲁棒性和性能。