### Error handling and limits

Reflection's write operations have preconditions; if they are not met, the program panics outright, so check before you call:

- Use `CanSet()` before writing a value. A pointer's `Elem()` is settable; a `Value` obtained straight from `ValueOf(x)` is not.
- For unexported fields (starting with a lowercase letter), `CanSet()` is `false` and `SetXxx` panics; the only way to change them is through `unsafe`, which is not recommended.
- The argument types to `Call` must match the method signature, or it panics; return values come out of a slice, and you have to assert their types yourself.

```go
package main

import (
    "fmt"
    "reflect"
)

func safeCall(fn interface{}, args ...interface{}) (results []interface{}, err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("reflect call panic: %v", r)
        }
    }()

    v := reflect.ValueOf(fn)
    in := make([]reflect.Value, len(args))
    for i, a := range args {
        in[i] = reflect.ValueOf(a)
    }
    out := v.Call(in)
    results = make([]interface{}, len(out))
    for i, r := range out {
        results[i] = r.Interface()
    }
    return
}

func Add(a, b int) int { return a + b }

func main() {
    res, err := safeCall(Add, 1, 2)
    fmt.Println(res, err) // prints: [3] <nil>

    _, err = safeCall(Add, 1, "2")
    fmt.Println(err) // prints: reflect call panic: reflect: Call using string as type int
}
```

### Performance

Reflection is slow in three places: arguments and return values have to be boxed into `reflect.Value`, type information is looked up at runtime, and `Call` goes through generic dispatch rather than a direct jump. On a hot path, reflection is at least an order of magnitude slower than a direct call; the exact multiplier varies with the scenario, so benchmark your own case with `testing.B`.

Order of alternatives for a hot path:

1. **Type switch**: when the set of types is small, use `switch v := x.(type)` — checked at compile time, no boxing.
2. **Generics** (Go 1.18+): if you can express it as a generic constraint, do that instead of reflection; once instantiated at compile time it becomes a direct call.
3. **Code generation**: when the type set is fixed but large, use `go generate` to produce concrete code.

### Concurrency

Reflection's write operations (`SetXxx`, `Call`) are not concurrency-safe: if multiple goroutines mutate the same `Value` at once, you need a lock. Read-only operations (`Type`, `Interface`, `Kind`) can be called concurrently. Objects created by reflection (`New`, `MakeSlice`) are each independent, so there is no shared-state problem.

### In summary

For reflection's write operations, check `CanSet` first, guarantee argument types yourself, and catch panics with `recover`; on hot paths prefer type switches, generics, and code generation; in concurrent code keep it read-only, or lock when you write. For the basics, see [Reflection basics](/reflection/Reflection.md).

## References

- [reflect standard library](https://pkg.go.dev/reflect)
- [unsafe standard library](https://pkg.go.dev/unsafe)

## Sibling pages

- [Reflection](/reflection/Reflection.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Reflection](/reflection/Reflection.md)
