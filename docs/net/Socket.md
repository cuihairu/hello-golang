### 第3章 套接字编程基础

#### 3.1 套接字概述

##### 3.1.1 套接字类型

套接字是网络编程中的基础概念，根据传输协议和数据传输方式的不同，套接字主要分为以下几种类型：

- **流套接字（Stream Socket）**：
  - 基于 TCP 协议，提供面向连接的、可靠的数据传输。
  - 适用于需要保证数据顺序和完整性的应用场景，如网页浏览和文件传输。

- **数据报套接字（Datagram Socket）**：
  - 基于 UDP 协议，提供无连接的、不可靠的数据传输。
  - 适用于对传输速度要求高但对数据可靠性要求不高的应用场景，如实时视频流和在线游戏。

- **原始套接字（Raw Socket）**：
  - 直接访问底层网络协议，通常用于开发和测试网络协议实现。

##### 3.1.2 套接字 API

套接字编程主要通过各种系统提供的 API 实现。在 Go 语言中，使用标准库 `net` 包进行套接字编程。`net` 包提供了丰富的函数和类型，用于创建和操作套接字。

#### 3.2 TCP 套接字编程

##### 3.2.1 创建 TCP 套接字

在 Go 中，创建 TCP 套接字非常简单，使用 `net.Listen` 函数即可：

```go
package main

import (
	"fmt"
	"net"
)

func main() {
	// 创建一个 TCP 套接字监听器
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Println("Error creating TCP socket:", err)
		return
	}
	defer listener.Close()
	fmt.Println("TCP socket created and listening on port 8080")
}
```

##### 3.2.2 连接与监听

在创建 TCP 套接字之后，需要处理连接请求并建立通信：

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
	// 处理连接
}
```

##### 3.2.3 数据传输

在 TCP 连接建立后，可以进行数据的读写操作：

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

#### 3.3 UDP 套接字编程

##### 3.3.1 创建 UDP 套接字

创建 UDP 套接字和创建 TCP 套接字类似，但使用的是 `net.ListenUDP` 函数：

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

##### 3.3.2 数据发送与接收

UDP 数据的发送与接收示例：

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

#### 3.4 套接字编程的常见问题

##### 3.4.1 套接字超时

套接字编程中，处理超时是确保程序稳定性的重要部分：

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
		listener.SetDeadline(time.Now().Add(10 * time.Second))
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
	// 处理连接
}
```

##### 3.4.2 数据丢失与重复

在网络通信中，数据丢失与重复是常见问题。使用 TCP 协议可以避免大部分数据丢失和重复的问题，因为 TCP 提供了可靠的数据传输。但在 UDP 中，这些问题则需要通过应用层协议来处理。

通过本章的学习，读者应能够理解和掌握套接字编程的基础知识，包括套接字类型、API 使用、TCP 和 UDP 套接字编程，以及常见问题的处理方法。这些知识是网络编程的重要基础，为后续高级主题的学习奠定了基础。