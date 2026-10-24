# Stack

A stack is a last-in-first-out (LIFO) linear data structure in which insertion and deletion are only allowed at the top. When implemented with a linked list, the head serves as the top, so both push and pop are $O(1)$.

### Core operations

1. **Push**: push an element onto the top.
2. **Pop**: pop the top element.
3. **Peek**: inspect the top element without removing it.
4. **IsEmpty / Len**: check emptiness and get the length.

### Code example (implemented in Go)

```go
package main

import "fmt"

// stackNode linked list node
type stackNode struct {
	val  int
	next *stackNode
}

// LinkedStack stack based on a singly linked list
type LinkedStack struct {
	top *stackNode
	n   int
}

// Push push onto the stack
func (s *LinkedStack) Push(v int) {
	s.top = &stackNode{val: v, next: s.top}
	s.n++
}

// Pop pop from the stack
func (s *LinkedStack) Pop() (int, bool) {
	if s.top == nil {
		return 0, false
	}
	v := s.top.val
	s.top = s.top.next
	s.n--
	return v, true
}

// Peek inspect the top
func (s *LinkedStack) Peek() (int, bool) {
	if s.top == nil {
		return 0, false
	}
	return s.top.val, true
}

// Len number of elements in the stack
func (s *LinkedStack) Len() int { return s.n }

func main() {
	s := &LinkedStack{}
	for _, v := range []int{1, 2, 3} {
		s.Push(v)
	}
	fmt.Println("len:", s.Len())

	if v, ok := s.Peek(); ok {
		fmt.Println("peek:", v)
	}
	for {
		v, ok := s.Pop()
		if !ok {
			break
		}
		fmt.Println("pop:", v)
	}
	_, ok := s.Pop()
	fmt.Println("empty pop ok:", ok)
}
```

Output:

```text
len: 3
peek: 3
pop: 3
pop: 2
pop: 1
empty pop ok: false
```

### Complexity analysis

- **Push / Pop / Peek**: $O(1)$.
- **Space**: $O(n)$, one extra pointer per node.

### Use cases

- Function call stacks, bracket matching, expression evaluation.
- Depth-first search (DFS), browser back/forward navigation, and similar.

### Summary

A linked-list stack needs no growth and every operation only touches the top pointer. Compared with a slice-based stack, it gives up cache locality in exchange for stable $O(1)$ performance.

## References

- [Stack (abstract data type) · Wikipedia](https://en.wikipedia.org/wiki/Stack_%28abstract_data_type%29))


## Sibling pages

- [SkipList](/algo/list/SkipList.md)
- [DynamicArray](/algo/list/DynamicArray.md)
- [HashLinkedList](/algo/list/HashLinkedList.md)
- [list](/algo/list/list.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [list](/algo/list/list.md)
