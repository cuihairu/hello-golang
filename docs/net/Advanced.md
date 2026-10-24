### Chapter 4: Advanced Network Programming

#### 4.1 Non-blocking I/O

The goal of non-blocking I/O is to not block the thread on reads and writes. There are three common approaches: select, poll, and epoll.

##### 4.1.1 I/O Multiplexing with select

`select` is an early I/O multiplexing technique that watches many file descriptors at once to see which ones are ready for reading or writing. Its limits are a finite number of file descriptors and lower efficiency.

**Sample code**:

```go
package main

import (
	"fmt"
	"net"
	"os"
	"syscall"
)

func main() {
	ln, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Println("Error listening:", err)
		os.Exit(1)
	}
	defer ln.Close()

	// Get the file descriptor for the listening socket (File() returns a dup'd *os.File and an error)
	tcpLn := ln.(*net.TCPListener)
	file, err := tcpLn.File()
	if err != nil {
		fmt.Println("Error getting file:", err)
		os.Exit(1)
	}
	defer file.Close()
	fd := int(file.Fd())

	for {
		readfds := &syscall.FdSet{}
		// Note: Go on Linux does not provide convenient FdSet.Set/IsSet methods,
		// so the bitmap has to be set by hand: Bits is [16]int64, bit fd is 1
		readfds.Bits[fd/64] |= 1 << (uint(fd) % 64)

		// The last argument to select is the timeout (Timeval); nil means block forever
		timeout := &syscall.Timeval{Sec: 1, Usec: 0}
		n, err := syscall.Select(fd+1, readfds, nil, nil, timeout)
		if err != nil {
			fmt.Println("Error in select:", err)
			continue
		}
		if n == 0 {
			continue // timeout, no ready descriptors
		}

		// Check the bitmap by hand as well
		if readfds.Bits[fd/64]&(1<<(uint(fd)%64)) != 0 {
			conn, err := ln.Accept()
			if err != nil {
				fmt.Println("Error accepting:", err)
				continue
			}

			go handleConnection(conn)
		}
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	buf := make([]byte, 1024)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			fmt.Println("Error reading:", err)
			return
		}
		fmt.Println("Received data:", string(buf[:n]))
	}
}
```

##### 4.1.2 I/O Multiplexing with poll

`poll` improves on `select` by removing the limit on the number of file descriptors, and it is more efficient. `poll` uses an array of structures to watch for events on file descriptors.

**Sample code**:

Note: Go's `syscall` package does not export `PollFd`, `POLLIN`, or `Poll` on Linux/amd64, so using poll requires the `golang.org/x/sys/unix` package (`go get golang.org/x/sys`):

```go
package main

import (
	"fmt"
	"net"
	"os"

	"golang.org/x/sys/unix"
)

func main() {
	ln, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Println("Error listening:", err)
		os.Exit(1)
	}
	defer ln.Close()

	tcpLn := ln.(*net.TCPListener)
	file, err := tcpLn.File()
	if err != nil {
		fmt.Println("Error getting file:", err)
		os.Exit(1)
	}
	defer file.Close()
	fd := int(file.Fd())

	fds := []unix.PollFd{{Fd: int32(fd), Events: unix.POLLIN}}

	for {
		n, err := unix.Poll(fds, -1) // -1 means block forever
		if err != nil {
			fmt.Println("Error in poll:", err)
			continue
		}
		if n == 0 {
			continue
		}

		if fds[0].Revents&unix.POLLIN != 0 {
			conn, err := ln.Accept()
			if err != nil {
				fmt.Println("Error accepting:", err)
				continue
			}

			go handleConnection(conn)
		}
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	buf := make([]byte, 1024)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			fmt.Println("Error reading:", err)
			return
		}
		fmt.Println("Received data:", string(buf[:n]))
	}
}
```

##### 4.1.3 I/O Multiplexing with epoll

`epoll` is a more efficient I/O multiplexing mechanism on Linux, suited for large-scale concurrent connections. `epoll` offers two modes: edge-triggered (ET) and level-triggered (LT), and is usually combined with event-driven programming.

**Sample code**:

