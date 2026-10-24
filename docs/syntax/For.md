### A Detailed Explanation of the `for` Loop in Go

`for` is the only loop statement in Go; the jobs done by `while` and `do-while` in C are all handled by it.

#### 1. Basic `for` Loop Syntax

The basic `for` loop syntax is similar to C, with the following structure:

```go
for init statement; condition; post statement {
    // loop body
}
```

Example:

```go
for i := 0; i < 10; i++ {
    fmt.Println(i)
}
```

This loop prints from 0 to 9.

#### 2. `for` Loop with `range`

`range` is used to iterate over arrays, slices, strings, maps, and channels. When iterating with `range`, it returns two values: the first is the index (or key), the second is the element (or value).

Example:

Iterating over an array or slice:

```go
nums := []int{2, 3, 4}
for i, num := range nums {
    fmt.Println(i, num)
}
```

Iterating over a string:

```go
str := "hello"
for i, ch := range str {
    fmt.Println(i, string(ch))
}
```

Iterating over a map:

```go
m := map[string]string{"a": "apple", "b": "banana"}
for k, v := range m {
    fmt.Println(k, v)
}
```

Iterating over a channel:

```go
ch := make(chan int, 2)
ch <- 1
ch <- 2
close(ch)
for val := range ch {
    fmt.Println(val)
}
```

#### 3. The Problem of Using Goroutines in `for` Loops Before Go 1.22

Before Go 1.22, the loop variable had only one instance for the entire loop. If you used goroutines inside a `for` loop, you would easily run into variable capture issues. Example:

```go
for i := 0; i < 10; i++ {
    go func() {
        fmt.Println(i)
    }()
}
```

The output of this code may not be the expected 0 to 9, but instead multiple identical values. This is because the closure captures the `i` variable, not its current value. The correct approach is to pass a copy of `i`:

```go
for i := 0; i < 10; i++ {
    go func(i int) {
        fmt.Println(i)
    }(i)
}
```

This ensures that each goroutine uses a different `i` value.

Starting with Go 1.22, the loop variable is given a new instance for each iteration, so the closure pattern above will directly produce 0 to 9. However, in code that needs to remain compatible with older versions, passing a copy via a parameter is still the safest habit.

#### 4. Using `defer` in `for` Loops

The `defer` statement is used to execute certain operations before a function returns. When using `defer` inside a `for` loop, be aware that `defer` does not execute at the end of each iteration; it is delayed until just before the entire function returns, executing in last-in, first-out order.

Example:

```go
for i := 0; i < 3; i++ {
    defer fmt.Println(i)
}
```

The output order is:

```
2
1
0
```

#### 5. Other Common Uses and Caveats

- **Infinite loop**: Omit all three parts to form an infinite loop.

    ```go
    for {
        // infinite loop body
    }
    ```

- **Single-condition loop**: Omit the initialization and post statements.

    ```go
    i := 0
    for i < 10 {
        fmt.Println(i)
        i++
    }
    ```

- **`break` and `continue` in loops**: `break` exits the loop, `continue` skips the current iteration.

    ```go
    for i := 0; i < 10; i++ {
        if i == 5 {
            break
        }
        if i%2 == 0 {
            continue
        }
        fmt.Println(i)
    }
    ```

- **Labels and multi-level loops**: Use labels to break out of nested loops.

    ```go
    outer:
    for i := 0; i < 3; i++ {
        for j := 0; j < 3; j++ {
            if i == 1 {
                break outer
            }
            fmt.Println(i, j)
        }
    }
    ```

Labels are only used in three places: `break`, `continue`, and `goto`; using them anywhere else will not compile.

## References

- [Language Spec · Statements](https://go.dev/ref/spec#Statements)
- [Effective Go · Control Structures](https://go.dev/doc/effective_go#control-structures)
- [Language Spec · For statements (including range)](https://go.dev/ref/spec#For_statements)
- [Official Blog · Fixing For Loops in Go 1.22](https://go.dev/blog/loopvar-preview)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Conditional](/syntax/Conditional.md)
- [ControlFlow](/syntax/ControlFlow.md)
- [Jump](/syntax/Jump.md)
- [Loop](/syntax/Loop.md)
