In Go, arithmetic operators perform basic mathematical operations on basic types such as integers and floating-point numbers:

### 1. List of arithmetic operators

1. **Addition operator (`+`)**
   - **Purpose**: Computes the sum of two numbers.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 5
         b := 3
         sum := a + b
         fmt.Println("Sum:", sum) // prints: Sum: 8
     }
     ```

2. **Subtraction operator (`-`)**
   - **Purpose**: Computes the difference between two numbers.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 5
         b := 3
         difference := a - b
         fmt.Println("Difference:", difference) // prints: Difference: 2
     }
     ```

3. **Multiplication operator (`*`)**
   - **Purpose**: Computes the product of two numbers.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 5
         b := 3
         product := a * b
         fmt.Println("Product:", product) // prints: Product: 15
     }
     ```

4. **Division operator (`/`)**
   - **Purpose**: Computes the quotient of two numbers. For integer division, the result rounds toward zero (the fractional part is dropped, e.g. `-10 / 3` gives `-3`); for floating-point division, you get the exact result.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 10
         b := 3
         quotient := a / b
         fmt.Println("Quotient:", quotient) // prints: Quotient: 3

         x := 10.0
         y := 3.0
         floatQuotient := x / y
         fmt.Println("Float Quotient:", floatQuotient) // prints: Float Quotient: 3.3333333333333335
     }
     ```

5. **Modulo operator (`%`)**
   - **Purpose**: Computes the remainder of dividing two numbers.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 10
         b := 3
         remainder := a % b
         fmt.Println("Remainder:", remainder) // prints: Remainder: 1
     }
     ```

6. **Increment operator (`++`)**
   - **Purpose**: Increments a variable's value by 1. Can only be used on variables, not constants.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         x := 5
         x++
         fmt.Println("x after increment:", x) // prints: x after increment: 6
     }
     ```

7. **Decrement operator (`--`)**
   - **Purpose**: Decrements a variable's value by 1. Can only be used on variables, not constants.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         y := 5
         y--
         fmt.Println("y after decrement:", y) // prints: y after decrement: 4
     }
     ```

### 2. Operator precedence

In Go, operator precedence determines the order in which operators in an expression are evaluated. Arithmetic operators have relatively high precedence, but lower than parentheses and some other operators (such as logical operators). The common order from high to low:

1. Parentheses `()`
2. Multiplication `*`, division `/` and modulo `%`
3. Addition `+` and subtraction `-`

Note: increment `++` and decrement `--` are **statements** in Go, not operators, so they can't appear inside an expression and therefore don't take part in precedence comparisons.

### 3. Examples

**Example 1: The effect of precedence**

```go
package main

import "fmt"

func main() {
    a := 5
    b := 3
    c := 2
    result := a + b * c // evaluates b * c first, then adds a
    fmt.Println("Result:", result) // prints: Result: 11
}
```

In this example, `b * c` is evaluated first, then the result is added to `a`, i.e. `5 + (3 * 2) = 11`.

**Example 2: Increment and decrement operations**

In Go, `++` and `--` are statements, so they can't be used as part of an expression the way you would in C/Java (`y := x++` and `w := --z` are both illegal). If you need the "read the value first, then increment (or decrement)" semantics, write it as two statements:

```go
package main

import "fmt"

func main() {
    x := 10
    y := x // read x's value first
    x++    // then increment
    fmt.Println("x:", x) // prints: x: 11
    fmt.Println("y:", y) // prints: y: 10

    z := 10
    w := z // read z's value first
    z--    // then decrement
    fmt.Println("z:", z) // prints: z: 9
    fmt.Println("w:", w) // prints: w: 10
}
```

In this example, `y` holds the value 10 that `x` had before the increment, and `w` holds the value 10 that `z` had before the decrement.

### 4. Summary

- **Arithmetic operators** are the tools for performing basic mathematical operations, including addition, subtraction, multiplication, division, modulo, increment and decrement.
- **Precedence** determines the order in which operators are evaluated within a complex expression.
- **Increment and decrement** operators increase or decrease a variable's value by 1.

Two things that trip people up: integer division rounds toward zero, and `++` and `--` are statements, not operators.

## References

- [Language Spec · Operators](https://go.dev/ref/spec#Operators)
- [Language Spec · Arithmetic operators](https://go.dev/ref/spec#Arithmetic_operators)

## Sibling pages

- [Assignment](/operator/Assignment.md)
- [BitLen](/operator/BitLen.md)
- [Bitwise](/operator/Bitwise.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Assignment](/operator/Assignment.md)
- [BitLen](/operator/BitLen.md)
- [Bitwise](/operator/Bitwise.md)
- [Cap](/operator/Cap.md)
- [Logical](/operator/Logical.md)
- [Operator](/operator/Operator.md)
- [Receiver](/operator/Receiver.md)
- [Relational](/operator/Relational.md)
- [TypeAssertion](/operator/TypeAssertion.md)
- [Unary](/operator/Unary.md)
