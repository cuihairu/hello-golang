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

Go 的 `netpoll` 主要在 `runtime/netpoll.go` 中实现，核心部分包括事件轮询（polling）、事件注册和处理、与 goroutine 的调度配合等。下面摘录的是 Go 1.27 源码（精简注释版），不同版本的字段和签名可能略有差异。

### 核心数据结构

#### `pollDesc`

`pollDesc` 是 `netpoll` 中的核心数据结构之一，用于描述一个网络 I/O 的文件描述符。每个被轮询的 fd 都对应一个 `pollDesc`，其中记录了读/写两侧正在等待的 goroutine 以及超时定时器等信息。

```go
type pollDesc struct {
    _     sys.NotInHeap
    link  *pollDesc      // 在 pollcache 中使用，由 pollcache.lock 保护
    fd    uintptr        // 在 pollDesc 生命周期内不变
    fdseq atomic.Uintptr // 防止使用已失效的 pollDesc

    atomicInfo atomic.Uint32 // 原子保存 closing/rd/wd 的摘要位，供 netpollcheckerr 免锁检查

    // rg、wg 原子访问，保存 g 指针：
    // pdReady（就绪）、pdWait（正在挂起）或正在等待读/写的 G
    rg atomic.Uintptr // 等待读的 goroutine
    wg atomic.Uintptr // 等待写的 goroutine

    lock    mutex // 保护以下字段
    closing bool
    rrun    bool      // 读超时定时器是否正在运行
    wrun    bool      // 写超时定时器是否正在运行
    user    uint32    // 用户可设置的 cookie
    rseq    uintptr   // 防止过期的读定时器
    rt      timer     // 读超时定时器
    rd      int64     // 读超时时间点（nanotime，-1 表示已过期）
    wseq    uintptr   // 防止过期的写定时器
    wt      timer     // 写超时定时器
    wd      int64     // 写超时时间点
    self    *pollDesc // 用于间接接口的存储，见 (*pollDesc).makeArg
}
```

### 事件注册和轮询

事件注册和轮询是 `netpoll` 的核心功能。

#### 事件注册

在 `netpoll` 中（Linux 实现 `runtime/netpoll_epoll.go`），注册一个文件描述符的事件是通过 `netpollopen` 函数完成的：

```go
// netpollopen 向 epoll 实例注册 fd（源码，Go 1.27）
func netpollopen(fd uintptr, pd *pollDesc) uintptr {
    var ev linux.EpollEvent
    ev.Events = linux.EPOLLIN | linux.EPOLLOUT | linux.EPOLLRDHUP | linux.EPOLLET
    tp := taggedPointerPack(unsafe.Pointer(pd), pd.fdseq.Load())
    *(*taggedPointer)(unsafe.Pointer(&ev.Data)) = tp
    return linux.EpollCtl(epfd, linux.EPOLL_CTL_ADD, int32(fd), &ev)
}
```

这里的 `netpollopen` 内部调用了 `epollctl`，最终执行底层的 `epoll_ctl` 系统调用，将文件描述符添加到 `epoll` 实例中。

#### 事件轮询

事件轮询是通过 `netpoll` 函数实现的。注意它的参数是延迟时间 `delay`（纳秒），而不是 `block bool`：

```go
// netpoll 检查就绪的网络连接（源码签名，Go 1.27）
// 返回就绪的 goroutine 列表；delay < 0 表示永久阻塞，delay == 0 表示非阻塞
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
        waitms = int32(delay / 1e6) // 换算为毫秒
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
            // 从 event.Data 中取出注册时的 pollDesc（Go 1.26 起为 taggedPointer）
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

这里的 `epollwait` 封装了底层的 `epoll_wait` 系统调用，等待 I/O 事件的发生。`epoll_wait` 返回后，`netpoll` 会遍历所有发生事件的文件描述符，并把需要唤醒的 goroutine 收集到 `gList` 中，交由调度器执行。

### 与 goroutine 的配合

`netpoll` 与 goroutine 的配合是通过 Go 的调度器实现的。当 `netpoll` 检测到 I/O 事件发生时，会唤醒相应的 goroutine 进行处理。

#### 唤醒 goroutine

当 `netpoll` 轮询到事件时，会调用 `netpollready` 函数把等待在该 `pollDesc` 上的 goroutine 放入待运行列表：

```go
// netpollready 把因等待 fd 读/写事件而阻塞的 goroutine 放入 toRun（源码签名，Go 1.27）
// mode 为 'r'、'w' 或 'r'+'w'
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

调度器（`findRunnable` 等）会定期调用 `netpoll`，将返回的 goroutine 列表注入运行队列；`gList` 是运行时内部的双向链表，`runqput`/`globrunqput` 等调度器内部函数负责把这些 goroutine 放入本地或全局运行队列，从而恢复被 I/O 阻塞的 goroutine 的执行。

### 为什么选择单一 Reactor 模型

从源码的设计可以看出，`netpoll` 选择单一 Reactor 模型主要有以下几个原因：

1. **简化实现**：单一 Reactor 模型的实现相对简单。所有事件集中在一个地方处理，代码维护和调试更加容易。
2. **减少上下文切换**：单一 Reactor 模型可以减少线程间的上下文切换。所有 I/O 操作在一个线程中处理，避免了多线程之间的锁竞争。
3. **充分利用 Go 的调度器**：Go 的调度器能管理大量 goroutine，I/O 事件一到就能分发给对应的 goroutine 处理。
4. **资源开销小**：线程数量和上下文切换都省下来，I/O 密集型任务里用更少的资源扛住更多连接。

回到代码：`netpoll` 只做三件事，把 fd 挂到 `epoll` 上、等事件、把等着的 goroutine 塞回运行队列。阻塞的活交给调度器，它自己一个线程就够。