## Reflection

### Introduction

Reflection lets a program inspect and operate on the type and value of a variable at runtime, at the cost of complexity and a performance hit, so only use it where necessary. The examples below cover reading type and value, creating and modifying values, calling methods and functions, reading struct tags, and deep copying.

### Why you need reflection

Reflection deals with type information that cannot be determined at compile time; it comes in handy for general-purpose libraries, serialization, and validation:

- **Serialization and deserialization**: converting data structures to JSON, XML, or other formats, or parsing data from those formats.
- **Data validation and processing**: validating data dynamically by reading struct tags.
- **Generic functions**: writing functions that handle inputs of arbitrary types.
- **Dynamic invocation**: calling an object's method dynamically without knowing the concrete type and method.

### Basic concepts

Reflection is provided mainly by the `reflect` package and includes a few key concepts:

- **Type**: represents the type of a variable, obtained through `reflect.Type`.
- **Value**: represents the value of a variable, obtained through `reflect.Value`.
- **Kind**: represents the underlying kind of a type, such as integer, float, struct, and so on.

#### Getting type and value

Use `reflect.TypeOf` and `reflect.ValueOf` to get a variable's type and value.

```go
package main

import (
    "fmt"
    "reflect"
)

func main() {
    var x float64 = 3.4

    t := reflect.TypeOf(x)
    v := reflect.ValueOf(x)

    fmt.Println("Type:", t)       // prints: Type: float64
    fmt.Println("Value:", v)      // prints: Value: 3.4
    fmt.Println("Kind:", t.Kind()) // prints: Kind: float64
}
```

### Dynamically creating and modifying values

Beyond reading, reflection can dynamically create and modify values.

```go
package main

import (
    "fmt"
    "reflect"
)

func main() {
    var x int
    v := reflect.ValueOf(&x).Elem()

    v.SetInt(42)
    fmt.Println("Value of x:", x)  // prints: Value of x: 42

    sliceType := reflect.SliceOf(reflect.TypeOf(0))
    slice := reflect.MakeSlice(sliceType, 0, 10)

    slice = reflect.Append(slice, reflect.ValueOf(1))
    slice = reflect.Append(slice, reflect.ValueOf(2))

    fmt.Println("Slice:", slice.Interface())  // prints: Slice: [1 2]
}
```

### Dynamically calling methods with arguments

With reflection you can look up a method by name and call it; arguments have to be wrapped as `reflect.Value` first.

```go
package main

import (
    "fmt"
    "reflect"
)

type Person struct {
    Name string
}

func (p Person) Greet(greeting string) {
    fmt.Printf("%s, my name is %s\n", greeting, p.Name)
}

func main() {
    p := Person{Name: "Alice"}
    v := reflect.ValueOf(p)

    method := v.MethodByName("Greet")
    args := []reflect.Value{reflect.ValueOf("Hello")}
    method.Call(args)  // prints: Hello, my name is Alice
}
```

### Handling struct tags

Struct tags have to be read out with reflection; both serialization and field validation rely on it.

```go
package main

import (
    "fmt"
    "reflect"
)

type User struct {
    Name string `json:"name" validate:"required"`
    Age  int    `json:"age" validate:"min=0"`
}

func main() {
    user := User{Name: "Alice", Age: 30}
    t := reflect.TypeOf(user)

    for i := 0; i < t.NumField(); i++ {
        field := t.Field(i)
        fmt.Printf("Field: %s, JSON Tag: %s, Validate Tag: %s\n",
            field.Name, field.Tag.Get("json"), field.Tag.Get("validate"))
    }
}
```

### Dynamically calling functions

A function value wrapped as `reflect.Value` can also be `Call`ed; arguments and results are both taken from slices.

```go
package main

import (
    "fmt"
    "reflect"
)

func Add(a, b int) int {
    return a + b
}

func main() {
    fn := reflect.ValueOf(Add)

    args := []reflect.Value{reflect.ValueOf(1), reflect.ValueOf(2)}

    results := fn.Call(args)

    fmt.Println("Result:", results[0].Int())  // prints: Result: 3
}
```

