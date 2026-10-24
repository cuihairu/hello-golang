In Go, type inference is when the compiler determines a variable's type automatically at compile time, based on context. It makes code more concise and readable, reducing the need to declare variable types explicitly.

### Basic use of type inference

Type inference in Go relies mainly on the short variable declaration operator `:=`. When you use `:=` to declare a variable, the compiler infers the variable's type from the value on the right.

### Examples

Here are some examples using type inference:

#### Integer type inference

```go
package main

import "fmt"

func main() {
    x := 10        // the compiler infers x's type as int
    y := 3.14      // the compiler infers y's type as float64
    z := "hello"   // the compiler infers z's type as string
    b := true      // the compiler infers b's type as bool

    fmt.Printf("x 的类型是 %T\n", x) // prints: x 的类型是 int
    fmt.Printf("y 的类型是 %T\n", y) // prints: y 的类型是 float64
    fmt.Printf("z 的类型是 %T\n", z) // prints: z 的类型是 string
    fmt.Printf("b 的类型是 %T\n", b) // prints: b 的类型是 bool
}
```

#### Collection type inference

Type inference applies to collection types as well, such as arrays, slices, and maps.

```go
package main

import "fmt"

func main() {
    nums := []int{1, 2, 3}              // inferred as []int
    nameAgeMap := map[string]int{"Alice": 25, "Bob": 30} // inferred as map[string]int

    fmt.Printf("nums 的类型是 %T\n", nums) // prints: nums 的类型是 []int
    fmt.Printf("nameAgeMap 的类型是 %T\n", nameAgeMap) // prints: nameAgeMap 的类型是 map[string]int
}
```

#### Function return type inference

Type inference can also be used for function return values. The compiler infers a variable's type from the value the function returns.

```go
package main

import "fmt"

func getValues() (int, string) {
    return 42, "hello"
}

func main() {
    x, y := getValues() // the compiler infers x's type as int, y's type as string

    fmt.Printf("x 的类型是 %T\n", x) // prints: x 的类型是 int
    fmt.Printf("y 的类型是 %T\n", y) // prints: y 的类型是 string
}
```

### Limitations of type inference

1. **Explicit declarations take precedence**: if a variable's type is declared explicitly, the compiler does not perform type inference.
2. **Local variables only**: type inference applies only to local variables inside a function; it cannot be used for global variables or constants.
3. **Inferred types must be consistent**: in a multiple assignment, all inferred types must be consistent.

### Example: explicit declarations take precedence

```go
package main

import "fmt"

func main() {
    var x int = 10 // x's type is declared explicitly as int
    y := 3.14     // the compiler infers y's type as float64

    fmt.Printf("x 的类型是 %T\n", x) // prints: x 的类型是 int
    fmt.Printf("y 的类型是 %T\n", y) // prints: y 的类型是 float64
}
```

### Example: type inference inside a function

```go
package main

import "fmt"

var g = "global" // global variables must declare their type explicitly

func main() {
    local := "local" // local variables can use type inference

    fmt.Println(g)    // prints: global
    fmt.Println(local) // prints: local
}
```

### Summary

`:=` only solves the problem of "writing less type inside a function": `x := 10` infers `int`, `y := 3.14` infers `float64`, and a multi-value return is inferred in one go. What it does not cover is anything outside a function — global variables and constants must spell out their type. In everyday code, use `:=` whenever you can, and fall back to `var x int32 = 0` when you need to control the width precisely (`int32`, `float32`).

## References

- [Language spec · Types](https://go.dev/ref/spec#Types)
- [Official blog · Type Inference](https://go.dev/blog/type-inference)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/zh/glossary.md)
- [Array](/type/Array.md)
- [Type](/type/Type.md)
