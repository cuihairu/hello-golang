Go's `goroutine` is a lightweight thread implementation, scheduled by the runtime, so writing concurrent programs doesn't require managing threads yourself. This page records its basic usage, pros and cons, and things to watch out for in practice.

### 1. Basic Usage

`goroutine` is started with the `go` keyword, which runs a function or method in the background, executing concurrently with other `goroutine`s. Using `goroutine` is simple: just add the `go` keyword before the function call.

#### Example Code

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
    go sayHello() // start a goroutine
    go sayGoodbye() // start another goroutine

    // wait a while to let the goroutines finish executing
    time.Sleep(6 * time.Second)
}
```

### 2. Pros and Cons

#### Pros

1. **Lightweight**: a single `goroutine` uses less memory than a thread, and creating and destroying it costs far less.
2. **Scheduling handled by the runtime**: the scheduler multiplexes a large number of `goroutine`s onto a small number of OS threads, growing and shrinking the count as the program needs.
3. **Simple to write**: just add `go` before a function call to start it; no explicit management of thread creation and destruction.

#### Cons

1. **Memory usage**: per-unit usage is small, but in large numbers they still consume a lot of memory.
2. **Debugging is complex**: debugging concurrent programs is far more complex than single-threaded ones; race conditions and deadlocks are hard to locate and fix.
3. **Scheduling latency**: under heavy load, scheduling and context switching introduce latency.

### 3. Usage Notes

1. **Ensure they exit**: a `goroutine` must be able to exit when it is no longer needed, or it will keep holding resources and cause a memory leak.
2. **Avoid data races**: protect shared data with a synchronization mechanism such as `sync.Mutex` or `sync.RWMutex`.
3. **Prefer `channel` for communication**: route both synchronization and data transfer over `channel`; it is easier to guarantee safety than sharing data directly.
4. **Set timeouts**: set timeouts when dealing with I/O operations or external resources, so `goroutine`s don't block for a long time and prevent the program from exiting normally.
5. **Handle errors**: errors inside a `goroutine` don't affect the main flow, but someone still needs to handle them; you can use `select` and `channel` to pass errors out.

### 4. Possible Problems

1. **Deadlock**: misusing synchronization mechanisms like `channel` causes deadlocks; make sure every `channel` has a corresponding sender and receiver.
2. **Resource leaks**: a `goroutine` that keeps running without exiting leaks; catch it with timeouts and cancellation.
3. **Race conditions**: they appear when shared resources lack synchronization protection; detect them with `go test -race`.
4. **Scheduling problems**: under heavy load, scheduling and context switching slow the program down; use profiling tools to locate the issue.

### 5. Stack and Scheduling

A goroutine's stack starts very small (about 2KB), grows as needed, and the upper limit is on the order of 1GB; most programs never fill it, which is the main reason it is lighter than an OS thread. The runtime scheduler multiplexes a large number of goroutines onto a small number of threads, and the mapping is transparent to the user.

One behavior to remember: when the main goroutine exits, all other goroutines are terminated immediately, whether or not they finished. So after launching background goroutines, the main goroutine must wait for them, using either a channel or `sync.WaitGroup`.

### 6. Waiting for a goroutine with a Channel

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

The main goroutine stops at `<-done` until the worker sends the completion signal.

### 7. Parallel Computation and Network Services

Split the data, compute each segment in one goroutine, then collect the results over a channel:

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

In network services, goroutines are likewise the default shape: the `net/http` server starts an independent goroutine per request to run the handler, so business code doesn't have to manage concurrent handling itself.

### 8. Pinning to an OS Thread

`runtime.LockOSThread` pins the current goroutine to the thread it is running on, and `UnlockOSThread` unbinds it:

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
        // after binding, this goroutine will not migrate to other threads;
        // resources that require a dedicated thread (like a GUI thread) are handled here
        fmt.Println("locked to one OS thread")
        close(done)
    }()
    <-done
}
```

Locking and unlocking must happen in the same goroutine, so these two lines are usually written inside the goroutine that needs the dedicated thread.

### 9. Controlling Count and Yielding the Scheduler

Goroutines are light, but if their count runs away they still eat up memory and scheduling overhead. To limit throughput, use a pool: a fixed number of workers pull tasks from a channel.

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

`runtime.Gosched` makes the current goroutine voluntarily yield its CPU time slice to other goroutines; `runtime.Goexit` terminates the current goroutine, but first runs its defers to completion.

### 10. Comparison with Coroutines in Other Languages

Python coroutines rely on `async` and `await` plus an event loop, mainly serving I/O-bound scenarios; CPU-bound tasks don't go concurrent automatically. Lua coroutines require manual switching. C++20 coroutines (`co_await`, `co_yield`) leave scheduling and resource management to the developer. C#'s `async`/`await` serves asynchronous I/O. Kotlin coroutines support structured concurrency and are the closest in shape to goroutines. The difference with goroutines is in the runtime: stack management, scheduling, and blocking switches are all handled by the runtime, and the user just writes `go` followed by a function.

### Summary

`goroutine` makes writing concurrent programs close to ordinary function calls, with synchronization handled by `channel` and the `sync` package working together. The key to using it well is making sure every `goroutine` can exit and shared data has synchronization protection; when something goes wrong, use `go test -race` and profiling tools to investigate.

## References

- [Effective Go · Concurrency](https://go.dev/doc/effective_go#concurrency)
- [Go Memory Model](https://go.dev/ref/mem)
- [sync standard library](https://pkg.go.dev/sync)
- [Language Spec · Go Statements](https://go.dev/ref/spec#Go_statements)
- [Effective Go · Goroutines](https://go.dev/doc/effective_go#goroutines)
- [Official codelab · Share Memory By Communicating](https://go.dev/blog/codelab-share)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
