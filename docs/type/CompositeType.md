复合类型在编程中是指由多个基本类型或者其他复合类型组合而成的数据结构。它们的出现主要为了解决以下几个问题：

### 1. 数据组织和管理

复合类型把多个相关联的数据组合在一起，让数据结构贴近实际问题中的关系。

例如，在一个社交网络应用中，一个用户的资料可能包括用户名、年龄、朋友列表等信息。用结构体（struct）把它们放在一起，读代码的人一眼就能看到用户数据有哪些字段。

```go
type User struct {
    Username string
    Age      int
    Friends  []string
}
```

### 2. 数据访问和操作

复合类型除了数据，还定义了对数据的访问和操作方法。通过方法（结构体方法、接口方法）把增、删、改、查的写法固定下来，调用方不用关心内部结构。

```go
// 定义结构体及方法
type User struct {
    Username string
    Age      int
    Friends  []string
}

func (u *User) AddFriend(friend string) {
    u.Friends = append(u.Friends, friend)
}

func (u *User) RemoveFriend(friend string) {
    for i, f := range u.Friends {
        if f == friend {
            u.Friends = append(u.Friends[:i], u.Friends[i+1:]...)
            return
        }
    }
}

// 使用示例
func main() {
    user := User{
        Username: "Alice",
        Age:      30,
        Friends:  []string{"Bob", "Charlie"},
    }

    user.AddFriend("David")
    fmt.Println(user.Friends)  // 输出: [Bob Charlie David]

    user.RemoveFriend("Charlie")
    fmt.Println(user.Friends)  // 输出: [Bob David]
}
```

### 3. 内存分配和性能优化

在底层实现上，复合类型的不同组成部分可能会被分配在内存的不同区域。切片（slice）作为动态数组的一种实现，能够自动调整长度和容量，不受固定长度数组的限制。

```go
// 切片作为动态数组的示例
func main() {
    // 初始创建一个空的整型切片
    var numbers []int

    // 添加元素
    numbers = append(numbers, 1)
    numbers = append(numbers, 2, 3, 4)

    // 打印切片内容
    fmt.Println(numbers)  // 输出: [1 2 3 4]
}
```

### 总结

复合类型干三件事：结构体把相关字段捆在一起，方法规定对数据的操作，切片按需扩缩容量。单个基本类型表达不了的形状，都靠它们拼出来。