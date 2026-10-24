# Singly Linked List

A singly linked list is the simplest form of linked list: each node contains data and a `next` pointer to its successor, and traversal can only proceed from the head node in the `next` direction.

### Structure definition

1. **Node**: `data` data field + `next` successor pointer.
2. **Head node `head`**: the entry point of the list; `head == nil` means the list is empty.
3. **Tail node**: the node whose `next == nil`.

### Common operations

1. **Insert at head**: point the new node at the old head, then update the head pointer, $O(1)$.
2. **Insert at tail**: follow `next` to the tail node and attach the new node, $O(n)$; maintaining a tail pointer can optimize this to $O(1)$.
3. **Search**: traverse from the head and compare, $O(n)$.
4. **Delete**: find the predecessor of the target node, then set `prev.next = target.next`, $O(n)$.
5. **Reverse**: point each node's `next` at its predecessor one by one, $O(n)$.

### Code example (implemented in Go)

```go
package main

import "fmt"

// Node singly linked list node
type Node struct {
	Val  int
	Next *Node
}

// SinglyLinkedList singly linked list with a head pointer
type SinglyLinkedList struct {
	head *Node
	size int
}

// PushFront insert at head, O(1)
func (s *SinglyLinkedList) PushFront(v int) {
	s.head = &Node{Val: v, Next: s.head}
	s.size++
}

// PushBack insert at tail, O(n)
func (s *SinglyLinkedList) PushBack(v int) {
	n := &Node{Val: v}
	if s.head == nil {
		s.head = n
	} else {
		p := s.head
		for p.Next != nil {
			p = p.Next
		}
		p.Next = n
	}
	s.size++
}

// Remove delete the first node whose value is v
func (s *SinglyLinkedList) Remove(v int) bool {
	if s.head == nil {
		return false
	}
	if s.head.Val == v {
		s.head = s.head.Next
		s.size--
		return true
	}
	p := s.head
	for p.Next != nil && p.Next.Val != v {
		p = p.Next
	}
	if p.Next == nil {
		return false
	}
	p.Next = p.Next.Next
	s.size--
	return true
}

// Contains check whether the value v is present
func (s *SinglyLinkedList) Contains(v int) bool {
	for p := s.head; p != nil; p = p.Next {
		if p.Val == v {
			return true
		}
	}
	return false
}

// Reverse reverse the list
func (s *SinglyLinkedList) Reverse() {
	var prev *Node
	cur := s.head
	for cur != nil {
		cur.Next, prev, cur = prev, cur, cur.Next
	}
	s.head = prev
}

// Print print the list
func (s *SinglyLinkedList) Print() {
	for p := s.head; p != nil; p = p.Next {
		fmt.Printf("%d -> ", p.Val)
	}
	fmt.Println("nil")
}

func main() {
	s := &SinglyLinkedList{}
	s.PushBack(1)
	s.PushBack(2)
	s.PushFront(0)
	s.Print() // 0 -> 1 -> 2 -> nil

	fmt.Println("contains 2:", s.Contains(2))
	s.Remove(1)
	s.Print() // 0 -> 2 -> nil

	s.Reverse()
	s.Print() // 2 -> 0 -> nil
}
```

### Complexity analysis

- **Insert/delete at head**: $O(1)$.
- **Insert at tail / delete by value / search**: $O(n)$.
- **Space**: one extra pointer per node, $O(n)$.

### Summary

A singly linked list has a simple structure and efficient head operations, making it a good fit as the underlying implementation for structures such as stacks and hash bucket chains. Because it does not support moving backwards, deleting a node requires finding its predecessor first — that is the main gap between it and a doubly linked list.

## References

- [Linked list · Wikipedia](https://en.wikipedia.org/wiki/Linked_list)


## Sibling pages

- [SkipList](/algo/list/SkipList.md)
- [DynamicArray](/algo/list/DynamicArray.md)
- [HashLinkedList](/algo/list/HashLinkedList.md)
- [Queue](/algo/list/Queue.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [SkipList](/algo/list/SkipList.md)
