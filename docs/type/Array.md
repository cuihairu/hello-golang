
> Perspective: this page records the semantics of arrays and slices in Go; for contiguous storage, random access, and complexity analysis of the array data structure, see the [array data structure notes](/zh/algo/array/Array.md).
In Go, an array has a fixed length and a single element type, while a slice can grow in length; the two differ in behavior in several respects.

### Array

An array is a fixed-length data structure; you must specify the length when declaring one. The length is part of the type, so `[5]int` and `[10]int` are two different types. Here are some properties of arrays:

- **Fixed length**: the length must be specified when declaring an array.
- **Passed by value**: when passed as a function argument, the array is copied in its entirety.
- **Performance optimization**: because the length is fixed, the compiler can optimize accordingly.

### Declaring and initializing an array

```go
package main

import "fmt"

func main() {
    var arr1 [5]int              // declares an array of 5 int elements, initialized to the zero value by default
    arr2 := [3]int{1, 2, 3}       // declares and initializes an array of 3 int elements
    arr3 := [...]int{1, 2, 3, 4}  // infers the array length as 4 from the initial values

    fmt.Println(arr1, arr2, arr3)
}
```

### Array usage example

```go
package main

import "fmt"

func main() {
    var arr [3]int
    arr[0] = 10
    arr[1] = 20
    arr[2] = 30

    fmt.Println("Array:", arr)      // prints the whole array
    fmt.Println("Length:", len(arr)) // prints the array length
}
```

### The difference between a slice and an array

A slice is a reference to a contiguous segment of an array; its length is variable and it can grow on demand. Compared with an array, a slice has these properties:

- **Dynamic length**: a slice's length can change at run time.
- **Reference type**: a slice references an array, so changes to the underlying array are reflected in the slice.
- **Efficient passing**: when passed as a function argument, only the slice reference is copied, not the whole data.

### Comparing an array and a slice in an example

```go
package main

import "fmt"

func main() {
    // array example
    arr := [3]int{1, 2, 3}
    modifyArray(arr)
    fmt.Println("Array after modifyArray:", arr)

    // slice example
    slice := []int{1, 2, 3}
    modifySlice(slice)
    fmt.Println("Slice after modifySlice:", slice)
}

func modifyArray(arr [3]int) {
    arr[0] = 100
}

func modifySlice(slice []int) {
    slice[0] = 100
}
```

In the example above, the `modifyArray` function cannot modify the array in `main`, because an array is passed by value as an argument. By contrast, `modifySlice` can modify the slice's elements, because a slice is passed by reference.

### Summary

Arrays and slices are common data structures in Go, each with its own properties and use cases:

- **Arrays** are fixed-length data structures, suited to scenarios where the size is fixed and access is sequential.
- **Slices** are dynamic-length reference types that support growth and slicing, suited to flexible data-processing needs.

The length is written into the type, so `[3]int` and `[5]int` are two types and are mutually incompatible; whenever the length changes, just use a slice.

## References

- [Language spec · Types](https://go.dev/ref/spec#Types)
- [Language spec · Array types](https://go.dev/ref/spec#Array_types)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [TypeInference](/type/TypeInference.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Assertion](/type/Assertion.md)
