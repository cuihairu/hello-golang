The short variable declaration uses `:=` to declare and initialize variables inside a function, one or more at a time.

### Basic syntax

```go
variableName := expression
```

### Detailed examples

#### 1. Short-declaring a single variable

```go
package main

import "fmt"

func main() {
    a := 1 // declare and initialize an integer variable a
    fmt.Println(a) // prints: 1
}
```

#### 2. Short-declaring multiple variables

```go
package main

import "fmt"

func main() {
    a, b, c := 1, 2, 3 // declare and initialize three variables at once
    fmt.Println(a, b, c) // prints: 1 2 3
}
```

#### 3. Combined with function return values

```go
package main

import "fmt"

func add(a, b int) int {
    return a + b
}

func main() {
    result := add(3, 4) // use a short declaration to receive the function's return value
    fmt.Println(result) // prints: 7
}
```

#### 4. Short declarations in a loop

```go
package main

import "fmt"

func main() {
    for i := 0; i < 5; i++ { // use a short declaration in a for loop
        fmt.Println(i)
    }
}
```

#### 5. Combined with an `if` statement

```go
package main

import "fmt"

func main() {
    if a := 10; a > 5 { // use a short declaration in an if statement
        fmt.Println(a) // prints: 10
    }
}
```

Here `a` is declared in the condition part of the `if`, and is only usable inside the `if` statement.

### Notes

1. **Only usable inside a function**: it doesn't work at package level (global scope).
2. **At least one new variable**: when short-declaring onto variables that already exist, at least one on the left must be new. For example:
    ```go
    package main

    import "fmt"

    func main() {
        a, b := 1, 2
        a, c := 3, 4 // here a is an existing variable, while c is a new one
        fmt.Println(a, b, c) // prints: 3 2 4
    }
    ```
3. **Type inference**: Go infers the variable's type automatically from the type of the expression on the right.

### Summary

`:=` merges declaration and initialization into one step. Two restrictions to remember: it only works inside a function, and when redeclaring existing variables, at least one variable on the left must be new.

## References

- [Effective Go (official)](https://go.dev/doc/effective_go)
- [Language spec · Short variable declarations](https://go.dev/ref/spec#Short_variable_declarations)


## Sibling pages

- [EffectiveGo](/idioms/EffectiveGo.md)
- [StructTags](/idioms/StructTags.md)
- [BlankIdentifier](/idioms/BlankIdentifier.md)
- [Range](/idioms/Range.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Range](/idioms/Range.md)
