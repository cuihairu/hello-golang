# Queue

A queue is a first-in-first-out (FIFO) linear data structure: elements enter at the rear (enqueue) and leave from the front (dequeue). Implemented with a singly linked list carrying a tail pointer, both operations run in $O(1)$.

### Core operations

1. **Enqueue**: append an element at the rear.
2. **Dequeue**: remove and return the front element.
3. **Front**: inspect the front element without removing it.

### Implementation notes

- Maintain both `head` and `tail` pointers: dequeue goes through `head`, enqueue goes through `tail`.
- With only a head pointer, enqueue must traverse to the tail, degrading to $O(n)$.
- When the queue is empty, `head == nil`; after enqueuing, both `head` and `tail` must point at the new node.

### Code example (implemented in Go)

```go
package main

import "fmt"

// qNode linked list node
type qNode struct {
	val  int
	next *qNode
}

// LinkedQueue queue based on a singly linked list
type LinkedQueue struct {
	head *qNode
	tail *qNode
	n    int
}

// Enqueue enqueue
func (q *LinkedQueue) Enqueue(v int) {
	node := &qNode{val: v}
	if q.tail == nil {
		q.head = node
		q.tail = node
	} else {
		q.tail.next = node
		q.tail = node
	}
	q.n++
}

// Dequeue dequeue
func (q *LinkedQueue) Dequeue() (int, bool) {
	if q.head == nil {
		return 0, false
	}
	v := q.head.val
	q.head = q.head.next
	if q.head == nil {
		q.tail = nil
	}
	q.n--
	return v, true
}

// Len queue length
func (q *LinkedQueue) Len() int { return q.n }

func main() {
	q := &LinkedQueue{}
	for _, v := range []int{1, 2, 3} {
		q.Enqueue(v)
	}
	fmt.Println("len:", q.Len())

	v, _ := q.Dequeue()
	fmt.Println("dequeue:", v)
	q.Enqueue(4)

	for {
		v, ok := q.Dequeue()
		if !ok {
			break
		}
		fmt.Println("dequeue:", v)
	}
	_, ok := q.Dequeue()
	fmt.Println("empty dequeue ok:", ok)
}
```

Output:

```text
len: 3
dequeue: 1
dequeue: 2
dequeue: 3
dequeue: 4
empty dequeue ok: false
```

### Complexity analysis

- **Enqueue / Dequeue**: $O(1)$.
- **Space**: $O(n)$.

### Use cases

- Task scheduling, message buffering, breadth-first search (BFS).
- Waiting queues in producer-consumer models.

### Summary

A linked-list queue uses head and tail pointers to make both enqueue and dequeue $O(1)$, and it avoids the "false overflow" problem that a circular array needs to handle. If you need a fixed capacity, you can switch to a circular buffer instead.

## References

- [Queue (abstract data type) · Wikipedia](https://en.wikipedia.org/wiki/Queue_%28abstract_data_type%29))

## Sibling pages

- [SkipList](/algo/list/SkipList.md)
- [DynamicArray](/algo/list/DynamicArray.md)
- [HashLinkedList](/algo/list/HashLinkedList.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [DynamicArray](/algo/list/DynamicArray.md)
- [HashLinkedList](/algo/list/HashLinkedList.md)
- [SinglyLinkedList](/algo/list/SinglyLinkedList.md)
