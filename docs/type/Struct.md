## Go语言中的`struct`详解

Go语言中的`struct`是一种聚合数据类型，把多个可以是不同类型的值组合在一起，地位相当于其他编程语言中的类或记录。

### 1. `struct`的基本语法

定义一个`struct`并创建其实例的基本语法如下：

```go
// 定义一个struct
type Person struct {
    Name string
    Age  int
}

// 创建实例
func main() {
    // 使用字段名初始化
    p1 := Person{Name: "Alice", Age: 30}
    
    // 按顺序初始化
    p2 := Person{"Bob", 25}
    
    // 零值初始化
    var p3 Person

    // 访问和修改字段
    p1.Name = "Charlie"
    fmt.Println(p1.Name, p1.Age)
    fmt.Println(p2) // 输出 {Bob 25}
    fmt.Println(p3) // 输出 { 0}（零值）
}
```

### 2. `struct`占用空间，空`struct`的使用

`struct`在内存中的占用空间取决于其字段类型和对齐方式。一个空的`struct{}`不占用任何空间（大小为0），通常用于信号传递或标识。

```go
type Empty struct{}

func main() {
    var e Empty
    fmt.Println(unsafe.Sizeof(e)) // 输出 0
}
```

### 3. `struct`绑定方法与面向对象编程，以及与`interface`的关系

在Go中，方法可以绑定到`struct`上，这允许我们模拟面向对象编程（OOP）。方法是定义在`struct`上的函数，可以使用值接收者或指针接收者。

```go
type Rectangle struct {
    Width, Height float64
}

// 值接收者方法
func (r Rectangle) Area() float64 {
    return r.Width * r.Height
}

// 指针接收者方法
func (r *Rectangle) Scale(factor float64) {
    r.Width *= factor
    r.Height *= factor
}

func main() {
    r := Rectangle{10, 20}
    fmt.Println(r.Area()) // 输出 200

    r.Scale(2)
    fmt.Println(r.Area()) // 输出 800
}
```

`interface`是Go中实现多态的关键，`struct`通过实现`interface`中的方法来满足该接口。

```go
type Shape interface {
    Area() float64
}

type Circle struct {
    Radius float64
}

func (c Circle) Area() float64 {
    return 3.14 * c.Radius * c.Radius
}

func main() {
    var s Shape
    s = Circle{10}
    fmt.Println(s.Area()) // 输出 314
}
```

### 4. 组合与聚合

#### 组合（Composition）

组合表示强拥有关系（strong ownership），即子对象的生命周期依赖于父对象。如果父对象被销毁，子对象也会被销毁。在Go中，组合通常通过将一个结构体嵌套在另一个结构体中来实现。

```go
package main

import "fmt"

// 定义一个 Base 结构体
type Base struct {
    Name string
}

// 为 Base 定义一个方法
func (b Base) SayHello() {
    fmt.Println("Hello, my name is", b.Name)
}

// 定义一个包含 Base 的结构体
type Derived struct {
    Base
    Age int
}

func main() {
    d := Derived{
        Base: Base{Name: "Alice"},
        Age:  30,
    }

    // 直接调用 Base 的方法
    d.SayHello() // 输出 "Hello, my name is Alice"
}
```

#### 聚合（Aggregation）

聚合表示弱拥有关系（weak ownership），即子对象的生命周期独立于父对象。子对象可以在多个父对象之间共享。在Go中，聚合通常通过指针来实现，即父对象持有子对象的指针。

```go
package main

import "fmt"

// 定义 Engine 结构体
type Engine struct {
    Power int
}

// 定义 Car 结构体，通过指针实现聚合
type Car struct {
    Brand  string
    Engine *Engine // 聚合，持有指针
}

func main() {
    e := &Engine{Power: 200}
    c1 := Car{Brand: "Toyota", Engine: e}
    c2 := Car{Brand: "Honda", Engine: e}

    fmt.Println(c1.Brand, "with power", c1.Engine.Power) // 输出 "Toyota with power 200"
    fmt.Println(c2.Brand, "with power", c2.Engine.Power) // 输出 "Honda with power 200"
}
```

### 5. 零值初始化

在Go中，所有变量在声明时都会自动初始化为零值。对于`struct`来说，每个字段都会被初始化为其类型的零值。

```go
type Person struct {
    Name  string
    Age   int
    Email string
}

func main() {
    var p Person
    fmt.Println(p) // 输出 { 0 }
}
```

### 6. 深拷贝与浅拷贝

在Go中，赋值操作会创建`struct`的浅拷贝。需要深拷贝时，引用类型的字段得手动复制一份。

#### 浅拷贝

