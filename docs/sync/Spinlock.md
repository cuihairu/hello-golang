### Spinlock

A spinlock is a busy-wait lock, used for synchronization in a multi-threaded or multi-process environment. Unlike a mutex, a spinlock does not put the waiting thread to sleep while waiting for the lock to be released; instead, it repeatedly loops and checks the lock's state. A spinlock is suitable for scenarios with short wait times, because it avoids the overhead of a thread context switch. However, if the wait time is long, a spinlock wastes CPU resources.

### How a spinlock works

A spinlock is usually implemented with atomic operations (such as CAS, Compare-And-Swap), ensuring that no other thread interferes with the lock's state when it is being checked and modified. When a thread tries to acquire a spinlock, it keeps checking whether the lock is available, and if it is not, it continues looping until the lock becomes available or some other condition is met (such as a timeout).

### Implementing a spinlock in Go

The Go standard library does not provide a spinlock implementation, but you can build one using Go's atomic operations library (`sync/atomic`) and the basic concurrency primitives.

#### Example of a spinlock

Here is an example of a spinlock implementation and its use:

```go
package main

import (
	"fmt"
	"runtime"
	"sync"
	"sync/atomic"
)

// Spinlock is a custom spinlock structure
type Spinlock struct {
	flag int32
}

// Lock acquires the spinlock
func (sl *Spinlock) Lock() {
	for !atomic.CompareAndSwapInt32(&sl.flag, 0, 1) {
		// spin-wait for the lock to be released
		runtime.Gosched() // yield the CPU, avoiding a long busy-wait
	}
}

// Unlock releases the spinlock
func (sl *Spinlock) Unlock() {
	atomic.StoreInt32(&sl.flag, 0)
}

var (
	counter int
	spinLock Spinlock
)

func increment(wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 0; i < 1000; i++ {
		spinLock.Lock()   // acquire the spinlock
		counter++
		spinLock.Unlock() // release the spinlock
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

#### Code explanation

1. **Defining the spinlock structure**:
    ```go
    type Spinlock struct {
        flag int32
    }
    ```

2. **The Lock method of the spinlock**:
    ```go
    func (sl *Spinlock) Lock() {
        for !atomic.CompareAndSwapInt32(&sl.flag, 0, 1) {
            // spin-wait for the lock to be released
            runtime.Gosched() // yield the CPU, avoiding a long busy-wait
        }
    }
    ```

    - Uses the `atomic.CompareAndSwapInt32` atomic operation to try to acquire the lock.
    - If the lock is held (`sl.flag` is not 0), it calls `runtime.Gosched()` to yield the CPU, avoiding a long busy-wait.

3. **The Unlock method of the spinlock**:
    ```go
    func (sl *Spinlock) Unlock() {
        atomic.StoreInt32(&sl.flag, 0)
    }
    ```

    - Uses the `atomic.StoreInt32` atomic operation to release the lock, setting `sl.flag` to 0.

4. **Protecting the critical section with a spinlock**:
    ```go
    func increment(wg *sync.WaitGroup) {
        defer wg.Done()
        for i := 0; i < 1000; i++ {
            spinLock.Lock()   // acquire the spinlock
            counter++
            spinLock.Unlock() // release the spinlock
        }
    }
    ```

5. **Main function**:
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

    - Starts 10 goroutines, each executing the `increment` function, which concurrently increment the value of `counter`.
    - Access to `counter` is protected by the spinlock, ensuring that only one goroutine can modify `counter` at any given time.

### Summary

The standard library does not have a ready-made spinlock; you can put one together with `sync/atomic`'s CAS and `runtime.Gosched()`: if you cannot get the lock, yield the CPU and try again. Do not use it for scenarios with long lock waits, because it burns CPU for nothing.

## References

- [sync standard library](https://pkg.go.dev/sync)
- [Go memory model](https://go.dev/ref/mem)
- [Official blog · Introducing the Go Race Detector](https://go.dev/blog/race-detector)


## Sibling pages

- [Atomic](/sync/Atomic.md)
- [Context](/sync/Context.md)
- [CriticalSection](/sync/CriticalSection.md)
- [Runtime](/sync/Runtime.md)
- [Sync](/sync/Sync.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Sync](/sync/Sync.md)
