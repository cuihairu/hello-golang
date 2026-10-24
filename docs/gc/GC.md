Go's garbage collector (GC, Garbage Collector) is a concurrent mark-and-sweep collector: marking and sweeping both run alongside user code, and the program is only briefly stopped when necessary.

### How Go's Garbage Collector Works

One GC cycle has two steps, marking and sweeping, and both phases run concurrently whenever possible.

#### 1. The Marking Phase

During the marking phase, the GC walks every live object and marks it "live". It starts from a set of objects called roots. These roots include global variables, local variables on the stack, and variables currently held in registers. The GC then recursively walks every object reachable from the roots and marks those as "live" too.

#### 2. The Sweeping Phase

During the sweeping phase, the GC walks the heap and clears every object that was not marked "live". Those objects are considered no longer in use, so their memory can be reclaimed and handed out again.

#### 3. Concurrent Execution

Go's garbage collector is a concurrent mark-and-sweep collector, which means it runs concurrently whenever possible to reduce its impact on the program. The marking and sweeping phases can run on multiple threads at once, cutting down the time the GC stops the program. The GC also uses an algorithm called "tricolor marking" to stay consistent while marking concurrently.

### The Tricolor Marking Algorithm

The tricolor marking algorithm divides objects into three classes:

1. **White: objects not yet visited**
2. **Gray: objects visited but not all of whose children have been visited**
3. **Black: objects visited and all of whose children have been visited**

The marking process goes like this:

1. Every object starts white.
2. Roots are marked gray and put into the mark queue.
3. Gray objects are processed one at a time: the object is marked black and the objects it references are marked gray.
4. When there are no more gray objects, marking is done. Everything still not marked black is white (unreachable) and can be swept.

### What Triggers Garbage Collection

Go's garbage collector starts a collection based on conditions such as the amount of memory allocated, the memory usage rate, and manual triggers. Typically, when the heap grows past a certain point, the GC runs on its own.

### Tuning the Garbage Collector

Go provides several knobs to tune the garbage collector for different workloads. For example:

- **The `GOGC` environment variable**: controls how often GC runs. The default is 100, meaning one collection is triggered for every 100% growth in heap memory. Lowering it triggers collections more often but increases GC overhead; raising it reduces collection frequency but can let memory usage grow.
- **The `runtime.GC()` function**: triggers garbage collection manually.
- **The `runtime.ReadMemStats()` function**: reads garbage collection statistics.

### Code Example

Trigger garbage collection manually and read the statistics:

```go
package main

import (
    "fmt"
    "runtime"
    "time"
)

func main() {
    // start a goroutine that allocates a lot of memory
    go func() {
        for i := 0; i < 10; i++ {
            _ = make([]byte, 10*1024*1024) // allocate 10 MB
            time.Sleep(1 * time.Second)
        }
    }()

    // trigger garbage collection manually
    runtime.GC()

    // read the garbage collection statistics
    var memStats runtime.MemStats
    runtime.ReadMemStats(&memStats)
    fmt.Printf("Allocated: %v MB\n", memStats.Alloc/1024/1024)
    fmt.Printf("Total Allocated: %v MB\n", memStats.TotalAlloc/1024/1024)
    fmt.Printf("Heap Allocated: %v MB\n", memStats.HeapAlloc/1024/1024)
    fmt.Printf("Number of GC: %v\n", memStats.NumGC)

    // let the program run a while so you can observe the GC
    time.Sleep(20 * time.Second)
}
```

The example starts a goroutine that allocates 10 MB a second to force garbage collection, has the main flow call `runtime.GC()` manually, and then prints the bytes allocated, total bytes allocated, and the GC count via `runtime.ReadMemStats`.

### When GC Affects Performance

A few situations make the GC show up in the program's performance:

1. **Frequent allocation and collection of small objects**:
   - When the program allocates and frees small objects all the time, the garbage collector may trigger often, which adds CPU consumption and pauses in execution (stops of goroutines).
   - Fix: reuse objects through an object pool (`sync.Pool`) to take pressure off the collector, or cut back on how often you allocate.

2. **Allocation and release of large objects**:
   - Frequent allocation and release of large objects — especially ones above the large-object threshold (32 KB, above which objects go straight to the heap) — puts more pressure on the heap and makes the collector run more often.
   - Fix: consider reusing large objects; you can also adjust the trigger threshold with the `GOGC` environment variable or `debug.SetMemoryLimit` (`GOMEMLIMIT`). `GODEBUG=gctrace=1` shows GC debug information.

3. **Long pause times**:
   - Go's garbage collector runs concurrently, but it can still cause long stop-the-world pauses in some situations, particularly during a full global collection.
   - Fix: try reducing long pauses by tuning GC parameters — adjust the trigger threshold with `GOGC`, or use `GODEBUG=gctrace=1` to look at detailed GC output and optimize the code.

4. **Memory leaks**:
   - If the program has a memory leak (objects no longer used but still holding memory), the collector may not reclaim them in time, so overall memory usage climbs and hurts performance.
   - Fix: use tools such as `pprof` to find and analyze the leak and fix the code in time.

The GC itself rarely becomes the bottleneck, but these four situations — allocating small objects too eagerly, creating and releasing large objects over and over, long pauses, and memory leaks — are where it shows up, and the fixes for each are listed above.

### The History of Go GC Optimizations

The throughline of every Go GC optimization is shortening the stop-the-world (STW) pause. What changed by version:

- **Go 1.3**: introduced parallel sweeping; marking still needed STW, and the pause was on the order of a few hundred milliseconds.
- **Go 1.5**: implemented concurrent mark and sweep; the pause dropped below 100 milliseconds.
- **Go 1.6**: used bitmaps to record where memory had been swept, improving the memory the collector itself consumed; the pause dropped below 10 milliseconds.
- **Go 1.7**: further optimizations brought the pause under 2 milliseconds.
- **Go 1.8**: introduced the hybrid write barrier, which cut STW time dramatically; the pause was around half a millisecond.
- **Go 1.9**: removed the rescanning of stacks entirely, improving GC efficiency further.
- **Go 1.14**: introduced asynchronous preemption, which fixed the long STW times caused by tight loops.

In particular, Go 1.18 added `debug.SetMemoryLimit`, a built-in function that adjusts the heap memory target that triggers GC, reducing the number of collections and the CPU they consume. In practice this improves the `gcTriggerHeap` policy: looking at the code, when `gcControllerState.heapGoalInternal` computes the HeapGoal it uses two methods — one from the `GOGC` value and one from the `memoryLimit` value — and takes whichever of the two is smaller as the HeapGoal.

The STW pause went from a few hundred milliseconds in Go 1.3 to half a millisecond in Go 1.8, and each segment of that curve corresponds to one of the version changes above.


### Summary

Go's GC does concurrent marking with tricolor marking, and once marking is consistent it sweeps the white objects. `GOGC` controls how often it triggers, defaulting to 100; `debug.SetMemoryLimit` adds a second cap on the heap target, and the smaller of the two becomes the HeapGoal.

## References

- [Official · A Guide to the Go Garbage Collector](https://go.dev/doc/gc-guide)
- [Official blog · Go GC: Prioritizing low latency and simplicity](https://go.dev/blog/go15gc)
- [Official blog · Getting to Go (GC evolution)](https://go.dev/blog/ismmkeynote)
- [Official blog · The Green Tea Garbage Collector](https://go.dev/blog/greenteagc)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
