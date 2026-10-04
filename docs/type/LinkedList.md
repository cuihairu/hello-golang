 在 Go 语言中，标准库没有单独的双向链表类型，双向链表由 `container/list` 包提供。

### `container/list` 包概述

这个包中主要包含以下几个结构和函数：

- **`List` 结构**：代表了双向链表。它包含了指向链表首尾元素的指针，以及链表的长度。

- **`Element` 结构**：代表链表中的每个元素。每个 `Element` 包含指向其前一个和后一个元素的指针，以及一个存储的值。

- **方法**：`List` 结构包含了一系列方法来操作双向链表，如插入、删除、迭代等操作。

### 基本操作示例

```go
package main

import (
    "container/list"
    "fmt"
)

func main() {
    // 创建一个新的双向链表
    mylist := list.New()

    // 向链表尾部插入元素
    mylist.PushBack(1)
    mylist.PushBack(2)
    mylist.PushBack(3)

    // 向链表头部插入元素
    mylist.PushFront(0)

    // 遍历链表并打印每个元素的值
    for e := mylist.Front(); e != nil; e = e.Next() {
        fmt.Println(e.Value)
    }

    // 删除链表中间的元素
    second := mylist.Front().Next()
    mylist.Remove(second)

    // 再次遍历链表并打印
    fmt.Println("After removal:")
    for e := mylist.Front(); e != nil; e = e.Next() {
        fmt.Println(e.Value)
    }
}
```

`list.New()` 创建链表，`PushBack`/`PushFront` 插入元素，`Front()` 加 `Next()` 遍历，`Remove` 删除。

### 注意事项

- **遍历顺序**：双向链表的遍历顺序是从头到尾，可以通过 `Front()` 和 `Back()` 方法分别获取首尾元素。
- **删除操作**：在删除元素时，需注意链表是否为空或元素是否存在。
- **性能考虑**：对于大量数据的频繁插入和删除操作，双向链表可能不如数组或切片高效，需要根据具体情况选择合适的数据结构。

### 总结

`container/list` 把双向链表做成了现成的容器，插入、删除、遍历都有对应方法。使用时注意两点：遍历要从 `Front()` 或 `Back()` 拿头尾节点开始；删除前先确认链表非空、元素存在。