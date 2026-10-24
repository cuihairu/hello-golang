### Critical Section

A critical section is a block of code in a multi-threaded or multi-process environment that accesses and modifies shared resources. To avoid data inconsistency and race conditions, you must ensure that only one thread or process executes the critical section's code at any given time. Critical sections are typically protected by synchronization mechanisms (such as mutexes).

### Critical sections in Go

In Go, you can use a mutex (`sync.Mutex`) to protect a critical section, ensuring that only one goroutine can access and modify shared resources at any given time. Here is a counter example:

#### Example of a critical section

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
		mu.Lock()   // enter the critical section
		counter++
		mu.Unlock() // leave the critical section
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

In this example, the access to `counter` inside the `increment` function is the critical section. By using `mu.Lock()` to acquire the lock before accessing the shared resource, you ensure that only one goroutine can enter the critical section. Once the access is complete, `mu.Unlock()` releases the lock, allowing other goroutines to enter the critical section.

#### Code explanation

1. **Define the mutex**:
    ```go
    var mu sync.Mutex
    ```

2. **Enter the critical section**:
    ```go
    mu.Lock()   // enter the critical section
    counter++
    mu.Unlock() // leave the critical section
    ```

3. **Main function**:
    ```go
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

In the main function, 10 goroutines are started, each executing the `increment` function, which concurrently increments the value of `counter`. Because access to `counter` is protected by the mutex, the final value of `counter` is always correct after all goroutines finish, namely `10 * 1000 = 10000`.

### Summary

By locking before and after the block of code that accesses shared resources (the critical section), only one thread or goroutine is inside the critical section at any moment, and data inconsistency and race conditions are avoided.

## References

- [sync standard library](https://pkg.go.dev/sync)
- [Go memory model](https://go.dev/ref/mem)
- [Official blog · Introducing the Go Race Detector](https://go.dev/blog/race-detector)
- [Go memory model · locks](https://go.dev/ref/mem#locks)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
- [Primitives](/sync/Primitives.md)
- [Spinlock](/sync/Spinlock.md)
- [Sync](/sync/Sync.md)
