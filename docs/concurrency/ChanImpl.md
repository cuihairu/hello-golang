A channel is the mechanism for passing data between goroutines, and underneath it is built from an `hchan` struct, two wait queues, and a mutex.

### Basic concepts of Go channels

1. **Unbuffered and buffered channels**:
   - **Unbuffered channel**: sends and receives must complete synchronously. A send blocks until the receiver is ready, and vice versa.
   - **Buffered channel**: allows a certain number of elements to be held in a buffer. When the buffer is full, a send blocks; when the buffer is empty, a receive blocks.

2. **Communication mechanism**:
   - Channel communication is essentially synchronized access to shared memory, passing data via blocking and wake-up.

### Underlying implementation of Go channels

There are three core data structures:

1. **The `hchan` struct**:
   - `hchan` is the core data structure of a channel in Go, defined in the `runtime/chan.go` file.

```go
type hchan struct {
    qcount   uint           // number of elements currently in the queue
    dataqsiz uint           // size of the circular buffer
    buf      unsafe.Pointer // pointer to the circular buffer
    elemsize uint16         // size of each element
    closed   uint32         // whether the channel is closed
    sendx    uint           // index for the send operation
    recvx    uint           // index for the receive operation
    recvq    waitq          // queue of goroutines waiting to receive
    sendq    waitq          // queue of goroutines waiting to send
    lock     mutex          // mutex protecting the channel
}
```

2. **The `waitq` struct**:
   - The `waitq` struct holds the queue of waiting goroutines.

```go
type waitq struct {
    first *sudog // head pointer of the wait queue
    last  *sudog // tail pointer of the wait queue
}
```

3. **The `sudog` struct**:
   - A `sudog` represents a goroutine that is blocked on a channel operation.

```go
type sudog struct {
    g          *g          // the blocked goroutine
    elem       unsafe.Pointer // pointer to the element
    next       *sudog       // next sudog in the queue
    prev       *sudog       // previous sudog in the queue
}
```

### Send and receive operations

#### Send operation

1. **Unbuffered channel**:
   - The send checks whether there is a goroutine waiting to receive; if so, it passes the data directly to the receiver and wakes the receiver up.
   - If there is no waiting receiver, the sender is blocked until a receiver is ready.

2. **Buffered channel**:
   - The send checks whether the buffer is full. If it is not full, the data is stored in the buffer and the buffer count is incremented.
   - If the buffer is full, the sender is blocked until there is space in the buffer.

```go
func chansend(c *hchan, ep unsafe.Pointer, block bool) bool {
    // some code omitted...

    // take the lock
    lock(&c.lock)

    // if the channel is closed, panic
    if c.closed != 0 {
        unlock(&c.lock)
        panic(plainError("send on closed channel"))
    }

    // unbuffered channel: pass the data straight to the waiting receiver
    if c.dataqsiz == 0 {
        // check whether there is a goroutine waiting to receive
        if sg := c.recvq.dequeue(); sg != nil {
            // hand the data to the receiver
            recv(c, sg, ep)
            unlock(&c.lock)
            // wake the receiver up
            goready(sg.g)
            return true
        }
    } else {
        // buffered channel: check whether the buffer is full
        if c.qcount < c.dataqsiz {
            // store the data in the buffer
            typedmemmove(c.elemtype, c.buf+uintptr(c.sendx)*uintptr(c.elemsize), ep)
            c.sendx++
            if c.sendx == c.dataqsiz {
                c.sendx = 0
            }
            c.qcount++
            unlock(&c.lock)
            return true
        }
    }

    // if block is false, return directly
    if !block {
        unlock(&c.lock)
        return false
    }

    // block the sender
    sg := acquireSudog()
    sg.elem = ep
    c.sendq.enqueue(sg)
    goparkunlock(&c.lock, "chan send", traceEvGoBlockSend, 2)
    return true
}
```

#### Receive operation

1. **Unbuffered channel**:
   - The receive checks whether there is a goroutine waiting to send; if so, it takes the data directly and wakes the sender up.
   - If there is no waiting sender, the receiver is blocked until a sender is ready.

2. **Buffered channel**:
   - The receive checks whether the buffer is empty. If it is not empty, the data is taken out of the buffer and the buffer count is decremented.
   - If the buffer is empty, the receiver is blocked until the buffer has data.

```go
func chanrecv(c *hchan, ep unsafe.Pointer, block bool) (selected, received bool) {
    // some code omitted...

    // take the lock
    lock(&c.lock)

    // if the channel is closed, return directly
    if c.closed != 0 && c.qcount == 0 {
        unlock(&c.lock)
        return true, false
    }

    // unbuffered channel: take the data directly
    if c.dataqsiz == 0 {
        // check whether there is a goroutine waiting to send
        if sg := c.sendq.dequeue(); sg != nil {
            // receive the data
            recv(c, sg, ep)
            unlock(&c.lock)
            // wake the sender up
            goready(sg.g)
            return true, true
        }
    } else {
        // buffered channel: check whether the buffer is empty
        if c.qcount > 0 {
            // take the data out of the buffer
            recvDirect(c, ep)
            unlock(&c.lock)
            return true, true
        }
    }

    // if block is false, return directly
    if !block {
        unlock(&c.lock)
        return false, false
    }

    // block the receiver
    sg := acquireSudog()
    sg.elem = ep
    c.recvq.enqueue(sg)
    goparkunlock(&c.lock, "chan receive", traceEvGoBlockRecv, 2)
    return true, true
}
```

### Summary

Channel sends and receives go through the same lock: first check whether anyone in the peer wait queue is waiting, and if so hand the data to them and wake them up; if not, put yourself into the queue and yield the current goroutine. An unbuffered channel only has the queue handoff step, while a buffered channel writes to the circular buffer first and only parks on the queue once the buffer is full.

## References

- [Effective Go · Concurrency](https://go.dev/doc/effective_go#concurrency)
- [Go Memory Model](https://go.dev/ref/mem)
- [sync standard library](https://pkg.go.dev/sync)
- [runtime source · chan.go](https://go.dev/src/runtime/chan.go)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Concurrency](/concurrency/Concurrency.md)
- [glossary](/glossary.md)