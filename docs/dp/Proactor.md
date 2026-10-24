### The Proactor Pattern in Detail

#### 1. Introduction to the Proactor Pattern

The Proactor Pattern is a design pattern for handling concurrent I/O operations, mainly used in event-driven systems. Unlike the Reactor Pattern, Proactor hands the I/O operations off to the operating system or an underlying library; the application only writes the logic that runs after the event completes and does not manage the I/O process itself.

**Core idea**: initiating the I/O operation and handling the completion notification are separated; the application only waits for completion events.

#### 2. Components of the Proactor Pattern

The Proactor Pattern typically consists of the following components:

1. **I/O Request Processor**: initiates asynchronous I/O requests and passes them to the I/O operation system or library.

2. **Completion Handler**: handles the callback logic that runs after an I/O operation completes.

3. **I/O Operation System**: executes the actual I/O operations and performs asynchronous notification. The operating system notifies the application once an I/O operation completes.

4. **Event Loop**: waits for I/O completion notifications and passes each notification to the corresponding completion handler.

#### 3. How the Proactor Pattern Works

1. **Initialization**: create the I/O request processor, the completion handler, and the event loop.

2. **Initiating the I/O request**: the I/O request processor issues an asynchronous I/O request and hands it to the operating system.

3. **Executing the I/O operation**: the operating system or underlying library carries out the I/O operation.

4. **Notifying completion**: once the I/O operation finishes, the operating system passes a completion notification to the event loop.

5. **Handling the completion**: the event loop receives the completion notification and passes it to the corresponding completion handler.

6. **Completion processing**: the completion handler runs the corresponding logic, such as reading the data or processing the request.

7. **Keep waiting**: the event loop goes back to waiting for new I/O completion notifications.

#### 4. Pros and cons of the Proactor Pattern

**Pros**:

- **Less application-side code**: the operating system or underlying library runs the I/O process, and the application only writes the post-completion logic.
- **Fits high-load scenarios**: systems that need to handle large numbers of concurrent I/O requests, such as network servers.

**Cons**:

- **OS-dependent**: it requires operating system or underlying library support for asynchronous I/O operations.
- **Higher complexity**: it involves operating-system I/O completion notifications and callback handling, which can add to the system's complexity.

#### 5. Applications of the Proactor Pattern

Common in systems that need a large amount of asynchronous I/O:

- **High-performance web servers**: handling large numbers of concurrent HTTP requests.
- **Database systems**: handling large numbers of asynchronous database operations.
- **Real-time data processing systems**: handling large real-time data streams.

#### 6. Example of the Proactor Pattern

Below is a simple example of the Proactor Pattern in Go. Since Go's `net` package does not directly support the Proactor Pattern, this example uses pseudocode to show how it works.

**Example code**:

```go
package main

import (
	"fmt"
	"net"
	"os"
)

type CompletionHandler func(conn net.Conn, data []byte)

type Proactor struct {
	handler CompletionHandler
}

func (p *Proactor) ListenAndServe(address string) {
	listener, err := net.Listen("tcp", address)
	if err != nil {
		fmt.Println("Error starting server:", err)
		os.Exit(1)
	}
	defer listener.Close()

	fmt.Println("Server is listening on", address)

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Error accepting connection:", err)
			continue
		}

		go p.handleConnection(conn)
	}
}

func (p *Proactor) handleConnection(conn net.Conn) {
	defer conn.Close()

	// read the data and handle it
	buffer := make([]byte, 1024)
	n, err := conn.Read(buffer)
	if err != nil {
		fmt.Println("Error reading data:", err)
		return
	}

	// call the completion handler
	if p.handler != nil {
		p.handler(conn, buffer[:n])
	}
}

func main() {
	proactor := &Proactor{
		handler: func(conn net.Conn, data []byte) {
			fmt.Printf("Received data: %s\n", string(data))
			conn.Write(data) // echo the data back
		},
	}

	proactor.ListenAndServe(":8080")
}
```

#### 7. Proactor Pattern compared with other patterns

- **Reactor Pattern**: the Reactor Pattern separates I/O operation handling from event dispatching, and the application has to manage the I/O process itself. The Proactor Pattern instead hands I/O operations entirely to the operating system or an underlying library, and the application only handles the post-completion logic.
- **Observer Pattern**: the Observer Pattern handles message passing and event notification between objects, while the Proactor Pattern handles asynchronous I/O operations.

#### 8. Conclusion

Handing I/O execution to the operating system while the application only handles completion events is the dividing line between Proactor and Reactor. It suits applications with heavy asynchronous I/O, such as network servers and real-time data processing systems.

## References

- [GoF "Design Patterns" Overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru Design Patterns Catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Observer](/dp/Observer.md)
- [Prototype](/dp/Prototype.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Observer](/dp/Observer.md)
- [Prototype](/dp/Prototype.md)
