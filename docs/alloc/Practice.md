### 内存分配的诊断与实践

分配器与 GC 的机制页在 [Alloc](Alloc.md) 与 [GC](GC.md)，这一页讲怎么诊断分配问题、内存何时真正归还操作系统、以及应用层自管内存的边界。

### 分配问题的诊断

`runtime.ReadMemStats` 是最直接的工具，看分配问题重点盯这几个字段：

| 字段 | 含义 |
| --- | --- |
| `HeapAlloc` | 当前堆上存活对象的总字节数 |
| `Sys` | 向操作系统申请的总字节数（含运行时自身） |
| `HeapReleased` | 已归还给操作系统的字节数 |
| `Mallocs` | 累计分配次数，分配速率过高时增长飞快 |
| `NumGC` | 累计 GC 次数 |

`HeapAlloc` 低而 `Sys` 高，说明堆里大部分是空闲-but-未归还的内存；`Mallocs` 涨得快而 `HeapAlloc` 不涨，说明在大量分配短命对象。

按位置定位分配热点用 pprof 的 heap 剖析：

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

用 `go tool pprof -top heap.out` 看占用最大的分配点（`inuse_space` 视角，采样估算，数值因机器而异）：

```plaintext
Showing nodes accounting for 5250.10kB, 100% of 5250.10kB total
      flat  flat%   sum%        cum   cum%
 4737.10kB 90.23% 90.23%  4737.10kB 90.23%  main.main
```

单个变量到底落在栈还是堆，用 `go build -gcflags=-m`，见 [逃逸分析](../var/Segment.md)。

### 内存何时归还操作系统

GC 回收的对象，内存回到分配器的空闲链表，并不立刻还给操作系统。后台的 scavenger 会慢慢把不用的页还回去，所以进程的 RSS 在流量高峰后要过一段时间才回落。要立刻归还，调 `debug.FreeOSMemory()`；容器里配 `GOMEMLIMIT` 让运行时自己盯着水位，见 [GC 调优](GC.md)。

### 自定义分配器的边界

Go 不支持替换内置分配器。"自定义分配器"在 Go 里的现实形态是应用层自管一块内存：用 `syscall.Mmap` 直接向操作系统申请，绕开运行时的堆，自己排布对象：

```go
package main

import (
	"fmt"
	"syscall"
	"unsafe"
)

func main() {
	// 向操作系统直接申请 4KB 匿名内存
	b, err := syscall.Mmap(-1, 0, 4096,
		syscall.PROT_READ|syscall.PROT_WRITE,
		syscall.MAP_PRIVATE|syscall.MAP_ANONYMOUS)
	if err != nil {
		panic(err)
	}
	defer syscall.Munmap(b)

	// 在这块内存上手工排布一个 int64 数组
	arr := unsafe.Slice((*int64)(unsafe.Pointer(&b[0])), 512)
	for i := range arr {
		arr[i] = int64(i * i)
	}
	fmt.Println(arr[10]) // 输出：100
}
```

这条路绕开了 GC，代价是生命周期全部自己管，`Munmap` 之后指针全是悬空的。绝大多数场景用 `sync.Pool` 复用对象就够了，mmap 自管内存留给超大定长缓冲这类特殊需求。

### 零值保证与共享陷阱

`new` 和 `make` 返回的内存都是清零的，读到的一定是零值，不会泄露上一个使用者留下的数据。真正的坑在共享：

- 切片共享底层数组：从大切片切出一小片长期持有，会把整个大数组都留在内存里。要切断关联就 `append([]T(nil), sub...)` 拷一份。
- map 和切片作为结构体字段是引用头，复制结构体不复制底层数据。
- `unsafe` 绕过类型系统后，零值保证和 GC 的可达性分析都可能失效，除非维护运行时内部结构，否则不用。
