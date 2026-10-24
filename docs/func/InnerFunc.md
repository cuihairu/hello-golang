# Go Built-in Functions
Go's built-in functions are a set of functions provided by the language itself, available without any explicit import. They cover type conversion, length and capacity queries, map insertion and deletion, and panic/recovery.

Below are Go's main built-in functions and their parameters.

### 1. `append`

**Function**: adds elements to a slice and returns a new slice.

**Parameters**:
- `s`: the slice.
- `elem`: the element or elements to add.

**Return value**: the new slice containing the added elements.

**Example**:

```go
package main

import "fmt"

func main() {
    s := []int{1, 2, 3}
    s = append(s, 4, 5)
    fmt.Println(s) // prints: [1 2 3 4 5]
}
```

### 2. `cap`

**Function**: returns the capacity of a slice, array, or channel.

**Parameters**:
- `v`: the slice, array, or channel.

**Return value**: the capacity as an integer.

**Example**:

```go
package main

import "fmt"

func main() {
    s := []int{1, 2, 3}
    fmt.Println(cap(s)) // prints: 3
}
```

### 3. `close`

**Function**: closes a channel, signaling receivers that no more data will be sent.

**Parameters**:
- `c`: the channel to close.

**Return value**: none.

**Example**:

```go
package main

import "fmt"

func main() {
    ch := make(chan int)
    go func() {
        for i := 0; i < 3; i++ {
            ch <- i
        }
        close(ch)
    }()

    for value := range ch {
        fmt.Println(value)
    }
}
```

### 4. `copy`

**Function**: copies elements from a source slice to a destination slice.

**Parameters**:
- `dst`: the destination slice.
- `src`: the source slice.

**Return value**: the number of elements actually copied.

**Example**:

```go
package main

import "fmt"

func main() {
    src := []int{1, 2, 3}
    dst := make([]int, len(src))
    n := copy(dst, src)
    fmt.Println(dst) // prints: [1 2 3]
    fmt.Println(n)   // prints: 3
}
```

### 5. `delete`

**Function**: removes a key-value pair from a map.

**Parameters**:
- `m`: the map.
- `key`: the key to delete.

**Return value**: none.

**Example**:

```go
package main

import "fmt"

func main() {
    m := map[string]int{"a": 1, "b": 2}
    delete(m, "b")
    fmt.Println(m) // prints: map[a:1]
}
```

### 6. `len`

**Function**: returns the length of a slice, array, map, or string.

**Parameters**:
- `v`: the slice, array, map, or string.

**Return value**: the length as an integer.

**Example**:

```go
package main

import "fmt"

func main() {
    s := []int{1, 2, 3}
    fmt.Println(len(s)) // prints: 3

    m := map[string]int{"a": 1, "b": 2}
    fmt.Println(len(m)) // prints: 2

    str := "hello"
    fmt.Println(len(str)) // prints: 5
}
```

### 7. `make`

**Function**: creates and initializes a slice, map, or channel.

**Parameters**:
- `t`: the type to create (`slice`, `map`, `channel`).
- `len`: (for slices) the initial length; (for maps) an optional initial capacity hint.
- `cap`: (for slices) the capacity. Note: when creating a map, `make` accepts at most one extra argument.

**Return value**: the newly created slice, map, or channel.

**Example**:

```go
package main

import "fmt"

func main() {
    // create a slice
    s := make([]int, 3, 5)
    fmt.Println(s) // prints: [0 0 0]
    fmt.Println(cap(s)) // prints: 5

    // create a map
    m := make(map[string]int)
    m["a"] = 1
    fmt.Println(m) // prints: map[a:1]

    // create a channel
    ch := make(chan int, 2)
    ch <- 1
    ch <- 2
    fmt.Println(<-ch) // prints: 1
}
```

### 8. `new`

**Function**: allocates memory, initializes it to its zero value, and returns a pointer to it.

**Parameters**:
- `t`: the type to allocate.

**Return value**: a pointer to the newly allocated memory.

**Example**:

```go
package main

import "fmt"

func main() {
    // create a zero value of type int
    p := new(int)
    fmt.Println(*p) // prints: 0
}
```

### 9. `panic`

**Function**: raises a runtime error; the program stops running and invokes the cleanup functions registered with `defer`.

**Parameters**:
- `v`: the value to panic with.

**Return value**: none.

**Example**:

```go
package main

import "fmt"

func main() {
    defer fmt.Println("Defer executed")
    panic("Something went wrong")
}
```

Runtime output (the `defer` cleanup runs first, then the program exits with a non-zero exit code; the stack trace portion varies by runtime environment):

```text
Defer executed
panic: Something went wrong
```

### 10. `recover`

**Function**: recovers from a `panic`, allowing the program to continue running.

**Parameters**:
- none.

**Return value**: the value passed to `panic`, or `nil` if there was no `panic`.

**Example**:

```go
package main

import "fmt"

func safeDivision(a, b int) (result int) {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("Recovered from panic:", r)
        }
    }()
    if b == 0 {
        panic("Division by zero")
    }
    return a / b
}

func main() {
    fmt.Println(safeDivision(10, 2)) // prints: 5
    fmt.Println(safeDivision(10, 0)) // first prints Recovered from panic: Division by zero, then prints the return value 0
}
```

### Summary

- **`append`**: adds elements to a slice.
- **`cap`**: returns the capacity of a slice, array, or channel.
- **`close`**: closes a channel.
- **`copy`**: copies elements from a source slice to a destination slice.
- **`delete`**: removes a key-value pair from a map.
- **`len`**: returns the length of a slice, array, map, or string.
- **`make`**: creates and initializes a slice, map, or channel.
- **`new`**: allocates memory, initializes it to its zero value, and returns a pointer.
- **`panic`**: raises a runtime error.
- **`recover`**: recovers from a `panic`.

`recover` only catches a `panic` when it is called inside a deferred function, which is exactly how `safeDivision` uses it; the rest can be called directly.

## References

- [Language Spec · Function declarations](https://go.dev/ref/spec#Function_declarations)
- [Language Spec · Calls](https://go.dev/ref/spec#Calls)
- [Effective Go · Functions](https://go.dev/doc/effective_go#functions)
- [Language Spec · Function literals](https://go.dev/ref/spec#Function_literals)


## Sibling pages

- [AnonymousFunc](/func/AnonymousFunc.md)
- [Defer](/func/Defer.md)
- [VariadicParameters](/func/VariadicParameters.md)
- [History](/func/History.md)
- [MultipleReturnValues](/func/MultipleReturnValues.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [History](/func/History.md)
- [MultipleReturnValues](/func/MultipleReturnValues.md)