```go
package main

import (
	"fmt"
	"net"
	"os"
	"syscall"
)

func main() {
	ln, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Println("Error listening:", err)
		os.Exit(1)
	}
	defer ln.Close()

	tcpLn := ln.(*net.TCPListener)
	listenFile, err := tcpLn.File()
	if err != nil {
		fmt.Println("Error getting file:", err)
		os.Exit(1)
	}
	defer listenFile.Close()
	listenFd := int(listenFile.Fd())
	epollFd, err := syscall.EpollCreate1(0)
	if err != nil {
		fmt.Println("Error creating epoll:", err)
		os.Exit(1)
	}
	defer syscall.Close(epollFd)

	event := syscall.EpollEvent{Events: syscall.EPOLLIN, Fd: int32(listenFd)}
	err = syscall.EpollCtl(epollFd, syscall.EPOLL_CTL_ADD, listenFd, &event)
	if err != nil {
		fmt.Println("Error adding listen fd to epoll:", err)
		os.Exit(1)
	}

	events := make([]syscall.EpollEvent, 10)
	for {
		n, err := syscall.EpollWait(epollFd, events, -1)
		if err != nil {
			fmt.Println("Error in epoll wait:", err)
			continue
		}

		for i := 0; i < n; i++ {
			if int(events[i].Fd) == listenFd {
				conn, err := ln.Accept()
				if err != nil {
					fmt.Println("Error accepting:", err)
					continue
				}

				connFile, err := conn.(*net.TCPConn).File()
				if err != nil {
					fmt.Println("Error getting conn file:", err)
					conn.Close()
					continue
				}
				connFd := int(connFile.Fd())
				event := syscall.EpollEvent{Events: syscall.EPOLLIN, Fd: int32(connFd)}
				err = syscall.EpollCtl(epollFd, syscall.EPOLL_CTL_ADD, connFd, &event)
				if err != nil {
					fmt.Println("Error adding conn fd to epoll:", err)
					conn.Close()
					continue
				}
			} else {
				go handleConnection(int(events[i].Fd))
			}
		}
	}
}

func handleConnection(fd int) {
	conn := os.NewFile(uintptr(fd), "")
	defer conn.Close()

	buf := make([]byte, 1024)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			fmt.Println("Error reading:", err)
			return
		}
		fmt.Println("Received data:", string(buf[:n]))
	}
}
```

#### 4.2 Event-Driven Programming

Event-driven programming is a paradigm that handles asynchronous events through an event loop and callback mechanism. It is especially well suited to I/O-bound and high-concurrency workloads.

##### 4.2.1 Event Loop

The event loop is the heart of event-driven programming: it keeps waiting for and dispatching events. Event loops are usually paired with non-blocking I/O and I/O multiplexing to handle events efficiently.

**Sample code**:

```go
package main

import (
	"fmt"
	"net"
	"time"
)

type EventLoop struct {
	events chan func()
}

func NewEventLoop() *EventLoop {
	return &EventLoop{events: make(chan func(), 1024)}
}

func (el *EventLoop) AddEvent(event func()) {
	el.events <- event
}

func (el *EventLoop) Run() {
	for event := range el.events {
		event()
	}
}

func main() {
	loop := NewEventLoop()
	go loop.Run()

	ln, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Println("Error listening:", err)
		return
	}
	defer ln.Close()

	go func() {
		for {
			conn, err := ln.Accept()
			if err != nil {
				fmt.Println("Error accepting:", err)
				continue
			}
			handleConnection(loop, conn)
		}
	}()

	time.Sleep(10 * time.Second)
}

func handleConnection(loop *EventLoop, conn net.Conn) {
	buf := make([]byte, 1024)
	go func() {
		for {
			n, err := conn.Read(buf)
			if err != nil {
				fmt.Println("Error reading:", err)
				conn.Close()
				return
			}
			loop.AddEvent(func() {
				fmt.Println("Received data:", string(buf[:n]))
			})
		}
	}()
}
```

##### 4.2.2 Callback Mechanism

The callback mechanism is an important part of event-driven programming. By calling a predefined callback function when an event fires, events are handled asynchronously.

**Sample code**:

```go
package main

import (
	"fmt"
	"net"
	"time"
)

type EventHandler func(data []byte)

func main() {
	handler := func(data []byte) {
		fmt.Println("Received data:", string(data))
	}

	ln, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Println("Error listening:", err)
		return
	}
	defer ln.Close()

	go func() {
		for {
			conn, err := ln.Accept()
			if err != nil {
				fmt.Println("Error accepting:", err)
				continue
			}
			handleConnection(conn, handler)
		}
	}()

	time.Sleep(10 * time.Second)
}

func handleConnection(conn net.Conn, handler EventHandler) {
	buf := make([]byte, 1024)
	go func() {
		for {
			n, err := conn.Read(buf)
			if err != nil {
				fmt.Println("Error reading:", err)
				conn.Close()
				return
			}
			handler(buf[:n])
		}


	}()
}
```

#### 4.3 Asynchronous I/O

Asynchronous I/O is a technique where an I/O operation returns immediately, before it finishes, and the result is handled through a callback function or event notification mechanism. Asynchronous I/O can improve an application's concurrency and responsiveness.

##### 4.3.1 Asynchronous I/O with IOCP

IOCP (I/O Completion Ports) is an efficient asynchronous I/O mechanism on Windows that achieves high-concurrency I/O through I/O completion ports and a thread pool.

**Sample code (pseudocode)**:

