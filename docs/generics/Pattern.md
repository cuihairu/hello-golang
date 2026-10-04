### 泛型编程模式

泛型让一份代码跑在多种类型上。本章讲四个模式：代码复用、类型安全、接口结合，以及泛型的局限。

#### 4.1 泛型与代码复用

泛型最直接的收益是复用：一份逻辑写一次，多种类型都能用，不用复制粘贴同一段代码。

**泛型容器**：
列表、栈、队列这类结构最值得做成泛型，装什么类型由使用者定。

示例：
```go
type List[T any] struct {
    items []T
}

func (l *List[T]) Add(item T) {
    l.items = append(l.items, item)
}

func (l *List[T]) Get(index int) T {
    return l.items[index]
}
```

在这个例子中，`List`结构体是一个通用的列表，可以存储任意类型的数据。

**泛型算法**：
排序、搜索这类算法同样可以泛型化，类型变了算法不变。

示例：
```go
func Find[T comparable](slice []T, value T) int {
    for i, v := range slice {
        if v == value {
            return i
        }
    }
    return -1
}
```

在这个例子中，`Find`函数可以在任意可比较类型的切片中查找指定值。

#### 4.2 泛型与类型安全

泛型在提供复用的同时保住类型安全。类型约束限定类型参数的范围，类型检查提前到编译期，运行时就不会冒出类型错误。

**类型约束确保类型安全**：
约束写明类型参数必须具备的方法，编译器照着检查，不满足就编译不过。

示例：
```go
type Stringer interface {
    String() string
}

func PrintStrings[T Stringer](items []T) {
    for _, item := range items {
        fmt.Println(item.String())
    }
}
```

在这个例子中，`PrintStrings`函数的类型参数`T`被约束为`Stringer`接口，确保所有传入的类型都实现了`String`方法。

#### 4.3 泛型与接口的结合

泛型接口把"操作哪些类型"也参数化：接口定义一组通用操作，各类型各自实现。

**定义泛型接口**：
接口里的方法签名直接使用类型参数。

示例：
```go
type Container[T any] interface {
    Add(item T)
    Remove() T
}
```

在这个例子中，`Container`接口定义了`Add`和`Remove`方法，任何实现该接口的类型都必须提供这些方法。

**实现泛型接口**：
实现泛型接口时，需要为特定类型提供接口定义的方法。

示例：
```go
type IntContainer struct {
    items []int
}

func (c *IntContainer) Add(item int) {
    c.items = append(c.items, item)
}

func (c *IntContainer) Remove() int {
    item := c.items[len(c.items)-1]
    c.items = c.items[:len(c.items)-1]
    return item
}

var _ Container[int] = &IntContainer{}
```

在这个例子中，`IntContainer`实现了`Container[int]`接口，提供了`Add`和`Remove`方法。

#### 4.4 泛型的局限与注意事项

泛型不是万能的，有几处局限要注意。

**类型参数过多**：
过多的类型参数会使代码难以理解，应尽量简化。

**性能开销**：
泛型代码在某些情况下可能引入性能开销，应注意性能分析和优化。

**接口约束**：
类型参数的约束应尽量明确，避免不必要的约束和复杂性。

#### 4.5 小结

用泛型记住三条：类型参数别堆多，性能敏感处实测，约束写到刚好够用。