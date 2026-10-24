# Stack

A stack is a last-in, first-out (LIFO) linear data structure: every insertion (push) and every deletion (pop) happens at the top. This page implements a generic stack with Go slices and uses it to solve the classic bracket-matching problem.

### Core operations

1. **Push**: the element enters the stack and becomes the new top.
2. **Pop**: pop and return the top element.
3. **Peek**: look at the top without popping.
4. **IsEmpty**: check whether the stack is empty.

### Algorithm steps (bracket matching)

1. Scan the string from left to right:
   - On a left bracket `(`, `[`, or `{`, push it.
   - On a right bracket, if the stack is empty or the top is not the matching left bracket, it does not match; otherwise pop the top.
2. After the scan, an empty stack means every bracket is correctly closed.

### Code example (Go implementation)

```go
package main

import "fmt"

// Stack is an int stack backed by a slice
type Stack struct {
	items []int
}

// Push adds to the stack
func (s *Stack) Push(v int) {
	s.items = append(s.items, v)
}

// Pop removes from the stack
func (s *Stack) Pop() (int, bool) {
	if len(s.items) == 0 {
		return 0, false
	}
	n := len(s.items) - 1
	v := s.items[n]
	s.items = s.items[:n]
	return v, true
}

// Peek looks at the top
func (s *Stack) Peek() (int, bool) {
	if len(s.items) == 0 {
		return 0, false
	}
	return s.items[len(s.items)-1], true
}

// IsEmpty reports whether it is empty
func (s *Stack) IsEmpty() bool { return len(s.items) == 0 }

// isMatched reports whether the bracket string matches
func isMatched(s string) bool {
	pairs := map[byte]byte{')': '(', ']': '[', '}': '{'}
	stack := make([]byte, 0, len(s))
	for i := 0; i < len(s); i++ {
		c := s[i]
		switch c {
		case '(', '[', '{':
			stack = append(stack, c)
		case ')', ']', '}':
			if len(stack) == 0 || stack[len(stack)-1] != pairs[c] {
				return false
			}
			stack = stack[:len(stack)-1]
		}
	}
	return len(stack) == 0
}

func main() {
	s := &Stack{}
	s.Push(1)
	s.Push(2)
	s.Push(3)
	if v, ok := s.Peek(); ok {
		fmt.Println("peek:", v)
	}
	for !s.IsEmpty() {
		v, _ := s.Pop()
		fmt.Println("pop:", v)
	}

	fmt.Println("()[]{} ->", isMatched("()[]{}"))
	fmt.Println("([)] ->", isMatched("([)]"))
	fmt.Println("{[()]} ->", isMatched("{[()]}"))
}
```

Running output:

```text
peek: 3
pop: 3
pop: 2
pop: 1
()[]{} -> true
([)] -> false
{[()]} -> true
```

### Complexity analysis

- **Push / Pop / Peek**: amortized $O(1)$ (after amortizing slice growth).
- **Space**: $O(n)$.

### Use cases

- The function call stack; explicit rewrites of recursion.
- Bracket matching, expression evaluation, depth-first search (DFS), undo operations.

### Summary

The stack has the simplest rules, but it is the skeleton underneath expression evaluation, DFS, and recursion. A slice-based stack is the least code, and with the top index at `len-1` it covers every operation.

## References

- [Stack (abstract data type) · Wikipedia](https://en.wikipedia.org/wiki/Stack_%28abstract_data_type%29))

## Sibling pages

- [Graph](/algo/Graph.md)
- [Inventory](/algo/Inventory.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Graph](/algo/Graph.md)
