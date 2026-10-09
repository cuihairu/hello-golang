### unsafe 不安全操作

`unsafe` 包提供编译期安全检查之外的四个能力：`Pointer`（通用指针）、`Sizeof`/`Offsetof`/`Alignof`（类型布局查询）、`Add`（指针步进）、`Slice`（凭指针和长度造切片）。用在和 C 互操作、序列化、性能敏感布局这几处，用错了就是悬垂指针和数据损坏。

### 指针规则

`unsafe.Pointer` 和 `*T` 之间可以自由转换，官方定的规则有六条，常用的三条：

- 任何类型的指针都能转成 `unsafe.Pointer`，也能转回来。
- `unsafe.Pointer` 能和 `uintptr` 互转，但 `uintptr` 是整数——转过去再转回来之间，如果 GC 移动或回收了对象，拿到的就是错的地址。
- 表达式里的 `unsafe.Pointer` 不能做算术，要转 `uintptr` 算完再转回，且保证指针在整个过程中存活。

### 类型布局

结构体的内存布局可以查清楚——这在做二进制协议、和 C 结构体对齐时是必需技能：

```go
package main

import (
	"fmt"
	"unsafe"
)

type T struct {
	a bool
	b int64
	c int32
}

func main() {
	var t T
	fmt.Println("size:", unsafe.Sizeof(t), "offset of b:", unsafe.Offsetof(t.b), "align of b:", unsafe.Alignof(t.b))
	// 输出：size: 24 offset of b: 8 align of b: 8
	fmt.Println("string size:", unsafe.Sizeof("")) // 输出：16（指针 + 长度）
}
```

`bool` 后跟 `int64` 要补 7 字节对齐，所以 `b` 的偏移是 8，整个结构体 24 字节。布局规则细节见 `unsafe` 包文档（golang.google.cn/pkg/unsafe）。

### 与 C 互操作

CGO 的边界上全靠 `unsafe.Pointer` 打通：Go 侧的指针传给 C 时转成 `unsafe.Pointer`，C 内存映射回 Go 类型也靠它。相关约束见 [CGO 工作原理与性能](../cgo/Internals.md) 的指针规则一节。

### 小结

`unsafe` 的四件套各有用途：指针打通类型系统边界，布局查询服务于二进制互操作，算术和切片服务于零拷贝处理。共同前提：保证指针存活、长度不越界。
