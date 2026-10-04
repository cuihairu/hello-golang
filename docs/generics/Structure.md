### 常见的数据结构

列表、栈、队列、集合、映射这五种结构，下面都用泛型重写一遍：类型参数一换，同一份代码服务所有元素类型。

#### 5.1 列表（List）

列表是线性结构，元素任意多个，增删和按下标访问都在底下的切片上完成。

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

存取都走 `items` 切片：`Add` 追加，`Remove` 按下标拼接删除，`Get` 按下标读，`Size` 返回长度。

#### 5.2 栈（Stack）

栈是后进先出（LIFO，Last In First Out）的结构，只有压入（Push）和弹出（Pop）两个动作。

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

队列是先进先出（FIFO，First In First Out）的结构，两头操作：入队（Enqueue）进，出队（Dequeue）出。

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

集合不存重复元素，只有添加、删除、查存在三个操作，元素类型限定为 `comparable`。

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

`Set` 的底层是 `map[T]struct{}`，借 map 的键去重，值永远是空结构体；`Add`、`Remove`、`Contains`、`Size` 各管一件事。

#### 5.5 映射（Map）

映射存键值对，按键查值；键要 `comparable`，值任意。

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

五个结构共用一套写法：切片做容器，泛型参数定元素类型。列表、栈、队列的底层都是 `[]T`，区别只在进出的位置；集合和映射借 `map` 实现，所以 `T` 和 `K` 都要满足 `comparable`。