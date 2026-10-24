# Double-Ended Queue
A double-ended queue (Deque) is a data structure that allows insertion and deletion at both ends, and it can be built on an array.

### Basic Operations of a Double-Ended Queue

Insertion, deletion, and access each come in a front and a back variant: insertion and deletion change the queue's contents, while access only reads the elements at the two ends.

### Array-Based Double-Ended Queue

An array implementation maintains two indexes, one pointing to the front of the queue and one to the back: the struct holds a fixed-length array, these two indexes, and an element count; insertion and deletion move the corresponding index according to the direction; full and empty queues are handled specially to avoid going out of the array bounds.

### Example Code

Below is a Go implementation with a fixed capacity:

```go
package main

import (
    "fmt"
)

type Deque struct {
    data       []int
    front, back int
    size       int
}

func NewDeque(capacity int) *Deque {
    return &Deque{
        data:  make([]int, capacity),
        front: -1,
        back: 0,
        size:  0,
    }
}

func (dq *Deque) IsEmpty() bool {
    return dq.size == 0
}

func (dq *Deque) IsFull() bool {
    return dq.size == len(dq.data)
}

func (dq *Deque) AddFront(value int) {
    if dq.IsFull() {
        panic("Deque is full")
    }
    if dq.IsEmpty() {
        dq.front = 0
        dq.back = 0
    } else {
        dq.front = (dq.front - 1 + len(dq.data)) % len(dq.data)
    }
    dq.data[dq.front] = value
    dq.size++
}

func (dq *Deque) AddBack(value int) {
    if dq.IsFull() {
        panic("Deque is full")
    }
    if dq.IsEmpty() {
        dq.front = 0
        dq.back = 0
    } else {
        dq.back = (dq.back + 1) % len(dq.data)
    }
    dq.data[dq.back] = value
    dq.size++
}

func (dq *Deque) RemoveFront() int {
    if dq.IsEmpty() {
        panic("Deque is empty")
    }
    value := dq.data[dq.front]
    dq.front = (dq.front + 1) % len(dq.data)
    dq.size--
    if dq.IsEmpty() {
        dq.front = -1
        dq.back = 0
    }
    return value
}

func (dq *Deque) RemoveBack() int {
    if dq.IsEmpty() {
        panic("Deque is empty")
    }
    value := dq.data[dq.back]
    dq.back = (dq.back - 1 + len(dq.data)) % len(dq.data)
    dq.size--
    if dq.IsEmpty() {
        dq.front = -1
        dq.back = 0
    }
    return value
}

func (dq *Deque) Front() int {
    if dq.IsEmpty() {
        panic("Deque is empty")
    }
    return dq.data[dq.front]
}

func (dq *Deque) Back() int {
    if dq.IsEmpty() {
        panic("Deque is empty")
    }
    return dq.data[dq.back]
}

func main() {
    deque := NewDeque(5)

    deque.AddBack(1)
    deque.AddBack(2)
    deque.AddFront(3)
    deque.AddFront(4)
    fmt.Println("Front:", deque.Front()) // Output: Front: 4
    fmt.Println("Back:", deque.Back())   // Output: Back: 2

    fmt.Println("Removed from front:", deque.RemoveFront()) // Output: Removed from front: 4
    fmt.Println("Removed from back:", deque.RemoveBack())   // Output: Removed from back: 2
}
```

### Code Walkthrough

`Deque` uses the slice `data` for storage, with `front` and `back` as the two end indexes and `size` tracking the current element count, which is also what distinguishes an "empty queue" from a "full queue." Every index move is written as `+ len(dq.data)` followed by a modulo, so wrapping around the array boundary never goes out of bounds.

`AddFront`/`AddBack` insert at the two ends, `RemoveFront`/`RemoveBack` delete at the two ends and return the element, and `Front`/`Back` are read-only. Inserting into a full queue, and deleting from or reading an empty queue, all panic; you can check with `IsFull`/`IsEmpty` before calling.

### Complexity

Insertion, deletion, and access at both ends are all O(1): a little index arithmetic plus a modulo, with no elements moved. Lookup by value is O(n), since you have to scan from one end to the other. Capacity is fixed at construction, and no memory is allocated during operations.

### Summary

Capacity is fixed at creation and never grows afterwards; insertion, deletion, and access at both ends are all a constant number of index operations.

## References

- [Double-ended queue · Wikipedia](https://en.wikipedia.org/wiki/Double-ended_queue)

## Sibling pages

- [DynamicArray](/algo/array/DynamicArray.md)
- [Array](/algo/array/Array.md)
- [CircularBuffer](/algo/array/CircularBuffer.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Array](/algo/array/Array.md)
- [CircularBuffer](/algo/array/CircularBuffer.md)
