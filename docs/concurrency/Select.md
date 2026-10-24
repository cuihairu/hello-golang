# The `select` statement in Go

`select` lets a single wait watch several channels at once: whichever channel becomes ready first, its `case` runs first. It is the multiplexing construct of Go concurrency, and `time.After` timeouts and fanning in results from many channels both rely on it.

## Basic usage of the `select` statement

The syntax and usage of the `select` statement are as follows:

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    ch1 := make(chan string)
    ch2 := make(chan string)

    go func() {
        time.Sleep(1 * time.Second)
        ch1 <- "one"
    }()

    go func() {
        time.Sleep(2 * time.Second)
        ch2 <- "two"
    }()

    select {
    case msg1 := <-ch1:
        fmt.Println("Received", msg1)
    case msg2 := <-ch2:
        fmt.Println("Received", msg2)
    case <-time.After(3 * time.Second):
        fmt.Println("Timeout")
    }
}
```

In this example, of the three `case`s on `ch1`, `ch2` and `time.After`, whichever becomes ready first runs first, and the rest are left for the next round. The concrete rules are in the features list below.

### Features of the `select` statement

1. **Choosing to execute**: `select` picks a `case` that can run immediately. If several `case`s can run, one is chosen at random.
2. **Blocking behavior**: if no `case` can run, `select` blocks until one of them can.
3. **Default branch**: if there is a `default` branch and all channels are blocked, the `default` branch runs immediately without blocking.

### Examples

#### Example 1: basic usage

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    ch := make(chan string)

    go func() {
        time.Sleep(2 * time.Second)
        ch <- "message"
    }()

    select {
    case msg := <-ch:
        fmt.Println("Received:", msg)
    case <-time.After(1 * time.Second):
        fmt.Println("Timeout")
    }
}
```

In this example, `ch` needs to wait 2 seconds before it has data, while `time.After(1 * time.Second)` only waits 1 second, so `"Timeout"` is printed.

#### Example 2: multiple channels

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    ch1 := make(chan string)
    ch2 := make(chan string)

    go func() {
        time.Sleep(1 * time.Second)
        ch1 <- "one"
    }()

    go func() {
        time.Sleep(2 * time.Second)
        ch2 <- "two"
    }()

    select {
    case msg1 := <-ch1:
        fmt.Println("Received", msg1)
    case msg2 := <-ch2:
        fmt.Println("Received", msg2)
    case <-time.After(3 * time.Second):
        fmt.Println("Timeout")
    }
}
```

In this example, `select` picks the first ready channel among `ch1` and `ch2` to handle, so `"Received one"` is printed.

## Underlying implementation of the `select` statement

### The scheduler and goroutines

Go's concurrency model is based on goroutines and the scheduler. A goroutine is a lightweight thread managed by the Go runtime. The scheduler manages all the goroutines and dispatches them across OS threads.

### How the `select` statement works

1. **Initialization**: when `select` runs, the Go runtime builds a list of all the `case`s and initializes the corresponding wait queues.
2. **Checking readiness**: the Go runtime iterates over all the `case`s and checks each channel's state. If it finds a `case` that can run immediately, it picks one of the ready `case`s at random, runs it, and skips the rest of the steps.
3. **Blocking and waiting**: if no `case` can run immediately, the current goroutine is added to the wait queue of every relevant channel and the current goroutine is suspended.
4. **Waking up and executing**: when a channel becomes available, the Go runtime wakes the goroutines waiting on it and checks again which `case` can run. The woken goroutine resumes `select` and picks a `case` that can run.

### Code analysis

Below is simplified pseudocode sketching the core logic of `select` (this is not the real source; the real implementation is the `selectgo` function in `runtime/select.go`, with the signature `func selectgo(cas0 *scase, order0 *uint16, pc0 *uintptr, nsends, nrecvs int, block bool) (int, bool)`):

```go
// pseudocode: outlines the overall flow of select
func selectSelect(cases []scase, block bool) (int, bool) {
    ncases := len(cases)

    // 1. walk through all cases and check whether any can proceed immediately
    var ready []int
    for i := 0; i < ncases; i++ {
        if caseCanProceed(&cases[i]) {
            ready = append(ready, i)
        }
    }
    if len(ready) > 0 {
        // 2. if several are ready, pick one at random to keep things fair
        return ready[fastrand()%uint32(len(ready))], true
    }
    if !block {
        return -1, false // returns directly when there is a default branch
    }

    // 3. add the current goroutine to the wait queue of each case's channel, then park
    gopark(selectGoPark, "select")

    // 4. once woken up by a channel, the waker records the matched case index and returns
    return parkResult(), true
}
```

### Conclusion

The behavior of `select` comes down to three points: when several `case`s are ready at the same time, pick one at random so that the same channel never monopolizes it; when none is ready, park the current goroutine and wait until any channel has activity before waking; when there is a `default`, do not park at all and take the `default` path and return directly. This logic is implemented by `selectgo` in `runtime/select.go` in the runtime, and the pseudocode above is its skeleton.

## References

- [Effective Go · Concurrency](https://go.dev/doc/effective_go#concurrency)
- [Go Memory Model](https://go.dev/ref/mem)
- [sync standard library](https://pkg.go.dev/sync)
- [Language Spec · Select statements](https://go.dev/ref/spec#Select_statements)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)