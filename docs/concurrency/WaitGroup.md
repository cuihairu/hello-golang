`sync.WaitGroup` is a synchronization primitive provided by the `sync` package in Go's standard library, used to wait for a group of goroutines to finish. It coordinates multiple goroutines with a counter: only when the count drops to zero does `Wait` return, which is how the main program waits for all the goroutines to finish their work.

### 1. Basic Usage

#### 1.1 Common Methods

- **`Add(int)`**: increments the value of the wait counter. Each call to `Add` increases the counter.
- **`Done()`**: decrements the value of the wait counter. When a goroutine finishes its task, it calls `Done` to notify the `WaitGroup`.
- **`Wait()`**: blocks the current goroutine until the counter reaches zero, meaning every goroutine has called `Done`.

#### 1.2 Example Code

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

func main() {
    var wg sync.WaitGroup

    // launch several goroutines
    for i := 1; i <= 3; i++ {
        wg.Add(1) // increment the counter
        go func(n int) {
            defer wg.Done() // decrement the counter when the goroutine finishes
            fmt.Printf("Goroutine %d is starting\n", n)
            time.Sleep(time.Second * 2) // simulate work
            fmt.Printf("Goroutine %d is done\n", n)
        }(i)
    }

    wg.Wait() // block the main goroutine until all goroutines finish
    fmt.Println("All goroutines are done")
}
```

### 2. How It Works

`sync.WaitGroup` is implemented on top of a counter and runtime semaphores.

#### 2.1 Counter

- `sync.WaitGroup` uses a counter to track how many goroutines are currently being waited on. `Add` increments the counter, `Done` decrements it, and `Wait` blocks until the counter reaches zero.

#### 2.2 Semaphores

- Internally it uses the runtime's semaphore mechanism (`runtime_Semacquire` / `runtime_Semrelease`) to implement blocking and notification. While the counter is non-zero, a goroutine calling `Wait` gets suspended; when the counter drops to zero, the runtime wakes up all the waiting goroutines.

### 3. Caveats and Common Problems

#### 3.1 Make sure `Done` calls match `Add` calls

Every goroutine that calls `Add` should have a corresponding `Done` call, otherwise `Wait` will block forever.

#### 3.2 Never let the `WaitGroup` counter go negative

If `Add` is called with a negative number that drives the counter below zero, or if `Done` is called more times than `Add`, the program panics immediately (`sync: negative WaitGroup counter`). Make sure all `Add` and `Done` calls line up.

#### 3.3 Call `Add` before `Wait`

`Add` must be called before `Wait`. Otherwise, if the counter is still zero when `Wait` is called, `Wait` returns immediately and the later goroutines are never waited on, which can lead to incorrect behavior. The most common approach is to call `wg.Add(n)` once before launching the goroutines, or to call `wg.Add(1)` right before each `go`.

#### 3.4 The New `Go` Method Added in Go 1.21+

Starting from Go 1.25, `sync.WaitGroup` provides a `Go` method. It does the counter increment, starts the goroutine, and calls `Done` when the task ends — all of it internally — which trims a lot of boilerplate:

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

### 4. Advanced Usage and Caveats

#### 4.1 Using `sync.WaitGroup` with `context`

In some more complex scenarios, you may need to combine `sync.WaitGroup` with `context.Context` to manage goroutine lifetimes and cancellation.

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

### Summary

`sync.WaitGroup` has just three methods: `Add` increments the count, `Done` decrements it, and `Wait` returns once the count hits zero. When you use it, call `Add` before `Wait`, and keep the number of `Add` and `Done` calls matched. If they do not line up, `Wait` either blocks forever or panics immediately (`sync: negative WaitGroup counter`).

## References

- [Effective Go · Concurrency](https://go.dev/doc/effective_go#concurrency)
- [Go Memory Model](https://go.dev/ref/mem)
- [sync standard library](https://pkg.go.dev/sync)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
