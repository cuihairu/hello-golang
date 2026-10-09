### 错误处理与限制

反射的写操作有前提条件，不满足时直接 panic，调用前要先检查：

- 改值前用 `CanSet()` 判断；拿到指针再 `Elem()` 是可改的，直接 `ValueOf(x)` 得到的 Value 不可改。
- 未导出字段（小写开头）的 `CanSet()` 是 `false`，`SetXxx` 会 panic；要改只能走 `unsafe`，不推荐。
- `Call` 的参数类型必须和方法签名匹配，否则 panic；返回值从切片里取，类型也要自己断言。

```go
package main

import (
    "fmt"
    "reflect"
)

func safeCall(fn interface{}, args ...interface{}) (results []interface{}, err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("reflect call panic: %v", r)
        }
    }()

    v := reflect.ValueOf(fn)
    in := make([]reflect.Value, len(args))
    for i, a := range args {
        in[i] = reflect.ValueOf(a)
    }
    out := v.Call(in)
    results = make([]interface{}, len(out))
    for i, r := range out {
        results[i] = r.Interface()
    }
    return
}

func Add(a, b int) int { return a + b }

func main() {
    res, err := safeCall(Add, 1, 2)
    fmt.Println(res, err) // 输出：[3] <nil>

    _, err = safeCall(Add, 1, "2")
    fmt.Println(err) // 输出：reflect call panic: reflect: Call using string as type int
}
```

### 性能

反射慢在三处：参数和返回值要装箱成 `reflect.Value`、类型信息在运行时查、`Call` 走的是通用分发而不是直接跳转。热路径上反射比直接调用慢一个量级以上，具体倍数随场景变，用 `testing.B` 基准测自己的场景。

热路径的替代顺序：

1. **类型 switch**：类型有限时用 `switch v := x.(type)`，编译期检查、无装箱。
2. **泛型**（Go 1.18+）：能写成泛型约束的别用反射，编译期实例化后就是直接调用。
3. **代码生成**：类型集合固定但很大时，用 `go generate` 生成具体代码。

### 并发

`reflect.Value` 的写操作（`SetXxx`、`Call`）不是并发安全的：多个 goroutine 同时改同一个 Value 要加锁。只读场景（`Type`、`Interface`、`Kind`）可以并发调用。反射创建的对象（`New`、`MakeSlice`）各自独立，不存在共享问题。

### 小结

反射的写操作先查 `CanSet`，参数类型自己保证，panic 用 `recover` 兜住；热路径优先类型 switch、泛型、代码生成；并发场景只读不写，写就加锁。基础用法见 [反射基础](Reflection.md)。
