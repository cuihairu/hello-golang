# 参数传递

在 Go 语言中，参数传递机制取决于传递的类型。理解这些机制对于编写高效、正确的 Go 代码至关重要。

## 1. 值传递

Go 语言中最基础的传递方式是**值传递**。函数参数是作为副本传递的，这意味着在函数内部修改参数不会影响原始变量。这种机制提供了安全性，避免了意外的数据修改。

### 基本示例

```go
package main

import "fmt"

func changeValue(x int) {
    x = 100
}

func main() {
    num := 5
    changeValue(num)
    fmt.Println("num:", num) // 输出: num: 5，未被修改
}
```

### 要点
- **整型、浮点型、布尔型、字符串** 等基本类型始终使用值传递
- 函数内部的修改不会影响外部变量
- 每次函数调用都会分配新栈帧，副本独立存在

## 2. 指针传递

为了能在函数内部修改原始变量，可以使用**指针传递**。通过传递指针，函数可以访问并修改指针所指向的原始值。

### 基本示例

```go
package main

import "fmt"

func changePointer(x *int) {
    *x = 100
}

func main() {
    num := 5
    changePointer(&num)
    fmt.Println("num:", num) // 输出: num: 100，已被修改
}
```

### 要点
- 使用 `&var` 获取变量的地址作为参数传递
- 在函数内部使用 `*ptr` 访问并修改原始值
- 对于大对象或需要修改原值的场景，推荐使用指针传递

## 3. slice 和 map 的“传递特性”

需要特别注意的是，**slice** 和 **map** 在 Go 中虽然也是传值，但传递的值是**底层数据结构的句柄**，这意味着在函数内部对 slice 或 map 的修改会反映在原始值上。

### Slice 传递示例

```go
package main

import "fmt"

func modifyElements(s []int) {
    s[0] = 100 // 修改元素会反映到原始 slice
}

func appendValue(s []int) []int {
    return append(s, 4) // append 可能创建新的底层数组，因此需要返回新 slice
}

func main() {
    // 方式1：修改元素（不重新分配），无需返回值
    s1 := []int{1, 2, 3}
    modifyElements(s1)
    fmt.Println("修改元素后:", s1) // 输出: 修改元素后: [100 2 3]

    // 方式2：append 可能重新分配底层数组，需要返回新 slice
    s2 := []int{1, 2, 3}
    s3 := appendValue(s2)
    fmt.Println("append 后原 slice:", s2) // 输出: append 后原 slice: [1 2 3]
    fmt.Println("append 后新 slice:", s3) // 输出: append 后新 slice: [1 2 3 4]
}
```

### Map 传递示例

```go
package main

import "fmt"

func modifyMap(m map[string]int) {
    m["key"] = 100 // 修改会反映在原始 map 上
    // 或者添加新键
    m["new_key"] = 200
}

func main() {
    original := make(map[string]int)
    original["existing"] = 50
    modifyMap(original)
    fmt.Println("map:", original) // 输出: map: map[existing:50 key:100 new_key:200]
}
```

### 要点
- **slice 和 map 的值包含指针到底层数据结构的引用**
- **修改 slice 元素或 map 内容** 会影响原始值
- **重新赋值 slice**（如 `s = append(s, ...)`）可能会创建新的底层数组，需要返回新的 slice 引用
- **map 的键值修改** 永远反映在原始 map 上

## 4. 结构体传递

结构体可以通过值传递或指针传递。值传递会复制整个结构体，而指针传递只复制指针（8或16字节）。

### 结构体值传递示例

```go
package main

import "fmt"

type Person struct {
    Name string
    Age  int
}

func setName(p Person) {
    p.Name = "Changed" // 仅修改副本，原始保持不变
}

func main() {
    p := Person{Name: "Alice"}
    setName(p)
    fmt.Println("姓名:", p.Name) // 输出: 姓名: Alice，未被修改
}
```

### 结构体指针传递示例

```go
package main

import "fmt"

type Person struct {
    Name string
    Age  int
}

func setNamePtr(p *Person) {
    p.Name = "Changed" // 修改原始结构体
}

func main() {
    p := Person{Name: "Alice"}
    setNamePtr(&p)
    fmt.Println("姓名:", p.Name) // 输出: 姓名: Changed，已被修改
}
```

### 选择建议
- **小结构体**（如包含 1-2 个 int/string 字段）可以使用**值传递**，避免内存拷贝开销
- **大结构体**或**需要在函数内修改结构体成员**时，使用**指针传递**
- Go 语言标准库中许多函数接受指针，因为这既高效又清晰

## 5. 推荐最佳实践

1. **对于基本类型**（int, float, bool, string）：使用值传递，默认即可
2. **对于大类型或需要修改**：使用指针传递 `*Type`
3. **对于 slice 和 map**：
   - 如果只需要修改内容（不重新分配），直接传递，修改会生效
   - 如果需要重新分配或返回，返回新的 slice/map
4. **文档注释**：在函数签名中清楚说明参数是值还是指针，帮助调用者理解行为
5. **一致性**：在同一类型的相关函数中保持一致的传递方式

通过合理选择参数传递方式，可以编写出既高效又清晰的 Go 代码，避免因误解传递机制而引入的 bug。
