`container/ring` 是 Go 标准库中的一个包，用于提供循环链表（环形链表）的实现。循环链表是一种数据结构，其中最后一个节点指向第一个节点，形成一个环。

### 基本使用

1. **创建环形链表**

   ```go
   package main

   import (
       "container/ring"
       "fmt"
   )

   func main() {
       // 创建一个包含 5 个元素的环形链表
       r := ring.New(5)

       // 为每个元素赋值
       for i := 0; i < r.Len(); i++ {
           r.Value = i
           r = r.Next()
       }

       // 遍历并打印环形链表的元素
       r.Do(func(p interface{}) {
           fmt.Println(p.(int))
       })
   }
   ```

2. **环形链表的长度**

   ```go
   length := r.Len()
   fmt.Println("Length of ring:", length)
   ```

3. **遍历环形链表**

   ```go
   r.Do(func(p interface{}) {
       fmt.Println(p)
   })
   ```

4. **移动指针**

   ```go
   // 向前移动 n 个位置
   r = r.Move(n)
   
   // 获取下一个元素
   next := r.Next()
   
   // 获取上一个元素
   prev := r.Prev()
   ```

5. **链接两个环形链表**

   ```go
   r2 := ring.New(3)
   r.Link(r2)
   ```

6. **从环形链表中删除元素**

   ```go
   r.Unlink(3) // 删除当前指针后面的 3 个元素
   ```

### 底层原理

`container/ring` 包中的环形链表通过 `ring.Ring` 结构体来实现，该结构体定义如下：

```go
type Ring struct {
    next, prev *Ring
    Value      interface{} // 任意类型的值
}
```

- `next` 和 `prev` 指向环形链表中的下一个和上一个元素，从而形成双向链表结构。
- `Value` 存储任意类型的值。

环形链表的主要特点是它的最后一个元素指向第一个元素，因此它是循环的。

### 几个重要的方法

1. **New(n int) *Ring**

   创建一个包含 n 个元素的环形链表，每个元素的值都为 nil。

2. **Len() int**

   返回环形链表中的元素个数。

3. **Link(s *Ring) *Ring**

   将环形链表 `s` 插入到当前环形链表之后，并返回新的环形链表的下一个元素。

4. **Unlink(n int) *Ring**

   从当前环形链表中删除 n 个元素，并返回删除的元素。

5. **Move(n int) *Ring**

   将当前环形链表移动 n 个位置，返回移动后的环形链表。

6. **Next() *Ring**

   返回环形链表的下一个元素。

7. **Prev() *Ring**

   返回环形链表的上一个元素。

8. **Do(f func(interface{}))**

   遍历环形链表中的每一个元素，并对每个元素执行函数 f。

### 示例解释

在上述示例中，我们创建了一个包含 5 个元素的环形链表，并为每个元素赋值。接着，我们使用 `Do` 方法遍历并打印了环形链表中的每个元素。环形链表的遍历实际上是通过 `next` 指针在内部进行循环移动，直到遍历所有元素为止。

### 应用场景

环形链表适用于需要循环访问数据结构的场景，如：
- 实现固定长度的缓冲区
- 实现循环调度算法
- 轮询机制等

这种数据结构的优势在于它可以高效地循环访问元素，同时避免了普通链表中复杂的边界条件处理。