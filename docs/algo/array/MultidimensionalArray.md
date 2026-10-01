# 多维数组
在 Go 语言中，多维数组是数组的扩展，用于表示具有更多维度的数据结构。多维数组在 Go 中是一种嵌套数组的形式，其内部每一层都是一个数组，可以使用它们来表示复杂的数据结构。

### 多维数组的基本概念

1. **定义和初始化**：
   多维数组可以通过嵌套数组的方式定义。例如，二维数组可以看作是一个包含多个一维数组的数组，三维数组则是包含多个二维数组的数组，依此类推。

   ```go
   var arr [2][3]int // 二维数组，包含 2 个一维数组，每个一维数组有 3 个整数
   ```

   可以使用初始化列表来初始化多维数组：

   ```go
   arr := [2][3]int{
       {1, 2, 3},
       {4, 5, 6},
   }
   ```

2. **访问和修改元素**：
   访问和修改多维数组的元素时，需要指定所有维度的索引。

   ```go
   arr := [2][3]int{
       {1, 2, 3},
       {4, 5, 6},
   }
   
   fmt.Println(arr[0][1]) // 输出 2
   arr[1][2] = 7
   fmt.Println(arr[1][2]) // 输出 7
   ```

3. **动态长度的多维数组**：
   Go 中的数组长度是固定的，不能在运行时改变。因此，如果需要动态的多维数组，可以使用切片（`slice`）来实现。切片允许在运行时动态调整大小。

   ```go
   // 二维切片的定义和初始化
   rows := 2
   cols := 3
   matrix := make([][]int, rows)
   for i := range matrix {
       matrix[i] = make([]int, cols)
   }

   matrix[0][0] = 1
   matrix[1][2] = 7
   ```

4. **遍历多维数组**：
   可以使用嵌套的 `for` 循环来遍历多维数组的元素。

   ```go
   arr := [2][3]int{
       {1, 2, 3},
       {4, 5, 6},
   }

   for i := range arr {
       for j := range arr[i] {
           fmt.Printf("%d ", arr[i][j])
       }
       fmt.Println()
   }
   ```

### 示例代码

以下是使用多维数组和切片的示例代码：

```go
package main

import (
    "fmt"
)

func main() {
    // 定义和初始化二维数组
    arr := [2][3]int{
        {1, 2, 3},
        {4, 5, 6},
    }
    
    // 访问和修改元素
    fmt.Println("Element at [0][1]:", arr[0][1])
    arr[1][2] = 7
    fmt.Println("Modified element at [1][2]:", arr[1][2])
    
    // 遍历二维数组
    fmt.Println("Elements in 2D array:")
    for i := range arr {
        for j := range arr[i] {
            fmt.Printf("%d ", arr[i][j])
        }
        fmt.Println()
    }
    
    // 创建和初始化二维切片
    rows := 2
    cols := 3
    matrix := make([][]int, rows)
    for i := range matrix {
        matrix[i] = make([]int, cols)
    }
    
    matrix[0][0] = 1
    matrix[1][2] = 7
    
    // 遍历二维切片
    fmt.Println("Elements in 2D slice:")
    for i := range matrix {
        for j := range matrix[i] {
            fmt.Printf("%d ", matrix[i][j])
        }
        fmt.Println()
    }
}
```

### 总结

多维数组在 Go 中通过嵌套数组实现，适用于需要固定大小的数据结构。对于动态大小的数据结构，切片提供了更大的灵活性。理解如何定义、访问、修改和遍历多维数组或切片对于处理复杂的数据结构非常重要。