### Synchronization Primitives

Synchronization primitives are the tools used in concurrent programming to control how multiple threads or goroutines access shared resources, ensuring data consistency and thread safety. Common synchronization primitives include:

1. **Mutex**
2. **RWMutex**
3. **WaitGroup**
4. **Cond**
5. **Once**
6. **Atomic Operations**
7. **Semaphore**

### Common synchronization primitives in Go

#### 1. Mutex

A mutex ensures that only one goroutine accesses a shared resource at a time.

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

#### 2. RWMutex

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

#### 3. WaitGroup

A WaitGroup is used to wait for a group of goroutines to finish.

```go
package main

import (
	"fmt"
	"sync"
)

func worker(id int, wg *sync.WaitGroup) {
	defer wg.Done()
	fmt.Printf("Worker %d starting\n", id)
	// simulate work
	fmt.Printf("Worker %d done\n", id)
}

func main() {
	var wg sync.WaitGroup

	for i := 1; i <= 5; i++ {
		wg.Add(1)
		go worker(i, &wg)
	}

	wg.Wait()
	fmt.Println("All workers done")
}
```

#### 4. Cond

A condition variable is used to block and wake goroutines, suited to more complex synchronization scenarios.

```go
package main

import (
	"fmt"
	"sync"
	"time"
)

var (
	mu   sync.Mutex
	cond = sync.NewCond(&mu)
)

func waitForCondition(id int, wg *sync.WaitGroup) {
	defer wg.Done()
	cond.L.Lock()
	cond.Wait()
	fmt.Printf("Goroutine %d activated\n", id)
	cond.L.Unlock()
}

func main() {
	var wg sync.WaitGroup

	for i := 1; i <= 3; i++ {
		wg.Add(1)
		go waitForCondition(i, &wg)
	}

	time.Sleep(time.Second)
	cond.Broadcast()
	wg.Wait()
	fmt.Println("All Goroutines activated")
}
```

#### 5. Once

Once is used to ensure a given operation runs only once.

```go
package main

import (
	"fmt"
	"sync"
)

var once sync.Once

func initialize() {
	fmt.Println("Initialized")
}

func worker(wg *sync.WaitGroup) {
	defer wg.Done()
	once.Do(initialize)
	fmt.Println("Worker done")
}

func main() {
	var wg sync.WaitGroup

	for i := 1; i <= 5; i++ {
		wg.Add(1)
		go worker(&wg)
	}

	wg.Wait()
	fmt.Println("All workers done")
}
```

#### 6. Atomic Operations

Atomic operations perform an atomic operation on a single variable, avoiding the overhead of using a lock.

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

#### 7. Semaphore

The Go standard library doesn't provide a semaphore implementation directly, but one can be built from primitives such as `sync.Cond` and `sync.Mutex`.

```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type Semaphore struct {
	cond *sync.Cond
	value int
}

func NewSemaphore(initial int) *Semaphore {
	return &Semaphore{
		cond: sync.NewCond(&sync.Mutex{}),
		value: initial,
	}
}

func (s *Semaphore) Acquire() {
	s.cond.L.Lock()
	defer s.cond.L.Unlock()
	for s.value <= 0 {
		s.cond.Wait()
	}
	s.value--
}

func (s *Semaphore) Release() {
	s.cond.L.Lock()
	defer s.cond.L.Unlock()
	s.value++
	s.cond.Signal()
}

func main() {
	var wg sync.WaitGroup
	sem := NewSemaphore(2)

	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			sem.Acquire()
			fmt.Printf("Goroutine %d acquired semaphore\n", id)
			time.Sleep(time.Second)
			fmt.Printf("Goroutine %d releasing semaphore\n", id)
			sem.Release()
		}(i)
	}

	wg.Wait()
	fmt.Println("All Goroutines finished")
}
```

### Summary

Mutexes and read-write locks protect shared data, a WaitGroup waits for a group of goroutines to finish, Cond handles waiting and waking, Once guarantees initialization runs only once, atomic operations skip the cost of locking, and a semaphore has to be assembled yourself from Cond and Mutex. For most cases, starting with `sync.Mutex` and `sync.WaitGroup` is enough; when reads outnumber writes, switch to `RWMutex`.

## References

- [sync standard library](https://pkg.go.dev/sync)
- [Go memory model](https://go.dev/ref/mem)
- [Official blog · Introducing the Go Race Detector](https://go.dev/blog/race-detector)
- [Go memory model · Synchronization](https://go.dev/ref/mem#synchronization)


## Sibling pages

- [Atomic](/sync/Atomic.md)
- [Context](/sync/Context.md)
- [CriticalSection](/sync/CriticalSection.md)
- [Mutex](/sync/Mutex.md)
- [RWMutex](/sync/RWMutex.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Atomic](/sync/Atomic.md)
