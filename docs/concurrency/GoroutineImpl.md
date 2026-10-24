Go's `goroutine` is a lightweight thread, underpinned at a lower level by the scheduler, stack management, and the runtime system.

### 1. Underlying Principles of `goroutine`

#### 1.1 Lightweight Threads

- **Cooperative scheduling primarily**: `goroutine` is a lightweight thread provided by the Go runtime system, scheduled at a lower level by Go's scheduler. Go's scheduler implements `goroutine` scheduling at the user level rather than relying on the OS thread scheduler, which allows `goroutine` to run more efficiently. Early Go scheduling relied on voluntary yielding at function call sites (cooperative scheduling); starting with Go 1.14, signal-based asynchronous preemption was introduced, ensuring that uncooperative goroutines can also be switched out.

- **Stack management**: `goroutine` uses a very small initial stack (usually only a few KB), a design that greatly reduces memory overhead. The Go runtime system automatically expands the stack size of a `goroutine` when needed, so a `goroutine` can handle complex recursive calls or deep operations while keeping a small memory footprint.

#### 1.2 Scheduler

- **M:N model**: Go uses an M:N scheduling model, where M stands for OS threads and N stands for `goroutine`. Multiple `goroutine`s can be scheduled onto a small number of OS threads; this design reduces thread-switching overhead and makes load balancing on multi-core CPUs easier.

- **Scheduler components**: Go's scheduler contains the following main components:
  - **`P` (Processor)**: represents a logical processor, responsible for executing `goroutine`. The scheduler decides how many `P`s there are based on the number of logical processors.
  - **`M` (Machine)**: represents an OS thread, responsible for executing the `goroutine` on a `P`. The scheduler dispatches `goroutine` onto `M`.
  - **`G` (Goroutine)**: represents a `goroutine`. Each `G` has its own stack and scheduling information.

- **Scheduling algorithm**: Go's scheduler uses a preemptive scheduling algorithm. `goroutine`s regularly rotate through time slices to ensure every `goroutine` gets execution time. The scheduler decides how to schedule `goroutine` based on its state (waiting, running, blocked, etc.).

### 2. Implementation Details of `goroutine`

#### 2.1 Stack Management

- **Initial stack**: every `goroutine` starts with a small initial stack (typically 2 KB). This small stack makes the cost of creating a `goroutine` very low.

- **Stack expansion**: when a `goroutine` needs more stack space, the Go runtime system automatically expands the stack. Stack expansion is done by copying the contents of the current stack into a larger memory region. This process is automatic and transparent to user code.

#### 2.2 Internal Structure of the Scheduler

- **Scheduling queues**: the scheduler maintains multiple queues to manage `goroutine`. The main ones are:
  - **Run queue**: holds `goroutine`s ready to execute.
  - **Wait queue**: holds `goroutine`s blocked waiting for I/O or other conditions.
  - **System queue**: holds `goroutine`s waiting for OS threads.

- **Work stealing**: the scheduler uses a work-stealing algorithm to balance load. Work stealing allows a busy `P` to steal `goroutine`s from other less busy `P`s, balancing the load and improving CPU utilization.

#### 2.3 Switching Between Threads and Coroutines

- **Context switching**: context switching for `goroutine` is far lighter than for OS threads, involving only user-level state save and restore, without going through the OS.

- **Preemption**: Go's scheduler periodically checks the state of `goroutine` and preempts, preventing individual `goroutine`s from holding the CPU for a long time.

### 3. Implementation Details and Examples

Below are some code examples and explanations of Go's `goroutine` implementation details (simplified pseudocode for clarity, not the real runtime source code; the actual implementation lives in files such as `runtime/proc.go`):

#### 3.1 Creating a `goroutine`

In Go, `goroutine` is created with the `go` keyword, which at a lower level actually calls relevant functions in the Go runtime:

```go
func newGoroutine(fn func()) *g {
    g := new(g)
    g.fn = fn
    g.stack = makeStack() // create the initial stack
    return g
}

func goStart(g *g) {
    // push goroutine g onto the scheduling queue
    sched.runQueue.push(g)
}
```

#### 3.2 Stack Expansion

When a `goroutine` needs more stack space, the Go runtime automatically expands the stack:

```go
func growStack(g *g) {
    oldStack := g.stack
    newStack := allocateNewStack()
    copyStack(oldStack, newStack)
    g.stack = newStack
}
```

#### 3.3 Scheduler Implementation

Inside the scheduler, multiple queues are maintained to manage the scheduling of `goroutine`:

```go
type Scheduler struct {
    runQueue queue.Queue // run queue
    waitQueue queue.Queue // wait queue
    mQueue queue.Queue // system queue
}

func (s *Scheduler) schedule() {
    // pop a goroutine from the run queue and execute it
    g := s.runQueue.pop()
    runGoroutine(g)
}
```

### Summary

Goroutines are cheap in two ways: the initial stack is only a few KB, so the creation cost is low; scheduling happens in user space, so switching doesn't trap into the OS. The M:N model then packs a large number of goroutines onto a small number of system threads, and it load-balances across multiple cores.

## References

- [Effective Go · Concurrency](https://go.dev/doc/effective_go#concurrency)
- [Go Memory Model](https://go.dev/ref/mem)
- [sync standard library](https://pkg.go.dev/sync)
- [Official · Go Scheduler Design Doc (golang.org/s/go11sched)](https://golang.org/s/go11sched)
- [runtime standard library](https://pkg.go.dev/runtime)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
