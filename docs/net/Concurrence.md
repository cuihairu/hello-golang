### 并发网络编程

#### 5.1 线程与进程

并发编程中，线程和进程是两个基本概念。线程是程序执行的最小单位，进程是程序的运行实例。

##### 5.1.1 线程的创建与管理

线程是轻量级的进程，可以共享进程的资源，如内存、文件描述符等。使用线程可以更高效地利用多核 CPU，提高并发处理能力。

**示例代码**：

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

##### 5.1.2 进程的创建与管理

进程是程序的执行实例，具有独立的地址空间。进程之间的通信通常需要使用 IPC（进程间通信）机制，如管道、信号、共享内存等。

**示例代码**（在 Unix 系统中）：

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

#### 5.2 使用线程池

线程池预先创建一定数量的线程，避免频繁创建和销毁线程的开销。

##### 5.2.1 线程池的概念

线程池是一组预先创建的线程，用来执行提交进来的任务。

##### 5.2.2 线程池的实现

线程池的实现通常包括任务队列、工作线程和线程管理器等组件。任务队列用于存储待处理的任务，工作线程从任务队列中获取任务并执行，线程管理器负责创建、销毁和管理工作线程。

**示例代码**：

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

#### 5.3 使用协程

协程是一种比线程更轻量级的并发编程技术，通过调度器在单个或多个线程上执行协程，从而实现并发执行。Go 语言中的协程称为 goroutine。

##### 5.3.1 协程的基本概念

协程是用户态的线程，由程序自行调度。协程切换的开销比线程和进程更低，适合用于高并发场景。

##### 5.3.2 协程的实现

协程的实现依赖于语言或库提供的调度器，如 Go 语言的 goroutine 调度器。调度器负责管理协程的创建、切换和销毁。

**示例代码**：

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

##### 5.3.3 协程在网络编程中的应用

协程在网络编程里最常见的用法是处理并发连接，一个连接开一个 goroutine，互不干扰，下面的例子就是这么写的。

**示例代码**：

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

### 结论

两个示例对应两条路：网络服务里每个连接开一个 goroutine，处理完就退出；线程池那节自己管任务队列和固定数量的工作线程。选哪条取决于任务是短命的连接还是长期复用的计算。