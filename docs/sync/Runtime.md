### Runtime knowledge relevant to Go concurrency and synchronization

In Go, the runtime package manages the underlying functions of goroutine scheduling, memory allocation, and garbage collection. How goroutines get scheduled, and how shared memory gets synchronized, the answers to both live in the runtime.

#### 1. Goroutine scheduling

A goroutine is a lightweight thread in Go, managed by the Go runtime. Goroutine scheduling is implemented by Go's M:N scheduler, where M represents operating system threads and N represents goroutines.

- **Goroutine**: every Go program creates a main goroutine when it starts.
- **M (Machine)**: represents an operating system thread.
- **P (Processor)**: represents a logical processor, responsible for running goroutines. The number of Ps is controlled by the `GOMAXPROCS` environment variable.
- **G (Goroutine)**: represents a goroutine; multiple goroutines can run on a single P.

The scheduler assigns goroutines to different Ps to run, and the Ps are assigned to Ms, so execution actually happens on operating system threads.

#### 2. The GMP model

The GMP model is the core mechanism the Go runtime uses to manage concurrency:

- **G (Goroutine)**: the goroutine managed by the Go runtime.
- **M (Machine)**: an operating system thread.
- **P (Processor)**: a logical processor that schedules goroutines onto Ms.

The number of Ps equals the value of `GOMAXPROCS`, representing how many goroutines can truly run Go code in parallel at any given moment. Through the GMP model, the Go runtime manages and schedules goroutines effectively, achieving efficient concurrency.

#### 3. Memory synchronization

Go provides a number of primitives for memory synchronization, ensuring memory visibility and consistency across multiple goroutines.

- **sync.Mutex**: a mutex, used to protect shared resources so that only one goroutine accesses them at any given time.
- **sync.RWMutex**: a read-write lock, which allows multiple read operations to run concurrently but makes write operations exclusive.
- **sync.WaitGroup**: a wait group, used to wait for a group of goroutines to complete.
- **sync.Cond**: a condition variable, used to block and wake goroutines.
- **sync.Once**: a one-shot operation, ensuring a given operation runs only once.
- **sync/atomic**: atomic operations, used to perform atomic operations on a single variable and avoid the overhead of locks.

#### 4. Runtime-related functions

- `runtime.GOMAXPROCS(n int) int`: sets the maximum number of CPUs (Ps) that can run Go code concurrently, and returns the previous setting.
- `runtime.Gosched()`: yields execution of the current goroutine, so the scheduler reschedules other goroutines.
- `runtime.Goexit()`: exits the current goroutine without affecting the execution of other goroutines.
- `runtime.NumCPU() int`: returns the number of CPUs on the current system.
- `runtime.NumGoroutine() int`: returns the number of currently live (existing) goroutines.

### Example code

The three examples correspond to GOMAXPROCS, a mutex, and atomic operations respectively:

#### Example of goroutine scheduling and GOMAXPROCS

```go
package main

import (
	"fmt"
	"runtime"
	"sync"
)

func main() {
	// set the maximum number of goroutines running in parallel
	runtime.GOMAXPROCS(4)

	var wg sync.WaitGroup

	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			fmt.Printf("Goroutine %d running\n", id)
		}(i)
	}

	wg.Wait()
	fmt.Println("All goroutines finished")
}
```

#### Memory synchronization with a Mutex and WaitGroup

```go
package main

import (
	"fmt"
	"sync"
)

var (
	counter int
	mu      sync.Mutex
	wg      sync.WaitGroup
)

func increment() {
	defer wg.Done()
	for i := 0; i < 1000; i++ {
		mu.Lock()
		counter++
		mu.Unlock()
	}
}

func main() {
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go increment()
	}

	wg.Wait()
	fmt.Println("Final Counter:", counter)
}
```

#### Memory synchronization with atomic operations

```go
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
)

var counter int32
var wg sync.WaitGroup

func increment() {
	defer wg.Done()
	for i := 0; i < 1000; i++ {
		atomic.AddInt32(&counter, 1)
	}
}

func main() {
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go increment()
	}

	wg.Wait()
	fmt.Println("Final Counter:", counter)
}
```

### Summary

At the runtime level there are just three things to remember: the upper limit on parallelism is set by `GOMAXPROCS`, which controls the number of Ps; a shared variable either gets a lock (`sync.Mutex`) or goes through `sync/atomic`; and to wait for a group of goroutines to wind down you use `sync.WaitGroup`. Pick the right one in all three cases and the vast majority of concurrency problems never show up.

## References

- [sync standard library](https://pkg.go.dev/sync)
- [Go memory model](https://go.dev/ref/mem)
- [Official blog · Introducing the Go Race Detector](https://go.dev/blog/race-detector)
- [runtime standard library](https://pkg.go.dev/runtime)
- [Official · Go scheduler design document (golang.org/s/go11sched)](https://golang.org/s/go11sched)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
- [Spinlock](/sync/Spinlock.md)
