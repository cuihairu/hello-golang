### Chapter 3: Socket Programming Basics

#### 3.1 Socket Overview

##### 3.1.1 Socket Types

A socket is a basic concept in network programming. Depending on the transport protocol and how the data is transferred, sockets fall mainly into the following types:

- **Stream socket**:
  - Based on TCP, providing connection-oriented, reliable data transmission.
  - Fits scenarios that need guaranteed ordering and integrity of data, such as web browsing and file transfer.

- **Datagram socket**:
  - Based on UDP, providing connectionless, unreliable data transmission.
  - Fits scenarios that value transmission speed over data reliability, such as live video streaming and online games.

- **Raw socket**:
  - Accesses the low-level network protocol directly; it is usually used to develop and test protocol implementations.

##### 3.1.2 Socket APIs

Socket programming goes through the APIs the system provides. In Go you use the standard library `net` package — the functions and types for creating and working with sockets all live in it.

#### 3.2 TCP Socket Programming

##### 3.2.1 Creating a TCP Socket

In Go, `net.Listen` creates a TCP socket in one step:

```go
package main

import (
	"fmt"
	"net"
)

func main() {
	// create a TCP socket listener
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Println("Error creating TCP socket:", err)
		return
	}
	defer listener.Close()
	fmt.Println("TCP socket created and listening on port 8080")
}
```

##### 3.2.2 Connecting and Listening

After creating a TCP socket, you need to handle connection requests and set up communication:

```go
package main

import (
	"fmt"
	"net"
)

func main() {
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Println("Error creating TCP socket:", err)
		return
	}
	defer listener.Close()

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Error accepting connection:", err)
			continue
		}
		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	fmt.Println("Connected to client:", conn.RemoteAddr().String())
	// handle the connection
}
```

##### 3.2.3 Data Transfer

Once the TCP connection is established, you can read from and write to it:

```go
package main

import (
	"bufio"
	"fmt"
	"net"
)

func handleConnection(conn net.Conn) {
	defer conn.Close()
	fmt.Println("Connected to client:", conn.RemoteAddr().String())

	scanner := bufio.NewScanner(conn)
	for scanner.Scan() {
		message := scanner.Text()
		fmt.Println("Received message:", message)
		_, err := conn.Write([]byte("Message received\n"))
		if err != nil {
			fmt.Println("Error writing to connection:", err)
			return
		}
	}
	if err := scanner.Err(); err != nil {
		fmt.Println("Error reading from connection:", err)
	}
}
```

#### 3.3 UDP Socket Programming

##### 3.3.1 Creating a UDP Socket

Creating a UDP socket is similar to creating a TCP socket, but you use the `net.ListenUDP` function:

```go
package main

import (
	"fmt"
	"net"
)

func main() {
	addr, err := net.ResolveUDPAddr("udp", ":8080")
	if err != nil {
		fmt.Println("Error resolving UDP address:", err)
		return
	}
	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		fmt.Println("Error creating UDP socket:", err)
		return
	}
	defer conn.Close()
	fmt.Println("UDP socket created and listening on port 8080")
}
```

##### 3.3.2 Sending and Receiving Data

An example of sending and receiving UDP data:

```go
package main

import (
	"fmt"
	"net"
)

func main() {
	addr, err := net.ResolveUDPAddr("udp", ":8080")
	if err != nil {
		fmt.Println("Error resolving UDP address:", err)
		return
	}
	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		fmt.Println("Error creating UDP socket:", err)
		return
	}
	defer conn.Close()

	buffer := make([]byte, 1024)
	for {
		n, remoteAddr, err := conn.ReadFromUDP(buffer)
		if err != nil {
			fmt.Println("Error reading from UDP:", err)
			continue
		}
		fmt.Printf("Received %d bytes from %s: %s\n", n, remoteAddr, string(buffer[:n]))

		_, err = conn.WriteToUDP([]byte("Message received"), remoteAddr)
		if err != nil {
			fmt.Println("Error writing to UDP:", err)
		}
	}
}
```

#### 3.4 Common Problems in Socket Programming

##### 3.4.1 Socket Timeouts

Reads and writes can block forever, so use `SetDeadline` to give the connection a deadline:

```go
package main

import (
	"fmt"
	"net"
	"time"
)

func main() {
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Println("Error creating TCP socket:", err)
		return
	}
	defer listener.Close()

	for {
		// net.Listener has no SetDeadline method, so assert to *net.TCPListener
		if tcpListener, ok := listener.(*net.TCPListener); ok {
			tcpListener.SetDeadline(time.Now().Add(10 * time.Second))
		}
		conn, err := listener.Accept()
		if err != nil {
			if err, ok := err.(net.Error); ok && err.Timeout() {
				fmt.Println("Accept timeout")
				continue
			}
			fmt.Println("Error accepting connection:", err)
			continue
		}
		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	fmt.Println("Connected to client:", conn.RemoteAddr().String())
	conn.SetDeadline(time.Now().Add(10 * time.Second))
	// handle the connection
}
```

##### 3.4.2 Data Loss and Duplication

Data loss and duplication are common problems in network communication. Using TCP avoids most of them, because TCP provides reliable data transmission. With UDP, these problems have to be handled by an application-layer protocol.

TCP uses `net.Listen` plus `Accept` to take connections, then `conn.Read` and `conn.Write` to read and write; UDP uses `ListenUDP` with `ReadFromUDP` and `WriteToUDP`. For timeouts use `SetDeadline`, leave packet loss and duplication to TCP, and if you go with UDP you handle them yourself at the application layer.

## References

- [net standard library](https://pkg.go.dev/net)
- [net/http standard library](https://pkg.go.dev/net/http)


## Sibling pages

- [Advanced](/net/Advanced.md)
- [Concurrence](/net/Concurrence.md)
- [Intro](/net/Intro.md)
- [SlidingWindow](/net/SlidingWindow.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [SlidingWindow](/net/SlidingWindow.md)
