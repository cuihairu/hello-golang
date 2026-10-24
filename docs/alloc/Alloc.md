This page collects the responsibilities and usage scenarios of `mspan`, `mcache`, `mcentral`, `mheap` and `heapArena` in Go's memory allocator, and how they map onto the three-tier Thread Cache, Central Cache and Heap structure.

### The Layered Structure of the Memory Allocator

Go's memory allocator has three tiers, from top to bottom:

1. **Thread Cache**
2. **Central Cache**
3. **Heap**

### Key Components and Their Relationships

In the runtime implementation, the three tiers land on `mcache`, `mcentral` and `mheap` respectively, plus two foundational structures, `mspan` and `heapArena`, for a total of five key components.

#### Relationship Diagram

```
Thread Cache (mcache)
       |
Central Cache (mcentral)
       |
Heap (mheap)
       |
heapArena
```

### Component Details and Usage Scenarios

#### 1. Thread Cache / mcache
`mcache` is a per-P (Processor) private cache, used to allocate small objects (less than 32 KB). It contains multiple `mspan`s, each holding objects of the same size class.

**Usage scenario**:
- Suited to frequently allocated and freed small objects. It reduces contention between threads and improves allocation efficiency.

**Example**:
```go
func allocateSmallObject(size int) {
    // allocate a small object (< 32 KB)
    mem := make([]byte, size)
    // use the memory to prevent it from being optimized away
    mem[0] = 1
    fmt.Println("Allocated small object")
}
```

#### 2. Central Cache / mcentral
`mcentral` manages the `mspan`s of each size class. It fetches new `mspan`s from `mheap` and returns exhausted `mspan`s back to `mheap`, serving as the middle layer between `mcache` and `mheap`.

**Usage scenario**:
- When the memory in `mcache` runs short, fetch a new `mspan` from `mcentral`.
- When `mcache` has surplus memory, hand it back to `mcentral`.

**Example** (illustrative pseudocode of the runtime internals, not directly compilable or runnable):
```go
func allocateFromCentralCache(sizeClass int) {
    // allocate memory from the central cache
    span := mcentral.alloc(sizeClass)
    // use the span to allocate the object
    obj := span.allocateObject()
    fmt.Println("Allocated object from central cache")
}
```

#### 3. Heap / mheap
`mheap` is the global heap memory manager, responsible for obtaining memory from the operating system and managing the allocation and reclamation of `mspan`s. It provides large blocks of memory (pages) and splits them into `mspan`s for `mcentral` to use.

**Usage scenario**:
- Suited to large object allocation (>= 32 KB).
- When `mcentral` requests a new `mspan`, memory is obtained from `mheap`.

**Example**:
```go
func allocateLargeObject(size int) {
    // allocate a large object (>= 32 KB)
    mem := make([]byte, size)
    // use the memory to prevent it from being optimized away
    mem[0] = 1
    fmt.Println("Allocated large object")
}
```

#### 4. mspan
`mspan` is a group of contiguous memory pages used to allocate objects. `mspan`s are divided by size class, and each class holds objects of similar size.

**Usage scenario**:
- Manages objects of the same size to improve allocation and release efficiency.
- Used by `mcache` and `mcentral` for object allocation.

**Example** (illustrative pseudocode of the runtime internals, not directly compilable or runnable):
```go
func allocateFromSpan(span *mspan, size int) {
    // allocate an object from the span
    obj := span.allocate(size)
    fmt.Println("Allocated object from span")
}
```

#### 5. heapArena
`heapArena` is a large block of memory that `mheap` obtains from the operating system. Each `heapArena` holds 64 MB of memory. It is used to manage and allocate memory pages.

**Usage scenario**:
- When `mheap` gets memory from the operating system, it is split into `heapArena`s.
- Provides the base memory that `mheap` manages.

**Example** (illustrative pseudocode of the runtime internals, not directly compilable or runnable):
```go
func allocateFromHeapArena(size int) {
    // allocate memory from the heapArena
    arena := newHeapArena(size)
    fmt.Println("Allocated memory from heap arena")
}
```

### The Memory Allocation Flow

1. **Small object allocation (<32 KB)**
   - When a goroutine requests a small object, `mcache` first checks whether enough memory is available.
   - If `mcache` has enough memory, the object is allocated directly and returned.
   - If `mcache` does not have enough memory, it requests a new `mspan` from `mcentral`.
   - If `mcentral` has no available `mspan`, it requests a new `mspan` from `mheap`.

2. **Large object allocation (>=32 KB)**
   - When a goroutine requests a large object, memory is requested directly from `mheap`.
   - `mheap` allocates memory pages of the corresponding size and returns them.

### Summary

Go's memory allocator is split across three tiers: `mcache`, `mcentral` and `mheap`. Small objects are allocated in place on the P-private `mcache`, with almost no contention between threads; only when that runs out does it ask `mcentral` for an `mspan`, and if that is also short, `mheap` asks the operating system for memory. The tiering can introduce memory fragmentation, in exchange for allocation speed that fits Go's concurrency model.

Below is an integrated code example that walks through the components:

```go
package main

import (
    "fmt"
    "sync"
)

func allocateSmallObject(size int) {
    // allocate a small object (< 32 KB)
    mem := make([]byte, size)
    // use the memory to prevent it from being optimized away
    mem[0] = 1
    fmt.Println("Allocated small object")
}

func allocateFromCentralCache(sizeClass int) {
    // simulate allocating memory from the central cache
    fmt.Println("Allocated object from central cache of size class", sizeClass)
}

func allocateLargeObject(size int) {
    // allocate a large object (>= 32 KB)
    mem := make([]byte, size)
    // use the memory to prevent it from being optimized away
    mem[0] = 1
    fmt.Println("Allocated large object")
}

func allocateFromSpan(spanSize, objSize int) {
    // simulate allocating an object from a span
    fmt.Printf("Allocated object of size %d from span of size %d\n", objSize, spanSize)
}

func allocateFromHeapArena(size int) {
    // simulate allocating memory from the heapArena
    fmt.Println("Allocated memory from heap arena of size", size)
}

func main() {
    var wg sync.WaitGroup
    wg.Add(3)

    // small object allocation
    go func() {
        defer wg.Done()
        allocateSmallObject(16 * 1024) // 16 KB
    }()

    // allocate an object from the central cache
    go func() {
        defer wg.Done()
        allocateFromCentralCache(1) // Size class 1
    }()

    // large object allocation
    go func() {
        defer wg.Done()
        allocateLargeObject(64 * 1024) // 64 KB
    }()

    wg.Wait()
    fmt.Println("All allocations finished")
}
```

This example threads through the small object, large object and central cache allocation paths; the real allocation logic all lives inside the Go runtime, and application code only ever sees calls like `make`.

## References

- [Official GC guide · Escape analysis and stack allocation](https://go.dev/doc/gc-guide#Escape_analysis)
- [Official GC guide](https://go.dev/doc/gc-guide)
- [Official blog · Allocating on the Stack](https://go.dev/blog/allocation-optimizations)
- [Official blog · Size-Specialized Memory Allocation](https://go.dev/blog/size-specialized-allocations)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Practice](/alloc/Practice.md)
- [glossary](/glossary.md)
