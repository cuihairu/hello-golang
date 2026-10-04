# GC

Go 的内存由运行时自动管理：分配器负责给对象分配内存，垃圾回收器（GC，Garbage Collector）负责回收不再使用的内存。本节从内存分配的视角介绍 GC 的基本原理、它与分配器的协作方式，以及常用的调优手段。

### GC 与内存分配器的关系

- **分配时**：小对象从 `mcache` → `mcentral` → `mheap` 的链路中获取内存；大对象（大于 32 KB）直接从 `mheap` 分配。
- **回收时**：GC 判断对象不再可达后，将其占用的 `mspan` 标记为空闲，这些 `mspan` 会重新回到分配器的空闲链表中供后续分配使用，而不是立刻归还操作系统。
- 因此，GC 的回收单位与分配单位一致，都是 `mspan`/页，这也是上一节介绍的分层结构的另一半。

### 基本原理：并发标记-清除

Go 的 GC 是并发三色标记-清除回收器：

1. **标记（Mark）**：从根对象（全局变量、各 goroutine 栈上的变量等）出发，通过三色抽象标记所有存活对象，标记过程与用户程序并发执行，仅在开始和结束时有两段极短的 STW（Stop-The-World）。
2. **清除（Sweep）**：清除未标记的对象占用的内存，清除操作也是并发/惰性进行的（分配内存时顺带完成一部分清扫工作）。

### 实践：观察 GC 的行为

下面的程序演示如何读取 GC 统计信息、手动触发 GC，并用 `runtime.MemStats` 观察 `HeapAlloc` 与 `NumGC` 的变化：

```go
package main

import (
	"fmt"
	"runtime"
	"time"
)

func main() {
	var mem runtime.MemStats

	fmt.Println("--- 分配前 ---")
	runtime.ReadMemStats(&mem)
	fmt.Println("HeapAlloc(KB):", mem.HeapAlloc/1024, "NumGC:", mem.NumGC)

	// 分配 100 个 1MB 的临时对象，让它们迅速变为垃圾
	for i := 0; i < 100; i++ {
		_ = make([]byte, 1024*1024)
	}

	fmt.Println("--- 分配后（GC 之前） ---")
	runtime.ReadMemStats(&mem)
	fmt.Println("HeapAlloc(KB):", mem.HeapAlloc/1024, "NumGC:", mem.NumGC)

	// 手动触发一次 GC
	runtime.GC()
	runtime.ReadMemStats(&mem)
	fmt.Println("--- 手动 GC 之后 ---")
	fmt.Println("HeapAlloc(KB):", mem.HeapAlloc/1024, "NumGC:", mem.NumGC)

	// 防止编译器把前面的分配提前优化掉
	time.Sleep(10 * time.Millisecond)
}
```

输出示例（具体数值因机器而异；注意分配 100 个 1MB 对象的过程中 GC 已自动触发过多次，所以 NumGC 已经增长）：

```
--- 分配前 ---
HeapAlloc(KB): 269 NumGC: 0
--- 分配后（GC 之前） ---
HeapAlloc(KB): 2355 NumGC: 36
--- 手动 GC 之后 ---
HeapAlloc(KB): 307 NumGC: 37
```

### 常用的 GC 调优手段

1. **GOGC**：控制 GC 触发时机，默认为 100，表示当新分配的内存达到上次存活内存的 100% 时触发 GC。增大该值会减少 GC 次数、增加内存占用；减小则相反。`GOGC=off` 可完全关闭 GC（仅用于实验）。

   ```sh
   GOGC=200 ./myapp   # 降低 GC 频率
   GOGC=50 ./myapp    # 更积极地进行 GC
   ```

2. **GOMEMLIMIT / debug.SetMemoryLimit**：Go 1.19 引入的软内存上限。运行时会在逼近上限时更频繁地 GC，适合内存受限的容器环境：

   ```go
   import "runtime/debug"

   func init() {
       debug.SetMemoryLimit(512 << 20) // 512 MiB
   }
   ```

3. **GOGC 与 GOMEMLIMIT 的配合**：Go 会同时考虑两者，取更先满足的条件触发 GC。推荐容器内同时设置两者，兼顾 CPU 开销与内存水位。

4. **减少垃圾产生**：相比调参，降低分配速率往往更有效：
   - 使用 `sync.Pool` 复用临时对象；
   - 预分配切片容量（`make([]T, 0, n)`），避免反复扩容；
   - 注意 `string` 与 `[]byte` 的相互转换会产生拷贝；
   - 避免不必要的指针装箱（如 `interface{}` 包装基本类型）。

```go
package main

import (
	"fmt"
	"runtime"
	"runtime/debug"
)

func main() {
	debug.SetGCPercent(200) // 相当于 GOGC=200

	// 用 sync.Pool 复用 4KB 的缓冲区，减少分配
	pool := sync.Pool{
		New: func() interface{} {
			buf := make([]byte, 4096)
			return &buf
		},
	}

	for i := 0; i < 1000; i++ {
		buf := pool.Get().(*[]byte)
		_ = (*buf)[0] // 使用缓冲区
		pool.Put(buf)
	}

	var mem runtime.MemStats
	runtime.ReadMemStats(&mem)
	fmt.Println("总分配次数(Mallocs):", mem.Mallocs)
}
```

### 常见误区

- **把 GC 当万能兜底**：GC 只回收不可达对象。把对象挂在一个永不清空的全局 map 上，GC 同样无法回收它，这就是典型的内存泄漏。
- **认为设置 `runtime.GC()` 能解决内存问题**：手动 GC 只是提前执行了本会发生的事情，频繁手动触发反而浪费 CPU。
- **忽略 goroutine 泄漏**：阻塞在 channel 上的 goroutine 及其引用的对象永远不可达回收，必要时用 `runtime.NumGoroutine()` 或 pprof 的 goroutine 剖析排查。

### 总结

Go 的 GC 与分层内存分配器（`mcache`/`mcentral`/`mheap`）是一体两面：分配器决定内存从哪里来，GC 决定内存何时回到分配器手中。调优时把 `GOGC`、`GOMEMLIMIT` 和分配速率放在一起看：前两个分别控制回收时机和内存上限，第三个决定垃圾产生得多快。
