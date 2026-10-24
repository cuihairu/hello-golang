Go has four ways to declare a variable: an explicit `var` declaration, `var` with initialization, the `:=` short declaration, and `var (...)` for bulk declarations. Anything not explicitly initialized gets its zero value.

### Defining variables

1. **Explicit declaration with the `var` keyword**:
   - This is the most basic form of variable declaration.
   - You must specify both the variable's name and its type.

   For example:
   ```go
   var age int
   var name string
   var isActive bool

   fmt.Println(age, name, isActive)
   ```

2. **Declaration with initialization using `var`**:
   - The variable is initialized at the same time it is declared.
   - The compiler infers the variable's type automatically.

   For example:
   ```go
   var age int = 30
   var name string = "Alice"
   var isActive bool = true

   fmt.Println(age, name, isActive)
   ```

3. **Short variable declaration (`:=`)**:
   - Inside a function, you can use `:=` for a short variable declaration.
   - The compiler infers the variable's type from the value on the right.
   - This form cannot be used outside a function (at package scope).

   For example:
   ```go
   age := 30
   name := "Alice"
   isActive := true

   fmt.Println(age, name, isActive)
   ```

4. **Bulk declaration**:
   - The `var` keyword can declare multiple variables at once.
   - You can initialize them at the same time as declaring them.

   For example:
   ```go
   package main

   import "fmt"

   func main() {
       var (
           age      int    = 30
           name     string = "Alice"
           isActive bool   = true
       )

       fmt.Println(age, name, isActive)
   }
   ```

### Initializing variables

In Go, a variable can be initialized at the time it is declared. If it is not explicitly initialized, the variable is given the zero value of its type.

1. **Zero-value initialization**:
   - When a variable is declared without explicit initialization, Go gives it its zero value.
   - Zero values by type:
     - Numeric types (including integers and floating-point numbers): 0
     - Boolean type: false
     - String type: the empty string ""
     - Pointers, functions, interfaces, slices, channels, and maps: nil

   For example:
   ```go
   var age int          // zero value is 0
   var name string      // zero value is ""
   var isActive bool    // zero value is false
   var pointer *int     // zero value is nil

   fmt.Println(age, name, isActive, pointer)
   ```

2. **Explicit initialization**:
   - A variable can be explicitly initialized when it is declared.

   For example:
   ```go
   var age int = 30
   var name string = "Alice"
   var isActive bool = true
   var pointer *int = nil

   fmt.Println(age, name, isActive, pointer)
   ```

3. **Initialization with short variable declaration**:
   - A short variable declaration initializes the variable at the same time it is declared.

   For example:
   ```go
   age := 30
   name := "Alice"
   isActive := true

   fmt.Println(age, name, isActive)
   ```

### Example code

Here is an example showing the different ways to define and initialize variables:

```go
package main

import "fmt"

func main() {
    // explicit declaration with the var keyword
    var age int
    var name string
    var isActive bool

    // print zero values
    fmt.Println("Age:", age)           // 0
    fmt.Println("Name:", name)         // ""
    fmt.Println("Is Active:", isActive) // false

    // declaration with initialization using var
    var age2 int = 30
    var name2 string = "Alice"
    var isActive2 bool = true

    // print initialized values
    fmt.Println("Age2:", age2)           // 30
    fmt.Println("Name2:", name2)         // Alice
    fmt.Println("Is Active2:", isActive2) // true

    // short variable declaration
    age3 := 25
    name3 := "Bob"
    isActive3 := false

    // print initialized values
    fmt.Println("Age3:", age3)           // 25
    fmt.Println("Name3:", name3)         // Bob
    fmt.Println("Is Active3:", isActive3) // false

    // bulk declaration
    var (
        age4      int    = 40
        name4     string = "Charlie"
        isActive4 bool   = true
    )

    // print initialized values
    fmt.Println("Age4:", age4)           // 40
    fmt.Println("Name4:", name4)         // Charlie
    fmt.Println("Is Active4:", isActive4) // true
}
```

### Summary

The four forms differ in where they can be used: `var` works at package level, `:=` only works inside a function, and bulk declaration groups a set of related variables together. The zero-value mechanism guarantees that every declared variable already has a definite value, so there is no footgun of an "uninitialized" variable.

## References

- [Language Spec · Variable declarations](https://go.dev/ref/spec#Variable_declarations)
- [Effective Go · Variables](https://go.dev/doc/effective_go#variables)
- [Effective Go · Initialization](https://go.dev/doc/effective_go#initialization)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/zh/glossary.md)
- [Assignment](/var/Assignment.md)
- [ScopeAndLifetime](/var/ScopeAndLifetime.md)
- [Variable](/var/Variable.md)
