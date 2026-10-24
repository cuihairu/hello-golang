# netpoll

`netpoll` is a Go library for handling high-concurrency network I/O. Built on I/O multiplexing, it manages network events efficiently. `netpoll`'s design is inspired by I/O multiplexing mechanisms such as `epoll` and `kqueue` on Unix. With `netpoll` you can manage a large number of network connections in a single thread, cutting down on context switches and lock contention and improving the system's concurrency.

### How `netpoll` Works

`netpoll` uses the Reactor model. The Reactor model is an event-driven design pattern that centralizes the handling of all I/O events in one place, improving system efficiency. In Go, `netpoll` is implemented in `runtime/netpoll.go`, and its core is based on `epoll` (Linux) or `kqueue` (the BSD family, including macOS).

Specifically, `netpoll`'s workflow is:

1. **Event registration**: register a network connection's file descriptor (fd) with `epoll` or `kqueue`, specifying the events you care about (read, write, exceptional, etc.).
2. **Event polling**: a dedicated goroutine polls for events. This goroutine calls `epoll_wait` or `kqueue`, waiting for events to occur.
3. **Event dispatch**: when an event fires, `netpoll` dispatches it to the appropriate handler.

### `netpoll` and Goroutines

The interplay between Go's goroutines and `netpoll` is key to its high concurrency. `netpoll` ties network I/O operations to goroutines and delivers:

1. **Non-blocking I/O**: `netpoll` achieves non-blocking I/O through I/O multiplexing, meaning a goroutine waiting on network I/O does not block other goroutines from running.
2. **Event-driven**: `netpoll` combines I/O events with goroutines through an event-driven model. When a network event occurs, the corresponding goroutine is woken up to handle it.
3. **Efficient scheduling**: Go's runtime scheduler manages goroutine scheduling efficiently. When `netpoll` polls an event, it can switch quickly to the corresponding goroutine to process it, reducing the cost of context switches.


## Source Code Implementation

Go's `netpoll` is mainly implemented in `runtime/netpoll.go`; the core includes event polling, event registration and handling, and coordination with goroutine scheduling. The excerpts below are from the Go 1.27 source (with comments trimmed), and fields and signatures may vary slightly between versions.

### Core Data Structures

#### `pollDesc`

`pollDesc` is one of the core data structures in `netpoll`, used to describe a file descriptor for a network I/O operation. Every polled fd maps to a `pollDesc`, which records the goroutines waiting on the read and write sides along with timeout timers and so on.

```go
type pollDesc struct {
    _     sys.NotInHeap
    link  *pollDesc      // used by pollcache, protected by pollcache.lock
    fd    uintptr        // unchanged during the pollDesc's lifetime
    fdseq atomic.Uintptr // prevents use of a stale pollDesc

    atomicInfo atomic.Uint32 // atomically stores the summary bits of closing/rd/wd, for lock-free checks by netpollcheckerr

    // rg and wg are accessed atomically and hold g pointers:
    // pdReady (ready), pdWait (currently suspended), or the G waiting to read/write
    rg atomic.Uintptr // the goroutine waiting to read
    wg atomic.Uintptr // the goroutine waiting to write

    lock    mutex // protects the fields below
    closing bool
    rrun    bool      // whether the read timeout timer is running
    wrun    bool      // whether the write timeout timer is running
    user    uint32    // a cookie the user can set
    rseq    uintptr   // prevents stale read timers
    rt      timer     // read timeout timer
    rd      int64     // read timeout point (nanotime; -1 means expired)
    wseq    uintptr   // prevents stale write timers
    wt      timer     // write timeout timer
    wd      int64     // write timeout point
    self    *pollDesc // used for indirect interface storage; see (*pollDesc).makeArg
}
```

### Event Registration and Polling

Event registration and polling are the core functions of `netpoll`.

#### Event Registration

In `netpoll` (the Linux implementation is `runtime/netpoll_epoll.go`), registering events on a file descriptor is done through the `netpollopen` function:

```go
// netpollopen registers the fd with the epoll instance (source, Go 1.27)
func netpollopen(fd uintptr, pd *pollDesc) uintptr {
    var ev linux.EpollEvent
    ev.Events = linux.EPOLLIN | linux.EPOLLOUT | linux.EPOLLRDHUP | linux.EPOLLET
    tp := taggedPointerPack(unsafe.Pointer(pd), pd.fdseq.Load())
    *(*taggedPointer)(unsafe.Pointer(&ev.Data)) = tp
    return linux.EpollCtl(epfd, linux.EPOLL_CTL_ADD, int32(fd), &ev)
}
```

`netpollopen` internally calls `epollctl`, which ultimately performs the underlying `epoll_ctl` system call, adding the file descriptor to the `epoll` instance.

#### Event Polling

Event polling is implemented by the `netpoll` function. Note that its argument is a delay `delay` (in nanoseconds), not `block bool`:

