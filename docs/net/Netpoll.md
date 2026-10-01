# netpoll

`netpoll` 是 Go 语言的一个用于处理高并发网络 I/O 的库。它基于 I/O 多路复用技术，实现了高效的网络事件管理。`netpoll` 的设计灵感来源于 Unix 系统中的 `epoll`、`kqueue` 等 I/O 多路复用机制。通过 `netpoll`，可以在单个线程中管理大量的网络连接，减少上下文切换和锁竞争，提高系统的并发性能。

### `netpoll` 的工作原理

`netpoll` 采用了 Reactor 模型。Reactor 模型是一种事件驱动的设计模式，通过将所有 I/O 事件集中到一个地方进行处理，从而提高系统的效率。在 Go 中，`netpoll` 是通过 `runtime/netpoll.go` 实现的，它的核心是基于 `epoll`（Linux）或 `kqueue`（BSD 系列，包括 macOS）的。

具体来说，`netpoll` 的工作流程如下：

1. **事件注册**：将网络连接的文件描述符（file descriptor, fd）注册到 `epoll` 或 `kqueue` 中，指定关心的事件（如读、写、异常等）。
2. **事件轮询**：使用一个专门的 Goroutine 进行事件轮询（polling）。这个 Goroutine 调用 `epoll_wait` 或 `kqueue`，等待事件发生。
3. **事件分发**：当事件发生时，`netpoll` 将事件分发给相应的处理函数进行处理。

### `netpoll` 与协程的配合

Go 语言的协程（goroutine）与 `netpoll` 的配合是其高并发能力的关键。`netpoll` 将网络 I/O 操作与 goroutine 进行结合，实现了以下几点：

1. **非阻塞 I/O**：`netpoll` 通过 I/O 多路复用实现了非阻塞 I/O，这意味着一个 goroutine 在等待网络 I/O 时不会阻塞其他 goroutine 的执行。
2. **事件驱动**：`netpoll` 通过事件驱动模型将 I/O 事件与 goroutine 结合起来。当一个网络事件发生时，会唤醒对应的 goroutine 进行处理。
3. **高效调度**：Go 语言的运行时调度器（scheduler）能够高效地管理 goroutine 的调度。当 `netpoll` 轮询到事件时，可以快速切换到对应的 goroutine 进行处理，减少了上下文切换的开销。


## 源码实现

Go 的 `netpoll` 主要在 `runtime/netpoll.go` 中实现，核心部分包括事件轮询（polling）、事件注册和处理、与 goroutine 的调度配合等。

### 核心数据结构

首先，我们来看一下 `netpoll` 中的一些核心数据结构。

#### `pollDesc`

`pollDesc` 是 `netpoll` 中的核心数据结构之一，用于描述一个网络 I/O 的文件描述符。它包含了文件描述符的状态信息以及事件处理函数。

```go
type pollDesc struct {
    link    *pollDesc // link for list of ready descriptors
    wd      *pollWork // work descriptor
    locking int32     // 0 if unlocked, 1 if locked
}
```

#### `pollWork`

`pollWork` 结构体描述了一个具体的 I/O 操作。

```go
type pollWork struct {
    fd       int32 // file descriptor
    mask     int32 // event mask (what events we are interested in)
    user     uintptr // user data (usually a pointer to the pollDesc)
}
```

### 事件注册和轮询

事件注册和轮询是 `netpoll` 的核心功能之一。我们来看一下这些功能的实现。

#### 事件注册

在 `netpoll` 中，注册一个文件描述符的事件是通过 `netpollopen` 函数完成的。

```go
func netpollopen(fd uintptr, pd *pollDesc) int32 {
    // 使用 epoll 或 kqueue 注册文件描述符
    return epollctl(epfd, _EPOLL_CTL_ADD, int32(fd), &ev)
}
```

这里的 `epollctl` 函数调用了底层的 `epoll_ctl` 系统调用，将文件描述符添加到 `epoll` 实例中。

#### 事件轮询

事件轮询是通过 `netpoll` 函数实现的。

```go
func netpoll(block bool) *g {
    var waitms int64
    if block {
        waitms = -1 // block indefinitely
    } else {
        waitms = 0 // return immediately
    }

    var events [128]epollevent
    n := epollwait(epfd, &events[0], int32(len(events)), waitms)
    if n < 0 {
        if n != -_EINTR {
            throw("runtime: netpoll: epollwait failed")
        }
        return nil
    }

    var gp *g
    for i := int32(0); i < n; i++ {
        ev := &events[i]
        pd := *(**pollDesc)(unsafe.Pointer(&ev.data))
        if (ev.events & (_EPOLLIN | _EPOLLRDHUP | _EPOLLHUP | _EPOLLERR)) != 0 {
            pd.setEventErr(_POLLERR)
        } else if (ev.events & _EPOLLIN) != 0 {
            pd.setEventErr(_POLLIN)
        } else if (ev.events & _EPOLLOUT) != 0 {
            pd.setEventErr(_POLLOUT)
        } else {
            throw("runtime: netpoll: unexpected epoll event")
        }
    }
    return gp
}
```

这里的 `epollwait` 调用了底层的 `epoll_wait` 系统调用，等待 I/O 事件的发生。`epoll_wait` 返回后，`netpoll` 会遍历所有发生事件的文件描述符，并将事件分发给相应的 `pollDesc` 进行处理。

### 与 goroutine 的配合

`netpoll` 与 goroutine 的配合是通过 Go 的调度器实现的。当 `netpoll` 检测到 I/O 事件发生时，会唤醒相应的 goroutine 进行处理。

#### 唤醒 goroutine

当 `netpoll` 轮询到事件时，会调用 `netpollready` 函数来唤醒相应的 goroutine。

```go
func netpollready(gp *g, pd *pollDesc, mode int32) {
    if !runqput(gp) {
        globrunqput(gp)
    }
    wakep()
}
```

这里的 `runqput` 和 `globrunqput` 是 Go 调度器的内部函数，用于将 goroutine 放入本地或全局运行队列中。`wakep` 函数则用于唤醒一个处理器（P），以便调度器可以立即处理新的 goroutine。

### 为什么选择单一 Reactor 模型

从源码的设计可以看出，`netpoll` 选择单一 Reactor 模型主要有以下几个原因：

1. **简化实现**：单一 Reactor 模型的实现相对简单。所有事件集中在一个地方处理，代码维护和调试更加容易。
2. **减少上下文切换**：单一 Reactor 模型可以减少线程间的上下文切换。所有 I/O 操作在一个线程中处理，避免了多线程之间的锁竞争。
3. **充分利用 Go 的调度器**：Go 的调度器非常高效，可以管理大量的 goroutine。单一 Reactor 模型可以充分利用调度器的优势，将 I/O 事件快速分发给相应的 goroutine 进行处理。
4. **高效资源利用**：单一 Reactor 模型可以更好地利用系统资源，特别是在 I/O 密集型任务中。通过减少线程和上下文切换的开销，可以更高效地处理大量并发连接。

总之，`netpoll` 的设计充分利用了 Go 语言的特点和优势，通过单一 Reactor 模型实现了高效的网络 I/O 处理。通过深入理解其源码设计，可以更好地掌握 Go 在高并发网络编程中的应用。