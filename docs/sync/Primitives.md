### 同步原语（Synchronization Primitives）

同步原语是并发编程中用来控制多个线程或Goroutine对共享资源的访问，以确保数据一致性和线程安全的工具。常见的同步原语包括：

1. **互斥锁（Mutex）**
2. **读写锁（RWMutex）**
3. **等待组（WaitGroup）**
4. **条件变量（Cond）**
5. **一次性操作（Once）**
6. **原子操作（Atomic Operations）**
7. **信号量（Semaphore）**

### Go中的常见同步原语

#### 1. 互斥锁（Mutex）

互斥锁用于确保在同一时间只有一个Goroutine访问共享资源。

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

#### 2. 读写锁（RWMutex）

读写锁允许多个读操作并发执行，但写操作是独占的。

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

#### 3. 等待组（WaitGroup）

等待组用于等待一组Goroutine完成。

```go
package main

import (
	"fmt"
	"sync"
)

func worker(id int, wg *sync.WaitGroup) {
	defer wg.Done()
	fmt.Printf("Worker %d starting\n", id)
	// 模拟工作
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

#### 4. 条件变量（Cond）

条件变量用于阻塞和唤醒Goroutine，适用于复杂的同步场景。

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

#### 5. 一次性操作（Once）

一次性操作用于确保某个操作只执行一次。

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

#### 6. 原子操作（Atomic Operations）

原子操作用于对单个变量进行原子操作，避免使用锁的开销。

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

#### 7. 信号量（Semaphore）

Go标准库没有直接提供信号量的实现，但可以通过`sync.Cond`和`sync.Mutex`等原语实现信号量。

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

### 小结

Go语言提供了多种同步原语，方便开发者在并发编程中实现线程安全和数据一致性。根据不同的需求，可以选择合适的同步原语来实现并发控制，从而编写出高效、可靠的并发程序。