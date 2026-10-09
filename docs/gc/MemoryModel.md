# Go 内存模型：什么时候一个 goroutine 能看到另一个的写

内存模型回答的是一个具体问题：A goroutine 改了变量，B goroutine 什么时候保证读到新值。官方文档 `/ref/mem` 是唯一权威，本仓此前只在首页提过这个词。内容取自官方页面，抓取于 2026-10-08。

## 一、官方开头的三句劝告

原文 Advice 一节写得很直白：

1. 同时被多个 goroutine 修改的数据必须串行访问，用 channel 操作或 `sync`、`sync/atomic` 里的同步原语保护。
2. 如果读完这份文档才能看懂自己程序的行为，那就是想多了。原话是 If you must read the rest of this document to understand the behavior of your program, you are being too clever. Don't be clever.

所以先给结论：不加同步就共享可变数据，读到什么都可能；加了同步，按下面的规则推。

## 二、几个定义

- **数据竞争**：对同一内存位置的写与另一个读或写同时发生，除非所有访问都是 `sync/atomic` 提供的原子访问。
- **DRF-SC**：没有数据竞争的 Go 程序，表现得就像所有 goroutine 复用在一个处理器上顺序执行。这个性质叫 data-race-free programs execute in a sequentially consistent manner。
- **实现的底线**：实现可以随时报告竞争并终止程序；除此之外，对单字或子字内存位置的每次读，必须观察到确实写入且尚未被覆盖的值。官方把这层约束描述为「更像 Java 或 JavaScript，而不是 C/C++」，因为在 C/C++ 里有竞争的程序含义完全未定义。

## 三、同步规则（原文的 Happens before 规则）

| 场景 | 保证 |
| --- | --- |
| 包初始化 | `q` 的所有 init 函数执行完，早于导入 `q` 的包 `p` 的任意 init 函数开始；所有 init 执行完，早于 `main.main` 开始 |
| 启动 goroutine | `go` 语句早于该 goroutine 的执行开始 |
| goroutine 退出 | **没有任何保证**。官方给的反例是退出前给全局变量赋值，其他 goroutine 不一定看得到，激进的编译器甚至可能删掉整条 `go` 语句 |
| channel 发送 | 某次发送早于对应那次接收的完成 |
| channel 关闭 | 关闭早于因通道关闭而返回零值的那次接收 |
| 无缓冲 channel 的接收 | 该接收早于对应那次发送的完成 |
| 缓冲 channel | 容量为 C 的通道，第 k 次接收早于第 k+C 次发送的完成（计数信号量可以这样建模） |
| 锁 | 对任意 `sync.Mutex` 或 `sync.RWMutex` 变量 `l` 与 `n < m`，第 `n` 次 `l.Unlock()` 早于第 `m` 次 `l.Lock()` 返回 |
| `sync.Once` | `once.Do(f)` 里 `f` 的那次执行完成，早于任何一次 `once.Do(f)` 的返回 |

`docs/concurrency/Chan.md` 讲的「发送方写完再被接收方读到」，底层依据就是表里 channel 那三行；`goroutine 退出无保证` 那一行则是 `docs/concurrency/` 里所有「等 goroutine 干完活再看结果」写法的理由。

## 四、形式化定义的骨架

官方的正式定义跟着 Boehm 与 Adve 2008 年 PLDI 论文《Foundations of the C++ Concurrency Memory Model》的路线走。三条需求：

1. 每个 goroutine 内的内存操作，要能对应到该 goroutine 的一次正确顺序执行，与语言规范里控制流结构规定的 sequenced before 关系一致。
2. 把映射限制到同步操作上时，必须能由同步操作的某个隐式全序解释，且这个全序与顺序、与读写到的值一致。
3. 普通读 `r` 读到的写 `w` 必须对它可见：`w` happens before `r`，并且不存在另一个 happens before `r` 的写 `w'` 也 happens before `w`……也就是取最新那个可见写。

读类操作包括读、原子读、mutex 加锁、channel 接收；写类操作包括写、原子写、mutex 解锁、channel 发送与关闭；原子比较并交换两边都算。

## 五、什么时候需要读这一页

- 写无锁的单例、懒初始化、状态机，却没用 `sync/atomic` 或 `sync.Once`。
- 用 goroutine 退出当「干完了」的信号，没有 channel 或 `WaitGroup` 等待。
- 缓冲 channel 当队列用，还假设「收到就等于对方已经写完内存」。

前两条按表里的规则直接判错，第三条要看容量：第 k 次接收只保证早于第 k+C 次发送。

## 来源

1. https://golang.google.cn/ref/mem — The Go Memory Model：Advice、Informal Overview、Synchronization 各小节与三条 Requirement（2026-10-08 抓取）
2. https://golang.google.cn/ref/spec — 语言规范中的表达式求值顺序（Requirement 1 引用）
