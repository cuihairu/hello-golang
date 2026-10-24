# Dynamic Array

A dynamic array builds on a fixed-length array by adding "automatic growth": when capacity runs out, it allocates a larger block of memory and copies the old elements over, so it supports unlimited appending. Go's slice is implemented with exactly this structure underneath.

### Structure definition

1. **data**: the underlying array, with capacity `cap`.
2. **size**: the current number of elements, `size <= cap`.
3. **Growth strategy**: when capacity runs out, the new capacity is taken as 2x the old one; amortized, each `Append` costs $O(1)$.

### Algorithm steps

1. **Append**: if `size == cap`, grow by 2x first, then write at position `size`.
2. **Insert(i)**: grow first if full, then shift `[i, size)` one slot to the right as a whole, and write the new element.
3. **Remove(i)**: shift `[i+1, size)` one slot to the left as a whole; once the element count drops, you can shrink the capacity to save memory.

### Code example (implemented in Go)

```go
package main

import "fmt"

// DynamicArray automatically growable dynamic array
type DynamicArray struct {
	data []int
	size int
}

// NewDynamicArray create a dynamic array with the given initial capacity
func NewDynamicArray(capacity int) *DynamicArray {
	if capacity < 1 {
		capacity = 1
	}
	return &DynamicArray{data: make([]int, capacity)}
}

// Append append an element, growing by 2x when capacity runs out
func (a *DynamicArray) Append(v int) {
	if a.size == len(a.data) {
		a.resize(a.size * 2)
	}
	a.data[a.size] = v
	a.size++
}

// Insert insert v at index i
func (a *DynamicArray) Insert(i, v int) bool {
	if i < 0 || i > a.size {
		return false
	}
	if a.size == len(a.data) {
		a.resize(a.size * 2)
	}
	copy(a.data[i+1:a.size+1], a.data[i:a.size])
	a.data[i] = v
	a.size++
	return true
}

// Remove delete the element at index i
func (a *DynamicArray) Remove(i int) (int, bool) {
	if i < 0 || i >= a.size {
		return 0, false
	}
	v := a.data[i]
	copy(a.data[i:a.size-1], a.data[i+1:a.size])
	a.size--
	a.data[a.size] = 0
	// shrink by half when the element count drops to 1/4 of capacity
	if a.size > 0 && a.size <= len(a.data)/4 {
		a.resize(len(a.data) / 2)
	}
	return v, true
}

// resize migrate to a new array with capacity newCap
func (a *DynamicArray) resize(newCap int) {
	newData := make([]int, newCap)
	copy(newData, a.data[:a.size])
	a.data = newData
}

// Len current number of elements
func (a *DynamicArray) Len() int { return a.size }

func main() {
	a := NewDynamicArray(2)
	for i := 1; i <= 6; i++ {
		a.Append(i * 10)
	}
	fmt.Println("len:", a.Len(), "cap:", len(a.data))

	a.Insert(2, 55)
	fmt.Println("after insert:", a.data[:a.size])

	v, ok := a.Remove(0)
	fmt.Println("removed:", v, ok)
	fmt.Println("after remove:", a.data[:a.size])
}
```

Output:

```text
len: 6 cap: 8
after insert: [10 20 55 30 40 50 60]
removed: 10 true
after remove: [20 55 30 40 50 60]
```

### Complexity analysis

- **Append at tail**: amortized $O(1)$ (the total cost of growth is spread across each append).
- **Insert/delete in the middle**: $O(n)$, elements must be moved.
- **Access by index**: $O(1)$.

### Summary

A dynamic array still allows $O(1)$ access by index, and doubling growth lets it keep appending. Once you understand it, you understand where Go slice `len/cap` comes from, and why preallocating capacity reduces copies when `append` is called frequently.

## References

- [Dynamic array · Wikipedia](https://en.wikipedia.org/wiki/Dynamic_array)

## Sibling pages

- [SkipList](/algo/list/SkipList.md)
- [HashLinkedList](/algo/list/HashLinkedList.md)
- [Queue](/algo/list/Queue.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [HashLinkedList](/algo/list/HashLinkedList.md)
- [Queue](/algo/list/Queue.md)
- [SinglyLinkedList](/algo/list/SinglyLinkedList.md)
- [Stack](/algo/list/Stack.md)
- [list](/algo/list/list.md)
