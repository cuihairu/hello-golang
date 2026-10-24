In Go, logical operators perform logical operations on boolean values. They're mainly used for control-flow decisions and condition tests. Here are Go's logical operators and how to use them:

### 1. List of logical operators

1. **Logical AND (`&&`)**
   - **Purpose**: The result is `true` only when both operands are `true`. If the first operand is `false`, the second operand is not evaluated (short-circuit behavior).
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := true
         b := false
         result := a && b
         fmt.Println("a && b:", result) // prints: a && b: false
     }
     ```

2. **Logical OR (`||`)**
   - **Purpose**: The result is `true` when at least one of the two operands is `true`. If the first operand is `true`, the second operand is not evaluated (short-circuit behavior).
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := true
         b := false
         result := a || b
         fmt.Println("a || b:", result) // prints: a || b: true
     }
     ```

3. **Logical NOT (`!`)**
   - **Purpose**: Inverts a boolean value: if the operand is `true` the result is `false`, and vice versa.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := true
         result := !a
         fmt.Println("!a:", result) // prints: !a: false
     }
     ```

### 2. Examples

**Example 1: Combining logical operators**

```go
package main

import "fmt"

func main() {
    x := 10
    y := 20
    z := 30

    // combining logical AND and logical OR
    result1 := (x < y) && (y < z)  // true && true = true
    result2 := (x > y) || (y < z)  // false || true = true

    fmt.Println("result1:", result1) // prints: result1: true
    fmt.Println("result2:", result2) // prints: result2: true
}
```

**Example 2: Short-circuit behavior**

Note: `1/0` is a constant expression, so Go reports a `division by zero` error at compile time and never gets to compile; below uses a function to demonstrate short-circuit behavior at run time:

```go
package main

import "fmt"

func checkDiv(n int) bool {
    // demonstrates short-circuit behavior: use a safe condition to avoid division by zero
    // when n is not 0, return true; otherwise return false
    // this lets us demonstrate the short-circuit behavior of && and || without triggering a panic
    return n != 0
}

func main() {
    a := false
    b := true

    // short-circuit: when the left side of && is false, the right-side checkDiv is not called,
    // so the division-by-zero panic is avoided
    result1 := a && checkDiv(1)
    // same for || when the left side is true, the right-side checkDiv is not called
    result2 := b || checkDiv(1)

    fmt.Println("result1:", result1) // prints: result1: false
    fmt.Println("result2:", result2) // prints: result2: true
}
```

### 3. Summary

- **Logical operators** perform logical operations on boolean values, mainly:
  - Logical AND (`&&`): the result is `true` only when both operands are `true`.
  - Logical OR (`||`): the result is `true` as long as one operand is `true`.
  - Logical NOT (`!`): inverts a boolean value.
- Logical operators have short-circuit behavior, i.e. in some cases the second operand is not evaluated, which improves efficiency or avoids errors.

The short-circuit behavior of `&&` and `||` is guaranteed by the language: the right-hand expression is only evaluated when needed, so guard checks that rely on this are safe.

## References

- [Language Spec · Operators](https://go.dev/ref/spec#Operators)
- [Language Spec · Logical operators](https://go.dev/ref/spec#Logical_operators)


## Sibling pages

- [Arithmetic](/operator/Arithmetic.md)
- [Assignment](/operator/Assignment.md)
- [BitLen](/operator/BitLen.md)
- [Cap](/operator/Cap.md)
- [Operator](/operator/Operator.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Cap](/operator/Cap.md)
- [Operator](/operator/Operator.md)
