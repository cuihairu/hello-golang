# 多维数组
多维数组是嵌套数组：每一层都是一个数组，二维数组装若干个一维数组，三维数组再装若干个二维数组，取值时逐层给下标。

### 多维数组的基本概念

1. **定义和初始化**：
   多维数组可以通过嵌套数组的方式定义。例如，二维数组可以看作是一个包含多个一维数组的数组，三维数组则是包含多个二维数组的数组，依此类推。

   ```go
   var arr [2][3]int // 二维数组，包含 2 个一维数组，每个一维数组有 3 个整数
   fmt.Println(arr) // [[0 0 0] [0 0 0]]
   ```

   也可以直接给出初始化列表：

   ```go
   arr := [2][3]int{
       {1, 2, 3},
       {4, 5, 6},
   }
   fmt.Println(arr) // [[1 2 3] [4 5 6]]
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
   Go 的数组长度固定，运行时改不了。需要动态增减元素就用切片（`slice`），它在运行时可调整大小。

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

### 复杂度

单个下标的读写是 O(1)：多维下标换算成一次地址偏移。遍历 $m \times n$ 的数组要把每个元素过一遍，O(mn)。数组长度固定，没有插入删除；行列会变就换二维切片，整行重建是 O(n)。

### 总结

多维数组是嵌套数组，长度固定，适合行列已知的数据。行列要变就用二维切片，每行得单独分配。定义、取值、赋值和嵌套 `for` 遍历，两者写法一样。