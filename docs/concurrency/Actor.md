### The Actor Model in Depth

#### 1. Introduction to the Actor Model

The Actor model is a mathematical model for concurrent computation, first proposed by Carl Hewitt in 1973. It abstracts the basic unit of computation in a system as an Actor; each Actor is an independent entity that interacts with others by passing messages. The Actor model is a great fit for building high-concurrency and distributed systems.

**Core idea**: each Actor is an independent, concurrent entity that communicates only by passing messages, which avoids the shared state and locks of traditional concurrent programming.

#### 2. Components of the Actor Model

1. **Actor**: the basic unit of computation. Every Actor has its own state and behavior; it can receive and handle messages, create new Actors, and send messages to other Actors.
2. **Message**: the only way Actors communicate. Messages are asynchronous; the sender does not have to wait for the receiver to finish processing.
3. **Mailbox**: every Actor has a mailbox that holds the messages it receives.

#### 3. How the Actor Model Works

1. **Sending a message**: an Actor communicates with other Actors by sending them messages.
2. **Receiving a message**: an Actor receives messages from its mailbox and handles them according to their type.
3. **Updating state**: an Actor can update its internal state based on the messages it receives.
4. **Creating new Actors**: an Actor can create new Actors as needed.

#### 4. Pros and Cons of the Actor Model

**Pros**:

- **Concurrency**: the Actor model supports concurrency by design; every Actor can run concurrently and independently.
- **Distributed systems**: Actors can be spread across different nodes and communicate by passing messages, which suits building distributed systems.
- **Fault tolerance**: an Actor can handle errors on its own without affecting the execution of other Actors.

**Cons**:

- **Message passing overhead**: frequent message passing can carry real overhead.
- **Debugging difficulty**: because communication between Actors is asynchronous, debugging concurrency problems can be quite hard.

#### 5. Where the Actor Model Applies

- **High-concurrency systems**: chat systems, real-time data processing systems.
- **Distributed systems**: microservice architectures, cloud computing platforms.
- **Game development**: game servers, real-time multiplayer games.

#### 6. An Actor Model Example

```go
package main

import (
	"fmt"
	"time"
)

// message definition
type Message interface{}

// Actor interface definition
type Actor interface {
	Receive(msg Message)
}

// SimpleActor is a simple Actor implementation
type SimpleActor struct {
	id      int
	mailbox chan Message
}

// NewSimpleActor creates a new SimpleActor
func NewSimpleActor(id int) *SimpleActor {
	return &SimpleActor{
		id:      id,
		mailbox: make(chan Message, 10),
	}
}

// Receive receives and handles a message
func (a *SimpleActor) Receive(msg Message) {
	switch msg := msg.(type) {
	case string:
		fmt.Printf("Actor %d received message: %s\n", a.id, msg)
	case int:
		fmt.Printf("Actor %d received number: %d\n", a.id, msg)
	default:
		fmt.Printf("Actor %d received unknown message\n", a.id)
	}
}

// Send sends a message
func (a *SimpleActor) Send(msg Message) {
	a.mailbox <- msg
}

// Start launches the Actor
func (a *SimpleActor) Start() {
	go func() {
		for msg := range a.mailbox {
			a.Receive(msg)
		}
	}()
}

func main() {
	actor1 := NewSimpleActor(1)
	actor2 := NewSimpleActor(2)

	actor1.Start()
	actor2.Start()

	actor1.Send("Hello, Actor 1")
	actor2.Send(42)
	actor1.Send("Another message for Actor 1")
	actor2.Send("Message for Actor 2")

	// give the goroutines some time to process messages
	time.Sleep(1 * time.Second)
}
```

In this example, we define a simple `SimpleActor`, where every `SimpleActor` has a `mailbox` for receiving messages and implements a `Receive` method to handle them. The `Send` method puts a message into the `mailbox`, and the `Start` method launches a goroutine to process messages.

#### 7. Comparing the Actor Model with Other Concurrency Models

- **Against CSP (Communicating Sequential Processes)**: the CSP model emphasizes passing messages through channels, while the Actor model emphasizes concurrency through message passing and independent Actor entities.
- **Against the thread model**: the traditional thread model uses locks and shared state for concurrency, which makes deadlocks and race conditions likely. The Actor model avoids these problems through message passing.

#### 8. Conclusion

The Actor model replaces shared state and locks with message passing: each Actor processes the messages in its own mailbox serially, so there is no shared-memory contention. The cost also comes from the messages. Passing them has overhead, and asynchronous communication makes concurrency problems harder to track down (see the pros and cons in section 4).

## References

- [Effective Go · Concurrency](https://go.dev/doc/effective_go#concurrency)
- [Go Memory Model](https://go.dev/ref/mem)
- [sync standard library](https://pkg.go.dev/sync)
- [Official codelab · Share Memory By Communicating](https://go.dev/blog/codelab-share)

## Sibling pages

- [Concurrency](/concurrency/Concurrency.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Concurrency](/concurrency/Concurrency.md)
- [glossary](/glossary.md)
