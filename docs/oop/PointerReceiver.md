# 基于指针对象的方法
在 Go 语言中，指针接收者（Pointer Receiver）让方法通过指针访问接收者对象，因此可以改到调用方手里的那个对象本身。

### 1. 指针接收者的定义

指针接收者是方法的接收者类型为指针类型的情况。指针接收者允许方法在调用时修改接收者对象的状态。

**方法定义语法：**

```go
func (receiver *ReceiverType) MethodName(params) ReturnType {
    // 方法体
}
```

- **receiver**：接收者变量，前面有一个 `*`，表示指针类型。
- **ReceiverType**：接收者的类型。
- **MethodName**：方法名称。
- **params**：参数列表。
- **ReturnType**：返回类型。

#### 示例：指针接收者的定义

```go
package main

import "fmt"

type Counter struct {
    value int
}

// 指针接收者的方法
func (c *Counter) Increment() {
    c.value++
}

func main() {
    c := Counter{value: 0}
    c.Increment()
    fmt.Println("Value after increment:", c.value) // 输出: Value after increment: 1
}
```

### 2. 使用指针接收者的优点

#### 1. 修改接收者的状态

指针接收者直接改到接收者对象的字段，改的就是调用方那一份。

**示例：修改接收者状态**

```go
package main

import "fmt"

type Account struct {
    Balance float64
}

// 指针接收者的方法
func (a *Account) Deposit(amount float64) {
    a.Balance += amount
}

func main() {
    acc := Account{Balance: 100}
    acc.Deposit(50)
    fmt.Println("Balance after deposit:", acc.Balance) // 输出: Balance after deposit: 150
}
```

#### 2. 避免复制开销

当接收者对象较大时，使用指针接收者可以避免每次方法调用时复制对象的开销，提高性能。

**示例：避免复制开销**

```go
package main

import "fmt"

type LargeStruct struct {
    Data [1000]int
}

// 指针接收者的方法
func (l *LargeStruct) UpdateData(index int, value int) {
    l.Data[index] = value
}

func main() {
    ls := LargeStruct{}
    ls.UpdateData(100, 42)
    fmt.Println("Data[100]:", ls.Data[100]) // 输出: Data[100]: 42
}
```

### 3. 值接收者与指针接收者的选择

#### 1. 值接收者

值接收者拿到的是副本，方法改的是自己那份，原始对象不会被动到；类型小、方法只读不改时选它。

#### 2. 指针接收者

指针接收者直接改原始对象，顺带省下复制一份的开销；要改状态、或者结构体本身较大时选它。

**示例：值接收者与指针接收者选择**

```go
package main

import "fmt"

type Person struct {
    Name string
}

// 值接收者：不会修改接收者
func (p Person) GetName() string {
    return p.Name
}

// 指针接收者：可以修改接收者
func (p *Person) SetName(name string) {
    p.Name = name
}

func main() {
    p := Person{Name: "Alice"}
    fmt.Println("Name:", p.GetName()) // 输出: Name: Alice

    p.SetName("Bob")
    fmt.Println("Updated Name:", p.GetName()) // 输出: Updated Name: Bob
}
```

### 4. 指针接收者的使用注意事项

- **避免混用**：在方法中选择值接收者或指针接收者时，应保持一致性，避免在同一类型的不同方法中混用。
- **初始化**：确保指针接收者的对象在调用方法之前已正确初始化，以避免空指针引用错误。
- **避免循环依赖**：避免在指针接收者的方法中引入不必要的复杂性，导致难以维护的代码。

### 总结

- **定义**：指针接收者的方法通过指针类型访问和修改接收者对象的状态。
- **优点**：可以修改对象状态，避免复制开销。
- **选择**：当需要修改接收者状态或对象较大时，使用指针接收者；当对象较小且方法不修改对象状态时，使用值接收者。

拿不准时看方法要不要改字段：要改就用指针接收者，不改就用值接收者，同一个类型内部保持一致。