# Concurrency
Go's concurrency model evolved from the influence of Erlang, the Actor model, and CSP (Communicating Sequential Processes).

### 1. Evolution of the Concurrency Model

#### 1.1 Erlang and the Actor Model

Erlang is a functional language originally designed for telecom systems, and its concurrency is built on the Actor model, which emphasizes isolation and message passing. The Actor model was proposed by Carl Hewitt and treats computation as a set of independent Actors: each Actor holds its own state and behavior, communicates with others through asynchronous messages, and does not directly share memory, thereby avoiding the race conditions and complex synchronization problems caused by shared state. This model suits high-concurrency and distributed systems.

#### 1.2 CSP (Communicating Sequential Processes)

CSP was proposed by Tony Hoare and emphasizes that processes communicate through message passing rather than shared memory. Processes are sequentially executing units of computation that interact by sending and receiving messages over pipes (channels); the way they interact and synchronize is therefore clearly defined, sidestepping the complexity of shared memory and locks.

### 2. Go's Concurrency Model

Go's concurrency model comes mainly from CSP, and also incorporates ideas from the Actor model, landing on two primitives: `goroutine` and `channel`.

#### 2.1 Goroutine

`goroutine` is Go's unit of concurrent execution, a kind of lightweight thread. The scheduler maps them onto a small number of OS threads, and the `go` keyword starts one with a single write. Its stack starts at a very small initial size and grows automatically as needed, so the memory overhead of a single `goroutine` is small.

#### 2.2 Channel

`channel` is the mechanism for communication and synchronization between `goroutine`s: safely sending and receiving data on it gets rid of the need for explicit locks and shared-memory problems. It comes in two modes, buffered and unbuffered; when both sides are not ready at the same time, send and receive block each other, and that is the synchronization semantics of a `channel`.

#### 2.3 Select Statement

`select` lets a `goroutine` wait on several `channel` operations at once, and when more than one is ready it picks one at random to run; multiplexing and timeouts both rely on it.

#### 2.4 The Scheduler

Go's scheduler is an M:N model: M stands for OS threads, N stands for `goroutine`s. The scheduler maps many `goroutine`s onto a small number of OS threads, scheduling with strategies such as work stealing and preemption (including signal-based asynchronous preemption), while also managing the creation, destruction, and context switching of `goroutine`s.

### 3. The CSP Model and Go's Concurrency Model

#### 3.1 Core Ideas of the CSP Model

In CSP, processes communicate by message passing and do not share memory; messages can be synchronous (send and receive happen at the same time) or asynchronous (sending does not wait for the receive to complete). Processes are sequentially executing units of computation that send and receive messages over pipes (channels) according to a defined protocol.

#### 3.2 The Relationship Between Go's Concurrency Model and CSP

The correspondence is: `channel` implements CSP's message passing, `goroutine` is similar to a CSP process (both are sequentially executing units of concurrency), and `select` corresponds to the CSP choice operation. The execution of these `goroutine`s is managed by Go's scheduler, and the process scheduling mechanism from CSP is implemented inside the scheduler.

### Summary

Go's concurrency model comes from CSP and the Actor model: `goroutine` is the unit of concurrent execution, `channel` handles communication and synchronization, and the scheduler maps many `goroutine`s onto a small number of OS threads. When writing concurrent programs, think through how data flows between `goroutine`s first: if it can be passed over a `channel`, don't share memory, and you save the locks too.

## References

- [Effective Go · Concurrency](https://go.dev/doc/effective_go#concurrency)
- [Go Memory Model](https://go.dev/ref/mem)
- [sync standard library](https://pkg.go.dev/sync)


## Sibling pages

- [Actor](/concurrency/Actor.md)
- [CSP](/concurrency/CSP.md)
- [Chan](/concurrency/Chan.md)
- [ChanImpl](/concurrency/ChanImpl.md)
- [ErrorGroup](/concurrency/ErrorGroup.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Actor](/concurrency/Actor.md)
