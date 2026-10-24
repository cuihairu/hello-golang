### Common Data Structures

Lists, stacks, queues, sets, and maps — five structures, each rewritten below with generics: swap the type parameter and the same code serves every element type.

#### 5.1 List

A list is a linear structure. It holds any number of elements, and append, delete, and index access all happen on the underlying slice.

**Generic list implementation**:
```go
type List[T any] struct {
    items []T
}

func (l *List[T]) Add(item T) {
    l.items = append(l.items, item)
}

func (l *List[T]) Remove(index int) {
    if index >= 0 && index < len(l.items) {
        l.items = append(l.items[:index], l.items[index+1:]...)
    }
}

func (l *List[T]) Get(index int) T {
    return l.items[index]
}

func (l *List[T]) Size() int {
    return len(l.items)
}
```

Both read and write go through the `items` slice: `Add` appends, `Remove` splices out by index, `Get` reads by index, and `Size` returns the length.

#### 5.2 Stack

A stack is a last-in-first-out (LIFO, Last In First Out) structure, with only two actions: push and pop.

**Generic stack implementation**:
```go
type Stack[T any] struct {
    items []T
}

func (s *Stack[T]) Push(item T) {
    s.items = append(s.items, item)
}

func (s *Stack[T]) Pop() T {
    if len(s.items) == 0 {
        var zero T
        return zero // return the zero value
    }
    item := s.items[len(s.items)-1]
    s.items = s.items[:len(s.items)-1]
    return item
}

func (s *Stack[T]) Peek() T {
    if len(s.items) == 0 {
        var zero T
        return zero // return the zero value
    }
    return s.items[len(s.items)-1]
}

func (s *Stack[T]) Size() int {
    return len(s.items)
}
```

In this example, the `Stack` struct implements a general-purpose stack that can store data of any type, and provides methods for pushing, popping, peeking at the top element, and getting the size.

#### 5.3 Queue

A queue is a first-in-first-out (FIFO, First In First Out) structure, operated at both ends: enqueue to go in, dequeue to come out.

**Generic queue implementation**:
```go
type Queue[T any] struct {
    items []T
}

func (q *Queue[T]) Enqueue(item T) {
    q.items = append(q.items, item)
}

func (q *Queue[T]) Dequeue() T {
    if len(q.items) == 0 {
        var zero T
        return zero // return the zero value
    }
    item := q.items[0]
    q.items = q.items[1:]
    return item
}

func (q *Queue[T]) Peek() T {
    if len(q.items) == 0 {
        var zero T
        return zero // return the zero value
    }
    return q.items[0]
}

func (q *Queue[T]) Size() int {
    return len(q.items)
}
```

In this example, the `Queue` struct implements a general-purpose queue that can store data of any type, and provides methods for enqueueing, dequeueing, peeking at the front element, and getting the size.

#### 5.4 Set

A set stores no duplicates. It has only three operations — add, remove, and check for presence — and the element type is limited to `comparable`.

**Generic set implementation**:
```go
type Set[T comparable] struct {
    items map[T]struct{}
}

func NewSet[T comparable]() *Set[T] {
    return &Set[T]{items: make(map[T]struct{})}
}

func (s *Set[T]) Add(item T) {
    s.items[item] = struct{}{}
}

func (s *Set[T]) Remove(item T) {
    delete(s.items, item)
}

func (s *Set[T]) Contains(item T) bool {
    _, exists := s.items[item]
    return exists
}

func (s *Set[T]) Size() int {
    return len(s.items)
}
```

The underlying structure of `Set` is `map[T]struct{}`, which uses the map's keys for deduplication; the value is always an empty struct. `Add`, `Remove`, `Contains`, and `Size` each do one thing.

#### 5.5 Map

A map stores key-value pairs and looks values up by key. The key must be `comparable`; the value can be anything.

**Generic map implementation**:
```go
type Map[K comparable, V any] struct {
    items map[K]V
}

func NewMap[K comparable, V any]() *Map[K, V] {
    return &Map[K, V]{items: make(map[K]V)}
}

func (m *Map[K, V]) Put(key K, value V) {
    m.items[key] = value
}

func (m *Map[K, V]) Get(key K) (V, bool) {
    value, exists := m.items[key]
    return value, exists
}

func (m *Map[K, V]) Remove(key K) {
    delete(m.items, key)
}

func (m *Map[K, V]) Size() int {
    return len(m.items)
}
```

In this example, the `Map` struct implements a general-purpose map that can store keys of any comparable type and values of any type, and provides methods for adding, looking up, deleting, and getting the size.

#### 5.6 Summary

All five structures share one approach: a slice or map as the container, with generic parameters fixing the element type. The lists, stacks, and queues all sit on `[]T` underneath, and only differ in where items enter and leave; sets and maps lean on `map`, so both `T` and `K` must satisfy `comparable`.

## References

- [Go Official Documentation · Getting started with generics (external link)](https://go.dev/doc/tutorial/generics)
- [Official blog · An Introduction To Generics](https://go.dev/blog/intro-generics)
- [Official blog · When To Use Generics](https://go.dev/blog/when-generics)
- [Language specification · Type parameter declarations](https://go.dev/ref/spec#Type_parameter_declarations)


## Sibling pages

- [Constraints](/generics/Constraints.md)
- [Generics](/generics/Generics.md)
- [Advanced](/generics/Advanced.md)
- [Performance](/generics/Performance.md)
- [Syntax](/generics/Syntax.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Performance](/generics/Performance.md)
- [Syntax](/generics/Syntax.md)
