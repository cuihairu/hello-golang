A channel in Go is the mechanism for passing data between goroutines, and the send and receive operations themselves also provide synchronization.

### Basic concepts

- **Unbuffered channel**: a send on an unbuffered channel blocks until a matching receive takes the value, and vice versa.
- **Buffered channel**: a buffered channel lets a sender send without immediately blocking while the buffer is not full, and a receiver receive without immediately blocking while the buffer is not empty.

### Creating a channel

Use `make` to create a channel:
- Unbuffered: `ch := make(chan int)`
- Buffered: `ch := make(chan int, 10)`  // capacity 10

A channel that is declared but not initialized has the zero value `nil`. Sending to and receiving from a nil channel blocks forever, and `close` on it panics (see the closing section below).

### Sending and receiving

- Send: `ch <- value`
- Receive: `value := <-ch`

### Blocking behavior

A send on an unbuffered channel waits for the receiver to be ready, and a receive waits for the sender to be ready; a buffered channel does not block a send while there is space in the buffer, and does not block a receive while there is data in it. Laid out case by case:

| Channel type | Operation | Peer status | Blocks? |
| --- | --- | --- | --- |
| Unbuffered | Send | Receiver present | Does not block |
| Unbuffered | Send | No receiver | Blocks |
| Unbuffered | Receive | Sender present | Does not block |
| Unbuffered | Receive | No sender | Blocks |
| Buffered | Send | Buffer not full | Does not block |
| Buffered | Send | Buffer full | Blocks |
| Buffered | Receive | Buffer not empty | Does not block |
| Buffered | Receive | Buffer empty | Blocks |

### Closing a channel

Use `close` to close a channel: `close(ch)`

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
##### Closing an uninitialized channel

From the source above you can see that closing a channel that was never initialized panics.

##### Closing a channel more than once

In Go, attempting to close a channel that is already closed causes a runtime error (panic). So you cannot safely close the same channel more than once.

```go
package main

func main() {
    ch := make(chan int)

    close(ch) // first close
    close(ch) // second close, causes a panic
}
```

Running the code above produces this error:

```
panic: close of closed channel
```

##### How to avoid closing a channel more than once

There are two ways to avoid closing twice: use `sync.Once` to guarantee that the close runs only once, or use `recover` to catch the panic (see below).

##### Using `sync.Once`

`sync.Once` ensures that an operation runs only once:

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

    closeChannel() // first close
    closeChannel() // calling again will not close the channel
}
```

##### Using a check

To check whether a channel is already closed, you can use `recover` to catch the `panic`:

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

    fmt.Println("Closing channel first time:", safeClose(ch)) // prints: Closing channel first time: false
    fmt.Println("Closing channel second time:", safeClose(ch)) // prints: Closing channel second time: true
}
```

In this example, the `safeClose` function uses `recover` to catch the `panic` and returns a boolean indicating whether the channel was already closed.


### Deadlock

When sends and receives are not paired, the waiting side hangs forever. The main goroutine sends a value that nobody receives, the runtime detects that every goroutine is asleep, and exits with a fatal error:

```go
package main

func main() {
    c := make(chan int)
    c <- 1 // blocks on the send, no other goroutine to receive
}
```

Running output:

```plaintext
fatal error: all goroutines are asleep - deadlock!

goroutine 1 [chan send]:
main.main()
```

(The full output also carries the file path and line number of the goroutine stack.)

The fix is to pair sends and receives: move the send into another goroutine, or add a buffer to the channel, or use `select` to switch between several operations, or use `range` to drain the channel before exiting. All of these patterns appear in the earlier sections.

### Channel operation example

```go
package main

import "fmt"

func main() {
    // create an unbuffered channel
    ch := make(chan int)

    // start a goroutine to send data to the channel
    go func() {
        ch <- 42
    }()

    // receive data from the channel
    value := <-ch
    fmt.Println("Received:", value)
}
```

### The `select` statement

The `select` statement is used to choose among multiple channel operations, much like the `switch` statement, but specifically for channels.

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

### Closing a channel with `defer`

To close a channel before a function returns, you can use the `defer` keyword:

```go
package main

import "fmt"

func main() {
    ch := make(chan int, 10)

    defer close(ch) // ensure the channel is closed before the function returns

    for i := 0; i < 10; i++ {
        ch <- i
    }

    for i := 0; i < 10; i++ {
        fmt.Println(<-ch)
    }
}
```

### One-way channels

A channel typed as `chan<- int` can only send, and one typed as `<-chan int` can only receive. Using one-way types in function parameters restricts the caller to either sending or receiving:

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

A two-way channel can be implicitly converted to a one-way channel, but not the other way around.

### Example: producer-consumer pattern

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

### Example: worker pool

A fixed number of workers pull jobs from the same `jobs` channel, write results into the `results` channel, and the main goroutine collects the results:

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

After `close(jobs)`, the workers' `range` loops finish on their own once the jobs are drained.

### Underlying implementation

Go's channel implementation lives in the `runtime` package, and the core is the `hchan` struct below plus two sets of wait queues.

1. **Data structure**: the channel's core data structure is defined in `runtime/chan.go`, and mainly consists of a queue for holding data items, a queue for goroutines waiting to send, and a queue for goroutines waiting to receive.

2. **Synchronization mechanism**: channel operations rely on the `mutex` and `sudog` structs for synchronization. The `mutex` protects the channel's data structure, and a `sudog` represents a goroutine waiting to send or receive.

3. **Operation process**:
   - Send: the send operation places the data item into the queue; if the queue is full it blocks until there is space.
   - Receive: the receive operation takes a data item out of the queue; if the queue is empty it blocks until there is data.
   - `select`: picks one ready operation among several channel operations.

Here is a simplified view of the channel's core data structure:

```go
type hchan struct {
    qcount   uint           // number of items in the queue
    dataqsiz uint           // size of the queue
    buf      unsafe.Pointer // circular buffer
    elemsize uint16         // size of each element
    closed   uint32         // whether the channel is closed

    sendx    uint   // send index
    recvx    uint   // receive index
    recvq    waitq  // queue of goroutines waiting to receive
    sendq    waitq  // queue of goroutines waiting to send
    lock     mutex  // mutex protecting the channel
}
```

`hchan` is guarded by a mutex; goroutines waiting to send hang on `sendq`, those waiting to receive hang on `recvq`, and both blocking and wake-up revolve around those two queues.

## References

- [Effective Go · Concurrency](https://go.dev/doc/effective_go#concurrency)
- [Go Memory Model](https://go.dev/ref/mem)
- [sync standard library](https://pkg.go.dev/sync)
- [Language Spec · Channel types](https://go.dev/ref/spec#Channel_types)
- [Language Spec · Receive operator](https://go.dev/ref/spec#Receive_operator)
- [Go Memory Model · Channel synchronization](https://go.dev/ref/mem#chan)
- [Effective Go · Channels](https://go.dev/doc/effective_go#channels)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Concurrency](/concurrency/Concurrency.md)
- [glossary](/glossary.md)