浅拷贝（shallow copy）是指直接赋值结构体或其指针，从而复制结构体的字段，但不复制引用类型字段指向的底层数据。对浅拷贝的结构体修改某些字段不会影响到原结构体，除非这些字段是引用类型（如指针、切片、映射等），这种情况下，两者共享底层数据。

```go
package main

import "fmt"

type Person struct {
    Name   string
    Age    int
    Friends []string
}

func main() {
    p1 := Person{Name: "Alice", Age: 30, Friends: []string{"Bob", "Charlie"}}
    p2 := p1 // 浅拷贝

    p2.Name = "Bob"
    p2.Friends[0] = "David"

    fmt.Println(p1.Name)   // 输出 "Alice"
    fmt.Println(p1.Friends) // 输出 "[David Charlie]"
    fmt.Println(p2.Name)   // 输出 "Bob"
    fmt.Println(p2.Friends) // 输出 "[David Charlie]"
}
```

在这个例子中，`p1`和`p2`是两个独立的结构体实例，对`p2.Name`的修改不会影响`p1.Name`。但是，由于`Friends`是一个切片（引用类型），`p1.Friends`和`p2.Friends`共享底层数据，对`p2.Friends`的修改会影响到`p1.Friends`。

#### 深拷贝

深拷贝（deep copy）是指复制整个结构体及其所有嵌套的引用类型字段，生成一个独立的副本，修改新结构体不会影响原结构体。深拷贝通常需要手动实现，特别是对于包含引用类型的结构体。

```go
package main

import "fmt"

// 定义Person结构体
type Person struct {
    Name    string
    Age     int
    Friends []string
}

// 深拷贝函数
func (p Person) DeepCopy() Person {
    // 复制基础字段
    newPerson := p

    // 手动复制引用类型字段
    newPerson.Friends = make([]string, len(p.Friends))
    copy(newPerson.Friends, p.Friends)

    return newPerson
}

func main() {
    p1 := Person{Name: "Alice", Age: 30, Friends: []string{"Bob", "Charlie"}}
    p2 := p1.DeepCopy() // 深拷贝

    p2.Name = "Bob"
    p2.Friends[0] = "David"

    fmt.Println(p1.Name)    // 输出 "Alice"
    fmt.Println(p1.Friends) // 输出 "[Bob Charlie]"
    fmt.Println(p2.Name)    // 输出 "Bob"
    fmt.Println(p2.Friends) // 输出 "[David Charlie]"
}
```

在这个例子中，通过实现`DeepCopy`方法，确保`p2`是`p1`的独立副本，对`p2`的修改不会影响到`p1`，包括引用类型字段。

#### 总结

- **浅拷贝**：通过直接赋值实现，复制值类型字段，但引用类型字段共享底层数据。
- **深拷贝**：需要手动实现，复制值类型字段和引用类型字段，生成完全独立的副本。

结构体里有切片、映射、指针这些引用类型字段时，赋值出来的两个结构体共用底层数据，改一边另一边跟着变——要隔离就得手动深拷贝。

### 7. 方法集（Method Sets）

方法集决定了一个类型是否实现了某个接口。对于类型T，其方法集包含所有使用值接收者声明的方法。对于类型*T，其方法集包含所有使用值接收者和指针接收者声明的方法。

```go
type Person struct {
    Name string
}

func (p Person) SayHello() {
    fmt.Println("Hello, my name is", p.Name)
}

func (p *Person) SetName(name string) {
    p.Name = name
}

func main() {
    p := Person{Name: "Alice"}
    p.SayHello() // 输出 "Hello, my name is Alice"

    p.SetName("Bob")
    p.SayHello() // 输出 "Hello, my name is Bob"
}
```

在Go语言中，方法集的继承遵循结构体的组合规则。结构体组合可以通过嵌套其他结构体来实现，这种方式允许一个结构体“继承”多个基类结构体的方法。然而，如果嵌套的结构体中存在同名方法，则需要显式指定访问哪个基类的同名方法，否则会导致编译错误。

#### 方法集继承规则

当一个结构体嵌套了另一个结构体时，它会“继承”嵌套结构体的方法。这意味着可以直接调用嵌套结构体的方法，而不需要显式访问嵌套的结构体。

##### 示例：单一继承

```go
package main

import "fmt"

type Base struct{}

func (b Base) SayHello() {
    fmt.Println("Hello from Base")
}

type Derived struct {
    Base
}

func main() {
    d := Derived{}
    d.SayHello() // 输出 "Hello from Base"
}
```

在这个例子中，`Derived`结构体嵌套了`Base`结构体，因此可以直接调用`Base`结构体的`SayHello`方法。

##### 示例：多重继承（方法冲突）

当一个结构体嵌套多个结构体时，如果这些嵌套的结构体中存在同名方法，则需要显式指定访问哪个基类的同名方法。

