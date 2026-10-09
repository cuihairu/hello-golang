### 编写 Plan9 程序

指令集参考见 [Plan 9 汇编指令](Assembly.md)，这一页讲怎么写出能被 Go 工具链接的汇编：伪寄存器、函数声明，以及一个可运行的完整例子。

### 伪寄存器

Plan9 汇编里这四个不是真实寄存器，是链接器的记号：

| 记号 | 含义 |
| --- | --- |
| `SB` | 静态基址，所有全局符号的锚点，写法 `symbol(SB)` |
| `FP` | 帧指针，访问调用方传进来的参数与返回值，写法 `a+0(FP)` |
| `SP` | 伪栈指针，指向当前帧局部变量区（与硬件 SP 不是一回事） |
| `PC` | 程序计数器，用于跳转寻址 |

符号名里的 `·`（中间点）分隔包名与函数名：`·Add(SB)` 在链接后就是 `main.Add`。

### 函数声明

每个汇编函数用 `TEXT` 声明，帧大小写成 `$帧字节数-参数加返回值字节数`：

```assembly
#include "textflag.h"

// func Add(a, b int64) int64
TEXT ·Add(SB), NOSPLIT, $0-24
    MOVQ a+0(FP), AX
    ADDQ b+8(FP), AX
    MOVQ AX, ret+16(FP)
    RET
```

`$0-24` 表示本函数不申请局部栈空间，参数加返回值共 24 字节（两个 int64 参数加一个 int64 返回值）。`NOSPLIT` 表示不加栈增长检查——只适用于确认不超栈的小函数，需要 `#include "textflag.h"` 提供这个宏。

Go 侧只要声明函数签名（不写函数体），链接器就会找到汇编实现：

```go
package main

import "fmt"

// Add 在 add.s 中用 Plan9 汇编实现
func Add(a, b int64) int64

func main() {
	fmt.Println(Add(2, 3)) // 输出：5
}
```

`.s` 文件与 `.go` 文件放在同一个包目录，`go build` 会自动把它们编在一起。

### 从 Go 生成汇编

手写汇编前，先看编译器生成什么。`go build -gcflags=-S` 打印每个函数的汇编（上面这个例子的调用点）：

```assembly
0x0020 00032 (main.go:9)	CALL	main.Add(SB)
0x0025 00037 (main.go:9)	XORPS	X15, X15
0x0029 00041 (main.go:9)	MOVQ	(TLS), R14
```

写性能敏感函数的流程：先用 Go 写出正确版本，`-gcflags=-S` 看编译器产物，确认热点后再决定要不要手写覆盖。`go tool objdump 二进制` 可以反汇编已编译产物，两者对照着看。

### 小结

伪寄存器（`SB`/`FP`/`SP`/`PC`）是链接器的语言，`TEXT` 声明里帧大小带出参数布局；Go 侧声明签名、汇编侧给实现，同目录即链接。真要动手前先看编译器生成的汇编，多数热点它已经排得不错。
