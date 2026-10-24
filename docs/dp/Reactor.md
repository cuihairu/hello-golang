### The Reactor Pattern

#### 1. Introduction to the Reactor Pattern

The Reactor Pattern is a design pattern for handling concurrent I/O events, mainly used in network servers and event-driven systems.

**Core idea**: the Reactor Pattern separates handling of I/O events from dispatching of the events, letting the system respond quickly when an event occurs.

#### 2. Components of the Reactor Pattern

The Reactor Pattern typically consists of the following components:

1. **Event Demultiplexer**: watches for the occurrence of multiple I/O events. It waits for I/O events to happen and passes them to the Reactor.

2. **Reactor**: receives events from the Event Demultiplexer and dispatches them to the corresponding handlers.

3. **Event Handlers**: handle the specific I/O events. Depending on the event type, a handler performs the appropriate action, such as reading data or processing a request.

4. **Dispatcher**: dispatches events from the Reactor to the appropriate event handler. The Dispatcher can be part of the Reactor or a standalone component.

#### 3. How the Reactor Pattern Works

1. **Initialization**: create the Event Demultiplexer, the Reactor, and the event handlers.

2. **Registering events**: register event handlers with the Reactor, specifying which I/O events need handling.

3. **Waiting for events**: the Event Demultiplexer starts waiting for I/O events to occur.

4. **Event occurs**: when an I/O event occurs, the Event Demultiplexer passes the event to the Reactor.

5. **Event dispatching**: the Reactor receives the event and dispatches it to the corresponding event handler via the Dispatcher.

6. **Event handling**: the event handler performs the corresponding action, such as reading data or processing a request.

7. **Keep waiting**: the Event Demultiplexer goes back to waiting for new I/O events.

#### 4. Pros and cons of the Reactor Pattern

**Pros**:

- A handful of components can handle large numbers of concurrent I/O events, which suits network-server-style workloads.
- Event handlers can be added and removed dynamically; when the load changes, the waiting and dispatching logic needs no changes.

**Cons**:

- **Complexity**: implementation and debugging can be fairly involved, since you have to manage event dispatching and scheduling.
- **Resource usage**: every I/O event needs handling resources allocated to it, which can waste resources.

#### 5. Applications of the Reactor Pattern

Network programming and event-driven systems commonly use the Reactor Pattern, especially under high concurrency, for example:

- **Web servers**: handling large numbers of concurrent HTTP requests.
- **Real-time chat systems**: handling large volumes of user messages and connections.
- **Game servers**: handling concurrent actions from large numbers of players.

#### 6. Example code for the Reactor Pattern

Below is a simple example implementation of the Reactor Pattern, using Go's `net` package to simulate a basic event-driven server:

```go
package main

import (
	"fmt"
	"net"
	"os"
)

type EventHandler interface {
	Handle(conn net.Conn)
}

type EchoHandler struct{}

func (e *EchoHandler) Handle(conn net.Conn) {
	defer conn.Close()
	for {
		buffer := make([]byte, 1024)
		n, err := conn.Read(buffer)
		if err != nil {
			fmt.Println("Error reading:", err)
			return
		}
		fmt.Printf("Received: %s\n", string(buffer[:n]))
		conn.Write(buffer[:n])
	}
}

func main() {
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Println("Error starting server:", err)
		os.Exit(1)
	}
	defer listener.Close()

	fmt.Println("Server is listening on port 8080...")

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Error accepting connection:", err)
			continue
		}

		go func(c net.Conn) {
			handler := &EchoHandler{}
			handler.Handle(c)
		}(conn)
	}
}
```

#### 7. Reactor Pattern compared with other patterns

- **Proactor Pattern**: both Proactor and Reactor are event-driven patterns, but Proactor moves the handling of I/O operations out of the application and into the operating system, while Reactor relies on the application to handle the I/O events.
- **Observer Pattern**: the Observer Pattern is mainly for message passing and event notification between objects, while the Reactor Pattern is for handling concurrent I/O events.

#### 8. Conclusion

The value of the Reactor Pattern lies in how cleanly it divides responsibility: the Event Demultiplexer only waits for events, the Reactor only dispatches, and the event handlers only do the business logic. Add a new kind of event handler and not a single line of the waiting or dispatching code changes.

## References

- [GoF "Design Patterns" Overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru Design Patterns Catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Proxy](/dp/Proxy.md)
- [Singleton](/dp/Singleton.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Proxy](/dp/Proxy.md)
- [Singleton](/dp/Singleton.md)
