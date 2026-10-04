在 Go 语言中，可变参数（variadic parameters）允许函数接受不定数量的参数：参数类型前加 `...`，函数内部把它们当作一个切片。

### 可变参数的定义

可变参数函数的定义语法是在参数类型之前使用三个点 `...`。在函数内部，可变参数作为一个切片处理。

#### 示例：定义和使用可变参数函数

```go
package main

import "fmt"

// 定义一个可变参数函数
func sum(nums ...int) int {
    total := 0
    for _, num := range nums {
        total += num
    }
    return total
}

func main() {
    fmt.Println(sum(1, 2, 3))    // 输出：6
    fmt.Println(sum(4, 5, 6, 7)) // 输出：22
    fmt.Println(sum())           // 输出：0
}
```

`nums` 在函数内部作为一个切片处理，用 `range` 遍历即可求和。

### 传递可变参数

调用可变参数函数时，可以直接传递任意数量的参数。还可以将现有的切片传递给可变参数函数，但需要在切片变量后加上 `...` 以展开切片。

#### 示例：传递切片作为可变参数

```go
package main

import "fmt"

func sum(nums ...int) int {
    total := 0
    for _, num := range nums {
        total += num
    }
    return total
}

func main() {
    numbers := []int{1, 2, 3, 4, 5}
    fmt.Println(sum(numbers...)) // 输出：15
}
```

`sum(numbers...)` 把 `numbers` 切片展开成一个个参数传给 `sum`。

### 可变参数和其他参数

在一个函数中，可以将可变参数与其他固定参数一起使用。注意，可变参数必须放在参数列表的最后。

#### 示例：固定参数和可变参数

```go
package main

import "fmt"

func greet(prefix string, names ...string) {
    for _, name := range names {
        fmt.Printf("%s %s\n", prefix, name)
    }
}

func main() {
    greet("Hello", "Alice", "Bob", "Charlie")
    // 输出：
    // Hello Alice
    // Hello Bob
    // Hello Charlie
}
```

### 内部实现机制

在函数内部，可变参数作为切片处理，这意味着可以使用切片的所有特性和方法。

#### 示例：访问可变参数

```go
package main

import "fmt"

func printDetails(details ...string) {
    fmt.Println("Number of details:", len(details))
    for i, detail := range details {
        fmt.Printf("Detail %d: %s\n", i+1, detail)
    }
}

func main() {
    printDetails("Name: Alice", "Age: 30", "Country: Wonderland")
    // 输出：
    // Number of details: 3
    // Detail 1: Name: Alice
    // Detail 2: Age: 30
    // Detail 3: Country: Wonderland
}
```

`details` 就是一个切片：用 `len` 取长度，用下标访问单个元素。

### 总结

可变参数解决的是参数个数不定的问题：定义时在类型前加 `...`，调用时可以直接传值，也可以用 `slice...` 把切片展开传入；函数内部拿到的就是一个切片。限制只有一条：它必须是参数列表的最后一项。