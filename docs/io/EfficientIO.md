###  Efficient IO operations

IO is often the slowest part of a program; saving one syscall or one round trip to disk pays off directly in latency. Four techniques are noted here: memory-mapped files, asynchronous IO, buffered reads and writes, and IO multiplexing, each with a Go snippet.

#### 6.1 Memory-mapped files

Memory-mapped files map a file's contents into a process's address space, so you operate on the file like memory, which makes reading and writing more efficient.

**Go example code**:
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

#### 6.2 Asynchronous IO

Asynchronous IO lets a program keep running other tasks while an IO operation is in progress instead of blocking, which improves efficiency.

**Go example code**:
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

#### 6.3 Using caching to optimize IO performance

Caching reduces disk IO operations and improves IO performance. The common approaches are in-memory caches and buffered streams.

**Go example code**:
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

#### 6.4 IO multiplexing

IO multiplexing watches multiple file descriptors from a single thread, so one thread can handle many IO operations at once and concurrency improves.

**Go example code**:
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

Each technique covers a different case: memory mapping removes the copy back and forth through read/write; asynchronous IO hands the waiting off to a goroutine; `bufio` coalesces many small reads and writes into large blocks; epoll lets one thread watch hundreds or thousands of connections. In day-to-day programs `bufio` is usually the first one you reach for; epoll only matters when you write your own network framework and bypass the standard library's wrappers.

## References

- [io standard library](https://pkg.go.dev/io)
- [os standard library](https://pkg.go.dev/os)
- [bufio standard library](https://pkg.go.dev/bufio)

## Sibling pages

- [Advanced](/io/Advanced.md)
- [CommonFormats](/io/CommonFormats.md)
- [Example](/io/Example.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Advanced](/io/Advanced.md)
- [CommonFormats](/io/CommonFormats.md)
- [Example](/io/Example.md)
- [File](/io/File.md)
- [FileAdvanced](/io/FileAdvanced.md)
- [FileOperation](/io/FileOperation.md)
- [IO](/io/IO.md)
- [InputOutput](/io/InputOutput.md)
- [ModIO](/io/ModIO.md)
- [ModOS](/io/ModOS.md)
- [ModPath](/io/ModPath.md)
- [Security](/io/Security.md)
- [Utils](/io/Utils.md)
