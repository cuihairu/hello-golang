In Go, unary operators are operators that act on a single operand. Here are Go's unary operators and how to use them:

### 1. Unary plus (`+`)

- **Purpose**: Represents the positive value of the operand.
- **Example**:
  ```go
  package main

  import "fmt"

  func main() {
      a := 5
      result := +a
      fmt.Println("+a:", result) // prints: +a: 5
  }
  ```

### 2. Unary minus (`-`)

- **Purpose**: Represents the negative value of the operand, i.e. negates the operand.
- **Example**:
  ```go
  package main

  import "fmt"

  func main() {
      a := 5
      result := -a
      fmt.Println("-a:", result) // prints: -a: -5
  }
  ```

### 3. Bitwise NOT (`^`)

- **Purpose**: Inverts all bits of the operand; only valid on integer types.
- **Example**:
  ```go
  package main

  import "fmt"

  func main() {
      a := 12 // binary: 1100
      result := ^a
      fmt.Println("^a:", result) // prints: ^a: -13 (after bitwise NOT, then two's complement)
  }
  ```

### 4. Increment (`++`)

- **Purpose**: Increases the operand's value by 1. The increment operator can only be used on variables and cannot be used inside an expression.
- **Example**:
  ```go
  package main

  import "fmt"

  func main() {
      a := 5
      a++
      fmt.Println("a++:", a) // prints: a++: 6
  }
  ```

### 5. Decrement (`--`)

- **Purpose**: Decreases the operand's value by 1. The decrement operator can only be used on variables and cannot be used inside an expression.
- **Example**:
  ```go
  package main

  import "fmt"

  func main() {
      a := 5
      a--
      fmt.Println("a--:", a) // prints: a--: 4
  }
  ```

### 6. Logical NOT (`!`)

- **Purpose**: Logically negates the operand, turning `true` into `false` and `false` into `true`.
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

### Summary

All six operators act on a single operand: `+`, `-`, `^`, `!` can appear inside an expression, while `++` and `--` can only stand alone as statements and cannot be written inside an expression.

## References

- [Language Spec · Operators](https://go.dev/ref/spec#Operators)
- [Language Spec · Arithmetic operators (unary +/-)](https://go.dev/ref/spec#Arithmetic_operators)
- [Language Spec · Address operators](https://go.dev/ref/spec#Address_operators)


## Sibling pages

- [Arithmetic](/operator/Arithmetic.md)
- [Assignment](/operator/Assignment.md)
- [BitLen](/operator/BitLen.md)
- [TypeAssertion](/operator/TypeAssertion.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [TypeAssertion](/operator/TypeAssertion.md)