```go
// netpoll checks for ready network connections (source signature, Go 1.27)
// returns a list of ready goroutines; delay < 0 means block forever, delay == 0 means non-blocking
func netpoll(delay int64) (gList, int32) {
    if epfd == -1 {
        return gList{}, 0
    }
    var waitms int32
    if delay < 0 {
        waitms = -1
    } else if delay == 0 {
        waitms = 0
    } else {
        waitms = int32(delay / 1e6) // convert to milliseconds
    }

    var events [128]linux.EpollEvent
retry:
    n, errno := linux.EpollWait(epfd, events[:], int32(len(events)), waitms)
    if errno != 0 {
        if errno != _EINTR {
            println("runtime: epollwait on fd", epfd, "failed with", errno)
            throw("runtime: netpoll failed")
        }
        goto retry
    }

    var toRun gList
    for i := int32(0); i < n; i++ {
        ev := events[i]
        if ev.Events == 0 {
            continue
        }
        var mode int32
        if ev.Events&(linux.EPOLLIN|linux.EPOLLRDHUP|linux.EPOLLHUP|linux.EPOLLERR) != 0 {
            mode += 'r'
        }
        if ev.Events&(linux.EPOLLOUT|linux.EPOLLHUP|linux.EPOLLERR) != 0 {
            mode += 'w'
        }
        if mode != 0 {
            // pull the pollDesc registered at event time out of event.Data (a taggedPointer since Go 1.26)
            tp := *(*taggedPointer)(unsafe.Pointer(&ev.Data))
            pd := (*pollDesc)(tp.pointer())
            tag := tp.tag()
            if pd.fdseq.Load() == tag {
                pd.setEventErr(ev.Events == linux.EPOLLERR, tag)
                netpollready(&toRun, pd, mode)
            }
        }
    }
    return toRun, 0
}
```

`epollwait` here wraps the underlying `epoll_wait` system call, waiting for I/O events. Once `epoll_wait` returns, `netpoll` iterates over every file descriptor that had an event and collects the goroutines that need to be woken into a `gList`, handing them to the scheduler to run.

### Coordinating with Goroutines

`netpoll` coordinates with goroutines through Go's scheduler. When `netpoll` detects that an I/O event has occurred, it wakes the corresponding goroutine to handle it.

#### Waking a Goroutine

When `netpoll` polls an event, it calls `netpollready` to put the goroutines blocked on that `pollDesc` into the runnable list:

```go
// netpollready puts the goroutines blocked waiting on an fd read/write event into toRun (source signature, Go 1.27)
// mode is 'r', 'w', or 'r'+'w'
func netpollready(toRun *gList, pd *pollDesc, mode int32) int32 {
    delta := int32(0)
    var rg, wg *g
    if mode == 'r' || mode == 'r'+'w' {
        rg = netpollunblock(pd, 'r', true, &delta)
    }
    if mode == 'w' || mode == 'r'+'w' {
        wg = netpollunblock(pd, 'w', true, &delta)
    }
    if rg != nil {
        toRun.push(rg)
    }
    if wg != nil {
        toRun.push(wg)
    }
    return delta
}
```

The scheduler (`findRunnable` and the like) calls `netpoll` periodically and injects the returned goroutine list into the run queue; `gList` is an internal doubly-linked list, and scheduler-internal functions such as `runqput`/`globrunqput` are responsible for placing these goroutines into local or global run queues, resuming the execution of goroutines that were blocked on I/O.

### Why Choose a Single Reactor Model

Looking at the source design, `netpoll` chooses a single Reactor model mainly for these reasons:

1. **Simpler implementation**: a single Reactor model is relatively simple to implement. All events are handled in one place, which makes the code easier to maintain and debug.
2. **Fewer context switches**: a single Reactor model reduces context switches between threads. All I/O operations happen in one thread, avoiding lock contention between threads.
3. **Makes full use of Go's scheduler**: Go's scheduler can manage a large number of goroutines, and as soon as an I/O event arrives it can dispatch it to the corresponding goroutine.
4. **Low resource overhead**: both thread count and context switches are kept down, so I/O-bound work gets more connections out of fewer resources.

Back to the code: `netpoll` does only three things — attach fds to `epoll`, wait for events, and shove the waiting goroutines back into the run queue. The blocking work is left to the scheduler; it can get by on a single thread.

## References

- [net standard library](https://pkg.go.dev/net)
- [net/http standard library](https://pkg.go.dev/net/http)
- [runtime source · netpoll.go](https://go.dev/src/runtime/netpoll.go)

## Sibling pages

- [Advanced](/net/Advanced.md)
- [Concurrence](/net/Concurrence.md)
- [Intro](/net/Intro.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Advanced](/net/Advanced.md)
- [Concurrence](/net/Concurrence.md)
- [Intro](/net/Intro.md)
- [Proto](/net/Proto.md)
