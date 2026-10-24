### Concurrent Network Programming

#### 5.1 Threads and Processes

In concurrent programming, threads and processes are the two fundamental concepts. A thread is the smallest unit of program execution, and a process is a running instance of a program.

##### 5.1.1 Creating and Managing Threads

Threads are lightweight processes that can share a process's resources, such as memory and file descriptors. Threads let you make better use of a multi-core CPU and improve concurrent processing.

**Sample code**:

```go
package main

import (
	"fmt"
	"time"
)

func printNumbers() {
	for i := 1; i <= 5; i++ {
		fmt.Println(i)
		time.Sleep(500 * time.Millisecond)
	}
}

func main() {
	go printNumbers()
	go printNumbers()
	time.Sleep(3 * time.Second)
}
```

##### 5.1.2 Creating and Managing Processes

A process is a running instance of a program with its own address space. Communication between processes usually needs an IPC (inter-process communication) mechanism, such as pipes, signals, or shared memory.

**Sample code** (on a Unix system):

```go
package main

import (
	"fmt"
	"os"
	"os/exec"
)

func main() {
	cmd := exec.Command("ls", "-l")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err := cmd.Run()
	if err != nil {
		fmt.Println("Error running command:", err)
	}
}
```

#### 5.2 Using a Thread Pool

A thread pool creates a fixed number of threads up front, avoiding the overhead of constantly creating and destroying threads.

##### 5.2.1 The Concept of a Thread Pool

A thread pool is a group of pre-created threads used to execute submitted tasks.

##### 5.2.2 Implementing a Thread Pool

A thread pool implementation usually includes a task queue, worker threads, and a thread manager. The task queue stores pending tasks; worker threads pull tasks from the queue and execute them; the thread manager handles creating, destroying, and managing worker threads.

**Sample code**:

```go
package main

import (
	"fmt"
	"sync"
)

type Task func()

type Worker struct {
	taskQueue chan Task
	wg        *sync.WaitGroup
}

func NewWorker(taskQueue chan Task, wg *sync.WaitGroup) *Worker {
	return &Worker{taskQueue: taskQueue, wg: wg}
}

func (w *Worker) Start() {
	go func() {
		for task := range w.taskQueue {
			task()
			w.wg.Done()
		}
	}()
}

type ThreadPool struct {
	taskQueue   chan Task
	workerCount int
	wg          *sync.WaitGroup
}

func NewThreadPool(workerCount int) *ThreadPool {
	taskQueue := make(chan Task)
	wg := &sync.WaitGroup{}
	pool := &ThreadPool{taskQueue: taskQueue, workerCount: workerCount, wg: wg}
	for i := 0; i < workerCount; i++ {
		worker := NewWorker(taskQueue, wg)
		worker.Start()
	}
	return pool
}

func (p *ThreadPool) Submit(task Task) {
	p.wg.Add(1)
	p.taskQueue <- task
}

func (p *ThreadPool) Wait() {
	p.wg.Wait()
	close(p.taskQueue)
}

func main() {
	pool := NewThreadPool(3)

	for i := 1; i <= 5; i++ {
		i := i
		pool.Submit(func() {
			fmt.Println("Task", i)
		})
	}

	pool.Wait()
}
```

#### 5.3 Using Goroutines

Goroutines are a lighter-weight concurrency mechanism than threads. A scheduler runs goroutines on one or more threads, achieving concurrent execution. In Go these are called goroutines.

##### 5.3.1 Basic Concepts of Goroutines

A goroutine is a user-space thread scheduled by the program itself. Switching between goroutines is cheaper than switching between threads or processes, which makes them a good fit for high-concurrency scenarios.

##### 5.3.2 Implementing Goroutines

A goroutine implementation depends on a scheduler provided by the language or a library, such as Go's goroutine scheduler. The scheduler manages creating, switching, and destroying goroutines.

**Sample code**:

```go
package main

import (
	"fmt"
	"time"
)

func printNumbers() {
	for i := 1; i <= 5; i++ {
		fmt.Println(i)
		time.Sleep(500 * time.Millisecond)
	}
}

func main() {
	go printNumbers()
	go printNumbers()
	time.Sleep(3 * time.Second)
}
```

##### 5.3.3 Goroutines in Network Programming

The most common use of goroutines in network programming is handling concurrent connections: one goroutine per connection, each independent of the others. The example below is written that way.

**Sample code**:

```go
package main

import (
	"bufio"
	"fmt"
	"net"
)

func handleConnection(conn net.Conn) {
	defer conn.Close()
	reader := bufio.NewReader(conn)
	for {
		message, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("Error reading:", err)
			return
		}
		fmt.Printf("Received: %s\n", message)

		response := "ACK\n"
		_, err = conn.Write([]byte(response))
		if err != nil {
			fmt.Println("Error writing:", err)
			return
		}
	}
}

func main() {
	ln, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Println("Error listening:", err)
		return
	}
	defer ln.Close()

	for {
		conn, err := ln.Accept()
		if err != nil {
			fmt.Println("Error accepting:", err)
			continue
		}
		go handleConnection(conn)
	}
}
```

### Conclusion

The two examples map to two paths: in a network service you spawn one goroutine per connection and it exits once handled; in the thread pool section you manage your own task queue and a fixed number of worker threads. Which one you pick depends on whether the work is short-lived connections or long-running reusable computation.

## References

- [net standard library](https://pkg.go.dev/net)
- [net/http standard library](https://pkg.go.dev/net/http)

## Sibling pages

- [Advanced](/net/Advanced.md)
- [Intro](/net/Intro.md)
- [Netpoll](/net/Netpoll.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Advanced](/net/Advanced.md)
- [Intro](/net/Intro.md)
- [Netpoll](/net/Netpoll.md)
- [Proto](/net/Proto.md)
- [SlidingWindow](/net/SlidingWindow.md)
- [Socket](/net/Socket.md)
