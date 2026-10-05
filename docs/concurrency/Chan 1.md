# Go 语言中的通道 (Channel)

## 1.1 通道的基本语法与使用

### 1.1.1 通道的概念

通道（Channel）是 Go 语言中的一种核心数据结构，用于在不同的 Goroutine 之间进行通信。它通过传递数据来同步 Goroutine 的执行。

### 1.1.2 通道的声明与初始化

通道用 `make` 初始化：

```go
package main

import "fmt"

func main() {
    // 声明一个整型通道
    var c chan int

    // 使用 make 函数初始化通道
    c = make(chan int)

    // 也可以直接声明并初始化通道
    d := make(chan int)

    fmt.Println(c, d)
}
```

### 1.1.3 发送和接收数据

通道使用操作符 `<-` 进行数据的发送和接收：

```go
package main

import "fmt"

func main() {
    c := make(chan int, 1)

    // 发送数据到通道
    c <- 42

    // 从通道接收数据
    value := <-c
    fmt.Println(value)
}
```

放到 goroutine 里跑一遍：

```go
package main

import "fmt"

func main() {
    c := make(chan int)

    go func() {
        c <- 42
    }()

    value := <-c
    fmt.Println(value)
}
```

## 1.2 带缓冲和无缓冲通道的阻塞情况

### 1.2.1 无缓冲通道

无缓冲通道在发送和接收操作完成之前会一直阻塞，直到有对应的接收或发送操作：

```go
package main

import "fmt"

func main() {
    c := make(chan int)

    go func() {
        c <- 42 // 阻塞，直到 main goroutine 接收数据
    }()

    value := <-c // 接收数据，解除阻塞
    fmt.Println(value)
}
```

### 1.2.2 带缓冲通道

带缓冲通道允许在没有接收方的情况下发送一定数量的数据。缓冲区满时，发送操作会阻塞；缓冲区为空时，接收操作会阻塞：

```go
package main

import "fmt"

func main() {
    c := make(chan int, 2)

    c <- 1 // 不阻塞
    c <- 2 // 不阻塞

    go func() {
        c <- 3 // 阻塞，直到 main goroutine 接收数据
    }()

    fmt.Println(<-c) // 接收数据，解除阻塞
    fmt.Println(<-c)
    fmt.Println(<-c)
}
```

### 1.2.3 阻塞情况对比表格

| 通道类型 | 发送操作 | 接收操作 | 是否阻塞 |
|:--------:|:--------:|:--------:|:--------:|
| 无缓冲通道 | 发送数据 | 无接收方 | 阻塞 |
| 无缓冲通道 | 发送数据 | 有接收方 | 不阻塞 |
| 带缓冲通道 | 发送数据，缓冲区未满 | 无接收方 | 不阻塞 |
| 带缓冲通道 | 发送数据，缓冲区已满 | 无接收方 | 阻塞 |
| 带缓冲通道 | 接收数据，缓冲区非空 | 无发送方 | 不阻塞 |
| 带缓冲通道 | 接收数据，缓冲区为空 | 无发送方 | 阻塞 |

## 1.3 通道死锁及其解决

### 1.3.1 死锁的概念

死锁是指程序中的两个或多个 Goroutine 互相等待对方释放资源，导致程序无法继续执行。

### 1.3.2 死锁示例

把发送放在主 goroutine、又没有第二个 goroutine 来接收，主 goroutine 会永远阻塞在 `c <- 1`。Go 运行时检测到所有 goroutine 都在等待，会直接报 fatal error 退出：

```go
package main

func main() {
    c := make(chan int)
    c <- 1 // 死锁：主 Goroutine 阻塞在发送操作，没有其他 Goroutine 接收数据
}
```

运行输出：

```plaintext
fatal error: all goroutines are asleep - deadlock!

goroutine 1 [chan send]:
main.main()
```

（完整输出还带有 goroutine 堆栈的文件路径与行号。）

### 1.3.3 解决死锁的方法

#### 使用 Goroutine 进行接收

```go
package main

import "fmt"

func main() {
    c := make(chan int)

    go func() {
        c <- 1
    }()

    value := <-c
    fmt.Println(value)
}
```

#### 关闭通道

```go
package main

import "fmt"

func main() {
    c := make(chan int)

    go func() {
        c <- 1
        close(c)
    }()

    for val := range c {
        fmt.Println(val)
    }
}
```

#### 使用带缓冲通道

```go
package main

import "fmt"

func main() {
    c := make(chan int, 1)
    c <- 1
    fmt.Println(<-c)
}
```

#### 使用 `select` 语句

```go
package main

import "fmt"

func main() {
    c1 := make(chan int)
    c2 := make(chan int)

    go func() {
        c1 <- 1
    }()
    go func() {
        c2 <- 2
    }()

    select {
    case val := <-c1:
        fmt.Println("Received from c1:", val)
    case val := <-c2:
        fmt.Println("Received from c2:", val)
    }
}
```

## 1.4 通道的高阶用法

### 1.4.1 单向通道

单向通道把操作限制成只发或只收，参数类型声明成 `chan<-` 或 `<-chan`：

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

### 1.4.2 通道选择（select）

`select` 语句用于在多个通道操作中进行选择，类似于 `switch` 语句，但每个 `case` 语句必须是一个通道操作。`select` 语句的语法如下：

```go
package main

import "fmt"

func main() {
    c1 := make(chan int)
    c2 := make(chan int)

    go func() {
        c1 <- 1
    }()
    go func() {
        c2 <- 2
    }()

    select {
    case val := <-c1:
        fmt.Println("Received from c1:", val)
    case val := <-c2:
        fmt.Println("Received from c2:", val)
    }
}
```

### 1.4.3 超时控制

通道可以与 `select` 语句配合，实现超时控制：

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    c := make(chan int)

    select {
    case res := <-c:
        fmt.Println(res)
    case <-time.After(time.Second * 1):
        fmt.Println("timeout")
    }
}
```

## 1.5 通道与 Goroutine 的配合

### 1.5.1 工作池（Worker Pool）

通道常用来做工作池：主 goroutine 往 `jobs` 通道里塞任务，固定数量的 worker 从里面领活干：

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

### 1.5.2 通道与同步

通道也可以用于同步 Goroutine 的执行顺序：

```go
package main

import "fmt"

func main() {
    done := make(chan bool)

    go func() {
        fmt.Println("Goroutine running")
        done <- true
    }()

    <-done
    fmt.Println("Main function")
}
```