## 反射（Reflection）

### 引言

反射让程序在运行时检查和操作变量的类型和值，代价是复杂度和性能开销，所以只在必要处用。下面的例子覆盖读取类型与值、创建和修改值、调用方法与函数、读结构体标签、深拷贝。

### 为什么需要反射

反射处理的是编译期确定不了的类型信息，通用库、序列化、校验这类工具用得上：

- **序列化和反序列化**：将数据结构转换为 JSON、XML 或其他格式，或者从这些格式解析数据。
- **数据验证和处理**：通过读取结构体标签动态验证数据。
- **通用函数**：编写处理任意类型输入的通用函数。
- **动态调用**：在不知道具体类型和方法的情况下，动态调用对象的方法。

### 基本概念

反射主要由 `reflect` 包提供，包含以下几个关键概念：

- **类型（Type）**：表示一个变量的类型，通过 `reflect.Type` 获取。
- **值（Value）**：表示一个变量的值，通过 `reflect.Value` 获取。
- **种类（Kind）**：表示类型的底层种类，如整数、浮点数、结构体等。

#### 获取类型和值

使用 `reflect.TypeOf` 和 `reflect.ValueOf` 可以获取变量的类型和值。

```go
package main

import (
    "fmt"
    "reflect"
)

func main() {
    var x float64 = 3.4

    t := reflect.TypeOf(x)
    v := reflect.ValueOf(x)

    fmt.Println("Type:", t)       // 输出：Type: float64
    fmt.Println("Value:", v)      // 输出：Value: 3.4
    fmt.Println("Kind:", t.Kind()) // 输出：Kind: float64
}
```

### 动态创建和修改值

反射除了读，还能动态创建和修改值。

```go
package main

import (
    "fmt"
    "reflect"
)

func main() {
    var x int
    v := reflect.ValueOf(&x).Elem()

    v.SetInt(42)
    fmt.Println("Value of x:", x)  // 输出：Value of x: 42

    sliceType := reflect.SliceOf(reflect.TypeOf(0))
    slice := reflect.MakeSlice(sliceType, 0, 10)

    slice = reflect.Append(slice, reflect.ValueOf(1))
    slice = reflect.Append(slice, reflect.ValueOf(2))

    fmt.Println("Slice:", slice.Interface())  // 输出：Slice: [1 2]
}
```

### 动态调用方法并传递参数

通过反射可以按名字找到方法再调用，参数要先包装成 `reflect.Value`。

```go
package main

import (
    "fmt"
    "reflect"
)

type Person struct {
    Name string
}

func (p Person) Greet(greeting string) {
    fmt.Printf("%s, my name is %s\n", greeting, p.Name)
}

func main() {
    p := Person{Name: "Alice"}
    v := reflect.ValueOf(p)

    method := v.MethodByName("Greet")
    args := []reflect.Value{reflect.ValueOf("Hello")}
    method.Call(args)  // 输出：Hello, my name is Alice
}
```

### 处理结构体标签

结构体标签（tag）要用反射读出来，序列化和字段校验都靠它。

```go
package main

import (
    "fmt"
    "reflect"
)

type User struct {
    Name string `json:"name" validate:"required"`
    Age  int    `json:"age" validate:"min=0"`
}

func main() {
    user := User{Name: "Alice", Age: 30}
    t := reflect.TypeOf(user)

    for i := 0; i < t.NumField(); i++ {
        field := t.Field(i)
        fmt.Printf("Field: %s, JSON Tag: %s, Validate Tag: %s\n",
            field.Name, field.Tag.Get("json"), field.Tag.Get("validate"))
    }
}
```

### 动态调用函数

函数值包装成 `reflect.Value` 后也能 `Call`，参数和结果都从切片里取。

```go
package main

import (
    "fmt"
    "reflect"
)

func Add(a, b int) int {
    return a + b
}

func main() {
    fn := reflect.ValueOf(Add)

    args := []reflect.Value{reflect.ValueOf(1), reflect.ValueOf(2)}

    results := fn.Call(args)

    fmt.Println("Result:", results[0].Int())  // 输出：Result: 3
}
```

### 实现通用函数

通过反射，可以编写处理任意类型输入的通用函数。例如，一个通用的 `Print` 函数，可以打印任意类型的值。

```go
package main

import (
    "fmt"
    "reflect"
)

func Print(v interface{}) {
    value := reflect.ValueOf(v)
    fmt.Printf("Type: %s, Value: %v\n", value.Type(), value.Interface())
}

func main() {
    Print(123)               // 输出：Type: int, Value: 123
    Print("hello")           // 输出：Type: string, Value: hello
    Print([]int{1, 2, 3})    // 输出：Type: []int, Value: [1 2 3]
}
```

### 实现深度拷贝

深度拷贝（deep copy）也用反射做：按 `Kind` 递归处理指针、结构体和切片，其余类型直接赋值。

```go
package main

import (
    "fmt"
    "reflect"
)

func DeepCopy(src interface{}) interface{} {
    srcVal := reflect.ValueOf(src)
    dstVal := reflect.New(srcVal.Type()).Elem()
    deepCopyRecursive(srcVal, dstVal)
    return dstVal.Interface()
}

func deepCopyRecursive(src, dst reflect.Value) {
    switch src.Kind() {
    case reflect.Ptr:
        if !src.IsNil() {
            dst.Set(reflect.New(src.Elem().Type()))
            deepCopyRecursive(src.Elem(), dst.Elem())
        }
    case reflect.Struct:
        for i := 0; i < src.NumField(); i++ {
            deepCopyRecursive(src.Field(i), dst.Field(i))
        }
    case reflect.Slice:
        if !src.IsNil() {
            dst.Set(reflect.MakeSlice(src.Type(), src.Len(), src.Cap()))
            for i := 0; i < src.Len(); i++ {
                deepCopyRecursive(src.Index(i), dst.Index(i))
            }
        }
    default:
        dst.Set(src)
    }
}

func main() {
    type Person struct {
        Name    string
        Friends []string
    }

    p1 := Person{Name: "Alice", Friends: []string{"Bob", "Charlie"}}
    p2 := DeepCopy(p1).(Person)

    p2.Name = "Alice Copy"
    p2.Friends[0] = "Bob Copy"

    fmt.Println("Original:", p1) // 输出：Original: {Alice [Bob Charlie]}
    fmt.Println("Copy:", p2)     // 输出：Copy: {Alice Copy [Bob Copy Charlie]}
}
```

### 反射与泛型

Go 1.18 引入泛型后，两者分工变清楚了：类型集合能用约束表达的，写泛型——编译期实例化，无运行时开销；只有类型集合开放、要到运行时才知道类型时才用反射。泛型函数实例化后就是普通函数，反射照样能拿到它的类型：

```go
package main

import (
	"fmt"
	"reflect"
)

func Sum[T int | float64](vals []T) T {
	var total T
	for _, v := range vals {
		total += v
	}
	return total
}

func main() {
	fmt.Println(Sum([]int{1, 2, 3}))        // 输出：6
	fmt.Println(Sum([]float64{1.5, 2.5}))   // 输出：4
	fmt.Println(reflect.TypeOf(Sum[int]))   // 输出：func([]int) int
}
```

同一件事两条路都通时（比如求和、比较、拷贝），优先泛型；反射留给序列化、标签处理这类真正的动态场景。

### 结论

反射的入口是 `TypeOf` 和 `ValueOf`；改值要先拿到指针再 `Elem`，用 `SetXxx` 写入；调用方法和函数都走 `Call`。代价是丢掉编译期检查、多一层运行时开销，序列化、校验、深拷贝这类场景才值得用。