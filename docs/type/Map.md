In Go, `map` is used to store key-value pairs. Insertion, deletion, and lookup are all constant-time operations. Here I first note down the usage, then look at the underlying implementation: the `hmap` struct, growth, and hashing.

### The Basic Concept of `map`

`map` is a collection in which every element is a key-value pair. Keys are unique, while values can be any type of data. `map` has the following characteristics:

- **Unordered**: the elements in a `map` are stored without order, so the iteration order may differ from one traversal to the next.
- **Dynamic growth**: a `map` can grow and shrink at runtime; there is no need to specify a capacity in advance.

### The Underlying Structure and Principles of `map`

In Go, `map` is implemented by an `hmap` struct defined in the `runtime/map.go` file. The `hmap` structure is as follows:

```go
type hmap struct {
    count     int            // number of elements in the map
    flags     uint8          // state flag
    B         uint8          // the size of the hash table buckets (2^B)
    noverflow uint16         // number of overflow buckets
    hash0     uint32         // hash seed
    buckets    unsafe.Pointer // pointer holding the buckets
    oldbuckets unsafe.Pointer // old buckets used to migrate data during growth
    nevacuate  uintptr        // number of elements to migrate
}
```

The fields of the `hmap` struct include:
- `count`: the number of key-value pairs in the `map`.
- `B`: the bucket size of the hash table; the actual capacity is `2^B`.
- `buckets`: the pointer holding the buckets, each of which stores a portion of the key-value pairs.
- `oldbuckets`: the old buckets used to migrate data during growth.
- `nevacuate`: after growth, the number of elements to migrate.

### `map` Optimizations

The `map` implementation does several things at key points:

1. **Hashing algorithm**: Go implements `map` using a hashing algorithm called `HashMap`, which guarantees fast lookup and insertion of elements.

2. **Growth mechanism**: when the number of elements in a `map` increases, Go automatically expands the `map`'s capacity to keep operations efficient. During growth, data is re-hashed and relocated so that elements are evenly distributed across the new buckets.

3. **Concurrency safety**: for concurrent read/write, Go uses locking to guarantee the atomicity of write operations, thereby keeping `map` safe under concurrency.

4. **Deletion optimization**: deleting from Go's `map` does not immediately remove the element; it only marks the bucket as deleted. This is faster.

### Basic Usage and Examples

Basic usage:

```go
package main

import "fmt"

func main() {
    // declare and initialize a map
    var m map[string]int
    m = make(map[string]int)

    // insert key-value pairs
    m["apple"] = 5
    m["banana"] = 2
    m["orange"] = 8

    // access a value in the map
    fmt.Println("Value of apple:", m["apple"]) // Output: Value of apple: 5

    // check whether a key exists
    if value, ok := m["banana"]; ok {
        fmt.Println("Value of banana:", value) // Output: Value of banana: 2
    }

    // delete a key-value pair
    delete(m, "orange")

    // iterate over the map
    for key, value := range m {
        fmt.Println(key, ":", value)
    }
}
```

The example covers six operations: declaration, insertion, value retrieval, existence check, deletion, and iteration. Note that the iteration order of a `map` is not deterministic.

### Notes

- **Concurrency safety**: when using a `map` in a concurrent program, write operations need locking to avoid race conditions.
- **Key uniqueness**: the keys of a `map` must be of a type that supports equality comparison, such as basic types or structs; they cannot be non-comparable types like slices, arrays, or functions.
- **Value type**: the values of a `map` can be any type, including built-in types, structs, and even other `map`s and slices.

### Summary

Two things to watch when using `map`: the key type must be comparable, and concurrent writes require your own locking.

## References

- [Language Specification · Types](https://go.dev/ref/spec#Types)
- [Language Specification · Map types](https://go.dev/ref/spec#Map_types)
- [Official Blog · Go maps in action](https://go.dev/blog/maps)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/zh/glossary.md)
- [Array](/type/Array.md)
- [BaseConv](/type/BaseConv.md)
- [Big](/type/Big.md)
- [Bool](/type/Bool.md)
- [Byte](/type/Byte.md)
- [Complex](/type/Complex.md)
- [CompositeType](/type/CompositeType.md)
- [Conv](/type/Conv.md)
- [Float](/type/Float.md)
- [HtmlTemplate](/type/HtmlTemplate.md)
- [Int](/type/Int.md)
- [Json](/type/Json.md)
- [LinkedList](/type/LinkedList.md)
- [Pointer](/type/Pointer.md)
- [Ring](/type/Ring.md)
- [Rune](/type/Rune.md)
- [String](/type/String.md)
- [Struct](/type/Struct.md)
- [Template](/type/Template.md)
- [Type](/type/Type.md)