### Implementing generic functions

With reflection you can write generic functions that handle inputs of any type. For example, a generic `Print` function that prints values of any type.

```go
package main

import (
    "fmt"
    "reflect"
)

func Print(v interface{}) {
    value := reflect.ValueOf(v)
    fmt.Printf("Type: %s, Value: %v\n", value.Type(), value.Interface())
}

func main() {
    Print(123)               // prints: Type: int, Value: 123
    Print("hello")           // prints: Type: string, Value: hello
    Print([]int{1, 2, 3})    // prints: Type: []int, Value: [1 2 3]
}
```

### Implementing a deep copy

A deep copy is also done with reflection: recurse by `Kind` handling pointers, structs, and slices, and assign the remaining types directly.

```go
package main

import (
    "fmt"
    "reflect"
)

func DeepCopy(src interface{}) interface{} {
    srcVal := reflect.ValueOf(src)
    dstVal := reflect.New(srcVal.Type()).Elem()
    deepCopyRecursive(srcVal, dstVal)
    return dstVal.Interface()
}

func deepCopyRecursive(src, dst reflect.Value) {
    switch src.Kind() {
    case reflect.Ptr:
        if !src.IsNil() {
            dst.Set(reflect.New(src.Elem().Type()))
            deepCopyRecursive(src.Elem(), dst.Elem())
        }
    case reflect.Struct:
        for i := 0; i < src.NumField(); i++ {
            deepCopyRecursive(src.Field(i), dst.Field(i))
        }
    case reflect.Slice:
        if !src.IsNil() {
            dst.Set(reflect.MakeSlice(src.Type(), src.Len(), src.Cap()))
            for i := 0; i < src.Len(); i++ {
                deepCopyRecursive(src.Index(i), dst.Index(i))
            }
        }
    default:
        dst.Set(src)
    }
}

func main() {
    type Person struct {
        Name    string
        Friends []string
    }

    p1 := Person{Name: "Alice", Friends: []string{"Bob", "Charlie"}}
    p2 := DeepCopy(p1).(Person)

    p2.Name = "Alice Copy"
    p2.Friends[0] = "Bob Copy"

    fmt.Println("Original:", p1) // prints: Original: {Alice [Bob Charlie]}
    fmt.Println("Copy:", p2)     // prints: Copy: {Alice Copy [Bob Copy Charlie]}
}
```

### Reflection and generics

After Go 1.18 introduced generics, the division of labor between the two became clearer: when the set of types can be expressed as a constraint, write generics — instantiated at compile time, no runtime overhead; only when the type set is open and the types are only known at runtime do you use reflection. Once a generic function is instantiated it is an ordinary function, and reflection can still get its type:

```go
package main

import (
	"fmt"
	"reflect"
)

func Sum[T int | float64](vals []T) T {
	var total T
	for _, v := range vals {
		total += v
	}
	return total
}

func main() {
	fmt.Println(Sum([]int{1, 2, 3}))        // prints: 6
	fmt.Println(Sum([]float64{1.5, 2.5}))   // prints: 4
	fmt.Println(reflect.TypeOf(Sum[int]))   // prints: func([]int) int
}
```

When both paths work for the same job (say summing, comparing, or copying), prefer generics; leave reflection for genuinely dynamic scenarios like serialization and tag handling.

### Conclusion

Reflection's entry points are `TypeOf` and `ValueOf`; to modify a value, first get a pointer then `Elem`, and write with `SetXxx`; calling methods and functions both go through `Call`. The cost is losing compile-time checking and adding a layer of runtime overhead, which is only worth it for scenarios like serialization, validation, and deep copying.

## References

- [Official blog · The Laws of Reflection](https://go.dev/blog/laws-of-reflection)
- [reflect standard library](https://pkg.go.dev/reflect)

## Sibling pages

- [Advanced](/reflection/Advanced.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
- [Advanced](/reflection/Advanced.md)
