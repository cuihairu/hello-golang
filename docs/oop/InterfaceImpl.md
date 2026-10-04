接口值在底层就是一个二元组：一个指向类型描述符的指针，加一个指向实际数据的指针。这一章从数据结构、方法表讲到汇编调用，最后落在 `nil` 接口和空接口这两处。

### 1. 接口的底层数据结构

Go 语言中的接口由两个主要部分组成：

1. **类型信息（Type Descriptor）**：描述接口实现的具体类型，包括方法表和类型信息。
2. **值信息（Value）**：存储实现接口的实际值，即对象实例。

接口的底层结构可以简化为以下结构（真实实现见 `runtime` 包中的 `eface`、`iface` 和 `itab` 结构体；注意 `type` 是 Go 关键字，不能用作字段名，这里用 `typ` 表示）：

```go
type _interface struct {
    typ   *typeDescriptor // 类型描述符
    value unsafe.Pointer  // 指向实际值
}
```

### 2. 类型描述符（Type Descriptor）

`typeDescriptor` 是一个内部结构，包含了类型的元数据，如方法表、类型名称等。每个实现了接口的类型都有一个对应的类型描述符。方法表是一个函数指针数组，其中每个指针指向实现了接口方法的实际函数。

**示例：接口的类型描述符**

```go
type typeDescriptor struct {
    methodTable *methodTable // 方法表
    typeName    string       // 类型名称
    // 其他元数据
}

type methodTable struct {
    // 函数指针数组
    methodPtrs []uintptr
}
```

### 3. 方法表（Method Table）

方法表是一个函数指针数组，其中的每个指针都指向接口方法的实现。方法表使得 Go 能够在运行时动态地调用接口的方法。

**示例：方法表结构**

```go
type methodTable struct {
    methods []func()
}
```

### 4. 接口的底层实现源码（简化版）

Go 语言的标准库中，接口的底层实现是相对复杂的，以下是简化的实现示例，说明了接口如何使用方法表和类型描述符。

```go
package main

import (
    "fmt"
    "reflect"
)

// 接口定义
type Speaker interface {
    Speak() string
}

// 类型实现接口
type Person struct {
    Name string
}

// 实现接口方法
func (p Person) Speak() string {
    return "Hi, I'm " + p.Name
}

func main() {
    var s Speaker = Person{Name: "Alice"}

    // 类型断言
    if person, ok := s.(Person); ok {
        fmt.Println("Person:", person.Name) // 输出: Person: Alice
    } else {
        fmt.Println("Not a Person")
    }

    // 使用 reflect 包获取接口底层信息
    t := reflect.TypeOf(s)
    fmt.Println("Type:", t) // 输出: Type: main.Person
    fmt.Println("Value:", reflect.ValueOf(s)) // 输出: Value: {Alice}
}
```

### 5. 底层实现示例（汇编）

接口方法的动态分派最终落在一小段汇编上。下面是一个简化的示例（以 `amd64` 架构为例）：

**示例：Go 汇编**

```assembly
TEXT runtime.reflectcall(SB), NOSPLIT, $0
	MOVQ	8(SP), SI
	MOVQ	16(SP), CX
	MOVQ	24(SP), DI
	CALL	runtime.callReflection
	RET
```

在上面的汇编代码中，`reflectcall` 函数是用来调用接口的实际方法。它通过 `MOVQ` 指令将参数加载到寄存器中，并调用 `runtime.callReflection` 函数来执行接口方法。

### 6. 接口的调用流程

当接口方法被调用时，Go 的运行时系统会根据接口的类型描述符和方法表来找到具体的实现。调用流程如下：

1. **获取类型描述符**：从接口中获取类型描述符，类型描述符包含了方法表和类型名称。
2. **获取方法表**：从类型描述符中获取方法表，方法表包含了接口方法的实现地址。
3. **调用方法**：根据方法表中的函数指针调用具体的实现函数。

### 7. 接口的零值和空接口

- **接口的零值**：接口的零值是 `nil`，它表示接口变量未被初始化。调用未初始化的接口方法会导致运行时错误。
- **空接口**：`interface{}` 可以表示任何类型的数据，因为它没有方法集合。空接口在通用函数和数据结构中非常有用。

**示例：空接口**

```go
package main

import "fmt"

func printAnything(i interface{}) {
    fmt.Println(i)
}

func main() {
    printAnything(42)         // 整数
    printAnything("hello")    // 字符串
    printAnything([]int{1, 2}) // 切片
}
```

### 总结

- **接口的底层数据结构**：包括类型描述符和方法表，用于存储接口的类型信息和方法实现。
- **类型描述符**：包含方法表和类型名称，用于描述实现接口的具体类型。
- **方法表**：函数指针数组，用于存储接口方法的实现。
- **汇编示例**：展示了接口的底层操作和调用流程。
- **接口的零值和空接口**：接口的零值是 `nil`，空接口可以接受任何类型的数据。

理解了"接口值 = 类型指针 + 数据指针"，两个问题就有了答案：为什么 `nil` 接口调用方法会 panic（类型指针为空，方法表无从查起）；为什么往接口里存一个值为 `nil` 的指针再判 `== nil` 得到 `false`（类型指针不为空）。