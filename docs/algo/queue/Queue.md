# Queue

A queue is a first-in, first-out (FIFO) linear data structure: elements may only be enqueued at the tail and dequeued from the head. This page implements a queue two ways — with a slice and with a circular array — and shows its typical use in breadth-first search.

### Core operations

1. **Enqueue**: add the element at the tail.
2. **Dequeue**: remove and return the head element.
3. **Peek**: look at the head element.

### Implementation approaches

1. **Slice queue**: `enqueue` uses `append`, `dequeue` takes `q[0]` then `q = q[1:]`. Simple and direct, but `q[1:]` only moves the slice header; the underlying array is never reused.
2. **Circular slice queue**: a `head` index plus a `count`, combined with modulo arithmetic, reuses a fixed array; memory stays constant.

### Code example (Go implementation)

```go
package main

import "fmt"

// IntQueue is a queue backed by a circular slice
type IntQueue struct {
	data  []int
	head  int
	count int
}

// NewIntQueue creates a queue with capacity n; it grows automatically when full
func NewIntQueue(n int) *IntQueue {
	return &IntQueue{data: make([]int, n)}
}

// Enqueue adds to the queue
func (q *IntQueue) Enqueue(v int) {
	if q.count == len(q.data) { // grow when full
		grown := make([]int, len(q.data)*2)
		for i := 0; i < q.count; i++ {
			grown[i] = q.data[(q.head+i)%len(q.data)]
		}
		q.data = grown
		q.head = 0
	}
	q.data[(q.head+q.count)%len(q.data)] = v
	q.count++
}

// Dequeue removes from the queue
func (q *IntQueue) Dequeue() (int, bool) {
	if q.count == 0 {
		return 0, false
	}
	v := q.data[q.head]
	q.head = (q.head + 1) % len(q.data)
	q.count--
	return v, true
}

// Len returns the queue length
func (q *IntQueue) Len() int { return q.count }

func main() {
	q := NewIntQueue(2)
	for i := 1; i <= 5; i++ { // deliberately exceed the initial capacity to trigger growth
		q.Enqueue(i * 10)
	}
	fmt.Println("len:", q.Len())

	q.Dequeue() // pop 10
	v, _ := q.Dequeue()
	fmt.Println("second:", v)

	for {
		v, ok := q.Dequeue()
		if !ok {
			break
		}
		fmt.Println("dequeue:", v)
	}
}
```

Running output:

```text
len: 5
second: 20
dequeue: 30
dequeue: 40
dequeue: 50
```

### Complexity analysis

- **Enqueue / Dequeue**: amortized $O(1)$.
- **Space**: $O(\text{capacity})$ for the circular implementation; the slice implementation can be as long as the underlying array.

### Use cases

- Breadth-first search (BFS), level-order traversal.
- Task queues, message buffering, print spooling.

### Summary

The key to a queue is "operate on both ends — out the head, in the tail." The circular-array implementation buys $O(1)$ enqueue/dequeue on fixed memory through modulo arithmetic, the same idea behind the standard library's `container/ring` and the internal buffering of channels.

## References

- [Queue (abstract data type) · Wikipedia](https://en.wikipedia.org/wiki/Queue_%28abstract_data_type%29))

## Sibling pages

- [Graph](/algo/Graph.md)
- [Inventory](/algo/Inventory.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Graph](/algo/Graph.md)
