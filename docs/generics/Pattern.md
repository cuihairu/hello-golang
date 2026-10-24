### Generic Programming Patterns

Generics let one piece of code run over many types. This page records four patterns: code reuse, type safety, combining with interfaces, and the limits of generics.

#### 4.1 Generics and Code Reuse

The most direct benefit of generics is reuse: write the logic once and every type can use it, without copy-pasting the same code.

**Generic containers**:
Structures like lists, stacks, and queues are the most worthwhile candidates for generics; the user decides what type to hold.

Example:
```go
type List[T any] struct {
    items []T
}

func (l *List[T]) Add(item T) {
    l.items = append(l.items, item)
}

func (l *List[T]) Get(index int) T {
    return l.items[index]
}
```

In this example, the `List` struct is a general-purpose list that can store data of any type.

**Generic algorithms**:
Algorithms like sorting and searching can be genericized the same way, so the algorithm does not change when the type does.

Example:
```go
func Find[T comparable](slice []T, value T) int {
    for i, v := range slice {
        if v == value {
            return i
        }
    }
    return -1
}
```

In this example, the `Find` function can look up a given value in a slice of any comparable type.

#### 4.2 Generics and Type Safety

Generics preserve type safety while providing reuse. Type constraints limit the range of a type parameter, type checking is moved up to compile time, and no type errors surface at runtime.

**Type constraints ensure type safety**:
A constraint spells out the methods a type parameter must have, the compiler checks against it, and code that does not satisfy it will not compile.

Example:
```go
type Stringer interface {
    String() string
}

func PrintStrings[T Stringer](items []T) {
    for _, item := range items {
        fmt.Println(item.String())
    }
}
```

In this example, the type parameter `T` of the `PrintStrings` function is constrained to the `Stringer` interface, ensuring every type passed in implements the `String` method.

#### 4.3 Combining Generics and Interfaces

A generic interface parameterizes "which types are operated on" too: the interface defines a set of general operations, and each type implements them on its own.

**Defining a generic interface**:
Method signatures inside the interface use the type parameter directly.

Example:
```go
type Container[T any] interface {
    Add(item T)
    Remove() T
}
```

In this example, the `Container` interface defines the `Add` and `Remove` methods, and any type that implements the interface must provide those methods.

**Implementing a generic interface**:
When implementing a generic interface, you provide the methods defined by the interface for a specific type.

Example:
```go
type IntContainer struct {
    items []int
}

func (c *IntContainer) Add(item int) {
    c.items = append(c.items, item)
}

func (c *IntContainer) Remove() int {
    item := c.items[len(c.items)-1]
    c.items = c.items[:len(c.items)-1]
    return item
}

var _ Container[int] = &IntContainer{}
```

In this example, `IntContainer` implements the `Container[int]` interface, providing the `Add` and `Remove` methods.

#### 4.4 Limits and Caveats of Generics

Generics are not a cure-all, and there are a few limitations worth knowing.

**Too many type parameters**:
Too many type parameters make code hard to understand, so simplify where possible.

**Performance overhead**:
Generic code may introduce performance overhead in some cases, so pay attention to profiling and optimization.

**Interface constraints**:
Keep the constraints on type parameters as explicit as possible, avoiding unnecessary constraints and complexity.

#### 4.5 Summary

Remember three things when using generics: do not pile up type parameters, measure where performance matters, and write constraints just specific enough to work.

## References

- [Go Official Documentation · Getting started with generics (external link)](https://go.dev/doc/tutorial/generics)
- [Official blog · An Introduction To Generics](https://go.dev/blog/intro-generics)
- [Official blog · When To Use Generics](https://go.dev/blog/when-generics)
- [Language specification · Type parameter declarations](https://go.dev/ref/spec#Type_parameter_declarations)

## Sibling pages

- [Constraints](/generics/Constraints.md)
- [Generics](/generics/Generics.md)
- [Advanced](/generics/Advanced.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Advanced](/generics/Advanced.md)
- [Performance](/generics/Performance.md)
