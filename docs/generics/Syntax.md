### Generics Fundamentals

This page records the basics of Go generics: type parameters, type constraints, generic functions, generic methods, and generic types — how each is defined and how each is used.

#### 2.1 Type Parameters and Type Constraints

Type parameters are the core concept of generics. They let you use a placeholder to represent some type when defining a function, method, or type, and specify the concrete type only at the point of use. Type constraints are used to restrict the range of concrete types a type parameter may accept.

**Type parameters**:
Type parameters are wrapped in square brackets `[]`, placed after the function name, method name, or type name. In Go, type parameters are usually denoted by a single capital letter, such as `T`, `K`, or `V`.

**Type constraints**:
A type constraint is a condition that restricts the range of types a type parameter may take. It can be any interface type. Go provides some predefined type constraints, such as `any` for any type, and `comparable` for types that support comparison operations.

Example:
```go
func PrintSlice[T any](s []T) {
    for _, v := range s {
        fmt.Println(v)
    }
}
```

In this example, `T` is a type parameter, and `any` is the type constraint, meaning `T` can be any type.

#### 2.2 Generic Functions and Methods

Generic functions and methods are functions and methods defined using type parameters. They can accept and return arguments of different types, without defining a separate function or method for each type.

**Generic functions**:
A generic function uses type parameters after the function name, and the function body can use those type parameters to define its parameters and return values.

Example:
```go
func Swap[T any](a, b T) (T, T) {
    return b, a
}
```

`Swap` takes two arguments of the same type and returns them swapped.

**Generic methods**:
Generic methods are similar to generic functions, but they are methods defined on a generic type, and they can use the type parameters of that generic type.

Example:
```go
type Pair[T any] struct {
    first, second T
}

func (p *Pair[T]) Swap() {
    p.first, p.second = p.second, p.first
}
```

This `Swap` is a method on `Pair` that swaps its two fields.

#### 2.3 Generic Types

A generic type is a struct, interface, or other type defined using type parameters. Generic types can hold data of different types, without defining a separate type for each data type.

**Generic structs**:
A generic struct uses type parameters after the struct name, and struct fields can use those type parameters to define their types.

Example:
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

`Box` can hold content of any type, with `SetContent` and `GetContent` handling read and write.

**Generic interfaces**:
Generic interfaces let you define a set of operations that can be implemented by different types, without defining a separate interface for each type.

Example:
```go
type Container[T any] interface {
    Add(item T)
    Remove() T
}
```

`Container` requires the implementer to provide the `Add` and `Remove` methods.

#### 2.4 Type Inference

Go's compiler can infer type parameters automatically in most cases, and it applies this to function calls, method calls, and type instantiation, which spares you writing the types by hand.

Example:
```go
func PrintSlice[T any](s []T) {
    for _, v := range s {
        fmt.Println(v)
    }
}

func main() {
    intSlice := []int{1, 2, 3}
    PrintSlice(intSlice) // compiler infers T as int
}
```

No type is written at the call site; the compiler works out from `intSlice` that `T` is `int`.

#### 2.5 Limitations and Caveats of Generics

Generics are not without cost. There are three things to watch when using them:
- **Too many type parameters**: too many type parameters make code hard to understand, so simplify where possible.
- **Performance overhead**: generic code may introduce performance overhead in some cases, so pay attention to profiling and optimization.
- **Interface constraints**: keep the constraints on type parameters as explicit as possible, avoiding unnecessary constraints and complexity.

#### 2.6 Summary

The point here fits in one sentence: type parameters are declared with square brackets, constraints bound the range they may take, and the compiler then infers the concrete type. Functions, methods, structs, and interfaces can all be parameterized this way, so the same thing does not need to be written once per type. I collected the three limitations in 2.5 and check them first when writing generics.

## References

- [Go Official Documentation · Getting started with generics (external link)](https://go.dev/doc/tutorial/generics)
- [Official blog · An Introduction To Generics](https://go.dev/blog/intro-generics)
- [Official blog · When To Use Generics](https://go.dev/blog/when-generics)
- [Language specification · Type parameter declarations](https://go.dev/ref/spec#Type_parameter_declarations)


## Sibling pages

- [Constraints](/generics/Constraints.md)
- [Generics](/generics/Generics.md)
- [Advanced](/generics/Advanced.md)
- [Structure](/generics/Structure.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Structure](/generics/Structure.md)
