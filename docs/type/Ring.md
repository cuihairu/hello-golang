`container/ring` is a package in the Go standard library that provides an implementation of a circular linked list (ring). A circular linked list is a data structure in which the last node points to the first node, forming a loop.

### Basic Usage

1. **Creating a ring**

   ```go
   package main

   import (
       "container/ring"
       "fmt"
   )

   func main() {
       // create a ring containing 5 elements
       r := ring.New(5)

       // assign a value to each element
       for i := 0; i < r.Len(); i++ {
           r.Value = i
           r = r.Next()
       }

       // iterate over and print the ring's elements
       r.Do(func(p interface{}) {
           fmt.Println(p.(int))
       })
   }
   ```

2. **Length of the ring**

   ```go
   length := r.Len()
   fmt.Println("Length of ring:", length)
   ```

3. **Iterating over the ring**

   ```go
   r.Do(func(p interface{}) {
       fmt.Println(p)
   })
   ```

4. **Moving the pointer**

   ```go
   // move forward by n positions
   r = r.Move(n)
   
   // get the next element
   next := r.Next()
   
   // get the previous element
   prev := r.Prev()
   ```

5. **Linking two rings together**

   ```go
   r2 := ring.New(3)
   r.Link(r2)
   ```

6. **Deleting elements from the ring**

   ```go
   r.Unlink(3) // delete the 3 elements after the current pointer
   ```

### Underlying Principles

The ring in the `container/ring` package is implemented by the `ring.Ring` struct, defined as follows:

```go
type Ring struct {
    next, prev *Ring
    Value      interface{} // a value of any type
}
```

- `next` and `prev` point to the next and previous elements in the ring, forming a doubly-linked structure.
- `Value` stores a value of any type.

The main characteristic of a ring is that its last element points back to the first element, making it circular.

### A Few Important Methods

1. **New(n int) *Ring**

   Creates a ring containing n elements, each with a value of nil.

2. **Len() int**

   Returns the number of elements in the ring.

3. **Link(s *Ring) *Ring**

   Inserts the ring `s` after the current ring and returns the next element of the new ring.

4. **Unlink(n int) *Ring**

   Removes n elements from the current ring and returns the removed elements.

5. **Move(n int) *Ring**

   Moves the current ring by n positions and returns the moved ring.

6. **Next() *Ring**

   Returns the next element of the ring.

7. **Prev() *Ring**

   Returns the previous element of the ring.

8. **Do(f func(interface{}))**

   Iterates over every element in the ring and applies the function f to each element.

### Explanation of the Example

The example uses `ring.New(5)` to create a ring of 5 elements, assigns values, then uses `Do` to iterate and print; inside `Do` it walks one loop along the `next` pointers, handing each element to the function in turn.

### Application Scenarios

Use it when you need circular access to data:
- fixed-size buffers
- cyclic scheduling or round-robin polling

Joining head to tail is its biggest convenience: after reaching the end, another `Next()` brings you back to the start, with none of the boundary checks a plain linked list requires.

## References

- [Language Specification · Types](https://go.dev/ref/spec#Types)
- [container/ring standard library](https://pkg.go.dev/container/ring)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [Pointer](/type/Pointer.md)
- [Rune](/type/Rune.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Pointer](/type/Pointer.md)
- [Rune](/type/Rune.md)
