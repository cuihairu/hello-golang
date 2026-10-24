### Go Slice Introduction

A slice is the structure Go uses to handle dynamically-sized collections. It is more flexible than an array: its length can change, and multiple slices can share the same underlying array.

### 1. Basic Usage

#### Declaration and Initialization

```go
package main

import "fmt"

func main() {
    // declare an empty int slice
    var s []int

    // initialize with a literal
    s2 := []int{1, 2, 3, 4, 5}

    // use the make function to create a slice with a specified length and capacity
    s3 := make([]int, 5)    // both length and capacity are 5
    s4 := make([]int, 3, 5) // length is 3, capacity is 5

    fmt.Println(s, s2, s3, s4)
}
```

#### Operating on Slices

```go
s := []int{1, 2, 3, 4, 5}
fmt.Println(s)            // prints: [1 2 3 4 5]

s = append(s, 6, 7)       // add elements
fmt.Println(s)            // prints: [1 2 3 4 5 6 7]

subSlice := s[1:4]        // slice operation, get a sub-slice
fmt.Println(subSlice)     // prints: [2 3 4]
```

### 2. Difference from Arrays

- **Length**: an array's length is fixed and must be specified at declaration; a slice's length is dynamic and can be adjusted at runtime.
- **Type**: an array's type includes length information, so `[5]int` and `[10]int` are different types; a slice carries no length information, only `[]int`.
- **Value type vs. reference type**: an array is a value type, so assignment and passing copy the whole array; a slice is a reference type, so assignment and passing share the underlying array.
- **Memory allocation**: an array's memory is contiguous and fixed in size; a slice is built on top of an array and can grow by extending capacity.

### 3. Underlying Implementation

At its core a slice is a struct with three fields:

- **Pointer**: points to the start of the underlying array.
- **Length**: the slice's current length, that is, the number of elements the slice contains.
- **Capacity**: the number of elements from the slice's start position to the end of the underlying array.

```go
type slice struct {
    array unsafe.Pointer
    len   int
    cap   int
}
```

When a slice grows beyond its capacity, the Go runtime allocates a larger array, copies the old array's contents into the new one, and then frees the old array's memory.

### 4. Common Pitfalls

#### Shared Underlying Array

Slices share their underlying array, so modifying one slice affects other slices that share the same underlying array.

```go
s := []int{1, 2, 3, 4, 5}
subSlice := s[1:4]
subSlice[0] = 100
fmt.Println(s)           // prints: [1 100 3 4 5]
```

#### Slice Growth

When a slice's capacity is insufficient, the append operation creates a new underlying array. This can cause some hard-to-spot bugs.

```go
s := []int{1, 2, 3}
t := s
s = append(s, 4)
s[0] = 100
fmt.Println(t)           // prints: [1 2 3], unaffected, because s now points to a new underlying array
```

#### Insufficient Capacity When Using make

When creating a slice with the `make` function, make sure you specify an appropriate capacity to avoid frequent memory reallocation.

```go
s := make([]int, 0, 3)
s = append(s, 1, 2, 3, 4)  // the fourth element forces the underlying array to grow
```

#### Slice Initialized to nil

An uninitialized slice defaults to nil, which is different from an empty slice. Using the `make` function ensures the slice is not nil.

```go
package main

import "fmt"

func main() {
    var s []int // s == nil
    if s == nil {
        fmt.Println("s is nil")
    }

    s = make([]int, 0) // s != nil
    if s != nil {
        fmt.Println("s is not nil")
    }
}
```

### Example Code

```go
package main

import "fmt"

func main() {
    // basic usage
    s := []int{1, 2, 3, 4, 5}
    fmt.Println(s)            // prints: [1 2 3 4 5]

    s = append(s, 6, 7)
    fmt.Println(s)            // prints: [1 2 3 4 5 6 7]

    subSlice := s[1:4]
    fmt.Println(subSlice)     // prints: [2 3 4]

    // shared underlying array
    subSlice[0] = 100
    fmt.Println(s)            // prints: [1 100 3 4 5 6 7]

    // slice growth
    t := s
    s = append(s, 8)
    s[0] = 200
    fmt.Println(t)            // prints: [1 100 3 4 5 6 7], unaffected

    // nil slice vs. empty slice
    var nilSlice []int
    emptySlice := make([]int, 0)
    fmt.Println(nilSlice == nil)  // prints: true
    fmt.Println(emptySlice == nil)  // prints: false
}
```

Three things to remember about slices: modifying a sub-slice changes the underlying array, growth makes the slice point elsewhere, and a nil slice is not the same as an empty slice.

## References

- [Language Specification · Types](https://go.dev/ref/spec#Types)
- [Language Specification · Slice types](https://go.dev/ref/spec#Slice_types)
- [Official Blog · Go Slices: usage and internals](https://go.dev/blog/slices-intro)
- [Official Blog · The mechanics of append](https://go.dev/blog/slices)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/zh/glossary.md)
- [Rune](/type/Rune.md)
- [String](/type/String.md)
