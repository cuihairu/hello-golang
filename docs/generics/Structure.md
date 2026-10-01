### 常见的数据结构

数据结构是程序设计的基础，通过合理选择和使用数据结构，可以大大提高程序的性能和可维护性。在泛型编程的帮助下，我们可以实现更加通用和高效的数据结构。本章将介绍一些常见的数据结构，包括列表、栈、队列、集合和映射，并通过泛型实现这些数据结构。

#### 5.1 列表（List）

列表是一种线性数据结构，可以存储任意数量的元素，并允许对这些元素进行添加、删除和访问操作。使用泛型实现列表，可以使其支持任意类型的数据。

**泛型列表实现**：
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

在这个例子中，`List`结构体实现了一个通用的列表，可以存储任意类型的数据，并提供添加、删除、访问和获取大小的方法。

#### 5.2 栈（Stack）

栈是一种后进先出（LIFO，Last In First Out）的数据结构，支持压入（Push）和弹出（Pop）操作。使用泛型实现栈，可以使其支持任意类型的数据。

**泛型栈实现**：
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
        return zero // 返回零值
    }
    item := s.items[len(s.items)-1]
    s.items = s.items[:len(s.items)-1]
    return item
}

func (s *Stack[T]) Peek() T {
    if len(s.items) == 0 {
        var zero T
        return zero // 返回零值
    }
    return s.items[len(s.items)-1]
}

func (s *Stack[T]) Size() int {
    return len(s.items)
}
```

在这个例子中，`Stack`结构体实现了一个通用的栈，可以存储任意类型的数据，并提供压入、弹出、查看栈顶元素和获取大小的方法。

#### 5.3 队列（Queue）

队列是一种先进先出（FIFO，First In First Out）的数据结构，支持入队（Enqueue）和出队（Dequeue）操作。使用泛型实现队列，可以使其支持任意类型的数据。

**泛型队列实现**：
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
        return zero // 返回零值
    }
    item := q.items[0]
    q.items = q.items[1:]
    return item
}

func (q *Queue[T]) Peek() T {
    if len(q.items) == 0 {
        var zero T
        return zero // 返回零值
    }
    return q.items[0]
}

func (q *Queue[T]) Size() int {
    return len(q.items)
}
```

在这个例子中，`Queue`结构体实现了一个通用的队列，可以存储任意类型的数据，并提供入队、出队、查看队首元素和获取大小的方法。

#### 5.4 集合（Set）

集合是一种不允许重复元素的数据结构，支持添加、删除和检查元素是否存在的操作。使用泛型实现集合，可以使其支持任意类型的数据。

**泛型集合实现**：
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

在这个例子中，`Set`结构体实现了一个通用的集合，可以存储任意可比较类型的数据，并提供添加、删除、检查是否存在和获取大小的方法。

#### 5.5 映射（Map）

映射是一种键值对的数据结构，支持通过键查找值的操作。使用泛型实现映射，可以使其支持任意类型的键和值。

**泛型映射实现**：
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

在这个例子中，`Map`结构体实现了一个通用的映射，可以存储任意可比较类型的键和任意类型的值，并提供添加、查找、删除和获取大小的方法。

#### 5.6 小结

本章介绍了几种常见的数据结构，包括列表、栈、队列、集合和映射，并通过泛型实现了这些数据结构。通过这些例子，读者可以看到泛型如何提高代码的通用性和复用性。在实际项目中，选择合适的数据结构并合理使用泛型，可以大大提高程序的性能和可维护性。接下来的章节将探讨更多复杂的泛型编程应用和实战案例，帮助读者深入理解和掌握Go泛型的强大功能。