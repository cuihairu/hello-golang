### Type Constraints

Type constraints are defined with interfaces, and they limit which types a type parameter may accept and which methods it must have. This page collects the predefined constraints, interface type constraints, and type sets.

#### 3.1 Predefined Constraints

Go provides some predefined type constraints to simplify common type restrictions. These predefined constraints include `any` and `comparable`.

**any**:
`any` is a special predefined constraint meaning the type parameter can be any type. Before Go 1.18, `any` was expressed with the empty interface `interface{}`, but `any` is now recommended as the default constraint for generics.

Example:
```go
func PrintSlice[T any](s []T) {
    for _, v := range s {
        fmt.Println(v)
    }
}
```

`T` is constrained to `any`, meaning it can be any type.

**comparable**:
`comparable` is another predefined constraint, meaning the type parameter must be a type that supports comparison operations. Types with the `comparable` constraint can be used in comparison operations (such as `==` and `!=`).

Example:
```go
func Contains[T comparable](s []T, v T) bool {
    for _, item := range s {
        if item == v {
            return true
        }
    }
    return false
}
```

`T` is constrained to `comparable`, meaning it can be compared, which ensures the `Contains` function can correctly determine whether an element is present.

#### 3.2 Interface Type Constraints

An interface type constraint uses an interface to specify which methods a type parameter must implement, and complex restrictions can be composed as needed.

**Defining an interface type constraint**:
First define an interface with its methods, then write that interface name in the type parameter; the type parameter must implement the methods in the interface.

Example:
```go
type Stringer interface {
    String() string
}

func PrintStrings[T Stringer](s []T) {
    for _, v := range s {
        fmt.Println(v.String())
    }
}
```

`T` is constrained to the `Stringer` interface, meaning the type parameter must implement the `String` method.

**Using an interface type constraint**:
Interface type constraints can be used in generic functions, generic methods, and generic types.

Example:
```go
type Stringer interface {
    String() string
}

type Box[T Stringer] struct {
    content T
}

func (b *Box[T]) PrintContent() {
    fmt.Println(b.content.String())
}
```

The `Box` type is constrained to the `Stringer` interface, meaning the type parameter must implement the `String` method.

#### 3.3 Type Sets

A type set defines a group of concrete types, and the type parameter can only be chosen from that group. It is written inside an interface, combining the `~` operator with concrete types.

**Defining a type set**:
A type set is defined by using the `~` operator and concrete types inside an interface. A type set can contain one or more concrete types.

Example:
```go
type Integer interface {
    ~int | ~int8 | ~int16 | ~int32 | ~int64
}

func SumIntegers[T Integer](a, b T) T {
    return a + b
}
```

The `Integer` interface defines a type set including `int`, `int8`, `int16`, `int32`, and `int64`. The type parameter `T` of the `SumIntegers` function is constrained to any one type in the `Integer` type set.

**Using a type set**:
Type sets can be used in generic functions, generic methods, and generic types, ensuring the type parameter belongs to the defined type set.

Example:
```go
type Number interface {
    ~int | ~float64
}

func AddNumbers[T Number](a, b T) T {
    return a + b
}
```

The `Number` interface defines a type set including `int` and `float64`. The type parameter `T` of the `AddNumbers` function is constrained to any one type in the `Number` type set.

#### 3.4 Multiple Constraints

A type parameter can be subject to multiple constraints at the same time, and all of them must be satisfied. The way to do it is to combine interfaces, for example by embedding one interface in another.

Example:
```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type ReadWriter interface {
    Reader
    Writer
}

func Copy[T ReadWriter](src, dst T) error {
    buf := make([]byte, 1024)
    for {
        n, err := src.Read(buf)
        if err == io.EOF {
            return nil // reached the end, normal termination
        }
        if err != nil {
            return err
        }
        if n == 0 {
            break
        }
        if _, err := dst.Write(buf[:n]); err != nil {
            return err
        }
    }
    return nil
}
```

The `ReadWriter` interface includes the methods of both the `Reader` and `Writer` interfaces, so the type parameter `T` of the `Copy` function must implement the `ReadWriter` interface.

#### 3.5 Summary

The three kinds of constraints each cover a part: `any` and `comparable` are ready-made, method sets use interface type constraints, concrete type collections use type sets, and multiple constraints are combined and written on the type parameter.

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
