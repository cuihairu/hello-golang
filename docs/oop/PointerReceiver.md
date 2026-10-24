# Methods with Pointer Receivers
In Go, a pointer receiver lets a method access the receiver object through a pointer, so it can modify the object the caller holds.

### 1. Defining a Pointer Receiver

A pointer receiver is when a method's receiver type is a pointer type. A pointer receiver lets the method modify the receiver object's state when it is called.

**Method definition syntax:**

```go
func (receiver *ReceiverType) MethodName(params) ReturnType {
    // method body
}
```

- **receiver**: the receiver variable, preceded by a `*`, indicating a pointer type.
- **ReceiverType**: the type of the receiver.
- **MethodName**: the method name.
- **params**: the list of parameters.
- **ReturnType**: the return type.

#### Example: Defining a pointer receiver

```go
package main

import "fmt"

type Counter struct {
    value int
}

// method with a pointer receiver
func (c *Counter) Increment() {
    c.value++
}

func main() {
    c := Counter{value: 0}
    c.Increment()
    fmt.Println("Value after increment:", c.value) // prints: Value after increment: 1
}
```

### 2. Advantages of Using Pointer Receivers

#### 1. Modifying the receiver's state

A pointer receiver writes straight into the receiver object's fields, changing the same copy the caller holds.

**Example: Modifying the receiver's state**

```go
package main

import "fmt"

type Account struct {
    Balance float64
}

// method with a pointer receiver
func (a *Account) Deposit(amount float64) {
    a.Balance += amount
}

func main() {
    acc := Account{Balance: 100}
    acc.Deposit(50)
    fmt.Println("Balance after deposit:", acc.Balance) // prints: Balance after deposit: 150
}
```

#### 2. Avoiding the cost of copying

When the receiver object is large, a pointer receiver avoids copying the object on every method call, improving performance.

**Example: Avoiding the cost of copying**

```go
package main

import "fmt"

type LargeStruct struct {
    Data [1000]int
}

// method with a pointer receiver
func (l *LargeStruct) UpdateData(index int, value int) {
    l.Data[index] = value
}

func main() {
    ls := LargeStruct{}
    ls.UpdateData(100, 42)
    fmt.Println("Data[100]:", ls.Data[100]) // prints: Data[100]: 42
}
```

### 3. Choosing Between Value Receivers and Pointer Receivers

#### 1. Value receiver

A value receiver gets a copy; the method changes its own copy, and the original object is untouched. Use it when the type is small and the method only reads without writing.

#### 2. Pointer receiver

A pointer receiver modifies the original object directly, and saves the cost of copying along the way. Use it when you need to change state, or when the struct is large.

**Example: Choosing between a value receiver and a pointer receiver**

```go
package main

import "fmt"

type Person struct {
    Name string
}

// value receiver: does not modify the receiver
func (p Person) GetName() string {
    return p.Name
}

// pointer receiver: can modify the receiver
func (p *Person) SetName(name string) {
    p.Name = name
}

func main() {
    p := Person{Name: "Alice"}
    fmt.Println("Name:", p.GetName()) // prints: Name: Alice

    p.SetName("Bob")
    fmt.Println("Updated Name:", p.GetName()) // prints: Updated Name: Bob
}
```

### 4. Caveats When Using Pointer Receivers

- **Avoid mixing**: when choosing between value receivers and pointer receivers for methods, stay consistent and avoid mixing them across different methods of the same type.
- **Initialization**: make sure the object for a pointer receiver is properly initialized before calling the method, to avoid nil pointer dereference errors.
- **Avoid circular dependencies**: avoid introducing unnecessary complexity in methods with pointer receivers, which leads to hard-to-maintain code.

### Summary

- **Definition**: a method with a pointer receiver accesses and modifies the receiver object's state through a pointer type.
- **Advantages**: it can modify an object's state and avoids the cost of copying.
- **Choice**: use a pointer receiver when you need to modify the receiver's state or the object is large; use a value receiver when the object is small and the method does not modify its state.

When in doubt, look at whether the method changes fields: if it does, use a pointer receiver; if it doesn't, use a value receiver, and stay consistent within the same type.

## References

- [Official FAQ · Type system](https://go.dev/doc/faq)
- [Language spec · Interface types](https://go.dev/ref/spec#Interface_types)
- [Effective Go · Methods](https://go.dev/doc/effective_go#methods)
- [Effective Go · Embedding](https://go.dev/doc/effective_go#embedding)
- [Language spec · Method sets](https://go.dev/ref/spec#Method_sets)
- [Effective Go · Pointers vs Values](https://go.dev/doc/effective_go#pointers_vs_values)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
- [InterfaceImpl](/oop/InterfaceImpl.md)
- [Methods](/oop/Methods.md)
- [OOP](/oop/OOP.md)
- [Poly](/oop/Poly.md)
