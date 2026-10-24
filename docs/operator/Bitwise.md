In Go, bitwise operators operate directly on the binary bits of integers. There are six in total; listed by purpose:

### 1. List of bitwise operators

1. **Bitwise AND (`&`)**
   - **Purpose**: Performs a bitwise AND on each bit of two integers. Each bit of the result is the bitwise AND of the corresponding bits of the two operands.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 12   // binary: 1100
         b := 7    // binary: 0111
         result := a & b
         fmt.Println("a & b:", result) // prints: a & b: 4 (binary: 0100)
     }
     ```

2. **Bitwise OR (`|`)**
   - **Purpose**: Performs a bitwise OR on each bit of two integers. Each bit of the result is the bitwise OR of the corresponding bits of the two operands.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 12   // binary: 1100
         b := 7    // binary: 0111
         result := a | b
         fmt.Println("a | b:", result) // prints: a | b: 15 (binary: 1111)
     }
     ```

3. **Bitwise XOR (`^`)**
   - **Purpose**: Performs a bitwise XOR on each bit of two integers. Each bit of the result is the bitwise XOR of the corresponding bits of the two operands.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 12   // binary: 1100
         b := 7    // binary: 0111
         result := a ^ b
         fmt.Println("a ^ b:", result) // prints: a ^ b: 11 (binary: 1011)
     }
     ```

4. **Bitwise NOT (`^`, unary operator)**
   - **Purpose**: Inverts each bit of an integer (turning each 0 bit into 1 and each 1 bit into 0).
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 12   // binary: 1100
         result := ^a
         fmt.Println("^a:", result) // prints: ^a: -13 (after bitwise NOT, expressed in two's complement)
     }
     ```

5. **Left shift (`<<`)**
   - **Purpose**: Shifts all bits of an integer left by the given number of positions, filling in zeros on the right.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 3    // binary: 0011
         result := a << 2
         fmt.Println("a << 2:", result) // prints: a << 2: 12 (binary: 1100)
     }
     ```

6. **Right shift (`>>`)**
   - **Purpose**: Shifts all bits of an integer right by the given number of positions. For unsigned integers, zeros are filled in on the left; for signed integers, the sign bit is filled in on the left (arithmetic right shift).
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 12   // binary: 1100
         result := a >> 2
         fmt.Println("a >> 2:", result) // prints: a >> 2: 3 (binary: 0011)
     }
     ```

### 2. Examples

**Example 1: Combining bitwise operators**

```go
package main

import "fmt"

func main() {
    a := 15   // binary: 1111
    b := 9    // binary: 1001

    fmt.Println("a & b:", a & b)  // prints: a & b: 9 (binary: 1001)
    fmt.Println("a | b:", a | b)  // prints: a | b: 15 (binary: 1111)
    fmt.Println("a ^ b:", a ^ b)  // prints: a ^ b: 6 (binary: 0110)
    fmt.Println("^a:", ^a)        // prints: ^a: -16
    fmt.Println("a << 1:", a << 1) // prints: a << 1: 30 (binary: 11110)
    fmt.Println("a >> 2:", a >> 2) // prints: a >> 2: 3 (binary: 0011)
}
```

### 3. Summary

- **Bitwise operators** are used for bit-level operations on integers, mainly including:
  - Bitwise AND (`&`)
  - Bitwise OR (`|`)
  - Bitwise XOR (`^`)
  - Bitwise NOT (`^`, unary operator)
  - Left shift (`<<`)
  - Right shift (`>>`)

Mnemonic-wise they split into two classes: `&`, `|` and the binary `^` merge bit by bit, while `<<`, `>>` are shifts equivalent to multiplying or dividing by a power of 2. The unary `^` inverts, then the result is interpreted as two's complement, so `^12` is -13.

## References

- [Language Spec · Operators](https://go.dev/ref/spec#Operators)

## Sibling pages

- [Arithmetic](/operator/Arithmetic.md)
- [Assignment](/operator/Assignment.md)
- [BitLen](/operator/BitLen.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Arithmetic](/operator/Arithmetic.md)
- [Assignment](/operator/Assignment.md)
- [BitLen](/operator/BitLen.md)
- [Cap](/operator/Cap.md)
