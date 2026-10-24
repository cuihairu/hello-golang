In Go, `nil` is a predefined identifier that represents the zero value, or the uninitialized value, of pointer, slice, map, channel, interface, and function types. What it means differs from type to type:

### 1. Pointer types

In Go, the zero value of a pointer type is `nil`. A `nil` pointer points to no valid memory address at all.

```go
func main() {
    var ptr *int
    fmt.Println(ptr) // prints: <nil>
}
```

### 2. Slices, maps, and channels

For slices, maps, and channels, the zero value is also `nil`. That means when they are uninitialized they are all given the value `nil`, indicating that no underlying data structure has been allocated for them yet.

```go
func main() {
    var slice []int
    var m map[string]int
    var ch chan string

    fmt.Println(slice) // prints: []
    fmt.Println(m)     // prints: map[]
    fmt.Println(ch)    // prints: <nil>
}
```

### 3. Interface types

For an interface variable, when it has not been initialized or assigned, the default value is also `nil`. A `nil` interface value holds neither a value nor a concrete type.

```go
func main() {
    var i interface{}
    fmt.Println(i) // prints: <nil>
}
```

### 4. Functions

In Go, the zero value of a function type is also `nil`. This represents an uninitialized function variable.

```go
func main() {
    var f func()
    fmt.Println(f) // prints: <nil>
}
```

### Where to use it

`nil` has several uses in real programming:

- **Initialization checks**: test whether a pointer, slice, map, channel, or interface has been initialized or assigned.
  
  ```go
  var ptr *int
  if ptr == nil {
      fmt.Println("Pointer is nil")
  }
  ```

- **Cleaning up resources**: set a reference you no longer need to `nil` so the underlying data structure loses its reference.

- **Default values**: a pointer or interface that is `nil` holds no valid value at all, so it can be used directly as a default.

### Things to watch

- Operating on a `nil` pointer, slice, map, channel, or interface can cause a runtime error. Check it for validity or initialize it before use.

- With a `nil` value of function type, trying to call it causes a runtime error. Check that the function is not `nil` before calling it.

### Example code

Here is an example showing how to use `nil` for initialization checks and for cleaning up resources:

```go
package main

import "fmt"

func main() {
    var ptr *int
    if ptr == nil {
        fmt.Println("Pointer is nil")
    }

    var ch chan int
    fmt.Println(ch) // prints: <nil>

    var f func()
    if f == nil {
        fmt.Println("Function is nil")
    }
}
```

### Summary

`nil` is the zero value of pointers, slices, maps, channels, interfaces, and functions, and its meaning varies with the type. Before operating on a variable whose value is `nil`, check for nil or initialize it first.

## References

- [Language specification · Constant declarations](https://go.dev/ref/spec#Constant_declarations)
- [Official blog · Constants](https://go.dev/blog/constants)
- [Language specification · Predeclared identifiers (nil)](https://go.dev/ref/spec#Predeclared_identifiers)
- [Language specification · The zero value](https://go.dev/ref/spec#The_zero_value)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Const](/const/Const.md)
- [TrueAndFalse](/const/TrueAndFalse.md)
- [glossary](/zh/glossary.md)
