###  高效 IO 操作

IO 往往是程序最慢的一环，省一次系统调用、少一次磁盘往返，收益直接体现在延迟上。本章给出四种做法：内存映射文件、异步 IO、缓冲读写、IO 多路复用，各配一段 Go 代码。

#### 6.1 内存映射文件

内存映射文件（Memory-Mapped Files）是一种将文件的内容映射到进程的地址空间的方法，这样可以像操作内存一样操作文件，从而提高文件读写效率。

**Go 示例代码**：
```go
package main

import (
    "fmt"
    "os"
    "syscall"
)

func memoryMapFile(filePath string) {
    file, err := os.OpenFile(filePath, os.O_RDWR, 0644)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    fi, err := file.Stat()
    if err != nil {
        fmt.Println("Error getting file info:", err)
        return
    }

    data, err := syscall.Mmap(int(file.Fd()), 0, int(fi.Size()), syscall.PROT_READ|syscall.PROT_WRITE, syscall.MAP_SHARED)
    if err != nil {
        fmt.Println("Error memory-mapping file:", err)
        return
    }
    defer syscall.Munmap(data)

    fmt.Println("File content before modification:")
    fmt.Println(string(data))

    copy(data, "Hello, Memory-Mapped File!")
    fmt.Println("File content after modification:")
    fmt.Println(string(data))
}

func main() {
    memoryMapFile("example.txt")
}
```

#### 6.2 异步 IO

异步IO（Asynchronous IO）允许程序在执行IO操作时不阻塞，可以继续执行其他任务，从而提高效率。

**Go 示例代码**：
```go
package main

import (
    "fmt"
    "io"
    "os"
)

func asyncRead(filePath string) {
    file, err := os.Open(filePath)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    buffer := make([]byte, 1024)
    done := make(chan bool)

    go func() {
        for {
            bytesRead, err := file.Read(buffer)
            if err != nil {
                if err != io.EOF {
                    fmt.Println("Error reading file:", err)
                }
                break
            }
            if bytesRead == 0 {
                break
            }
            fmt.Print(string(buffer[:bytesRead]))
        }
        done <- true
    }()

    fmt.Println("Reading file asynchronously...")
    <-done
    fmt.Println("Read complete")
}

func main() {
    asyncRead("example.txt")
}
```

#### 6.3 使用缓存优化 IO 性能

使用缓存可以减少磁盘IO操作，提高IO性能。常用的方法包括使用内存缓存和缓冲流。

**Go 示例代码**：
```go
package main

import (
    "bufio"
    "fmt"
    "io"
    "os"
)

func writeWithCache(filePath string, content string) {
    file, err := os.Create(filePath)
    if err != nil {
        fmt.Println("Error creating file:", err)
        return
    }
    defer file.Close()

    writer := bufio.NewWriter(file)
    _, err = writer.WriteString(content)
    if err != nil {
        fmt.Println("Error writing to file:", err)
        return
    }

    writer.Flush()
}

func readWithCache(filePath string) {
    file, err := os.Open(filePath)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    reader := bufio.NewReader(file)
    for {
        line, err := reader.ReadString('\n')
        if err != nil {
            if err != io.EOF {
                fmt.Println("Error reading file:", err)
            }
            break
        }
        fmt.Print(line)
    }
}

func main() {
    writeWithCache("example.txt", "Hello, cached IO!\nThis is a test.")
    readWithCache("example.txt")
}
```

#### 6.4 IO 多路复用

IO多路复用（IO Multiplexing）是一种在单个线程中监视多个文件描述符的技术，可以同时处理多个IO操作，提高并发性能。

**Go 示例代码**：
```go
package main

import (
    "fmt"
    "net"
    "os"
    "syscall"
)

func main() {
    listenFD, err := syscall.Socket(syscall.AF_INET, syscall.SOCK_STREAM, syscall.IPPROTO_TCP)
    if err != nil {
        fmt.Println("Error creating socket:", err)
        os.Exit(1)
    }
    defer syscall.Close(listenFD)

    addr := syscall.SockaddrInet4{Port: 8080}
    copy(addr.Addr[:], net.ParseIP("127.0.0.1").To4())

    err = syscall.Bind(listenFD, &addr)
    if err != nil {
        fmt.Println("Error binding socket:", err)
        os.Exit(1)
    }

    err = syscall.Listen(listenFD, 10)
    if err != nil {
        fmt.Println("Error listening on socket:", err)
        os.Exit(1)
    }

    epfd, err := syscall.EpollCreate1(0)
    if err != nil {
        fmt.Println("Error creating epoll:", err)
        os.Exit(1)
    }
    defer syscall.Close(epfd)

    err = syscall.EpollCtl(epfd, syscall.EPOLL_CTL_ADD, listenFD, &syscall.EpollEvent{
        Events: syscall.EPOLLIN,
        Fd:     int32(listenFD),
    })
    if err != nil {
        fmt.Println("Error adding listenFD to epoll:", err)
        os.Exit(1)
    }

    events := make([]syscall.EpollEvent, 10)
    for {
        n, err := syscall.EpollWait(epfd, events, -1)
        if err != nil {
            fmt.Println("Error waiting on epoll:", err)
            os.Exit(1)
        }

        for i := 0; i < n; i++ {
            if events[i].Fd == int32(listenFD) {
                connFD, _, err := syscall.Accept(listenFD)
                if err != nil {
                    fmt.Println("Error accepting connection:", err)
                    continue
                }

                err = syscall.EpollCtl(epfd, syscall.EPOLL_CTL_ADD, connFD, &syscall.EpollEvent{
                    Events: syscall.EPOLLIN,
                    Fd:     int32(connFD),
                })
                if err != nil {
                    fmt.Println("Error adding connFD to epoll:", err)
                    syscall.Close(connFD)
                }
            } else {
                buffer := make([]byte, 1024)
                n, err := syscall.Read(int(events[i].Fd), buffer)
                if err != nil {
                    fmt.Println("Error reading from connection:", err)
                    syscall.Close(int(events[i].Fd))
                    continue
                }

                fmt.Println("Received data:", string(buffer[:n]))
                syscall.Close(int(events[i].Fd))
            }
        }
    }
}
```

四种手段各管一段：内存映射省掉 read/write 的来回拷贝；异步 IO 把等待让给 goroutine；`bufio` 把多次小读写攒成大块；epoll 用一个线程盯住成百上千个连接。日常程序里最先用上的通常是 `bufio`，epoll 只有在自己写网络框架、绕开标准库封装时才需要直接操作。