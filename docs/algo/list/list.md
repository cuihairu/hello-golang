# Linked List

A linked list is a linear data structure that chains scattered memory blocks together through pointers. Each node stores data plus a pointer to its successor (and possibly its predecessor); insertions and deletions only require changing pointers, without moving any elements.

### Classification of linked lists

1. **Singly linked list**: each node has only one `next` pointer, so traversal can only go from head to tail.
2. **Doubly linked list**: each node holds both `prev` and `next`, allowing traversal in both directions.
3. **Circular linked list**: the tail node's `next` points back to the head node, forming a loop.

### Linked list vs. array

| Operation | Array | Linked list |
| ---- | ---- | ---- |
| Random access | $O(1)$ | $O(n)$ |
| Insert/delete at head | $O(n)$ | $O(1)$ |
| Insert/delete after a known node | $O(n)$ | $O(1)$ |
| Memory | contiguous | scattered, with extra pointer overhead |

### Code example (implemented in Go)

Below I use the Go standard library `container/list` to demonstrate common doubly linked list operations, and also show how to reverse a hand-written singly linked list:

```go
package main

import (
	"container/list"
	"fmt"
)

// ListNode singly linked list node
type ListNode struct {
	Val  int
	Next *ListNode
}

// reverse reverses a singly linked list
func reverse(head *ListNode) *ListNode {
	var prev *ListNode
	for head != nil {
		head.Next, prev, head = prev, head, head.Next
	}
	return prev
}

func printChain(head *ListNode) {
	for p := head; p != nil; p = p.Next {
		fmt.Printf("%d -> ", p.Val)
	}
	fmt.Println("nil")
}

func main() {
	// standard library doubly linked list
	l := list.New()
	e2 := l.PushBack(2)      // [2]
	l.PushFront(1)           // [1 2]
	l.InsertBefore(0, e2)    // [1 0 2]
	l.PushBack(3)            // [1 0 2 3]
	l.Remove(l.Front().Next()) // remove 0 -> [1 2 3]

	for e := l.Front(); e != nil; e = e.Next() {
		fmt.Printf("%d ", e.Value)
	}
	fmt.Println()

	// hand-written singly linked list, then reverse it
	head := &ListNode{1, &ListNode{2, &ListNode{3, nil}}}
	printChain(head)
	printChain(reverse(head))
}
```

Output:

```text
1 2 3 
1 -> 2 -> 3 -> nil
3 -> 2 -> 1 -> nil
```

### Complexity analysis

- **Search**: $O(n)$, you have to walk the pointers one by one.
- **Insert/delete at head**: $O(1)$.
- **Insert/delete after a given position**: $O(1)$ (when you already hold that node's pointer).

### Summary

A linked list trades random access for flexible insertion and deletion. When I debug composite structures like skip lists and LRU caches, I also reach for these basics — singly linked list reversal and the fast/slow pointer technique.

## References

- [Linked list · Wikipedia](https://en.wikipedia.org/wiki/Linked_list)


## Sibling pages

- [SkipList](/algo/list/SkipList.md)
- [DynamicArray](/algo/list/DynamicArray.md)
- [HashLinkedList](/algo/list/HashLinkedList.md)
- [Stack](/algo/list/Stack.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Stack](/algo/list/Stack.md)
