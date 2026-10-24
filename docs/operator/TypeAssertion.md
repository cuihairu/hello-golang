A type assertion checks at runtime which concrete type is actually held in an interface value, and pulls the value out.

### Basic syntax of a type assertion

Basic syntax:

```go
value, ok := interface.(T)
```

- **`interface`** is the interface value being asserted.
- **`T`** is the concrete type you are asserting.
- **`value`** is the concrete-typed value when the assertion succeeds.
- **`ok`** is a boolean that says whether the assertion succeeded.

### Two forms of type assertion

1. **Successful assertion (with a return value)**

   ```go
   var i interface{} = "hello"
   s, ok := i.(string)
   if ok {
       fmt.Println("String value:", s)
   } else {
       fmt.Println("Not a string")
   }
   ```

   `ok` tells you whether the assertion succeeded, and `s` is the concrete value you get when it does.

2. **Direct assertion (without a return value)**

   ```go
   var i interface{} = "hello"
   s := i.(string)
   fmt.Println("String value:", s)
   ```

   This form takes the value outright; a failed assertion panics. When you are unsure of the type, the form with a return value is the safer choice.

### Example code

#### Example 1: Assertion succeeds

```go
package main

import "fmt"

func main() {
    var i interface{} = 42
    value, ok := i.(int)
    if ok {
        fmt.Println("The value is an int:", value)
    } else {
        fmt.Println("The value is not an int")
    }
}
```

#### Example 2: Assertion fails

```go
package main

import "fmt"

func main() {
    var i interface{} = "hello"
    value, ok := i.(int)
    if ok {
        fmt.Println("The value is an int:", value)
    } else {
        fmt.Println("The value is not an int")
    }
}
```

### Type assertions on the empty interface

The empty interface `interface{}` can hold a value of any type. When you need to turn a value in an empty interface into a concrete type, you can use a type assertion:

```go
package main

import "fmt"

func printValue(v interface{}) {
    switch v := v.(type) {
    case int:
        fmt.Println("Integer:", v)
    case string:
        fmt.Println("String:", v)
    default:
        fmt.Println("Unknown type")
    }
}

func main() {
    printValue(10)       // prints: Integer: 10
    printValue("hello")  // prints: String: hello
    printValue(3.14)     // prints: Unknown type
}
```

### Summary

- A **type assertion** lets you check an interface value's actual type at runtime and convert it to that type.
- An **assertion with a return value** lets you safely check whether the assertion succeeded, avoiding runtime errors.
- A **direct assertion** returns no success flag, but a failed assertion causes a runtime error.
- The **empty interface** can hold a value of any type, so type assertions are especially useful when working with empty interfaces.

Each of the three forms covers one case: when you know the type is right, use the direct assertion; when you are unsure, check with `ok`; when you need a branch per type, use `switch v := v.(type)`.

## References

- [Language specification · Operators](https://go.dev/ref/spec#Operators)
- [Language specification · Type assertions](https://go.dev/ref/spec#Type_assertions)


## Sibling pages

- [Arithmetic](/operator/Arithmetic.md)
- [Assignment](/operator/Assignment.md)
- [BitLen](/operator/BitLen.md)
- [Relational](/operator/Relational.md)
- [Unary](/operator/Unary.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Relational](/operator/Relational.md)
- [Unary](/operator/Unary.md)
