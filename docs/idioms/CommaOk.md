In Go, the `comma ok` idiom is a common pattern for telling whether an operation succeeded. It shows up frequently in type assertions, map lookups, and channel receives.

### `comma ok` in type assertions

When asserting an interface value to a concrete type, you can use `comma ok` to tell whether the assertion succeeded.

```go
package main

import "fmt"

func main() {
    var i interface{} = "hello"

    // assertion succeeds
    if s, ok := i.(string); ok {
        fmt.Println("string value:", s)
    } else {
        fmt.Println("not a string")
    }

    // assertion fails
    if n, ok := i.(int); ok {
        fmt.Println("int value:", n)
    } else {
        fmt.Println("not an int")
    }
}
```

Output:

```
string value: hello
not an int
```

When `ok` is `true`, you get the asserted concrete value; when it's `false`, the value is the zero value and the program takes the `else` branch.

### `comma ok` in map lookups

When looking up a key in a map, you can use the `comma ok` idiom to tell whether the key exists.

```go
package main

import "fmt"

func main() {
    m := map[string]int{"a": 1, "b": 2}

    // look up an existing key
    if value, ok := m["a"]; ok {
        fmt.Println("Found value:", value)
    } else {
        fmt.Println("Key not found")
    }

    // look up a missing key
    if value, ok := m["c"]; ok {
        fmt.Println("Found value:", value)
    } else {
        fmt.Println("Key not found")
    }
}
```

Output:

```
Found value: 1
Key not found
```

The zero value you get from a bare `m["c"]` can't distinguish "the key is missing" from "the value really is 0"; adding `ok` separates the two cases.

### `comma ok` in channel receives

When receiving from a channel, you can use the `comma ok` idiom to tell whether the channel is closed.

```go
package main

import (
    "fmt"
)

func main() {
    ch := make(chan int, 1)
    ch <- 1
    close(ch)

    // receive a value from the channel
    if value, ok := <-ch; ok {
        fmt.Println("Received value:", value)
    } else {
        fmt.Println("Channel closed")
    }

    // receive again from the now-closed channel
    if value, ok := <-ch; ok {
        fmt.Println("Received value:", value)
    } else {
        fmt.Println("Channel closed")
    }
}
```

Output:

```
Received value: 1
Channel closed
```

Receiving from a closed channel doesn't block; the zero value paired with `ok == false` is the signal that "the channel is closed".

### Summary

The `comma ok` idiom is a common Go programming pattern for telling whether an operation succeeded. It's mainly used in these situations:

1. **Type assertions**: whether an interface-to-concrete assertion succeeded.
2. **Map lookups**: whether a key exists in the map.
3. **Channel receives**: whether the channel is closed.

All three share one form: the value on the left, `ok` on the right for success or failure. It removes the separate "check existence, then fetch" two-step, and avoids the zero-value ambiguity.

## References

- [Effective Go (official)](https://go.dev/doc/effective_go)
- [Language spec · Type assertions (comma-ok form)](https://go.dev/ref/spec#Type_assertions)
- [Language spec · Receive operator](https://go.dev/ref/spec#Receive_operator)

## Sibling pages

- [EffectiveGo](/idioms/EffectiveGo.md)
- [StructTags](/idioms/StructTags.md)
- [BlankIdentifier](/idioms/BlankIdentifier.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [BlankIdentifier](/idioms/BlankIdentifier.md)
