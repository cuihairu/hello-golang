Go 语言中的通道（channel）是 goroutine 之间传递数据的机制，读写操作本身也能起到同步作用。

### 基本概念

- **无缓冲通道（Unbuffered Channel）**：一个无缓冲通道的发送操作会阻塞，直到有一个对应的接收操作来接收数据，反之亦然。
- **有缓冲通道（Buffered Channel）**：一个有缓冲通道允许发送方在缓冲区未满时发送数据，而不会立即阻塞。接收方在缓冲区不为空时可以接收数据，而不会立即阻塞。

### 创建通道

使用 `make` 函数创建通道：
- 无缓冲通道：`ch := make(chan int)`
- 有缓冲通道：`ch := make(chan int, 10)`  // 容量为 10

只声明不初始化的通道是零值 `nil`。对 nil 通道发送和接收都会永久阻塞，`close` 它会 panic（见下文关闭一节）。

### 发送和接收

- 发送：`ch <- value`
- 接收：`value := <-ch`

### 阻塞行为

无缓冲通道的发送要等接收方就位，接收要等发送方就位；带缓冲通道在缓冲区有空位时不阻塞发送，有数据时不阻塞接收。逐条列出来：

| 通道类型 | 操作 | 对端状态 | 是否阻塞 |
| --- | --- | --- | --- |
| 无缓冲 | 发送 | 有接收方 | 不阻塞 |
| 无缓冲 | 发送 | 无接收方 | 阻塞 |
| 无缓冲 | 接收 | 有发送方 | 不阻塞 |
| 无缓冲 | 接收 | 无发送方 | 阻塞 |
| 带缓冲 | 发送 | 缓冲区未满 | 不阻塞 |
| 带缓冲 | 发送 | 缓冲区已满 | 阻塞 |
| 带缓冲 | 接收 | 缓冲区非空 | 不阻塞 |
| 带缓冲 | 接收 | 缓冲区为空 | 阻塞 |

### 关闭通道

使用 `close` 关闭通道：`close(ch)`

```go
if c == nil {  
    panic(plainError("close of nil channel"))  
}  
  
lock(&c.lock)  
if c.closed != 0 {  
    unlock(&c.lock)  
    panic(plainError("close of closed channel"))  
}
```
##### 关闭未初始化的通道

从上面的源码可以看到，通道没有初始化时关闭它会 panic。

##### 多次关闭通道

在 Go 语言中，尝试关闭一个已经关闭的通道会导致运行时错误（panic）。因此，不能安全地多次关闭同一个通道。

```go
package main

func main() {
    ch := make(chan int)

    close(ch) // 第一次关闭
    close(ch) // 第二次关闭，会引发 panic
}
```

运行上述代码会引发以下错误：

```
panic: close of closed channel
```

##### 如何避免多次关闭通道

避免重复关闭有两种做法：用 `sync.Once` 保证关闭只执行一次，或者用 `recover` 兜住 panic（见下文）。

##### 使用 `sync.Once`

`sync.Once` 确保某个操作只执行一次：

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    var once sync.Once
    ch := make(chan int)

    closeChannel := func() {
        once.Do(func() {
            close(ch)
            fmt.Println("Channel closed")
        })
    }

    closeChannel() // 第一次关闭
    closeChannel() // 再次调用不会关闭通道
}
```

##### 使用检查机制

检查通道是否已经关闭，可以通过 `recover` 来捕获 `panic`：

```go
package main

import (
    "fmt"
)

func safeClose(ch chan int) (closed bool) {
    defer func() {
        if r := recover(); r != nil {
            closed = true
        }
    }()
    close(ch)
    return false
}

func main() {
    ch := make(chan int)

    fmt.Println("Closing channel first time:", safeClose(ch)) // 输出：Closing channel first time: false
    fmt.Println("Closing channel second time:", safeClose(ch)) // 输出：Closing channel second time: true
}
```

在这个示例中，`safeClose` 函数通过 `recover` 捕获 `panic` 并返回一个布尔值，表示通道是否已经关闭。


### 死锁

发送和接收没有配对时，等待的一方会被永远挂住。主 goroutine 发了一个没人收的值，运行时检测到所有 goroutine 都在睡眠，直接报 fatal error 退出：

```go
package main

func main() {
    c := make(chan int)
    c <- 1 // 阻塞在发送上，没有其他 goroutine 来接收
}
```

运行输出：

```plaintext
fatal error: all goroutines are asleep - deadlock!

goroutine 1 [chan send]:
main.main()
```

（完整输出还带 goroutine 堆栈的文件路径与行号。）

解法就是让收发配对：把发送放进另一个 goroutine，或者给通道加缓冲，或者用 `select` 在多个操作之间换道，或者用 `range` 消费完再退出。这些写法上文各节都有。

### 通道操作示例

```go
package main

import "fmt"

