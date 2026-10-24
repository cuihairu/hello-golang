### A Detailed Explanation of the `if` Statement in Go

The `if` statement is the basic control structure for conditional branching. Go's `if` supports `else`, supports multiple conditional branches, and can include an initialization statement before the condition; the scope of any declared variable is limited to the `if/else` blocks.

#### 1. Basic `if` Statement

The basic `if` statement structure is as follows:

```go
if condition {
    // code executed when the condition is true
}
```

Example:

```go
x := 10
if x > 5 {
    fmt.Println("x is greater than 5")
}
```

#### 2. `if` Statement with `else`

When you need to execute other code when the condition is false, use the `else` statement:

```go
if condition {
    // code executed when the condition is true
} else {
    // code executed when the condition is false
}
```

Example:

```go
x := 3
if x > 5 {
    fmt.Println("x is greater than 5")
} else {
    fmt.Println("x is not greater than 5")
}
```

#### 3. `if-else if-else` Statement

You can use multiple `else if` statements to check multiple conditions:

```go
if condition 1 {
    // code executed when condition 1 is true
} else if condition 2 {
    // code executed when condition 2 is true
} else {
    // code executed when all conditions are false
}
```

Example:

```go
x := 7
if x > 10 {
    fmt.Println("x is greater than 10")
} else if x > 5 {
    fmt.Println("x is greater than 5 but less than or equal to 10")
} else {
    fmt.Println("x is 5 or less")
}
```

#### 4. `if` Statement with an Initialization Statement

Go's `if` statement supports adding a simple initialization statement before the condition expression, separated from the condition by a semicolon. This allows you to perform a one-time computation or assignment before evaluating the condition.

```go
if init statement; condition {
    // code executed when the condition is true
}
```

Example:

```go
if x := 10; x > 5 {
    fmt.Println("x is greater than 5")
}
```

This form is especially useful in scenarios that require a temporary variable, for example:

```go
someFunction := func() error {
    return errors.New("something went wrong")
}

if err := someFunction(); err != nil {
    fmt.Println("Error:", err)
}
```

#### 5. Variable Scope in `if` Statements

Variables declared in an `if` statement have scope limited to the `if` block and the corresponding `else` block.

Example:

```go
if x := 10; x > 5 {
    fmt.Println("x is greater than 5")
} else {
    fmt.Println("x is not greater than 5")
    // x is still accessible here
    fmt.Println(x)
}
// x is not accessible here
// fmt.Println(x) // compile error
```

#### 6. Nested `if` Statements

`if` statements can be nested, meaning one `if` statement can contain another:

```go
x := 8
if x > 5 {
    if x < 10 {
        fmt.Println("x is between 5 and 10")
    }
}
```

You can also combine `else if` and `else` to write nested `if` statements, making the code logic clearer:

```go
x := 8
if x > 10 {
    fmt.Println("x is greater than 10")
} else if x > 5 {
    if x < 10 {
        fmt.Println("x is between 5 and 10")
    } else {
        fmt.Println("x is 10")
    }
} else {
    fmt.Println("x is 5 or less")
}
```

#### 7. Common Uses and Caveats of `if` Statements

- **Checking whether a string is empty**:

    ```go
    str := "hello"
    if str != "" {
        fmt.Println("str is not empty")
    }
    ```

- **Checking whether a slice or array is empty**:

    ```go
    nums := []int{1, 2, 3}
    if len(nums) > 0 {
        fmt.Println("nums is not empty")
    }
    ```

- **Error handling**:

    ```go
    someFunction := func() error {
        return errors.New("something went wrong")
    }

    if err := someFunction(); err != nil {
        fmt.Println("Error:", err)
    }
    ```

- **Caveat**: In complex conditional checks, use parentheses to make the operator precedence explicit and improve code readability.

    ```go
    x, y, z := 7, 3, 3
    if (x > 5 && y < 10) || (z == 3) {
        fmt.Println("Complex condition met")
    }
    ```

## References

- [Language Spec · Statements](https://go.dev/ref/spec#Statements)
- [Effective Go · Control Structures](https://go.dev/doc/effective_go#control-structures)
- [Language Spec · If statements](https://go.dev/ref/spec#If_statements)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Conditional](/syntax/Conditional.md)
- [Jump](/syntax/Jump.md)
