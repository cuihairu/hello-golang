### Memory Synchronization

Memory synchronization is a key concept in concurrent programming, used to ensure that access to and modification of shared data by multiple threads or goroutines is visible and consistent. In an environment with multi-core processors and multi-level caches, the order of operations between threads may be reordered, so synchronization primitives (such as locks and atomic operations) are needed to guarantee correct memory visibility.

### Memory synchronization in Go

In Go, memory synchronization can be achieved in the following ways:

1. **Mutex**: ensures that only one goroutine accesses the critical section at any given time.
2. **Read-write lock (RWMutex)**: allows multiple read operations to run concurrently, but write operations are exclusive.
3. **Atomic operations**: provide low-level synchronization primitives for performing atomic operations on a single variable.
4. **Channel**: Go's built-in concurrency primitive, used to pass data between goroutines and to synchronize.

#### Example of a mutex

A mutex ensures that only one goroutine accesses shared data at any given time.

```go
package main

import (
	"fmt"
	"sync"
)

var (
	counter int
	mu      sync.Mutex
)

func increment(wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 0; i < 1000; i++ {
		mu.Lock()
		counter++
		mu.Unlock()
	}
}

func main() {
	var wg sync.WaitGroup

	for i := 0; i < 10; i++ {
		wg.Add(1)
		go increment(&wg)
	}

	wg.Wait()
	fmt.Println("Final Counter:", counter)
}
```

#### Example of a read-write lock

A read-write lock allows multiple read operations to run concurrently, but write operations are exclusive.

```go
package main

import (
	"fmt"
	"sync"
)

var (
	counter int
	rwMutex sync.RWMutex
)

func readCounter(id int, wg *sync.WaitGroup) {
	defer wg.Done()
	rwMutex.RLock()
	defer rwMutex.RUnlock()
	fmt.Printf("Goroutine %d reading counter: %d\n", id, counter)
}

func writeCounter(id int, wg *sync.WaitGroup) {
	defer wg.Done()
	rwMutex.Lock()
	defer rwMutex.Unlock()
	counter++
	fmt.Printf("Goroutine %d writing counter: %d\n", id, counter)
}

func main() {
	var wg sync.WaitGroup

	for i := 1; i <= 5; i++ {
		wg.Add(1)
		go readCounter(i, &wg)
	}

	for i := 1; i <= 2; i++ {
		wg.Add(1)
		go writeCounter(i, &wg)
	}

	wg.Wait()
	fmt.Println("Final Counter:", counter)
}
```

#### Example of atomic operations

Atomic operations are used to perform atomic operations on a single variable, avoiding the overhead of locks.

```go
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
)

var counter int32

func increment(wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 0; i < 1000; i++ {
		atomic.AddInt32(&counter, 1)
	}
}

func main() {
	var wg sync.WaitGroup

	for i := 0; i < 10; i++ {
		wg.Add(1)
		go increment(&wg)
	}

	wg.Wait()
	fmt.Println("Final Counter:", counter)
}
```

#### Example of a channel

A channel is used to pass data between goroutines and to synchronize.

```go
package main

import (
	"fmt"
	"sync"
)

func increment(ch chan int, wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 0; i < 1000; i++ {
		ch <- 1
	}
}

func counter(ch chan int, wg *sync.WaitGroup) {
	defer wg.Done()
	counter := 0
	for i := 0; i < 10000; i++ {
		counter += <-ch
	}
	fmt.Println("Final Counter:", counter)
}

func main() {
	var wg sync.WaitGroup
	ch := make(chan int)

	wg.Add(1)
	go counter(ch, &wg)

	for i := 0; i < 10; i++ {
		wg.Add(1)
		go increment(ch, &wg)
	}

	wg.Wait()
}
```

### Summary

The four synchronization primitives each have their own role: a mutex protects the critical section, a read-write lock lets concurrent reads through when reads far outnumber writes, atomic operations save the lock overhead for a single variable, and a channel replaces shared memory with data passing. Which one to use depends on the granularity of the shared data and the read-write ratio.

## References

- [sync standard library](https://pkg.go.dev/sync)
- [Go memory model](https://go.dev/ref/mem)
- [Official blog · Introducing the Go Race Detector](https://go.dev/blog/race-detector)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
