### Introduction to Go Generics

Generics have long been a standard feature in many programming languages, yet Go did not provide native support until Go 1.18. Before that, writing generic data structures and algorithms meant relying on `interface{}` plus type assertions, with type checking deferred to runtime.

#### 1.1 Basic Concepts of Generics

Generics let you use type parameters when defining types, interfaces, and methods, and specify the concrete type only at the point of use. The main benefits:
- **Code reuse**: generic data structures and algorithms are written once, reducing duplicated code.
- **Type safety**: type checking happens at compile time, avoiding type-conversion errors at runtime.
- **Readability**: types appear in the signature, so call sites do not have to chase type assertions to confirm types.

#### 1.2 Design Philosophy of Go Generics

Go's design philosophy emphasizes simplicity and clarity, and it held to that line when introducing generics. There are three design principles:
- **Principle of least surprise**: the introduction of generics should match developers' expectations, without bringing in complex syntax and concepts.
- **Type inference**: minimize explicit type-parameter declarations and simplify code through type inference.
- **Performance and efficiency**: ensure generic code performs no worse than non-generic code, avoiding unnecessary runtime overhead.

#### 1.3 Motivation and History of Introducing Generics in Go 1.18

Discussion of generics began early in Go's history, was set aside in several versions, and the Go team finally introduced it officially in Go 1.18.

The generics features in Go 1.18 include:
- **Type parameters**: allow functions and types to accept one or more type parameters.
- **Type constraints**: define the constraints on type parameters through interfaces.
- **Type inference**: the compiler can infer type parameters automatically, reducing explicit type declarations.

With these three, a single function or type can serve many types, and type checking is done at compile time.

#### 1.4 Basic Syntax of Generics

In Go, type parameters are wrapped in square brackets `[]`, placed after the function name or type name. Below are basic syntax examples for generic functions and generic types:

**Generic functions**:
```go
func PrintSlice[T any](s []T) {
    for _, v := range s {
        fmt.Println(v)
    }
}
```

**Generic types**:
```go
type Box[T any] struct {
    content T
}

func (b *Box[T]) SetContent(content T) {
    b.content = content
}

func (b *Box[T]) GetContent() T {
    return b.content
}
```

In the examples above, `T` is a type parameter, and `any` is a predefined type constraint meaning any type.

#### 1.5 Application Scenarios for Go Generics

Common application scenarios:
- **Data structures**: such as lists, stacks, queues, and dictionaries.
- **Algorithms**: such as sorting, searching, and tree and graph algorithms.
- **Practical utilities**: such as caching systems and event-handling systems.

#### 1.6 Summary

One core piece of syntax: type parameters go inside square brackets, constraints are expressed with interfaces, and you can omit them when the compiler can infer them. The sections that follow show how generics are used concretely in data structures and algorithms.

## References

- [Go Official Documentation · Getting started with generics (external link)](https://go.dev/doc/tutorial/generics)
- [Official blog · An Introduction To Generics](https://go.dev/blog/intro-generics)
- [Official blog · When To Use Generics](https://go.dev/blog/when-generics)
- [Language specification · Type parameter declarations](https://go.dev/ref/spec#Type_parameter_declarations)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Advanced](/generics/Advanced.md)
- [Pattern](/generics/Pattern.md)
- [Performance](/generics/Performance.md)
- [Structure](/generics/Structure.md)
- [Syntax](/generics/Syntax.md)
- [glossary](/glossary.md)
