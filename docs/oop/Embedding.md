Go 没有传统面向对象里的继承，嵌入结构体是 Go 的做法：把一个结构体匿名嵌进另一个结构体，字段和方法就能直接复用。

### 1. 嵌入结构体的定义

嵌入结构体是将一个结构体作为另一个结构体的字段进行定义。这种方式允许外部结构体直接访问嵌入结构体的字段和方法。

#### 示例：基本的嵌入结构体

```go
package main

import "fmt"

// 基础结构体
type Person struct {
    Name string
    Age  int
}

// 另一个结构体嵌入 Person
type Employee struct {
    Person      // 嵌入结构体
    EmployeeID string
}

func main() {
    e := Employee{
        Person:      Person{Name: "Alice", Age: 30},
        EmployeeID: "E123",
    }
    fmt.Println("Name:", e.Name)         // 通过嵌入结构体访问字段
    fmt.Println("Age:", e.Age)           // 通过嵌入结构体访问字段
    fmt.Println("Employee ID:", e.EmployeeID)
}
```

### 2. 嵌入结构体的优点

#### 1. 代码复用

字段和方法写一次，嵌入它的结构体都能直接用，不用复制粘贴。

#### 2. 简化设计

通用功能集中在一个结构体里，别的结构体嵌它就能获得这些功能。

#### 3. 类似继承

Go 没有继承，要复用字段和方法时，嵌入结构体是最接近的写法。

### 3. 访问嵌入结构体的字段和方法

嵌入结构体的字段和方法可以直接访问，就像它们是外部结构体的一部分一样。

#### 示例：访问嵌入结构体的字段和方法

```go
package main

import "fmt"

type Address struct {
    Street, City, State string
}

type Person struct {
    Name    string
    Address // 嵌入结构体
}

func main() {
    p := Person{
        Name: "Bob",
        Address: Address{
            Street: "123 Main St",
            City:   "Springfield",
            State:  "IL",
        },
    }
    fmt.Println("Name:", p.Name)
    fmt.Println("Street:", p.Street) // 直接访问嵌入结构体的字段
    fmt.Println("City:", p.City)
    fmt.Println("State:", p.State)
}
```

### 4. 方法和嵌入结构体

当嵌入结构体中定义了方法时，外部结构体可以直接调用这些方法。

#### 示例：嵌入结构体中的方法

```go
package main

import "fmt"

type Person struct {
    Name string
}

func (p Person) Greet() string {
    return "Hello, " + p.Name
}

type Employee struct {
    Person
    EmployeeID string
}

func main() {
    e := Employee{
        Person:      Person{Name: "Charlie"},
        EmployeeID: "E456",
    }
    fmt.Println(e.Greet()) // 直接调用嵌入结构体的方法
}
```

### 5. 方法重定义

如果外部结构体和嵌入结构体都有相同名称的方法，外部结构体的方法会覆盖嵌入结构体的方法。用嵌入结构体的类型名可以显式访问被覆盖的方法。

#### 示例：方法重定义

```go
package main

import "fmt"

type Base struct{}

func (b Base) Do() {
    fmt.Println("Base Do")
}

type Derived struct {
    Base
}

func (d Derived) Do() {
    fmt.Println("Derived Do")
}

func main() {
    d := Derived{}
    d.Do()          // 输出: Derived Do
    d.Base.Do()     // 输出: Base Do
}
```

### 6. 嵌入的多重结构体

一个结构体可以嵌入多个结构体，把几个结构体的功能组合到一起。

#### 示例：多重嵌入

```go
package main

import "fmt"

type Address struct {
    Street string
}

type ContactInfo struct {
    Email string
}

type Person struct {
    Address     // 嵌入结构体
    ContactInfo // 嵌入结构体
    Name        string
}

func main() {
    p := Person{
        Address:     Address{Street: "456 Elm St"},
        ContactInfo: ContactInfo{Email: "bob@example.com"},
        Name:        "Bob",
    }
    fmt.Println("Name:", p.Name)
    fmt.Println("Street:", p.Street)
    fmt.Println("Email:", p.Email)
}
```

### 7. 匿名字段

在 Go 中，嵌入结构体的字段是匿名的，即不需要给嵌入的结构体字段命名。这种方式使得嵌入结构体的字段可以直接访问。

#### 示例：匿名字段

```go
package main

import "fmt"

type Engine struct {
    Horsepower int
}

type Car struct {
    Engine     // 匿名嵌入
    Model string
}

func main() {
    c := Car{
        Engine: Engine{Horsepower: 150},
        Model:  "Toyota Camry",
    }
    fmt.Println("Model:", c.Model)
    fmt.Println("Horsepower:", c.Horsepower) // 直接访问匿名字段的字段
}
```

### 总结

嵌入把内层结构体的字段和方法提升到外层结构体的命名空间：`e.Name` 不用写成 `e.Person.Name`；名字冲突时外层覆盖内层，想调内层的就用 `d.Base.Do()` 这样的完整写法。