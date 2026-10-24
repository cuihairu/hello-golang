In Go, the `context` package is responsible for passing contextual information in concurrent programming: handling timeouts, cancellations, and carrying request-scoped data. Its use cases related to concurrency synchronization include:

1. **Controlling the lifecycle of goroutines**: Using `context` lets you pass cancel signals across multiple goroutines, thereby controlling their lifetimes.
2. **Timeout control**: Through `context` you can set a timeout to ensure an operation completes within a specified time.
3. **Passing request-scoped data**: You can share request-scoped data, such as authentication info or a trace ID, across multiple goroutines.

### 1. Basic concepts

#### 1.1 Types of `context`

- **`context.Context`**: The basic context interface, providing cancellation, timeouts, and data passing.
- **`context.Background()`**: Returns a root context, usually used at the top level of a program, as the parent of other contexts.
- **`context.TODO()`**: Used to indicate a context that hasn't been determined yet.

#### 1.2 Cancelling a context

A cancellable context can be created with `context.WithCancel`. The cancel signal propagates to every goroutine created from that context.

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
			// simulate work
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
	cancel() // send cancel signal, stop all workers

	// wait for all workers to finish
	time.Sleep(time.Second)
	fmt.Println("All workers stopped")
}
```

### 2. Timeout control

`context.WithTimeout` or `context.WithDeadline` can set a timeout on a context. When the timeout fires, the context is cancelled automatically.

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

	// wait for all workers to finish or time out
	time.Sleep(time.Second)
	fmt.Println("All workers stopped")
}
```

### 3. Passing request-scoped data

`context.WithValue` can be used to place data into a context. Across multiple goroutines, that data can then be retrieved from the context.

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

### 4. Combining with other synchronization primitives

`context` can be combined with other synchronization primitives (such as `sync.WaitGroup`, `sync.Mutex`, and so on) to achieve more complex synchronization and control.

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

### Summary

context does three things: `WithCancel` stops multiple goroutines, `WithTimeout` cancels automatically when the deadline arrives, and `WithValue` carries request-scoped data; pair it with `sync.WaitGroup` when you need to wait.

## References

- [sync standard library](https://pkg.go.dev/sync)
- [Go memory model](https://go.dev/ref/mem)
- [Official blog · Introducing the Go Race Detector](https://go.dev/blog/race-detector)
- [context standard library](https://pkg.go.dev/context)
- [Official blog · Go Concurrency Patterns: Context](https://go.dev/blog/context)
- [Official blog · Contexts and structs](https://go.dev/blog/context-and-structs)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
- [Primitives](/sync/Primitives.md)
- [Spinlock](/sync/Spinlock.md)
- [Sync](/sync/Sync.md)
