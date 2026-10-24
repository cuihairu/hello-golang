Go's scheduler decides which `goroutine` runs on which `M`; what it manages is `goroutine` scheduling, context switching, and resource allocation. Here it's laid out in three parts — components, working process, and optimization — with code.

### 1. Internal structure of the Go scheduler

#### 1.1 Main components

- **`G` (Goroutine)**: Represents a `goroutine`, containing the information about its execution context, such as the stack and program counter.
- **`M` (Machine)**: Represents an OS thread, used to actually run `goroutine`s.
- **`P` (Processor)**: Represents a logical processor, the unit that schedules `goroutine`s. Each `P` maintains a run queue holding `goroutine`s waiting to run.

#### 1.2 Data structures

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

### 2. How the scheduler works

#### 2.1 Creating and destroying `goroutine`s

- **Creating a `goroutine`**:

When the `go` keyword launches a new `goroutine`, the Go runtime creates a `G` object and places it into the run queue of some `P`. If no `P` is available, it may be placed into the system queue.

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

- **Destroying a `goroutine`**:

When a `goroutine` finishes executing or is cancelled, the scheduler cleans up the associated resources.

```go
func destroyGoroutine(g *g) {
    // Clean up the goroutine's stack and other resources
    freeStack(g.stack)
    // Remove the goroutine from the run queue if necessary
}
```

#### 2.2 Scheduling and context switching

- **Scheduling**:

The scheduler periodically takes a `goroutine` from each `P`'s run queue and assigns it to an idle `M` thread for execution.

```go
func schedule(p *p) {
    g := p.runq.pop() // Get the next goroutine from the run queue
    if g != nil {
        p.m.curg = g // Assign the goroutine to the OS thread
        executeGoroutine(g)
    }
}
```

- **Context switching**:

A `goroutine` context switch involves saving and restoring the `goroutine`'s registers and stack.

```go
func contextSwitch(g1 *g, g2 *g) {
    saveContext(g1) // Save the context of the current goroutine
    loadContext(g2) // Load the context of the new goroutine
}
```

#### 2.3 Preemptive scheduling

- **Preemption**:

The scheduler periodically preempts running `goroutine`s to prevent one `goroutine` from holding the CPU for too long.

```go
func checkPreemption() {
    current := getCurrentGoroutine()
    if needsPreemption(current) {
        // Preempt the current goroutine and reschedule it
        rescheduleGoroutine(current)
    }
}
```

- **Scheduling period**:

The scheduler sets a scheduling period (usually a few milliseconds); at the end of each period it checks the currently running `goroutine` and decides whether a context switch is needed.

```go
func schedulerTick() {
    for {
        time.Sleep(schedulingInterval) // Wait for the scheduling interval
        checkPreemption() // Check if preemption is needed
    }
}
```

#### 2.4 Handling blocking and waiting

- **Blocking**:

When a `goroutine` is waiting on some resource or operation (for example waiting to send or receive on a `channel`), the scheduler removes it from the run queue.

```go
func blockGoroutine(g *g) {
    g.status = blocked // Mark the goroutine as blocked
    // Move the goroutine to the waiting queue
    moveToWaitingQueue(g)
}
```

- **Waiting queue**:

Blocked `goroutine`s are placed into the waiting queue. When a resource becomes available, the scheduler checks the waiting queue and reschedules those `goroutine`s.

```go
func unblockGoroutine(g *g) {
    if isResourceAvailable() {
        g.status = runnable
        p := getAvailableP()
        p.runq.push(g) // Add the goroutine back to the run queue
    }
}
```

#### 2.5 Work stealing

- **Work stealing**:

The scheduler uses a work-stealing algorithm to balance load. A busy `P` can steal `goroutine`s from a less busy `P`.

```go
func stealWork(fromP *p, toP *p) {
    if !fromP.runq.isEmpty() {
        g := fromP.runq.pop()
        toP.runq.push(g) // Move the goroutine to the other processor's queue
    }
}
```

### 3. Scheduler optimization and tuning

#### 3.1 GOMAXPROCS

- **GOMAXPROCS**:

Concurrency can be tuned with the `runtime.GOMAXPROCS` function or an environment variable. `GOMAXPROCS` controls the number of logical processors `P` running Go code simultaneously, i.e. the maximum parallelism for running `goroutine`s; it does not limit the total number of OS threads `M` — when an `M` blocks on a system call or cgo, the runtime automatically creates or reuses a new `M`.

```go
runtime.GOMAXPROCS(4) // set the number of logical processors P executing Go code simultaneously to 4
```

#### 3.2 Scheduler performance

- **Scheduler optimizations**:

The scheduler keeps overhead down with three things: work stealing spreads a busy `P`'s work to an idle `P`; preemption stops one `goroutine` from monopolizing the CPU; and when an `M` blocks on a system call or cgo, the runtime creates or reuses an `M`, so the `goroutine` doesn't get stuck with it.

### Summary

The scheduler's skeleton is the three-tier G, M, P: `G` is the `goroutine`, `M` is the OS thread, and `P` holds the run queue. `GOMAXPROCS` sets how many `P`s run Go code at the same time; it doesn't govern the number of `M`s. Work stealing and preemption solve the two problems of uneven load and CPU monopolization, respectively.

## References

- [Effective Go · Concurrency](https://go.dev/doc/effective_go#concurrency)
- [Go memory model](https://go.dev/ref/mem)
- [sync standard library](https://pkg.go.dev/sync)
- [Official · Go scheduler design doc (golang.org/s/go11sched)](https://golang.org/s/go11sched)
- [runtime standard library](https://pkg.go.dev/runtime)
- [Official blog · Go runtime: 4 years later](https://go.dev/blog/go119runtime)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
