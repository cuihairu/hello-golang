### Mutex

A mutex is a synchronization mechanism: at any given moment it lets only one thread enter the critical section, used to block race conditions.

### Mutex in Go

In Go, the mutex is provided by the standard library `sync` package. The common type is `sync.Mutex`, which has two main methods:

- `Lock()`: acquires the lock; if the lock is already held, the goroutine calling this method blocks until the lock is released.
- `Unlock()`: releases the lock, allowing other blocked goroutines to acquire it. Releasing a lock that is not held panics outright (`sync: unlock of unlocked mutex`).
- `TryLock()` (Go 1.18+): tries to acquire the lock, returning `true` on success; if the lock is held it returns `false` immediately without waiting.

#### A mutex example

The example below protects a `counter` with `sync.Mutex`:

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
		mu.Lock()   // lock, enter the critical section
		counter++
		mu.Unlock() // unlock, leave the critical section
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

#### Code walkthrough

1. **Define the mutex and the shared variable**:
    ```go
    var (
        counter int
        mu      sync.Mutex
    )
    ```

2. **Use the mutex to protect the critical section**:
    ```go
    func increment(wg *sync.WaitGroup) {
        defer wg.Done()
        for i := 0; i < 1000; i++ {
            mu.Lock()   // lock, enter the critical section
            counter++
            mu.Unlock() // unlock, leave the critical section
        }
    }
    ```

3. **The main function**:
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

In the main function, 10 goroutines are started, each running the `increment` function, and these functions increment the value of `counter` concurrently. Because access to `counter` is protected by the mutex, once all goroutines have finished, the final value of `counter` is always correct, i.e. `10 * 1000 = 10000`.

### Non-blocking acquisition with TryLock

In some situations, when you cannot get the lock it is better to go do something else rather than wait. You can use `TryLock` for that:

```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	var mu sync.Mutex

	mu.Lock() // hold the lock first, simulating that it is held

	if mu.TryLock() {
		fmt.Println("got the lock")
		mu.Unlock()
	} else {
		fmt.Println("lock is held, go do something else")
	}

	mu.Unlock()
}
```

Output:

```
lock is held, go do something else
```

### Usage guidelines

1. **Locking and unlocking must come in pairs**: a repeated `Unlock` or unlocking an unlocked lock both panic. For functions with many branches, the recommended fixed pattern is:

   ```go
   var mu sync.Mutex

   mu.Lock()
   defer mu.Unlock()
   ```

2. **Do not lock twice**: `sync.Mutex` is not reentrant; two `Lock()` calls from the same goroutine will block forever.

3. **Do not copy a lock**: the mutex achieves mutual exclusion through internal state; after a by-value copy, each copy is independent of the others. A lock should be passed between functions as a pointer, and a struct containing a lock should not be passed by value either. The code below is caught by `go vet`:

   ```go
   type Counter struct {
       mu sync.Mutex
       n  int
   }

   // wrong: a value receiver copies the lock
   // func (c Counter) BadInc() { c.mu.Lock(); c.n++; c.mu.Unlock() }

   // right: use a pointer receiver
   func (c *Counter) Inc() {
       c.mu.Lock()
       defer c.mu.Unlock()
       c.n++
   }
   ```

4. **Keep the lock hold time as short as possible**: put only the necessary shared-data access in the critical section; move I/O and time-consuming computation outside the lock.

5. **Use a consistent lock order with multiple locks**: when you need to hold multiple locks at the same time, all goroutines must acquire them in the same order, otherwise they will wait on each other and form a deadlock.

### Summary

`sync.Mutex`'s `Lock`/`Unlock` wrap the critical section, and while the lock is held, other goroutines block on `Lock`. In the example above 10 goroutines each add 1000 times, so `counter` ends up at 10000; remove `Lock`/`Unlock` and the result is no longer necessarily that number. Use `TryLock` when you do not want to wait when you cannot get the lock; remember the two rules that the lock is not reentrant and not copyable, and you will avoid the common mutex bugs.

## References

- [sync standard library](https://pkg.go.dev/sync)
- [Go memory model](https://go.dev/ref/mem)
- [Official blog · Introducing the Go Race Detector](https://go.dev/blog/race-detector)
- [Go memory model · Locks](https://go.dev/ref/mem#locks)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
- [Primitives](/sync/Primitives.md)
