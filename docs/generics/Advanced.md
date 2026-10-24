### Advanced Topics

Beyond the basics, Go generics have several advanced areas: genericized design patterns, custom and composed type constraints, generic interfaces, and the combination of generics with reflection.

#### 8.1 Generic Programming Design Patterns

Applying design patterns with generics mostly means moving "which type to target" into a type parameter. There are three common ones in Go:

**1. Factory Pattern**:
The factory pattern creates object instances and applies when you need to create objects of different types. Using generics for the factory pattern lets you create objects of any type.

Example:
```go
type Factory[T any] interface {
    Create() T
}

type IntFactory struct{}

func (f *IntFactory) Create() int {
    return 0
}

type StringFactory struct{}

func (f *StringFactory) Create() string {
    return ""
}
```

In this example, the `Factory` interface has only the `Create` method, and the return type is decided by `T`; `IntFactory` and `StringFactory` each fix `T` to `int` and `string`.

**2. Adapter Pattern**:
The adapter pattern converts one interface into another and applies when you need to be compatible with different interfaces. Using generics for the adapter pattern lets the adapter support any type.

Example:
```go
type Adapter[T any] struct {
    value T
}

func (a *Adapter[T]) GetValue() T {
    return a.value
}

func (a *Adapter[T]) SetValue(value T) {
    a.value = value
}
```

In this example, the `Adapter` struct stores a value with `T`, and reading and writing it use the same type.

**3. Strategy Pattern**:
The strategy pattern defines a family of algorithms that can be interchanged. Using generics for the strategy pattern lets you pass different algorithms as a generic parameter.

Example:
```go
type Strategy[T any] interface {
    Execute(input T) T
}

type AddStrategy struct{}

func (s *AddStrategy) Execute(input int) int {
    return input + 1
}

type MultiplyStrategy struct{}

func (s *MultiplyStrategy) Execute(input int) int {
    return input * 2
}
```

In this example, the `Strategy` interface defines the method that executes an algorithm, and the different concrete strategies (`AddStrategy` and `MultiplyStrategy`) implement this interface to provide different algorithms.

#### 8.2 Advanced Type Constraints

**1. Custom Constraints**:
Go generics allow custom type constraints to implement more complex behavior. For example, you can define a custom constraint that requires a type to implement certain interfaces.

Example:
```go
type Adder[T any] interface {
    Add(a, b T) T
}

type IntAdder struct{}

func (a *IntAdder) Add(a1, b1 int) int {
    return a1 + b1
}

type FloatAdder struct{}

func (a *FloatAdder) Add(a1, b1 float64) float64 {
    return a1 + b1
}
```

In this example, the `Adder` interface defines an addition operation, and `IntAdder` and `FloatAdder` implement this interface to support addition on different types.

**2. Composite Constraints**:
Composite type constraints let you combine multiple type constraints into one, defining more complex type conditions. For example, you can define a type constraint that requires a type to implement several interfaces at once.

Example:
```go
type Stringer interface {
    String() string
}

type Formatter interface {
    Format() string
}

type StringFormatter interface {
    Stringer
    Formatter
}
```

In this example, the `StringFormatter` interface combines the `Stringer` and `Formatter` interfaces, requiring the implementer to provide the methods of both interfaces.

#### 8.3 Generic Interfaces

**1. Generic Interface Definition**:
Generic interfaces let you define generic methods, which can be used to handle data of any type.

Example:
```go
type Processor[T any] interface {
    Process(data T) T
}

type IntProcessor struct{}

func (p *IntProcessor) Process(data int) int {
    return data * 2
}

type StringProcessor struct{}

func (p *StringProcessor) Process(data string) string {
    return strings.ToUpper(data)
}
```

In this example, the `Processor` interface defines a method for processing data, and `IntProcessor` and `StringProcessor` implement this interface to support processing different types of data.

**2. Generic Interface Implementation**:
When implementing a generic interface, you can define an implementation for a specific type and make sure it meets the interface's requirements.

Example:
```go
type Container[T any] interface {
    Add(item T)
    Get(index int) T
}

type IntContainer struct {
    items []int
}

func (c *IntContainer) Add(item int) {
    c.items = append(c.items, item)
}

func (c *IntContainer) Get(index int) int {
    return c.items[index]
}

type StringContainer struct {
    items []string
}

func (c *StringContainer) Add(item string) {
    c.items = append(c.items, item)
}

func (c *StringContainer) Get(index int) string {
    return c.items[index]
}
```

In this example, the `Container` interface defines add and get operations, and `IntContainer` and `StringContainer` implement this interface to support container operations on different types.

#### 8.4 Generics and Reflection

Generics fix types at compile time, and reflection inspects types at runtime; put them together and you can read the type information of a generic value at runtime and operate on it.

**1. Getting generic type information with reflection**:
With reflection you can obtain the name, fields, and methods of a generic type and operate on them dynamically.

Example:
```go
import (
    "fmt"
    "reflect"
)

func PrintType[T any](value T) {
    t := reflect.TypeOf(value)
    fmt.Println("Type:", t)
}

func main() {
    PrintType(123)          // Type: int
    PrintType("hello")      // Type: string
    PrintType([]int{1, 2})  // Type: []int
}
```

In this example, the `PrintType` function uses reflection to get and print the type information of the value passed in.

**2. Returning a zero-value instance**:
Inside a generic function, `var zero T` gives you a zero-value instance of `T`. Reflection cannot help with this step — reflection cannot determine a type parameter out of thin air; it only operates on already instantiated concrete types.

Example:
```go
import (
    "fmt"
)

func NewInstance[T any]() T {
    var zero T
    return zero
}

func main() {
    intInstance := NewInstance[int]()
    stringInstance := NewInstance[string]()
    fmt.Println("Int instance:", intInstance)        // Int instance: 0
    fmt.Println("String instance:", stringInstance)  // String instance:
}
```

In this example, `NewInstance` returns a zero value of `T` via `var zero T`, with no reflection needed at all.

#### 8.5 Summary

This section puts generics into the factory, adapter, and strategy patterns, and records the custom constraint, interface composition, reflection for type information, and `var zero T` for a zero value; see [Generic structures in practice](/generics/Structure.md) for related examples.

## References

- [Go Official Documentation · Getting started with generics (external link)](https://go.dev/doc/tutorial/generics)
- [Official blog · An Introduction To Generics](https://go.dev/blog/intro-generics)
- [Official blog · When To Use Generics](https://go.dev/blog/when-generics)
- [Language specification · Type parameter declarations](https://go.dev/ref/spec#Type_parameter_declarations)

## Sibling pages

- [Constraints](/generics/Constraints.md)
- [Generics](/generics/Generics.md)
- [Pattern](/generics/Pattern.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Pattern](/generics/Pattern.md)
- [Performance](/generics/Performance.md)
- [Structure](/generics/Structure.md)
- [Syntax](/generics/Syntax.md)
