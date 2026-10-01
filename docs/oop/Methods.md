# 方法声明
在 Go 语言中，方法是与特定类型相关联的函数。方法可以与结构体类型、自定义类型等关联。以下是对 Go 方法的详细介绍，包括方法定义、接收者、方法类型、以及各种方法的示例。

### 1. 方法定义

方法的定义语法如下：

```go
func (receiver ReceiverType) MethodName(params) ReturnType {
    // 方法体
}
```

- **receiver**：接收者变量，表示方法作用于哪个类型的值。
- **ReceiverType**：接收者的类型。
- **MethodName**：方法名称。
- **params**：参数列表。
- **ReturnType**：返回类型。

#### 示例：基本方法定义

```go
package main

import "fmt"

type Circle struct {
    Radius float64
}

// 定义方法
func (c Circle) Area() float64 {
    return 3.14 * c.Radius * c.Radius
}

func main() {
    circle := Circle{Radius: 5}
    fmt.Println("Area:", circle.Area()) // 输出: Area: 78.5
}
```

### 2. 方法接收者

方法的接收者可以是值类型或指针类型。

- **值接收者**：方法接收者是类型的副本。方法不能修改原始值。
- **指针接收者**：方法接收者是类型的指针。方法可以修改原始值。

#### 示例：值接收者与指针接收者

```go
package main

import "fmt"

type Rectangle struct {
    Width, Height int
}

// 值接收者：方法不能修改 Rectangle 实例
func (r Rectangle) Area() int {
    return r.Width * r.Height
}

// 指针接收者：方法可以修改 Rectangle 实例
func (r *Rectangle) Scale(factor int) {
    r.Width *= factor
    r.Height *= factor
}

func main() {
    rect := Rectangle{Width: 10, Height: 5}
    fmt.Println("Area:", rect.Area()) // 输出: Area: 50

    rect.Scale(2)
    fmt.Println("Scaled Width:", rect.Width)  // 输出: Scaled Width: 20
    fmt.Println("Scaled Height:", rect.Height) // 输出: Scaled Height: 10
}
```

### 3. 方法与自定义类型

Go 允许为自定义类型定义方法。这些自定义类型可以是基本类型的别名或结构体的别名。

#### 示例：自定义类型的方法

```go
package main

import "fmt"

// 自定义类型
type MyInt int

// 自定义类型的方法
func (n MyInt) Double() MyInt {
    return n * 2
}

func main() {
    num := MyInt(10)
    fmt.Println("Double:", num.Double()) // 输出: Double: 20
}
```

### 4. 方法与接口

方法可以用在接口中，接口定义了一组方法，任何实现了这些方法的类型都可以被视为实现了该接口。

#### 示例：接口中的方法

```go
package main

import "fmt"

// 定义接口
type Speaker interface {
    Speak() string
}

// 实现接口的类型
type Dog struct{}

func (d Dog) Speak() string {
    return "Woof!"
}

type Cat struct{}

func (c Cat) Speak() string {
    return "Meow!"
}

func main() {
    var speaker Speaker

    speaker = Dog{}
    fmt.Println(speaker.Speak()) // 输出: Woof!

    speaker = Cat{}
    fmt.Println(speaker.Speak()) // 输出: Meow!
}
```

### 5. 方法的接收者类型

- **值接收者**：适用于不需要修改接收者值的方法，避免在每次调用方法时都复制接收者对象。
- **指针接收者**：适用于需要修改接收者值的方法或接收者对象较大时，避免复制开销。

### 6. 方法的嵌套

Go 支持通过嵌入（embedding）实现类似继承的功能。嵌入允许一个结构体包含另一个结构体，从而获得其字段和方法。

#### 示例：嵌入的结构体

```go
package main

import "fmt"

// 基础结构体
type Animal struct {
    Name string
}

func (a Animal) Speak() string {
    return "Some generic sound"
}

// 继承 Animal 的结构体
type Dog struct {
    Animal
    Breed string
}

func main() {
    dog := Dog{Animal: Animal{Name: "Buddy"}, Breed: "Golden Retriever"}
    fmt.Println(dog.Name)  // 输出: Buddy
    fmt.Println(dog.Speak()) // 输出: Some generic sound
}
```

### 总结

- **方法定义**：通过接收者类型和方法名称定义与特定类型相关联的函数。
- **接收者类型**：可以是值类型或指针类型，决定了方法是否可以修改原始值。
- **自定义类型的方法**：可以为基本类型或结构体的自定义类型定义方法。
- **接口中的方法**：接口定义了一组方法，类型通过实现接口的方法来满足接口要求。
- **方法嵌入**：通过结构体嵌入实现类似继承的功能。

这些特性使得 Go 语言能够灵活地实现面向对象编程的核心概念，同时保持语言的简洁性和高效性。