```go
package main

import "fmt"

type A struct{}

func (a A) SayHello() {
    fmt.Println("Hello from A")
}

type B struct{}

func (b B) SayHello() {
    fmt.Println("Hello from B")
}

type C struct {
    A
    B
}

func main() {
    c := C{}
    // c.SayHello() // 编译错误：ambiguous selector c.SayHello
    c.A.SayHello() // 输出 "Hello from A"
    c.B.SayHello() // 输出 "Hello from B"
}
```

在这个例子中，`C`结构体嵌套了`A`和`B`两个结构体，并且这两个结构体中都有`SayHello`方法。直接调用`c.SayHello()`会导致编译错误，因为编译器无法确定应该调用哪个`SayHello`方法。需要显式指定调用`c.A.SayHello()`或`c.B.SayHello()`。

##### 小结

嵌套结构体的方法会提升到外层，调用时不用写全路径；两个嵌套结构体有同名方法时，`c.SayHello()` 编译不过，必须写 `c.A.SayHello()` 或 `c.B.SayHello()`。

### 8. 结构体标签（Struct Tags）

结构体标签用于为字段添加元数据，通常用于反射（reflection），特别是在序列化和反序列化（如JSON、XML）时。

```go
type Person struct {
    Name  string `json:"name"`
    Age   int    `json:"age"`
    Email string `json:"email,omitempty"` // 如果字段值为空，则忽略
}

func main() {
    p := Person{Name: "Alice", Age: 30}
    data, _ := json.Marshal(p)
    fmt.Println(string(data)) // 输出 {"name":"Alice","age":30}
}
```

### 9. 反射与`struct`

反射能在运行时读类型和值：`reflect.TypeOf` 拿到类型，`NumField`、`Field` 逐个遍历字段，字段上的 tag 也一起取出来。

```go
import (
    "fmt"
    "reflect"
)

type Person struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}

func main() {
    p := Person{Name: "Alice", Age: 30}
    t := reflect.TypeOf(p)
    for i := 0; i < t.NumField(); i++ {
        field := t.Field(i)
        fmt.Println(field.Name, field.Tag)
    }
}
```

### 10. 可见性规则

在Go中，字段和方法的可见性通过名称的首字母决定。如果名称以大写字母开头，则该字段或方法是导出的（即公开的）；如果以小写字母开头，则是未导出的（即私有的）。

```go
type Person struct {
    Name  string // 公开
    email string // 私有
}

func main() {
    p := Person{Name: "Alice", email: "alice@example.com"}
    fmt.Println(p.Name) // 输出 "Alice"
    // fmt.Println(p.email) // 编译错误，email字段是私有的
}
```

### 11. JSON序列化与反序列化

通过`encoding/json`包可以很方便地将`struct`序列化为JSON格式或从JSON格式反序列化为`struct`。

```go
import (
    "encoding/json"
    "fmt"
)

type Person struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}

func main() {
    p := Person{Name: "Alice", Age: 30}
    data, _ := json.Marshal(p)
    fmt.Println(string(data)) // 输出 {"name":"Alice","age":30}

    var p2 Person
    json.Unmarshal(data, &p2)
    fmt.Println(p2) // 输出 {Alice 30}
}
```

### 12. 类型

提升与同名字段

嵌套结构体的字段会被提升到外层：外层没有同名成员时，直接访问 `b.Name` 等价于访问 `b.A.Name`。

```go
package main

import "fmt"

type A struct {
    Name string
}

type B struct {
    A
    Age int
}

func main() {
    b := B{}
    b.Name = "Alice" // 等价于 b.A.Name = "Alice"，Name 由 A 提升到 B
    fmt.Println(b.Name) // 输出 "Alice"
}
```

两个嵌套结构体带同名成员时不再提升：比如 `D` 同时嵌 `B` 和 `C`、两者都有 `A.Name`，`d.Name` 会编译报错 `ambiguous selector`，必须写全 `d.B.Name` 或 `d.C.Name`（第 13 节就是这个场景）。

### 13. 嵌套与菱形继承

当多个嵌套结构体包含同名字段时，直接访问这些字段会导致歧义。解决方法是显式指定嵌套结构体。

```go
type A struct {
    Name string
}

type B struct {
    A
    Age int
}

type C struct {
    A
    Email string
}

type D struct {
    B
    C
}

func main() {
    d := D{}
    d.B.Name = "Alice"
    d.C.Name = "Bob"

    fmt.Println(d.B.Name) // 输出 "Alice"
    fmt.Println(d.C.Name) // 输出 "Bob"
}
```

### 小结

这一章的落点：字段类型和对齐方式决定占用空间，空`struct{}`占 0 字节；值接收者和指针接收者决定方法集，也就决定能不能满足接口；组合用嵌入，聚合用指针；序列化靠标签里的字段名。