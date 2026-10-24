In Go, relational operators compare two values; the result is a boolean (`true` or `false`). There are 6 in total:

### 1. List of relational operators

1. **Equal (`==`)**
   - **Purpose**: Checks whether two values are equal.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 5
         b := 5
         result := (a == b)
         fmt.Println("a == b:", result) // prints: a == b: true
     }
     ```

2. **Not equal (`!=`)**
   - **Purpose**: Checks whether two values are not equal.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 5
         b := 3
         result := (a != b)
         fmt.Println("a != b:", result) // prints: a != b: true
     }
     ```

3. **Greater than (`>`)**
   - **Purpose**: Checks whether the left value is greater than the right value.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 5
         b := 3
         result := (a > b)
         fmt.Println("a > b:", result) // prints: a > b: true
     }
     ```

4. **Less than (`<`)**
   - **Purpose**: Checks whether the left value is less than the right value.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 3
         b := 5
         result := (a < b)
         fmt.Println("a < b:", result) // prints: a < b: true
     }
     ```

5. **Greater than or equal (`>=`)**
   - **Purpose**: Checks whether the left value is greater than or equal to the right value.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 5
         b := 5
         result := (a >= b)
         fmt.Println("a >= b:", result) // prints: a >= b: true
     }
     ```

6. **Less than or equal (`<=`)**
   - **Purpose**: Checks whether the left value is less than or equal to the right value.
   - **Example**:
     ```go
     package main

     import "fmt"

     func main() {
         a := 3
         b := 5
         result := (a <= b)
         fmt.Println("a <= b:", result) // prints: a <= b: true
     }
     ```

### 2. Examples

**Example 1: Comparing integers**

```go
package main

import "fmt"

func main() {
    x := 10
    y := 20

    fmt.Println("x == y:", x == y)  // prints: x == y: false
    fmt.Println("x != y:", x != y)  // prints: x != y: true
    fmt.Println("x > y:", x > y)    // prints: x > y: false
    fmt.Println("x < y:", x < y)    // prints: x < y: true
    fmt.Println("x >= y:", x >= y)  // prints: x >= y: false
    fmt.Println("x <= y:", x <= y)  // prints: x <= y: true
}
```

**Example 2: Comparing strings**

```go
package main

import "fmt"

func main() {
    str1 := "hello"
    str2 := "world"

    fmt.Println("str1 == str2:", str1 == str2)  // prints: str1 == str2: false
    fmt.Println("str1 != str2:", str1 != str2)  // prints: str1 != str2: true
    fmt.Println("str1 > str2:", str1 > str2)    // prints: str1 > str2: false
    fmt.Println("str1 < str2:", str1 < str2)    // prints: str1 < str2: true
}
```

### 3. Summary

- **Relational operators** compare the relationship between values.
- They include:
  - Equal (`==`)
  - Not equal (`!=`)
  - Greater than (`>`)
  - Less than (`<`)
  - Greater than or equal (`>=`)
  - Less than or equal (`<=`)
- Relational operators return a boolean (`true` or `false`) representing the result of the comparison.

The condition expressions in `if` and `for` are almost entirely built from these 6 operators; combined with `&&` and `||` you can compose any test you need.

## References

- [Language Spec · Operators](https://go.dev/ref/spec#Operators)
- [Language Spec · Comparison operators](https://go.dev/ref/spec#Comparison_operators)


## Sibling pages

- [Arithmetic](/operator/Arithmetic.md)
- [Assignment](/operator/Assignment.md)
- [BitLen](/operator/BitLen.md)
- [Receiver](/operator/Receiver.md)
- [TypeAssertion](/operator/TypeAssertion.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Receiver](/operator/Receiver.md)
- [TypeAssertion](/operator/TypeAssertion.md)