func main() {
    // 创建一个无缓冲通道
    ch := make(chan int)

    // 启动一个 goroutine 发送数据到通道
    go func() {
        ch <- 42
    }()

    // 从通道接收数据
    value := <-ch
    fmt.Println("Received:", value)
}
```

### `select` 语句

`select` 语句用于在多个通道操作中进行选择，类似于 `switch` 语句，但专门用于处理通道。

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    ch1 := make(chan int)
    ch2 := make(chan int)

    go func() {
        time.Sleep(1 * time.Second)
        ch1 <- 1
    }()

    go func() {
        time.Sleep(2 * time.Second)
        ch2 <- 2
    }()

    select {
    case msg1 := <-ch1:
        fmt.Println("Received from ch1:", msg1)
    case msg2 := <-ch2:
        fmt.Println("Received from ch2:", msg2)
    case <-time.After(3 * time.Second):
        fmt.Println("Timeout")
    }
}
```

### 使用 `defer` 关闭通道

在函数返回之前关闭通道，可以使用 `defer` 关键字：

```go
package main

import "fmt"

func main() {
    ch := make(chan int, 10)

    defer close(ch) // 确保函数结束前关闭通道

    for i := 0; i < 10; i++ {
        ch <- i
    }

    for i := 0; i < 10; i++ {
        fmt.Println(<-ch)
    }
}
```

### 单向通道

类型写成 `chan<- int` 的通道只能发送，写成 `<-chan int` 的只能接收。函数参数用单向类型，可以限定调用方只能收或只能发：

```go
package main

import "fmt"

func sendOnly(c chan<- int) {
    c <- 1
}

func receiveOnly(c <-chan int) {
    fmt.Println(<-c)
}

func main() {
    c := make(chan int)
    go sendOnly(c)
    receiveOnly(c)
}
```

双向通道可以隐式转成单向，反过来不行。

### 范例：生产者-消费者模式

```go
package main

import (
    "fmt"
    "sync"
)

func producer(ch chan int, wg *sync.WaitGroup) {
    for i := 0; i < 10; i++ {
        ch <- i
    }
    close(ch)
    wg.Done()
}

func consumer(ch chan int, wg *sync.WaitGroup) {
    for value := range ch {
        fmt.Println("Received:", value)
    }
    wg.Done()
}

func main() {
    ch := make(chan int, 10)
    var wg sync.WaitGroup

    wg.Add(1)
    go producer(ch, &wg)

    wg.Add(1)
    go consumer(ch, &wg)

    wg.Wait()
}
```

### 范例：工作池

固定数量的 worker 从同一个 `jobs` 通道领任务，结果写进 `results` 通道，主 goroutine 收结果：

```go
package main

import (
    "fmt"
    "time"
)

func worker(id int, jobs <-chan int, results chan<- int) {
    for j := range jobs {
        fmt.Printf("Worker %d started job %d\n", id, j)
        time.Sleep(time.Second)
        fmt.Printf("Worker %d finished job %d\n", id, j)
        results <- j * 2
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)

    for w := 1; w <= 3; w++ {
        go worker(w, jobs, results)
    }

    for j := 1; j <= 5; j++ {
        jobs <- j
    }
    close(jobs)

    for a := 1; a <= 5; a++ {
        fmt.Println(<-results)
    }
}
```

`close(jobs)` 之后，worker 的 `range` 循环在任务取完时自动结束。

### 底层实现原理

Go 通道的实现在 `runtime` 包里，核心是下面这个 `hchan` 结构和两组等待队列。

1. **数据结构**：通道的核心数据结构定义在 `runtime/chan.go` 中，主要包括一个队列用于存储数据项、一个队列用于等待发送的 goroutine 和一个队列用于等待接收的 goroutine。

2. **同步机制**：通道操作的同步机制依赖于 `mutex` 和 `sudog` 结构体，`mutex` 用于保护通道的数据结构，`sudog` 用于表示等待发送或接收的 goroutine。

3. **操作过程**：
   - 发送操作：发送操作会将数据项放入队列，如果队列已满则阻塞，等待有空间时继续。
   - 接收操作：接收操作会从队列中取出数据项，如果队列为空则阻塞，等待有数据时继续。
   - `select` 语句：在多个通道操作之间选一个就绪的操作执行。

以下是通道核心数据结构的简化示例：

```go
type hchan struct {
    qcount   uint           // 队列中的数据项数量
    dataqsiz uint           // 队列的大小
    buf      unsafe.Pointer // 环形队列缓冲区
    elemsize uint16         // 元素的大小
    closed   uint32         // 通道是否已关闭

    sendx    uint   // 发送索引
    recvx    uint   // 接收索引
    recvq    waitq  // 等待接收的 goroutine 队列
    sendq    waitq  // 等待发送的 goroutine 队列
    lock     mutex  // 保护通道的互斥锁
}
```

`hchan` 由一把互斥锁保护，待发送的 goroutine 挂在 `sendq`、待接收的挂在 `recvq`，阻塞和唤醒都围绕这两条队列发生。