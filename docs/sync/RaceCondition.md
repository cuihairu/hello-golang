### Race Condition

A race condition occurs when multiple threads or processes concurrently access and modify a shared resource, and the final result depends on the order in which those access operations execute. A race condition can lead to inconsistent data or undefined behavior in a program. Simply put, when two or more threads access a shared resource at the same time, data conflicts can result if proper synchronization is not applied.

### Race condition examples in Go

Go encourages concurrent programming, so race conditions come up more often. Here is an example that goes wrong first, then the fix with synchronization added.

#### Example of a race condition

```go
package main

import (
	"fmt"
	"sync"
)

var counter int

func increment(wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 0; i < 1000; i++ {
		counter++
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

In this example, multiple goroutines concurrently execute the `increment` function, each of which increments `counter`. Because there is no synchronization mechanism, multiple goroutines may access and modify `counter` at the same time, causing a race condition. Run this code several times and the final value of `counter` may differ each run, because it depends on the order in which the goroutines run.

#### Solving the race condition with a mutex

To avoid a race condition, you can use a mutex to ensure that only one goroutine can access and modify the shared resource at any given time. Here is the modified example, which uses a mutex to synchronize access to `counter`.

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

In this modified example, `sync.Mutex` is used to create a mutex `mu`. Before each modification of `counter`, `mu.Lock()` acquires the lock, and after the modification `mu.Unlock()` releases it. This ensures that only one goroutine can modify `counter` at any given time, avoiding the race condition.

Run this code, and no matter how many times, the final value of `counter` should always be 10000 (because there are 10 goroutines, each incrementing 1000 times).

### Race detection tool

Go provides a built-in race detector that can detect race conditions in a program at run time. When running a program, use the `-race` flag to enable race detection:

```sh
go run -race main.go
```

Once enabled, whenever a real concurrent conflicting access actually happens along the run path, `-race` prints out the two conflicting read/write locations. I usually run `-race` once before merging concurrent code.

## References

- [sync standard library](https://pkg.go.dev/sync)
- [Go memory model](https://go.dev/ref/mem)
- [Official blog · Introducing the Go Race Detector](https://go.dev/blog/race-detector)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
