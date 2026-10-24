### Diagnosing and Practicing Memory Allocation

The allocator and GC mechanism pages are [Alloc](/alloc/Alloc.md) and [GC](/alloc/GC.md). This page covers how to diagnose allocation problems, when memory is actually returned to the operating system, and where the boundary of application-managed memory sits.

### Diagnosing Allocation Problems

`runtime.ReadMemStats` is the most direct tool. When looking at allocation problems, watch these fields:

| Field | Meaning |
| --- | --- |
| `HeapAlloc` | total bytes of live objects currently on the heap |
| `Sys` | total bytes requested from the operating system (including the runtime itself) |
| `HeapReleased` | bytes already handed back to the operating system |
| `Mallocs` | cumulative number of allocations; grows fast when the allocation rate is too high |
| `NumGC` | cumulative number of GC cycles |

A low `HeapAlloc` with a high `Sys` means most of the heap is free-but-not-yet-returned memory. `Mallocs` climbing quickly while `HeapAlloc` stays flat means you are allocating a lot of short-lived objects.

To locate allocation hotspots by call site, use pprof's heap profile:

```go
package main

import (
	"fmt"
	"os"
	"runtime/pprof"
)

func main() {
	data := make([][]byte, 0, 10)
	for i := 0; i < 10; i++ {
		data = append(data, make([]byte, 1024*1024))
	}
	_ = data

	f, err := os.Create("heap.out")
	if err != nil {
		panic(err)
	}
	defer f.Close()
	pprof.WriteHeapProfile(f)
	fmt.Println("heap profile written")
}
```

`go tool pprof -top heap.out` shows the largest allocation sites (the `inuse_space` view; sampled estimates, values vary by machine):

```plaintext
Showing nodes accounting for 5250.10kB, 100% of 5250.10kB total
      flat  flat%   sum%        cum   cum%
 4737.10kB 90.23% 90.23%  4737.10kB 90.23%  main.main
```

Whether a single variable lands on the stack or the heap — use `go build -gcflags=-m`; see [escape analysis](/var/Segment.md).

### When Memory Is Returned to the Operating System

Objects reclaimed by the GC go back to the allocator's free lists; they are not handed to the operating system immediately. A background scavenger gradually returns the pages that are not used, which is why a process's RSS only drops back a while after peak traffic. To return it immediately, call `debug.FreeOSMemory()`; in containers, set `GOMEMLIMIT` and let the runtime watch the watermark itself — see [GC tuning](/alloc/GC.md).

### The Boundaries of a Custom Allocator

Go does not support replacing the built-in allocator. The realistic form of a "custom allocator" in Go is an application managing a block of memory on its own: call `syscall.Mmap` to ask the operating system directly, bypassing the runtime's heap, and lay out the objects yourself:

```go
package main

import (
	"fmt"
	"syscall"
	"unsafe"
)

func main() {
	// ask the operating system directly for 4KB of anonymous memory
	b, err := syscall.Mmap(-1, 0, 4096,
		syscall.PROT_READ|syscall.PROT_WRITE,
		syscall.MAP_PRIVATE|syscall.MAP_ANONYMOUS)
	if err != nil {
		panic(err)
	}
	defer syscall.Munmap(b)

	// lay out an int64 array by hand on that block
	arr := unsafe.Slice((*int64)(unsafe.Pointer(&b[0])), 512)
	for i := range arr {
		arr[i] = int64(i * i)
	}
	fmt.Println(arr[10]) // prints: 100
}
```

This path bypasses the GC, at the cost of owning the lifetimes yourself entirely — after `Munmap` every pointer into it is dangling. For most cases, reusing objects through `sync.Pool` is enough; hand-rolled mmap memory is for special needs like very large fixed-size buffers.

### Zero Values and the Sharing Trap

Memory returned by `new` and `make` is zeroed out; what you read is always the zero value, never leftover data from a previous user. The real trap is sharing:

- Slices share their underlying array: carve a small piece out of a big slice and hold onto it long-term, and the whole large array stays in memory. To sever the link, `append([]T(nil), sub...)` makes a copy.
- A map or slice used as a struct field is a reference header; copying the struct does not copy the underlying data.
- Once `unsafe` bypasses the type system, both the zero-value guarantee and the GC's reachability analysis can break down. Unless you are maintaining runtime internals, do not use it.

## References

- [Official GC guide · Escape analysis and stack allocation](https://go.dev/doc/gc-guide#Escape_analysis)
- [Official GC guide](https://go.dev/doc/gc-guide)
- [Official GC guide · Optimization guide](https://go.dev/doc/gc-guide#Optimization_guide)
- [Official GC guide · General advice](https://go.dev/doc/gc-guide#General_advice)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
