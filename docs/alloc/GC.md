# GC

Go's memory is managed automatically by the runtime: the allocator hands memory to objects, and the garbage collector (GC, Garbage Collector) reclaims memory that is no longer in use. This page records the basic principles of GC, how it cooperates with the allocator, and the common tuning knobs, all from the memory allocation angle.

### How GC Relates to the Memory Allocator

- **On allocation**: small objects take the `mcache` -> `mcentral` -> `mheap` path to get memory; large objects (larger than 32 KB) are allocated straight from `mheap`.
- **On reclamation**: once the GC decides an object is no longer reachable, it marks the `mspan` it occupied as free. Those `mspan`s go back to the allocator's free lists for future allocations instead of being returned to the operating system right away.
- So the GC's unit of reclamation matches the allocator's unit of allocation — both are `mspan`/pages. This is the other half of the layered structure introduced in the previous section.

### Basic Principles: A Summary from the Allocation View

The Go GC is a concurrent tri-color mark-and-sweep collector; marking starts from the root objects, unreachable objects are swept, and there are only short STW phases in between. For the full marking, tri-color abstraction and triggering mechanism, see the [GC internals notes](/gc/GC.md). What stays here is the practical view: how it cooperates with the allocator and how to tune it.

### In Practice: Observing GC Behavior

The program below shows how to read GC statistics, trigger a GC manually, and watch `HeapAlloc` and `NumGC` change through `runtime.MemStats`:

```go
package main

import (
	"fmt"
	"runtime"
	"time"
)

func main() {
	var mem runtime.MemStats

	fmt.Println("--- Before allocation ---")
	runtime.ReadMemStats(&mem)
	fmt.Println("HeapAlloc(KB):", mem.HeapAlloc/1024, "NumGC:", mem.NumGC)

	// allocate 100 temporary 1MB objects so they quickly become garbage
	for i := 0; i < 100; i++ {
		_ = make([]byte, 1024*1024)
	}

	fmt.Println("--- After allocation (before GC) ---")
	runtime.ReadMemStats(&mem)
	fmt.Println("HeapAlloc(KB):", mem.HeapAlloc/1024, "NumGC:", mem.NumGC)

	// trigger a GC manually
	runtime.GC()
	runtime.ReadMemStats(&mem)
	fmt.Println("--- After the manual GC ---")
	fmt.Println("HeapAlloc(KB):", mem.HeapAlloc/1024, "NumGC:", mem.NumGC)

	// keep the compiler from optimizing the earlier allocations away
	time.Sleep(10 * time.Millisecond)
}
```

Sample output (exact values vary by machine; note that the GC already fired on its own several times while the 100 1MB objects were being allocated, so NumGC has already grown):

```
--- Before allocation ---
HeapAlloc(KB): 269 NumGC: 0
--- After allocation (before GC) ---
HeapAlloc(KB): 2355 NumGC: 36
--- After the manual GC ---
HeapAlloc(KB): 307 NumGC: 37
```

### Common GC Tuning Knobs

1. **GOGC**: controls when the GC triggers. The default is 100, meaning a GC runs when newly allocated memory reaches 100% of the memory that survived the last cycle. Raising the value means fewer GC cycles and more memory held; lowering it does the opposite. `GOGC=off` turns the GC off entirely (experiments only).

   ```sh
   GOGC=200 ./myapp   # lower the GC frequency
   GOGC=50 ./myapp    # run GC more aggressively
   ```

2. **GOMEMLIMIT / debug.SetMemoryLimit**: a soft memory limit introduced in Go 1.19. The runtime GCs more often as it approaches the limit, which suits memory-constrained container environments:

   ```go
   package main

   import "runtime/debug"

   func init() {
       debug.SetMemoryLimit(512 << 20) // 512 MiB
   }

   func main() {}
   ```

3. **GOGC and GOMEMLIMIT together**: Go considers both and triggers the GC on whichever condition is met first. In containers it is worth setting both, to balance CPU cost against the memory watermark.

4. **Produce less garbage**: compared with turning knobs, lowering the allocation rate is usually more effective:
   - reuse temporary objects with `sync.Pool`;
   - pre-allocate slice capacity (`make([]T, 0, n)`) to avoid repeated growth;
   - remember that converting between `string` and `[]byte` copies;
   - avoid needless pointer boxing (such as wrapping basic types in `interface{}`).

```go
package main

import (
	"fmt"
	"runtime"
	"runtime/debug"
	"sync"
)

func main() {
	debug.SetGCPercent(200) // equivalent to GOGC=200

	// reuse 4KB buffers through sync.Pool to cut allocations
	pool := sync.Pool{
		New: func() interface{} {
			buf := make([]byte, 4096)
			return &buf
		},
	}

	for i := 0; i < 1000; i++ {
		buf := pool.Get().(*[]byte)
		_ = (*buf)[0] // use the buffer
		pool.Put(buf)
	}

	var mem runtime.MemStats
	runtime.ReadMemStats(&mem)
	fmt.Println("total allocations (Mallocs):", mem.Mallocs)
}
```

### Common Misconceptions

- **Treating the GC as a catch-all**: the GC only reclaims unreachable objects. Hang objects on a global map that never empties and the GC cannot reclaim them either — a textbook memory leak.
- **Believing `runtime.GC()` fixes memory problems**: a manual GC only runs early what would have happened anyway; triggering it by hand frequently just wastes CPU.
- **Ignoring goroutine leaks**: a goroutine blocked on a channel, and every object it references, stay reachable and un-reclaimable forever. When needed, track them down with `runtime.NumGoroutine()` or pprof's goroutine profile.

### Summary

Go's GC and the layered allocator (`mcache`/`mcentral`/`mheap`) are two sides of the same system: the allocator decides where memory comes from, the GC decides when it returns to the allocator. When tuning, read `GOGC`, `GOMEMLIMIT` and the allocation rate together: the first two control when reclamation happens and the memory ceiling, the third decides how fast garbage is produced.

## References

- [Official GC guide · Escape analysis and stack allocation](https://go.dev/doc/gc-guide#Escape_analysis)
- [Official GC guide](https://go.dev/doc/gc-guide)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Practice](/alloc/Practice.md)
- [glossary](/glossary.md)
