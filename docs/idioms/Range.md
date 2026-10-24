# range
In Go, `range` is the keyword used to iterate over data structures. It walks arrays, slices, maps, strings, and channels, with one uniform way of writing it.

### Basic usage

The `range` keyword is used inside a `for` loop and can iterate over every kind of data structure. On each iteration, `range` returns one or more values, depending on the type of the data structure.

#### Example: iterating over arrays and slices

```go
package main

import "fmt"

func main() {
    // iterate over an array
    arr := [3]int{1, 2, 3}
    for index, value := range arr {
        fmt.Printf("Index: %d, Value: %d\n", index, value)
    }

    // iterate over a slice
    slice := []int{4, 5, 6}
    for index, value := range slice {
        fmt.Printf("Index: %d, Value: %d\n", index, value)
    }
}
```

**Output:**

```
Index: 0, Value: 1
Index: 1, Value: 2
Index: 2, Value: 3
Index: 0, Value: 4
Index: 1, Value: 5
Index: 2, Value: 6
```

#### Example: iterating over a map

```go
package main

import "fmt"

func main() {
    // iterate over a map
    m := map[string]int{"a": 1, "b": 2, "c": 3}
    for key, value := range m {
        fmt.Printf("Key: %s, Value: %d\n", key, value)
    }
}
```

**Output:**

```
Key: a, Value: 1
Key: b, Value: 2
Key: c, Value: 3
```

> Note: Go deliberately randomizes map iteration order, so the order in which key-value pairs appear can differ on every run (the output above is just one possible ordering). Program logic should not rely on map iteration order.

#### Example: iterating over a string

```go
package main

import "fmt"

func main() {
    // iterate over a string
    s := "hello"
    for index, char := range s {
        fmt.Printf("Index: %d, Rune: %c\n", index, char)
    }
}
```

**Output:**

```
Index: 0, Rune: h
Index: 1, Rune: e
Index: 2, Rune: l
Index: 3, Rune: l
Index: 4, Rune: o
```

#### Example: iterating over a channel

```go
package main

import "fmt"

func main() {
    ch := make(chan int)

    // start a goroutine that sends data to the channel
    go func() {
        for i := 0; i < 3; i++ {
            ch <- i
        }
        close(ch)
    }()

    // iterate over the channel
    for value := range ch {
        fmt.Println("Received:", value)
    }
}
```

**Output:**

```
Received: 0
Received: 1
Received: 2
```

### How `range` works

- **Arrays and slices**: `range` returns two values — the index and the corresponding element. While iterating, `range` copies the array or slice element, so to modify an element you usually have to work through the index directly.
  
- **Maps**: `range` returns two values — the key and the corresponding value. The traversal order of key-value pairs is unordered, because maps themselves are unordered.

- **Strings**: `range` returns two values — the index and the character (rune). A rune is a Unicode code point; `range` walks the string rune by rune, even when a character spans multiple bytes.

- **Channels**: `range` keeps receiving from the channel until it is closed. Closing the channel terminates the `range` loop.

### Summary

- One `range` form walks five kinds of structures: arrays, slices, maps, strings, channels.
- Arrays and slices give index and value; maps give key and value; strings give byte index and rune; channels receive until closed.

The loop body doesn't need a separate implementation per data type — that's the direct benefit `range` brings.

## References

- [Effective Go (official)](https://go.dev/doc/effective_go)
- [Language spec · For statements (range clause)](https://go.dev/ref/spec#For_statements)
- [Official blog · Range Over Function Types](https://go.dev/blog/range-functions)


## Sibling pages

- [EffectiveGo](/idioms/EffectiveGo.md)
- [StructTags](/idioms/StructTags.md)
- [BlankIdentifier](/idioms/BlankIdentifier.md)
- [Labels](/idioms/Labels.md)
- [ShortVarDecl](/idioms/ShortVarDecl.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Labels](/idioms/Labels.md)
- [ShortVarDecl](/idioms/ShortVarDecl.md)
