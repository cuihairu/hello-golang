# 并发编程
Go 的并发模型受 Erlang、Actor 模型和 CSP（Communicating Sequential Processes）影响演化而来。

### 1. 并发模型的演化历史

#### 1.1 Erlang 和 Actor 模型

Erlang 是函数式语言，最初为电信系统设计，它的并发建立在 Actor 模型上，强调隔离和消息传递。Actor 模型由 Carl Hewitt 提出，把计算看作一组独立的 Actor：每个 Actor 持有自己的状态和行为，通过异步消息互相通信，而不直接共享内存，由此避开了共享状态导致的竞态条件和复杂的同步问题。这种模型适合高并发和分布式系统。

#### 1.2 CSP（Communicating Sequential Processes）

CSP 由 Tony Hoare 提出，强调进程之间用消息传递通信，而不是共享内存。进程是顺序执行的计算单元，通过在管道（channels）上收发消息来交互；交互和同步的方式因此有明确定义，绕开了内存共享和锁的复杂性。

### 2. Go 的并发模型

Go 的并发模型主要来自 CSP，也结合了 Actor 模型的思想，落点是 `goroutine` 和 `channel` 两个原语。

#### 2.1 Goroutine

`goroutine` 是 Go 的并发执行单元，一种轻量级的线程。调度器把它映射到少量操作系统线程上，`go` 关键字一写就能启动。它的栈从很小的初始值开始，按需自动扩展，单个 `goroutine` 的内存开销因此很小。

#### 2.2 Channel

`channel` 是 `goroutine` 之间通信和同步的机制：在它上面安全地收发数据，就省掉了显式的锁和共享内存问题。它分缓冲和非缓冲两种模式；两边没同时准备好时，发送和接收互相阻塞，这就是 `channel` 的同步语义。

#### 2.3 Select 语句

`select` 让 `goroutine` 同时等多个 `channel` 操作，多个都就绪时随机挑一个执行，多路复用和超时都靠它。

#### 2.4 调度器

Go 的调度器是 M:N 模型：M 代表操作系统线程，N 代表 `goroutine`。调度器把多个 `goroutine` 映射到少量操作系统线程上，用工作窃取与抢占（含基于信号的异步抢占）等策略调度，同时管 `goroutine` 的创建、销毁和上下文切换。

### 3. CSP 模型和 Go 的并发模型

#### 3.1 CSP 模型的核心思想

CSP 里的进程靠消息传递通信，不共享内存；消息可以同步（收发同时发生），也可以异步（发送不等接收完成）。进程是顺序执行的计算单元，按定义好的协议经由管道（channels）收发消息。

#### 3.2 Go 的并发模型与 CSP 的关系

对应关系是：`channel` 实现 CSP 的消息传递，`goroutine` 与 CSP 的进程类似（都是顺序执行的并发单元），`select` 对应 CSP 的选择操作。这些 `goroutine` 的执行由 Go 的调度器管理，CSP 中的进程调度机制在调度器内部实现。

### 总结

Go 的并发模型来自 CSP 和 Actor 模型：`goroutine` 是并发执行单元，`channel` 负责通信和同步，调度器把多个 `goroutine` 映射到少量操作系统线程上。写并发程序时先想清楚数据在 `goroutine` 之间怎么流动：能通过 `channel` 传递就不共享内存，锁也就省了。
