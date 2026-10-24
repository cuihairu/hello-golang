### Atomic operations

An atomic operation is indivisible: during its execution, no other thread can observe an intermediate state. Compared with locking, it skips the overhead of the lock.

### CAS (Compare-and-Swap)

CAS (Compare-and-Swap) is a common atomic operation, used to implement lock-free algorithms. A CAS operation takes three arguments: a memory location (V), an expected value (A), and a new value (B). It works like this: if the value at memory location V equals the expected value A, then the value at V is updated to the new value B; otherwise, nothing is done.

### Atomic operations in Go

Go provides the `sync/atomic` package, which contains several common atomic operation functions:

- `atomic.AddInt32`, `atomic.AddInt64`, `atomic.AddUint32`, `atomic.AddUint64`: add a value to a variable atomically.
- `atomic.LoadInt32`, `atomic.LoadInt64`, `atomic.LoadUint32`, `atomic.LoadUint64`: read a variable's value atomically.
- `atomic.StoreInt32`, `atomic.StoreInt64`, `atomic.StoreUint32`, `atomic.StoreUint64`: store a value into a variable atomically.
- `atomic.CompareAndSwapInt32`, `atomic.CompareAndSwapInt64`, `atomic.CompareAndSwapUint32`, `atomic.CompareAndSwapUint64`: perform a CAS operation atomically.

#### An example of a CAS operation

The following is an example using a CAS operation:

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
	for {
		// get the current value of counter
		oldValue := atomic.LoadInt32(&counter)
		// compute the new value of counter
		newValue := oldValue + 1
		// try to update counter with a CAS operation
		if atomic.CompareAndSwapInt32(&counter, oldValue, newValue) {
			break
		}
		// if CAS fails, retry
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

#### Examples of other common atomic operations

The following are some examples using other common atomic operations:

1. **Atomic addition**:

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

2. **Atomic load and store**:

```go
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
)

var counter int32

func readCounter(id int, wg *sync.WaitGroup) {
	defer wg.Done()
	value := atomic.LoadInt32(&counter)
	fmt.Printf("Goroutine %d read counter: %d\n", id, value)
}

func writeCounter(id int, wg *sync.WaitGroup) {
	defer wg.Done()
	atomic.StoreInt32(&counter, int32(id))
	fmt.Printf("Goroutine %d wrote counter: %d\n", id, id)
}

func main() {
	var wg sync.WaitGroup

	for i := 1; i <= 5; i++ {
		wg.Add(1)
		go readCounter(i, &wg)
	}

	for i := 1; i <= 5; i++ {
		wg.Add(1)
		go writeCounter(i, &wg)
	}

	wg.Wait()
	fmt.Println("Final Counter:", counter)
}
```

### Common uses of atomic operations

1. **Counters**: Atomic operations are often used to implement concurrency-safe counters, such as click counts and visit statistics.
2. **Lock-free queues**: Lock-free queues are built on atomic operations, skipping lock and unlock.
3. **State flags**: Use atomic operations to update state flags, ensuring the consistency of the state.
4. **Reference counting**: Atomic operations are used to implement reference counting, managing the lifecycle of resources.

### Summary

`sync/atomic` provides four kinds of operations by type — add, read, write, and CAS. For shared variables like a counter, these are enough; you do not need to reach for a lock.

## References

- [sync standard library](https://pkg.go.dev/sync)
- [Go memory model](https://go.dev/ref/mem)
- [Official blog · Introducing the Go Race Detector](https://go.dev/blog/race-detector)
- [sync/atomic standard library](https://pkg.go.dev/sync/atomic)
- [Go memory model · Atomic operations](https://go.dev/ref/mem#atomic)

## Sibling pages

- [Primitives](/sync/Primitives.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
- [Primitives](/sync/Primitives.md)
- [Spinlock](/sync/Spinlock.md)
- [Sync](/sync/Sync.md)
