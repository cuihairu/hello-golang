### Go语言的 `for` 循环详解

`for` 是Go语言中唯一的循环语句，C 语言里 while、do-while 干的活都由它承担。

#### 1. 基本的 `for` 循环写法

基本的 `for` 循环语法与C语言类似，结构如下：

```go
for 初始化语句; 条件表达式; 后置语句 {
    // 循环体
}
```

示例：

```go
for i := 0; i < 10; i++ {
    fmt.Println(i)
}
```

这个循环从0打印到9。

#### 2. 使用 `range` 的 `for` 循环

`range` 用于遍历数组、切片、字符串、map 以及通道。用 `range` 遍历时，会返回两个值：第一个是索引（或键），第二个是元素（或值）。

示例：

遍历数组或切片：

```go
nums := []int{2, 3, 4}
for i, num := range nums {
    fmt.Println(i, num)
}
```

遍历字符串：

```go
str := "hello"
for i, ch := range str {
    fmt.Println(i, string(ch))
}
```

遍历 map：

```go
m := map[string]string{"a": "apple", "b": "banana"}
for k, v := range m {
    fmt.Println(k, v)
}
```

遍历通道：

```go
ch := make(chan int, 2)
ch <- 1
ch <- 2
close(ch)
for val := range ch {
    fmt.Println(val)
}
```

#### 3. Go 1.22 以前的 `for` 循环中使用协程的问题

在 Go 1.22 之前，循环变量在整个循环中只有一个实例，如果在 `for` 循环中使用协程（goroutine），容易出现变量捕获的问题。示例：

```go
for i := 0; i < 10; i++ {
    go func() {
        fmt.Println(i)
    }()
}
```

这段代码输出的结果可能不是预期的0到9，而是多个相同的值。原因在于闭包函数中捕获了 `i` 变量，而不是其当前值。正确的做法是传递 `i` 的副本：

```go
for i := 0; i < 10; i++ {
    go func(i int) {
        fmt.Println(i)
    }(i)
}
```

这样可以确保每个协程都使用不同的 `i` 值。

从 Go 1.22 开始，循环变量改为每次迭代都创建一个新实例，上面的闭包写法可以直接得到 0 到 9，但在需要兼容旧版本的代码中，传参复制的写法仍然是最稳妥的习惯。

#### 4. `for` 循环中的 `defer` 使用

`defer` 语句用于在函数返回之前执行某些操作。在 `for` 循环中使用 `defer` 需要注意，`defer` 不会在每轮迭代结束时执行，而是延迟到整个函数返回之前，按照后进先出的顺序统一执行。

示例：

```go
for i := 0; i < 3; i++ {
    defer fmt.Println(i)
}
```

输出顺序是：

```
2
1
0
```

#### 5. 其他常见用法和注意事项

- **无限循环**：省略所有三部分，形成无限循环。

    ```go
    for {
        // 无限循环体
    }
    ```

- **单条件循环**：省略初始化语句和后置语句。

    ```go
    i := 0
    for i < 10 {
        fmt.Println(i)
        i++
    }
    ```

- **循环中的 `break` 和 `continue`**：`break` 退出循环，`continue` 跳过当前迭代。

    ```go
    for i := 0; i < 10; i++ {
        if i == 5 {
            break
        }
        if i%2 == 0 {
            continue
        }
        fmt.Println(i)
    }
    ```

- **标签和多重循环**：使用标签可以跳出多重循环。

    ```go
    outer:
    for i := 0; i < 3; i++ {
        for j := 0; j < 3; j++ {
            if i == 1 {
                break outer
            }
            fmt.Println(i, j)
        }
    }
    ```

标签只在 `break`、`continue` 和 `goto` 三处使用，别的位置写了编译不过。