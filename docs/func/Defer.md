# defer
### Go 中的 `defer` 详解

在 Go 语言中，`defer` 用于在函数返回之前执行延迟操作，典型用途是资源释放和清理。

#### 基本用法

`defer` 语句注册一个函数调用，这个函数会在包含 `defer` 语句的函数执行完毕后执行。`defer` 的语法如下：

```go
func functionName() {
    defer deferredFunction()
    // 函数体
}
```

#### 示例：基本用法

```go
package main

import "fmt"

func deferExample() (result int) {
    result = 1
    defer func() {
        fmt.Println("Deferred function called")
        result = 2
    }()
    return
}

func multipleDefers() {
    defer fmt.Println("First deferred")
    defer fmt.Println("Second deferred")
    fmt.Println("Function body")
}

func main() {
    fmt.Println("Starting deferExample:")
    fmt.Println("Return value:", deferExample())

    fmt.Println("\nStarting multipleDefers:")
    multipleDefers()
}
```

**输出：**

```
Starting deferExample:
Deferred function called
Return value: 2

Starting multipleDefers:
Function body
Second deferred
First deferred
```

### 多个 `defer` 的触发顺序

多个 `defer` 语句按照后进先出（LIFO）的顺序执行。这意味着最后一个注册的 `defer` 语句最先执行。

#### 示例：多个 `defer` 语句

```go
package main

import "fmt"

func multipleDefers() {
    defer fmt.Println("First deferred")
    defer fmt.Println("Second deferred")
    fmt.Println("Function body")
}

func main() {
    multipleDefers()
}
```

**输出：**

```
Function body
Second deferred
First deferred
```

### `defer` 与 `return` 的关系

- `defer` 语句在 `return` 执行之后，但在函数真正返回之前执行。
- `defer` 语句可以访问函数的返回值，并且可以修改它们。

#### 示例：`defer` 与 `return` 的关系

```go
package main

import "fmt"

func modifyReturnValue() (result int) {
    result = 1
    defer func() {
        fmt.Println("Deferred function modifies result")
        result = 2
    }()
    return
}

func main() {
    fmt.Println("Return value:", modifyReturnValue())
}
```

**输出：**

```
Deferred function modifies result
Return value: 2
```

### `defer` 与 `for`

在 `for` 循环里用 `defer`，主要注意注册次数和执行顺序这两点；Go 1.14 之后 `defer` 本身的开销也降了不少。

### `defer` 在 `for` 循环中的使用注意事项

#### 1. 每次循环迭代都会注册一个新的 `defer`

每次迭代都会注册一个新的 `defer`，这些调用要等到函数返回才执行；循环次数多时，注册的数据结构一直占着，执行也被攒到最后一刻。

#### 2. `defer` 语句的执行顺序

后注册的先执行。多个资源一起申请时，释放顺序要按这条规则核对。

#### 示例：在 `for` 循环中使用 `defer`

```go
package main

import "fmt"

func main() {
    for i := 0; i < 3; i++ {
        defer fmt.Printf("Deferred: %d\n", i)
    }
}
```

**输出：**

```
Deferred: 2
Deferred: 1
Deferred: 0
```

在这个示例中，尽管 `defer` 语句在循环的每次迭代中都被注册，但它们的执行顺序是相反的，这体现了 `defer` 语句的 LIFO 特性。

### Go 的改进

Go 的 `defer` 机制在版本间有过几次改进，主要是性能。

#### 1. Go 1.14 及以后的性能优化

Go 1.14 起，`defer` 的注册和执行开销都降了，栈管理也更省，高频调用 `defer` 的代码最先受益。

#### 2. 堆栈分配优化

在 Go 1.14 版本之前，`defer` 的开销相对较大，因为每个 `defer` 语句都会在栈上分配一个新的数据结构。Go 1.14 引入了更高效的堆栈分配策略，以减少 `defer` 的开销，尤其是在循环和高并发场景中。

#### 示例：性能改进

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    start := time.Now()
    for i := 0; i < 1000000; i++ {
        defer fmt.Println("Deferred:", i)
    }
    fmt.Println("Time taken:", time.Since(start))
}
```

在 Go 1.14 及以后的版本中，上述示例的执行时间会明显低于早期版本，这反映了 `defer` 性能优化的效果。

#### 总结

- **基本用法**：`defer` 在函数返回之前执行，用于资源清理。
- **`for` 循环中的使用**：每次循环迭代都会注册一个新的 `defer`，执行顺序按 LIFO 规则。
- **Go 的改进**：Go 1.14 及以后版本优化了 `defer` 的性能，减少了开销，并改进了堆栈管理。

### `defer` 的底层实现

`defer` 的底层通过栈结构实现。每当遇到 `defer` 语句时，Go 会将待执行的函数调用和参数压入栈中。在函数返回之前，Go 会按 LIFO 顺序依次弹出栈中的函数调用并执行。

#### 汇编示例

为了理解底层实现，可以查看 Go 的汇编代码。以下是一个简单的汇编代码片段，展示了 `defer` 的处理（部分简化）：

```assembly
TEXT main.deferredExample(SB), NOSPLIT, $0
	MOVQ	$1, result(SP)
	// 设置 deferred function
	MOVQ	$deferFunction(SB), R8
	MOVQ	R8, deferCall(SP)
	RET

TEXT main.multipleDefers(SB), NOSPLIT, $0
	// 设置第一个 deferred function
	MOVQ	$firstDeferred(SB), R8
	MOVQ	R8, deferCall1(SP)
	// 设置第二个 deferred function
	MOVQ	$secondDeferred(SB), R8
	MOVQ	R8, deferCall2(SP)
	RET

TEXT deferFunction(SB), NOSPLIT, $0
	// 执行 deferred function
	RET

TEXT firstDeferred(SB), NOSPLIT, $0
	// 执行第一个 deferred function
	RET

TEXT secondDeferred(SB), NOSPLIT, $0
	// 执行第二个 deferred function
	RET
```

### 总结

- **基本用法**：`defer` 用于在函数返回之前执行清理操作。
- **多个 `defer` 语句**：按照后进先出（LIFO）顺序执行。
- **与 `return` 的关系**：`defer` 语句在 `return` 执行后但在函数真正返回之前执行，可以修改返回值。
- **底层实现**：`defer` 使用栈结构来管理函数调用，确保按 LIFO 顺序执行。