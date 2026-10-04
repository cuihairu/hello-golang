Go 的调度器决定哪个 `goroutine` 在哪个 `M` 上跑，管的是 `goroutine` 的调度、上下文切换和资源分配。下面按组件、工作过程、优化三部分拆开讲，配代码说明。

### 1. Go 调度器的内部结构

#### 1.1 主要组件

- **`G`（Goroutine）**：代表一个 `goroutine`，包含了执行上下文的信息，比如栈、程序计数器等。
- **`M`（Machine）**：代表操作系统线程，用于实际执行 `goroutine`。
- **`P`（Processor）**：代表逻辑处理器，调度 `goroutine` 的工作单位。每个 `P` 维护一个运行队列，存放待执行的 `goroutine`。

#### 1.2 数据结构

```go
// Goroutine structure
type g struct {
    stack      stack // Goroutine's stack
    status     int   // Goroutine's status (running, waiting, etc.)
    sched       bool // Indicates if the goroutine is scheduled
}

// Machine structure
type m struct {
    g0 *g         // Initial goroutine for the thread
    curg *g       // Currently running goroutine
    p *p          // Associated processor
    // ... other fields
}

// Processor structure
type p struct {
    runq queue     // Queue for runnable goroutines
    m *m           // Associated OS thread
    // ... other fields
}

// Queue for runnable goroutines
type queue struct {
    head *g
    tail *g
}
```

### 2. 调度器的工作原理

#### 2.1 创建和销毁 `goroutine`

- **创建 `goroutine`**：

当调用 `go` 关键字启动新的 `goroutine` 时，Go 运行时系统会创建一个 `G` 对象并将其放入某个 `P` 的运行队列中。如果没有可用的 `P`，则可能会将其放入系统队列中。

```go
func newGoroutine(fn func()) *g {
    g := &g{
        stack: makeStack(),
        status: runnable, // Mark as runnable
    }
    // Initialize the goroutine with the function to execute
    g.stack = initStack(fn)
    return g
}

func startGoroutine(g *g) {
    p := getAvailableP() // Get an available processor
    p.runq.push(g)      // Add the goroutine to the processor's run queue
}
```

- **销毁 `goroutine`**：

当 `goroutine` 执行完毕或被取消时，调度器会清理相关资源。

```go
func destroyGoroutine(g *g) {
    // Clean up the goroutine's stack and other resources
    freeStack(g.stack)
    // Remove the goroutine from the run queue if necessary
}
```

#### 2.2 调度和上下文切换

- **调度**：

调度器周期性地从每个 `P` 的运行队列中取出一个 `goroutine`，将其分配给空闲的 `M` 线程执行。

```go
func schedule(p *p) {
    g := p.runq.pop() // Get the next goroutine from the run queue
    if g != nil {
        p.m.curg = g // Assign the goroutine to the OS thread
        executeGoroutine(g)
    }
}
```

- **上下文切换**：

`goroutine` 的上下文切换涉及到保存和恢复 `goroutine` 的寄存器和栈。

```go
func contextSwitch(g1 *g, g2 *g) {
    saveContext(g1) // Save the context of the current goroutine
    loadContext(g2) // Load the context of the new goroutine
}
```

#### 2.3 抢占式调度

- **抢占**：

调度器会定期对正在运行的 `goroutine` 进行抢占，以防止某个 `goroutine` 长时间占用 CPU。

```go
func checkPreemption() {
    current := getCurrentGoroutine()
    if needsPreemption(current) {
        // Preempt the current goroutine and reschedule it
        rescheduleGoroutine(current)
    }
}
```

- **调度周期**：

调度器设置了一个调度周期（通常是几毫秒），在每个周期结束时，调度器会检查当前正在运行的 `goroutine` 并决定是否需要进行上下文切换。

```go
func schedulerTick() {
    for {
        time.Sleep(schedulingInterval) // Wait for the scheduling interval
        checkPreemption() // Check if preemption is needed
    }
}
```

#### 2.4 处理阻塞和等待

- **阻塞**：

当 `goroutine` 在等待某些资源或操作时（例如等待 `channel` 发送或接收），调度器会将其从运行队列中移除。

```go
func blockGoroutine(g *g) {
    g.status = blocked // Mark the goroutine as blocked
    // Move the goroutine to the waiting queue
    moveToWaitingQueue(g)
}
```

- **等待队列**：

阻塞的 `goroutine` 会被放入等待队列中。调度器会在资源变得可用时，检查等待队列并重新调度这些 `goroutine`。

```go
func unblockGoroutine(g *g) {
    if isResourceAvailable() {
        g.status = runnable
        p := getAvailableP()
        p.runq.push(g) // Add the goroutine back to the run queue
    }
}
```

#### 2.5 工作窃取

- **工作窃取**：

调度器使用工作窃取算法来平衡负载。一个忙碌的 `P` 可以从其他较空闲的 `P` 中窃取 `goroutine`。

```go
func stealWork(fromP *p, toP *p) {
    if !fromP.runq.isEmpty() {
        g := fromP.runq.pop()
        toP.runq.push(g) // Move the goroutine to the other processor's queue
    }
}
```

### 3. 调度器的优化和调整

#### 3.1 GOMAXPROCS

- **GOMAXPROCS**：

通过 `runtime.GOMAXPROCS` 函数或环境变量设置可以调整并发度。`GOMAXPROCS` 控制的是同时执行 Go 代码的逻辑处理器 `P` 的数量，也就是同时运行 `goroutine` 的最大并行度；它并不限制操作系统线程 `M` 的总数——当 `M` 因系统调用或 cgo 而阻塞时，运行时会自动创建或复用新的 `M`。

```go
runtime.GOMAXPROCS(4) // 设置同时执行 Go 代码的逻辑处理器 P 的数量为 4
```

#### 3.2 调度器性能

- **调度器优化**：

调度器用三件事压住开销：工作窃取把忙 `P` 的活分给闲 `P`；抢占防止某个 `goroutine` 长时间占着 CPU；`M` 被系统调用或 cgo 阻塞时，运行时新建或复用 `M`，`goroutine` 不跟着卡住。

### 总结

调度器的骨架是 G、M、P 三层：`G` 是 `goroutine`，`M` 是操作系统线程，`P` 挂着运行队列。`GOMAXPROCS` 定的是同时执行 Go 代码的 `P` 有多少个，`M` 的数量不受它管。工作窃取和抢占分别解决负载不均和独占 CPU 两个问题。