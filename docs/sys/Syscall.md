### syscall 系统调用

`syscall` 包直接暴露操作系统接口：进程、文件、网络、时间的底层操作都在这里。多数场景用 `os`、`net` 这些高层包就够，需要精确控制（特殊标志、平台特有调用）时才落到 `syscall`。

### 常用调用

```go
package main

import (
	"fmt"
	"syscall"
)

func main() {
	fmt.Println("pid:", syscall.Getpid())
	fmt.Println("uid:", syscall.Getuid(), "gid:", syscall.Getgid())
}
```

输出（数值因机器而异）：

```plaintext
pid: 2798227
uid: 1000 gid: 1000
```

### 底层形式

所有调用最终都走 `syscall.Syscall`：传系统调用号和参数，返回结果和 errno：

```go
r1, _, errno := syscall.Syscall(syscall.SYS_GETPID, 0, 0, 0)
fmt.Println("raw pid:", r1, "errno:", errno) // 输出：raw pid: 2801914 errno: errno 0
```

`Getpid` 这类包装函数就是在这个基础上加了错误处理。需要平台特有调用（比如 Linux 的 `epoll`、`inotify`）时，直接查 `syscall` 包对应平台的源码文件。

### 跨平台注意

`syscall` 的接口按平台分文件（`syscall_linux.go`、`syscall_darwin.go`……），同一个函数在不同系统上签名可能不同。要写跨平台代码，用 `golang.org/x/sys/unix`（或 `windows`）——它把平台差异收敛成统一接口，是官方推荐的路径。

### 小结

`syscall` 是操作系统接口的直连层：简单调用用包装函数，特殊需求用 `Syscall` 原始形式，跨平台交给 `golang.org/x/sys`。
