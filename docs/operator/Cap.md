In Go, the **capacity operator** is not a standalone operator; you get the capacity of collection types (slices, arrays, channels) through the built-in function `cap`.

### 1. **The concept of capacity**

- **Capacity** refers to the maximum number of elements a collection type can hold without reallocating memory. For slices and arrays, capacity is the length from the start of the slice or array to the end of its underlying array.

### 2. **Getting capacity with the `cap` function**

- **Slice**: the `cap` function returns the slice's capacity, i.e. the length from the slice's starting position to the end of the underlying array.
- **Array**: the `cap` function returns the array's length and capacity; the two values are the same.
- **Channel**: the `cap` function returns the channel's buffer capacity, i.e. the maximum number of elements the channel can buffer.

### Example code

#### Capacity of a slice

```go
package main

import "fmt"

func main() {
    s := make([]int, 5, 10) // create a slice with length 5 and capacity 10
    fmt.Println("Slice:", s)
    fmt.Println("Length:", len(s))
    fmt.Println("Capacity:", cap(s)) // prints: Capacity: 10
}
```

In this example, `cap(s)` returns 10, because the slice `s` has a capacity of 10.

#### Capacity of an array

```go
package main

import "fmt"

func main() {
    a := [5]int{1, 2, 3, 4, 5}
    fmt.Println("Array:", a)
    fmt.Println("Length:", len(a))
    fmt.Println("Capacity:", cap(a)) // prints: Capacity: 5
}
```

In this example, `cap(a)` returns 5, because the length and the capacity of the array `a` are both 5.

#### Capacity of a channel

```go
package main

import "fmt"

func main() {
    c := make(chan int, 5) // create a channel with a buffer capacity of 5
    fmt.Println("Channel capacity:", cap(c)) // prints: Channel capacity: 5
}
```

In this example, `cap(c)` returns 5, because the channel `c` has a buffer capacity of 5.

### Summary

- **Capacity** is the maximum number of elements a collection can hold without reallocating memory.
- **Go uses the `cap` function** to get the capacity of slices, arrays, and channels:
  - **Slice**: `cap(slice)` returns the slice's capacity.
  - **Array**: `cap(array)` returns the array's length and capacity (the two are the same).
  - **Channel**: `cap(channel)` returns the capacity of the channel's buffer.

To judge whether a slice is about to grow, read `len` and `cap` together: `len` is the number of elements already stored, `cap` is how many it can hold without reallocating memory.

## References

- [Language specification · Operators](https://go.dev/ref/spec#Operators)
- [builtin standard library · cap/len](https://pkg.go.dev/builtin)


## Sibling pages

- [Arithmetic](/operator/Arithmetic.md)
- [Assignment](/operator/Assignment.md)
- [BitLen](/operator/BitLen.md)
- [Bitwise](/operator/Bitwise.md)
- [Logical](/operator/Logical.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Logical](/operator/Logical.md)
