# Concurrent Programming
Go's concurrency model evolved under the influence of Erlang, the Actor model, and CSP (Communicating Sequential Processes).

### 1. The evolution of concurrency models

#### 1.1 Erlang and the Actor model

Erlang is a functional language, originally designed for telecom systems. Its concurrency is built on the Actor model, which emphasizes isolation and message passing. The Actor model was proposed by Carl Hewitt and treats computation as a set of independent actors: each actor holds its own state and behavior, and they talk to each other through asynchronous messages instead of directly sharing memory. That sidesteps the race conditions and complex synchronization problems that shared state causes. This model suits high-concurrency and distributed systems.

#### 1.2 CSP (Communicating Sequential Processes)

CSP was proposed by Tony Hoare and emphasizes that processes communicate through message passing rather than shared memory. A process is a sequentially executing unit of computation; processes interact by sending and receiving messages over pipes (channels). The way interaction and synchronization happen is therefore clearly defined, which avoids the complexity of memory sharing and locks.

### 2. Go's concurrency model

Go's concurrency model comes mainly from CSP, with ideas from the Actor model folded in too, and it lands on two primitives: `goroutine` and `channel`.

#### 2.1 Goroutine

A `goroutine` is Go's unit of concurrent execution, a kind of lightweight thread. The scheduler maps it onto a small number of OS threads, and a single `go` keyword starts one. Its stack starts at a very small initial size and grows automatically on demand, so the memory cost of a single `goroutine` is small.

#### 2.2 Channel

A `channel` is the mechanism for communication and synchronization between `goroutine`s: sending and receiving data safely over it removes the need for explicit locks and the problems of shared memory. It comes in two modes, buffered and unbuffered; when both sides aren't ready at the same time, the send and the receive block each other. That is the synchronization semantics of a `channel`.

#### 2.3 The select statement

`select` lets a `goroutine` wait on multiple `channel` operations at once. When several are ready, it picks one at random to execute. Both multiplexing and timeouts rely on it.

#### 2.4 The scheduler

Go's scheduler is an M:N model: M stands for OS threads, N stands for `goroutine`s. The scheduler maps many `goroutine`s onto a small number of OS threads, dispatching them with strategies like work stealing and preemption (including signal-based asynchronous preemption), and it also manages `goroutine` creation, destruction, and context switching.

### 3. The CSP model and Go's concurrency model

#### 3.1 Core ideas of the CSP model

In CSP, processes communicate through message passing and don't share memory; messages can be synchronous (send and receive happen at the same time) or asynchronous (the send doesn't wait for the receive to complete). A process is a sequentially executing unit of computation, sending and receiving messages over pipes (channels) according to a defined protocol.

#### 3.2 How Go's concurrency model relates to CSP

The correspondence is: `channel` implements CSP's message passing, `goroutine` is analogous to a CSP process (both are sequentially executing units of concurrency), and `select` corresponds to CSP's choice operation. The execution of these `goroutine`s is managed by Go's scheduler, and the process-scheduling mechanism of CSP is implemented inside the scheduler.

### Summary

Go's concurrency model comes from CSP and the Actor model: `goroutine` is the unit of concurrent execution, `channel` handles communication and synchronization, and the scheduler maps many `goroutine`s onto a small number of OS threads. When you write concurrent code, think first about how data flows between `goroutine`s: if you can pass it through a `channel`, don't share memory, and you save the lock too.

## References

- [Effective Go · Concurrency](https://go.dev/doc/effective_go#concurrency)
- [Go Memory Model](https://go.dev/ref/mem)
- [sync standard library](https://pkg.go.dev/sync)


## Sibling pages

- [Actor](/zh/concurrency/Actor.md)
- [CSP](/zh/concurrency/CSP.md)
- [Chan](/zh/concurrency/Chan.md)
- [ChanImpl](/zh/concurrency/ChanImpl.md)
- [ErrorGroup](/zh/concurrency/ErrorGroup.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Actor](/zh/concurrency/Actor.md)
