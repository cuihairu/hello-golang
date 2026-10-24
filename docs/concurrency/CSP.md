### The CSP Model in Depth

#### 1. Introduction to CSP

CSP (Communicating Sequential Processes) is a concurrency model proposed by the British mathematician Tony Hoare in 1978. It argues for organizing concurrency through message passing between processes instead of shared memory. Go's goroutines and channels are the CSP model in practice.

CSP abstracts the unit of concurrent execution into a process; processes talk to each other by sending messages over channels and never share memory.

#### 2. Components of the CSP Model

1. **Process**: an independently executing concurrent entity, similar to a thread or coroutine. Each process runs its own code on its own.
2. **Channel**: the medium through which processes pass messages. Through a channel a process can send and receive messages, giving you either synchronous or asynchronous communication.

#### 3. How the CSP Model Works

You create new processes to get concurrency, and from then on the only two actions are: the sender writes a message into a channel, and the receiver reads it out. Reads and writes can be synchronous, completing only when both sides are ready; or they can use a buffered channel, where the sender does not wait for the receiver.

#### 4. Pros and Cons of the CSP Model

**Pros**:

- Intuitive model: communication happens at both ends of a channel, so when reading code you can follow the channel to find both sender and receiver.
- No shared memory and no locks, which avoids the race conditions and deadlocks that shared memory brings.
- The channel abstraction is not bound to process boundaries; swap it for network communication and you can scale to distributed scenarios.

**Cons**:

- Messages must be copied and scheduled, so frequent passing has overhead.
- In scenarios that demand high throughput, that overhead becomes a bottleneck.

#### 5. Where the CSP Model Applies

- **High-concurrency systems**: network servers, real-time data processing systems.
- **Event-driven systems**: GUI event handling, asynchronous task scheduling.
- **Distributed systems**: distributed computing over network communication.

#### 6. A CSP Model Example

A Go example dispatching tasks with a channel:

```go
package main

import (
	"fmt"
	"time"
)

// the worker function simulates a concurrent task
func worker(id int, jobs <-chan int, results chan<- int) {
	for j := range jobs {
		fmt.Printf("Worker %d started job %d\n", id, j)
		time.Sleep(time.Second) // simulate the work taking a while
		fmt.Printf("Worker %d finished job %d\n", id, j)
		results <- j * 2 // send back the result
	}
}

func main() {
	const numJobs = 5
	jobs := make(chan int, numJobs)
	results := make(chan int, numJobs)

	// launch 3 worker goroutines
	for w := 1; w <= 3; w++ {
		go worker(w, jobs, results)
	}

	// send 5 jobs
	for j := 1; j <= numJobs; j++ {
		jobs <- j
	}
	close(jobs)

	// collect the results
	for a := 1; a <= numJobs; a++ {
		<-results
	}
}
```

The example launches 3 worker goroutines to process 5 jobs: jobs are handed out through the `jobs` channel, each worker picks up a job, does the work, and writes its result into `results`; main exits once it has collected all 5 results.

#### 7. Comparing CSP with Other Concurrency Models

- **Against the Actor model**: the CSP model emphasizes passing messages through channels, while the Actor model emphasizes concurrency through message passing and independent Actor entities. CSP is simpler and more direct, better for communication between processes, while the Actor model is more flexible and better suited to complex concurrent and distributed systems.
- **Against the thread model**: the traditional thread model uses locks and shared state for concurrency, which makes deadlocks and race conditions likely. The CSP model avoids these problems through message passing, giving you safe and simple concurrent programming.

#### 8. Conclusion

CSP splits the unit of concurrency and the communication medium into two separate things, and Go implements it with goroutines and channels. When you write a concurrent program, first draw the data flow as "who sends, who receives," then decide how many goroutines to start.

## References

- [Effective Go · Concurrency](https://go.dev/doc/effective_go#concurrency)
- [Go Memory Model](https://go.dev/ref/mem)
- [sync standard library](https://pkg.go.dev/sync)
- [Hoare 1978 · Communicating Sequential Processes (original CACM paper DOI)](https://dl.acm.org/doi/10.1145/359576.359585)
- [CSP overview (Wikipedia)](https://en.wikipedia.org/wiki/Communicating_sequential_processes)
- [Official blog · Go Concurrency Patterns: Pipelines](https://go.dev/blog/pipelines)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Concurrency](/concurrency/Concurrency.md)
- [glossary](/glossary.md)