```c
// This is pseudocode for an IOCP example; a real implementation would need the Windows API
#include <windows.h>
#include <stdio.h>

void CALLBACK IoCompletionCallback(DWORD errorCode, DWORD numberOfBytesTransferred, LPOVERLAPPED overlapped) {
    printf("I/O operation completed with %d bytes transferred.\n", numberOfBytesTransferred);
}

int main() {
    HANDLE iocp = CreateIoCompletionPort(INVALID_HANDLE_VALUE, NULL, 0, 0);

    HANDLE file = CreateFile("example.txt", GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_FLAG_OVERLAPPED, NULL);
    CreateIoCompletionPort(file, iocp, (ULONG_PTR)file, 0);

    char buffer[1024];
    OVERLAPPED overlapped = {0};
    ReadFile(file, buffer, sizeof(buffer), NULL, &overlapped);

    DWORD numberOfBytesTransferred;
    ULONG_PTR completionKey;
    LPOVERLAPPED completedOverlapped;
    GetQueuedCompletionStatus(iocp, &numberOfBytesTransferred, &completionKey, &completedOverlapped, INFINITE);

    IoCompletionCallback(0, numberOfBytesTransferred, completedOverlapped);

    CloseHandle(file);
    CloseHandle(iocp);
    return 0;
}
```

##### 4.3.2 Asynchronous I/O with io_uring

io_uring is a high-performance asynchronous I/O mechanism in the Linux kernel that uses ring buffers for efficient submission and completion notification of I/O operations.

**Sample code (pseudocode)**:

```c
// This is pseudocode for an IO_uring example; a real implementation would need the Linux IO_uring API
#include <liburing.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

int main() {
    struct io_uring ring;
    io_uring_queue_init(32, &ring, 0);

    int fd = open("example.txt", O_RDONLY | O_DIRECT);
    char buffer[4096];

    struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
    io_uring_prep_read(sqe, fd, buffer, sizeof(buffer), 0);
    io_uring_submit(&ring);

    struct io_uring_cqe *cqe;
    io_uring_wait_cqe(&ring, &cqe);

    printf("I/O operation completed with %d bytes read.\n", cqe->res);
    io_uring_cqe_seen(&ring, cqe);

    close(fd);
    io_uring_queue_exit(&ring);
    return 0;
}
```

#### 4.4 Network Protocol Parsing

This section looks at how to parse three protocols: HTTP, WebSocket, and a custom protocol that follows its own format.

##### 4.4.1 HTTP Protocol Parsing

HTTP (Hypertext Transfer Protocol) is an application-layer protocol for distributed, collaborative, hypermedia information systems. HTTP is the foundation of the web and communicates through a request/response mechanism.

**Sample code**:

```go
package main

import (
	"fmt"
	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello, World!")
}

func main() {
	http.HandleFunc("/", handler)
	http.ListenAndServe(":8080", nil)
}
```

##### 4.4.2 WebSocket Protocol Parsing

WebSocket is a full-duplex communication protocol that exchanges data in real time between client and server over a single TCP connection.

**Sample code**:

```go
package main

import (
	"fmt"
	"net/http"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
}

func handler(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		fmt.Println("Error upgrading to websocket:", err)
		return
	}
	defer conn.Close()

	for {
		messageType, message, err := conn.ReadMessage()
		if err != nil {
			fmt.Println("Error reading message:", err)
			return
		}
		fmt.Printf("Received: %s\n", message)

		if err := conn.WriteMessage(messageType, message); err != nil {
			fmt.Println("Error writing message:", err)
			return
		}
	}
}

func main() {
	http.HandleFunc("/", handler)
	http.ListenAndServe(":8080", nil)
}
```

##### 4.4.3 Custom Protocols

A custom protocol follows whatever format you define. The example below is the simplest case: one message per line, and whatever comes in gets an `ACK` sent back.

**Sample code**:

```go
package main

import (
	"bufio"
	"fmt"
	"net"
	"strings"
)

func handleConnection(conn net.Conn) {
	defer conn.Close()
	reader := bufio.NewReader(conn)
	for {
		message, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("Error reading:", err)
			return
		}
		message = strings.TrimSpace(message)
		fmt.Printf("Received: %s\n", message)

		response := "ACK\n"
		_, err = conn.Write([]byte(response))
		if err != nil {
			fmt.Println("Error writing:", err)
			return
		}
	}
}

func main() {
	ln, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Println("Error listening:", err)
		return
	}
	defer ln.Close()

	for {
		conn, err := ln.Accept()
		if err != nil {
			fmt.Println("Error accepting:", err)
			continue
		}
		go handleConnection(conn)
	}
}
```

### Conclusion

select, poll, and epoll solve "one thread watching many connections"; the event loop and callbacks solve "who picks up an event when it arrives"; IOCP and io_uring take the asynchronous submit-then-notify path; and protocol parsing decides how to carve individual messages out of a byte stream. Go's `net` and `net/http` already wrap all of this in the standard library. These lower-level approaches are here so you can see why they are designed the way they are.

## References

- [net standard library](https://pkg.go.dev/net)
- [net/http standard library](https://pkg.go.dev/net/http)

## Sibling pages

- [Concurrence](/net/Concurrence.md)
- [Intro](/net/Intro.md)
- [Netpoll](/net/Netpoll.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Concurrence](/net/Concurrence.md)
- [Intro](/net/Intro.md)
- [Netpoll](/net/Netpoll.md)
- [Proto](/net/Proto.md)
- [SlidingWindow](/net/SlidingWindow.md)
- [Socket](/net/Socket.md)
