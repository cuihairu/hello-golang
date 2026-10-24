### syscall system calls

The `syscall` package exposes the operating system interface directly: the low-level operations for processes, files, networking, and time all live here. In most scenarios the high-level packages `os` and `net` are enough; you drop down to `syscall` only when you need precise control (special flags, platform-specific calls).

### Common calls

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

Output (the numbers vary by machine):

```plaintext
pid: 2798227
uid: 1000 gid: 1000
```

### The low-level form

Every call ultimately goes through `syscall.Syscall`: pass the system call number and arguments, and get back a result and an errno:

```go
package main

import (
	"fmt"
	"syscall"
)

func main() {
	r1, _, errno := syscall.Syscall(syscall.SYS_GETPID, 0, 0, 0)
	fmt.Println("raw pid:", r1, "errno:", errno) // prints: raw pid: 2801914 errno: errno 0
}
```

Wrapped functions like `Getpid` are just this plus error handling. When you need a platform-specific call (Linux's `epoll` and `inotify`, for example), go straight to the `syscall` package's source file for that platform.

### Cross-platform caveats

`syscall`'s interface is split across per-platform files (`syscall_linux.go`, `syscall_darwin.go`, ...), so the same function may have a different signature on different systems. For cross-platform code use `golang.org/x/sys/unix` (or `windows`) -- it collapses platform differences into a unified interface and is the officially recommended path.

### In short

`syscall` is the direct line to the operating system interface: use the wrapped functions for simple calls, the raw `Syscall` form for special needs, and hand cross-platform work off to `golang.org/x/sys`.

## References

- [syscall standard library](https://pkg.go.dev/syscall)
- [os standard library](https://pkg.go.dev/os)

## Sibling pages

- [Plugin](/sys/Plugin.md)
- [Sys](/sys/Sys.md)
- [Unsafe](/sys/Unsafe.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Plugin](/sys/Plugin.md)
- [Sys](/sys/Sys.md)
- [Unsafe](/sys/Unsafe.md)
