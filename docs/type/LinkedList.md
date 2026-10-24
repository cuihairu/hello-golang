 In Go, the standard library has no dedicated doubly-linked-list type; it is provided by the `container/list` package.

### Overview of the `container/list` Package

This package mainly contains the following structures and functions:

- **`List` structure**: represents a doubly-linked list. It contains pointers to the first and last elements of the list, as well as the list's length.

- **`Element` structure**: represents each element in the list. Every `Element` contains pointers to its previous and next elements, along with a stored value.

- **Methods**: the `List` structure contains a series of methods for operating on a doubly-linked list, such as insertion, deletion, and iteration.

### Basic Operations Example

```go
package main

import (
    "container/list"
    "fmt"
)

func main() {
    // create a new doubly-linked list
    mylist := list.New()

    // insert elements at the tail of the list
    mylist.PushBack(1)
    mylist.PushBack(2)
    mylist.PushBack(3)

    // insert an element at the head of the list
    mylist.PushFront(0)

    // iterate over the list and print each element's value
    for e := mylist.Front(); e != nil; e = e.Next() {
        fmt.Println(e.Value)
    }

    // delete an element from the middle of the list
    second := mylist.Front().Next()
    mylist.Remove(second)

    // iterate again and print
    fmt.Println("After removal:")
    for e := mylist.Front(); e != nil; e = e.Next() {
        fmt.Println(e.Value)
    }
}
```

`list.New()` creates the list, `PushBack`/`PushFront` insert elements, `Front()` combined with `Next()` iterates, and `Remove` deletes.

### Notes

- **Iteration order**: the iteration order of a doubly-linked list is from head to tail; use the `Front()` and `Back()` methods to get the first and last elements respectively.
- **Deletion**: when deleting an element, be careful about whether the list is empty or whether the element exists.
- **Performance considerations**: for frequent insertion and deletion of large amounts of data, a doubly-linked list may be less efficient than an array or slice; choose the appropriate data structure based on the specific situation.

### Summary

`container/list` turns the doubly-linked list into a ready-made container, with corresponding methods for insertion, deletion, and iteration. Two things to note when using it: start iterating from the head or tail node obtained via `Front()` or `Back()`; before deleting, confirm the list is not empty and the element exists.

## References

- [Language Specification · Types](https://go.dev/ref/spec#Types)
- [container/list standard library](https://pkg.go.dev/container/list)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [Json](/type/Json.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Json](/type/Json.md)
