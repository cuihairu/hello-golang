
> Perspective: This page records assignment operators by operator class; for declarations, short variable declarations and common assignment patterns see [Variable assignment notes](/var/Assignment.md).
In Go, assignment operators assign a value to a variable. Beyond the basic assignment operator, Go also provides several compound assignment operators that combine an operation with an assignment. Here are Go's assignment operators and how to use them:

### 1. Basic assignment operator

- **Assignment operator (`=`)**
  - **Purpose**: Assigns the value on the right to the variable on the left.
  - **Example**:
    ```go
    package main

    import "fmt"

    func main() {
        var x int
        x = 10
        fmt.Println("x =", x) // prints: x = 10
    }
    ```

### 2. Compound assignment operators

These operators combine an operation and an assignment, keeping the code more concise.

1. **Addition assignment (`+=`)**
   - **Purpose**: Adds the right-hand value to the left-hand variable, then assigns the result back to the left-hand variable.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 5
         a += 3 // equivalent to a = a + 3
         fmt.Println("a += 3:", a) // prints: a += 3: 8
     }
     ```

2. **Subtraction assignment (`-=`)**
   - **Purpose**: Subtracts the right-hand value from the left-hand variable, then assigns the result back to the left-hand variable.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 10
         a -= 4 // equivalent to a = a - 4
         fmt.Println("a -= 4:", a) // prints: a -= 4: 6
     }
     ```

3. **Multiplication assignment (`*=`)**
   - **Purpose**: Multiplies the left-hand variable by the right-hand value, then assigns the result back to the left-hand variable.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 3
         a *= 4 // equivalent to a = a * 4
         fmt.Println("a *= 4:", a) // prints: a *= 4: 12
     }
     ```

4. **Division assignment (`/=`)**
   - **Purpose**: Divides the left-hand variable by the right-hand value, then assigns the result back to the left-hand variable.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 20
         a /= 5 // equivalent to a = a / 5
         fmt.Println("a /= 5:", a) // prints: a /= 5: 4
     }
     ```

5. **Modulo assignment (`%=`)**
   - **Purpose**: Takes the remainder of dividing the left-hand variable by the right-hand value, then assigns the result back to the left-hand variable.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 17
         a %= 5 // equivalent to a = a % 5
         fmt.Println("a %= 5:", a) // prints: a %= 5: 2
     }
     ```

6. **Bitwise AND assignment (`&=`)**
   - **Purpose**: Performs a bitwise AND between the left-hand variable and the right-hand value, then assigns the result back to the left-hand variable.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 12 // binary: 1100
         b := 7  // binary: 0111
         a &= b  // equivalent to a = a & b
         fmt.Println("a &= b:", a) // prints: a &= b: 4 (binary: 0100)
     }
     ```

7. **Bitwise OR assignment (`|=`)**
   - **Purpose**: Performs a bitwise OR between the left-hand variable and the right-hand value, then assigns the result back to the left-hand variable.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 12 // binary: 1100
         b := 7  // binary: 0111
         a |= b  // equivalent to a = a | b
         fmt.Println("a |= b:", a) // prints: a |= b: 15 (binary: 1111)
     }
     ```

8. **Bitwise XOR assignment (`^=`)**
   - **Purpose**: Performs a bitwise XOR between the left-hand variable and the right-hand value, then assigns the result back to the left-hand variable.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 12 // binary: 1100
         b := 7  // binary: 0111
         a ^= b  // equivalent to a = a ^ b
         fmt.Println("a ^= b:", a) // prints: a ^= b: 11 (binary: 1011)
     }
     ```

9. **Left shift assignment (`<<=`)**
   - **Purpose**: Shifts the bits of the left-hand variable left by the number of positions given on the right, then assigns the result back to the left-hand variable.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 3 // binary: 0011
         a <<= 2 // equivalent to a = a << 2
         fmt.Println("a <<= 2:", a) // prints: a <<= 2: 12 (binary: 1100)
     }
     ```

10. **Right shift assignment (`>>=`)**
    - **Purpose**: Shifts the bits of the left-hand variable right by the number of positions given on the right, then assigns the result back to the left-hand variable.
    - **Example**:
      ```go
      package main

      import "fmt"

      func main() {
          a := 12 // binary: 1100
          a >>= 2 // equivalent to a = a >> 2
          fmt.Println("a >>= 2:", a) // prints: a >>= 2: 3 (binary: 0011)
      }
      ```

### Summary

- **Assignment operators** assign values to variables, and include:
  - The basic assignment operator (`=`)
  - Compound assignment operators (addition `+=`, subtraction `-=`, multiplication `*=`, division `/=`, modulo `%=`, bitwise AND `&=`, bitwise OR `|=`, bitwise XOR `^=`, left shift `<<=`, right shift `>>=`)

Each compound assignment operator is equivalent to the corresponding operation plus an assignment; the example comments show the equivalent form, e.g. `a += 3` is equivalent to `a = a + 3`.

## References

- [Language Spec · Operators](https://go.dev/ref/spec#Operators)
- [Language Spec · Assignment](https://go.dev/ref/spec#Assignment)

## Sibling pages

- [Arithmetic](/operator/Arithmetic.md)
- [BitLen](/operator/BitLen.md)
- [Bitwise](/operator/Bitwise.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Arithmetic](/operator/Arithmetic.md)
- [BitLen](/operator/BitLen.md)
- [Bitwise](/operator/Bitwise.md)
- [Cap](/operator/Cap.md)
- [Logical](/operator/Logical.md)
- [Operator](/operator/Operator.md)
- [Receiver](/operator/Receiver.md)
- [Relational](/operator/Relational.md)
- [TypeAssertion](/operator/TypeAssertion.md)
- [Unary](/operator/Unary.md)
